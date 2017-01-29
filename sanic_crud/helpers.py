from datetime import datetime
from sanic.response import json
from .messages import ErrorInvalidJSON, ErrorNonNullableFieldInsert, ErrorPrimaryKeyUpdateInsert, ErrorInvalidField, \
	ErrorFieldOutOfRange, ErrorInvalidFilterOption, FILTER_OPTIONS, ErrorTypeDatetime, ErrorTypeInteger, \
    ErrorTypeBoolean


# Validates request data for a put or a post
def validation(func):
    def wrapped(self, request, *args, **kwargs):
        model = self.model
        config = model.crud_config

        fields = config.fields
        field_names = config.get_field_names()
        primary_key = config.primary_key
        required_fields = config.required_fields

        # min/max value size for fields
        field_default_size = {
            'int': {'min': -2147483647, 'max': 2147483647},
            'bigint': {'min': -9223372036854775808, 'max': 9223372036854775807},
            'primary_key': {'min': -2147483647, 'max': 2147483647},

        }

        # min/max length for fields
        field_default_length = {
            'string': {'min': 0, 'max': 255}
        }

        # verify the request data is valid JSON
        try:
            request_data = request.json
        except ValueError:
            return response_json(status_code=400, message=ErrorInvalidJSON)

        # Verify all non-nullable fields are present only needs to be done on post
        if request.method == 'POST':
            for field in field_names:
                field_obj = fields.get(field)

                if not field_obj.null:
                    if field not in request.json or request.json.get(field) is None:
                        return response_json(status_code=400,
                                             message=ErrorNonNullableFieldInsert.format(field, required_fields))

        # Verify the user is not trying to mess with the primary key
        if primary_key in request_data:
            return response_json(status_code=400,
                                 message=ErrorPrimaryKeyUpdateInsert)

        # Verify all of the request_data are valid model fields
        for key in request_data:
            if key not in fields:
                return response_json(ErrorInvalidField.format(key, field_names))

        # Verify all of the request_data is a valid type for the database
        for key, value in request_data.items():
            field_type_invalid = _validate_field_type(fields.get(key), value)
            field_type = fields.get(key).db_field

            if field_type_invalid:
                return field_type_invalid

            # Verify min/max size
            if field_type in field_default_size:
                min_size = field_default_size.get(field_type).get('min')
                max_size = field_default_size.get(field_type).get('max')

                if not min_size <= value <= max_size:
                    return response_json(status_code=400,
                                         message=ErrorFieldOutOfRange.format(key, min_size, max_size))
            # verify field length
            if field_type in field_default_length:
                min_length = field_default_length.get(field_type).get('min')
                max_length = field_default_length.get(field_type).get('max')

                if not min_length <= len(value) <= max_length:
                    return response_json(status_code=400,
                                         message=ErrorFieldOutOfRange(key, min_length, max_length))

        return func(self, request, *args, **kwargs)

    return wrapped


def collection_filter(func):
    def wrapped(self, request, *args, **kwargs):
        model = self.model
        config = model.crud_config

        fields = config.fields
        field_names = config.get_field_names()
        query = model.select()

        # Iterate over args and split the filters
        for key, value in request.args.items():
            # skip over include foreign_keys flag
            if key == 'foreign_keys':
                continue

            filter_parts = key.split('__')
            field = filter_parts[0]
            comparison = '='

            # If the length is 2, then there is a filter component
            if len(filter_parts) == 2:
                comparison = filter_parts[1]

            # Validate that a supported comparison is used
            if comparison not in FILTER_OPTIONS:
                return response_json(status_code=400,
                                     message=ErrorInvalidFilterOption.format(comparison, FILTER_OPTIONS))

            # Validate that the field is part of the table
            if field not in fields:
                return response_json(status_code=400,
                                     message=ErrorInvalidField.format(key, field_names))

            # Validate that the value is the correct type
            if comparison in ['in', 'notin']:
                value = value.split(',')

            if comparison != 'null':
                for item in value:
                    field_type_invalid = _validate_field_type(fields.get(field), item)
                    if field_type_invalid:
                        return field_type_invalid

            model_field = getattr(model, field)

            # Build the query from comparisons
            if comparison == '=':
                query = query.where(model_field == value)
            elif comparison == 'null':
                query = query.where(model_field.is_null(True if value == 1 else False))
            elif comparison == 'startswith':
                query = query.where(model_field.startswith(value))
            elif comparison == 'contains':
                query = query.where(model_field.contains(value))
            elif comparison == 'lt':
                query = query.where(model_field < value)
            elif comparison == 'lte':
                query = query.where(model_field <= value)
            elif comparison == 'gt':
                query = query.where(model_field > value)
            elif comparison == 'gte':
                query = query.where(model_field >= value)
            elif comparison == 'in':
                query = query.where(model_field << value)
            elif comparison == 'notin':
                query = query.where(~(model_field << value))

        kwargs['filtered_results'] = query

        return func(self, request, *args, **kwargs)

    return wrapped


# Helper function, takes in a database field and an input value to make sure the input is the correct type for the db
def _validate_field_type(field, value):
    expected_field_type = field.db_field

    if expected_field_type in ['int', 'bool']:
        try:
            int(value)
        except (ValueError, TypeError):
            return response_json(status_code=400,
                                 message=ErrorTypeInteger.format(value) if expected_field_type in ['int'] else ErrorTypeBoolean.format(value))

    elif expected_field_type == 'datetime':
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return response_json(status_code=400,
                                 message=ErrorTypeDatetime.format(value))

    return False


def response_json(data=None, status_code=None, message=None, page=None, total_pages=None):
    response_data = {
        'data': data,
        'status_code': status_code,
        'message': message
    }

    if page:
        response_data['page'] = page
    if total_pages:
        response_data['total_pages'] = total_pages

    response = json(response_data, status=status_code)

    return response


# Gets a model with a primary key
def get_model(primary_key, model):
    try:
        pk_field = model.crud_config.primary_key
        return model.get(getattr(model, pk_field) == primary_key)
    except model.DoesNotExist:
        return {}