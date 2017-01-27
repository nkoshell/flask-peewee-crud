from .base_resource import _BaseResource
from .helpers import response_json, validation, collection_filter
from .messages import ErrorTypeInteger, MAX_RESULTS_PER_PAGE, SuccessOk, SuccessRowCreated
from playhouse.shortcuts import model_to_dict
from sanic.log import log
import traceback

from math import ceil


# Resource for multiple objects
class BaseCollectionResource(_BaseResource):
    model = None

    @collection_filter
    def get(self, request, **kwargs):
        try:
            # Verify page is an int
            try:
                page = int(request.args.get('page', 1))
            except ValueError:
                return response_json(status_code=400,
                                     message=ErrorTypeInteger.format('page'))

            include_foreign_keys = True if 'foreign_keys' in request.args \
                                           and request.args['foreign_keys'][0] == 'true' else False

            results = []
            data = kwargs.get('filtered_results')
            total_records = data.count()
            total_pages = ceil(total_records / MAX_RESULTS_PER_PAGE)
            data = data.paginate(page, MAX_RESULTS_PER_PAGE)

            for row in data:
                results.append(model_to_dict(row, backrefs=include_foreign_keys))

            return response_json(data=results,
                                 status_code=200,
                                 message=SuccessOk,
                                 page=page,
                                 total_pages=total_pages)
        except Exception as e:
            log.error(e.with_traceback())
            return response_json(message=str(e),
                                 status_code=500)

    @validation
    def post(self, request):
        try:
            result = self.model.create(**request.json)
            return response_json(data=model_to_dict(result),
                                 status_code=200,
                                 message=SuccessRowCreated.format(result.id)
                                 )
        except Exception as e:
            log.error(traceback.print_exc())
            return response_json(message=str(e),
                                 status_code=500)