import inflect
from flask import jsonify
from werkzeug.exceptions import HTTPException, default_exceptions

from .config import CrudConfig, CrudShortcuts
from .resources import BaseCollectionResource
from .resources import BaseSingleResource

p = inflect.engine()


def make_json_app(app):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """

    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    for code in default_exceptions.keys():
        app.register_error_handler(code, make_json_error)

    return app


def generate_crud(app, model_array):
    app = make_json_app(app)
    # Setup Configuration
    base_config = app.config.crud_config if hasattr(app.config, 'crud_config') else CrudConfig
    for model in model_array:
        if not hasattr(model, 'crud_config'):
            config = base_config
        else:
            config = model.crud_config

        # Some handy shortcuts
        shortcuts = CrudShortcuts(model)
        model.shortcuts = shortcuts

        # Generate Resources and Routes
        base_uri = model.route_url if hasattr(model, 'route_url') else shortcuts.base_uri
        attrs = {'model': model, 'config': config, 'app': app}
        SingleResource = type('SingleResource', (BaseSingleResource,), attrs)
        CollectionResource = type('CollectionResource', (BaseCollectionResource,), attrs)
        app.add_url_rule(
            base_uri + '/<{}:{}>'.format(shortcuts.primary_key_type, shortcuts.primary_key),
            view_func=SingleResource.as_view(shortcuts.table_name),

        )
        app.add_url_rule(
            base_uri,
            view_func=CollectionResource.as_view(p.plural(shortcuts.table_name))
        )

    # Add base route
    app.add_url_rule('/', view_func=_generate_base_route(model_array), methods=['GET'])


def _generate_base_route(model_array):
    tables = {}

    for model in model_array:
        fields = []
        table_name = model.shortcuts.table_name
        required_fields = model.shortcuts.required_fields
        for field, field_object in model.shortcuts.fields.items():
            field_name = field_object.name
            field_type = field_object.get_db_field()
            is_required = field_name in required_fields or field_type == 'primary_key'

            fields.append({
                'field_name': field_name,
                'field_type': field_type,
                'is_required': is_required
            })

        tables[table_name] = {
            'route_url': model.route_url if hasattr(model, 'route_url') else '/{}'.format(table_name),
            'fields': fields
        }

    def base_route():
        response_data = {
            'data': {'routes': tables},
            'status_code': 200,
            'message': 'OK'
        }

        return jsonify(response_data)

    return base_route
