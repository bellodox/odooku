# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)


# List of REST resources in current file:
#   (url prefix)               (method)     (action)
# /api/model.name                GET     - Read all (with optional filters, offset, limit, order)
# /api/model.name/<id>           GET     - Read one
# /api/model.name                POST    - Create one
# /api/model.name/<id>           PUT     - Update one
# /api/model.name/<id>           DELETE  - Delete one
# /api/model.name/<id>/<method>  PUT     - Call method (with optional parameters)


# List of IN/OUT data (json data and HTTP-headers) for each REST resource:

# /api/model.name  GET  - Read all (with optional filters, offset, limit, order)
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (optional filters (Odoo domain), offset, limit, order)
#           {                                       # editable
#               "filters": "[('some_field_1', '=', some_value_1), ('some_field_2', '!=', some_value_2), ...]",
#               "offset":  XXX,
#               "limit":   XXX,
#               "order":   "list_of_fields"  # default 'name asc'
#           }
# OUT data:
OUT__model_name__read_all__SUCCESS_CODE = 200       # editable
#   JSON:
#       {
#           "count":   XXX,     # number of returned records
#           "results": [
OUT__model_name__read_all__JSON = (                 # editable
    'id',
    'name',
)
#           ]
#       }

# /api/model.name/<id>  GET  - Read one
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (optional parameter 'search_field' for search object not by 'id' field)
#           {"search_field": "some_field_name"}     # editable
# OUT data:
OUT__model_name__read_one__SUCCESS_CODE = 200       # editable
OUT__model_name__read_one__JSON = (                 # editable
    # (The order of fields of different types maybe arbitrary)
    # simple fields (non relational):
    'simple_field_1',
    'simple_field_2',
    ...
    # many2one fields:
    
    'many2one_field_1',     # will return just 'id'
    OR
    ('many2one_field_1', (  # will return dictionary of inner fields
        'inner_field_1',
        'inner_field_2',
        ...
    )),
    
    'many2one_field_2',
    OR
    ('many2one_field_2', (
        'inner_field_1',
        'inner_field_2',
        ...
    )),
    
    ...
    # one2many fields:
    ('one2many_field_1', [(
        'inner_field_1',
        'inner_field_2',
        ...
    )]),
    ('one2many_field_2', [(
        'inner_field_1',
        'inner_field_2',
        ...
    )]),
    ...
    # many2many fields:
    ('many2many_field_1', [(
        'inner_field_1',
        'inner_field_2',
        ...
    )]),
    ('many2many_field_2', [(
        'inner_field_1',
        'inner_field_2',
        ...
    )]),
    ...
)

# /api/model.name  POST  - Create one
# IN data:
#   HEADERS:
#       'access_token'
#   DEFAULTS:
#       (optional default values of fields)
DEFAULTS__model_name__create_one__JSON = {          # editable
            #"some_field_1": some_value_1,
            #"some_field_2": some_value_2,
            #...
}
#   JSON:
#       (fields and its values of created object;
#        don't forget about model's mandatory fields!)
#           ...                                     # editable
# OUT data:
OUT__model_name__create_one__SUCCESS_CODE = 200     # editable
OUT__model_name__create_one__JSON = (               # editable
    'id',
)

# /api/model.name/<id>  PUT  - Update one
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (fields and new values of updated object)   # editable
#           ...
# OUT data:
OUT__model_name__update_one__SUCCESS_CODE = 200     # editable

# /api/model.name/<id>  DELETE  - Delete one
# IN data:
#   HEADERS:
#       'access_token'
# OUT data:
OUT__model_name__delete_one__SUCCESS_CODE = 200     # editable

# /api/model.name/<id>/<method>  PUT  - Call method (with optional parameters)
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (named parameters of method)                # editable
#           ...
# OUT data:
OUT__model_name__call_method__SUCCESS_CODE = 200    # editable


# HTTP controller of REST resources:

class ControllerREST(http.Controller):
    
    # Read all (with optional filters, offset, limit, order):
    @http.route('/api/model.name', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__model_name__GET(self):
        return wrap__resource__read_all(
            modelname = 'model.name',
            default_domain = [],
            success_code = OUT__model_name__read_all__SUCCESS_CODE,
            OUT_fields = OUT__model_name__read_all__JSON
        )
    
    # Read one:
    @http.route('/api/model.name/<id>', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__model_name__id_GET(self, id):
        return wrap__resource__read_one(
            modelname = 'model.name',
            id = id,
            success_code = OUT__model_name__read_one__SUCCESS_CODE,
            OUT_fields = OUT__model_name__read_one__JSON
        )
    
    # Create one:
    @http.route('/api/model.name', methods=['POST'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__model_name__POST(self):
        return wrap__resource__create_one(
            modelname = 'model.name',
            default_vals = DEFAULTS__model_name__create_one__JSON,
            success_code = OUT__model_name__create_one__SUCCESS_CODE,
            OUT_fields = OUT__model_name__create_one__JSON
        )
    
    # Update one:
    @http.route('/api/model.name/<id>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__model_name__id_PUT(self, id):
        return wrap__resource__update_one(
            modelname = 'model.name',
            id = id,
            success_code = OUT__model_name__update_one__SUCCESS_CODE
        )
    
    # Delete one:
    @http.route('/api/model.name/<id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__model_name__id_DELETE(self, id):
        return wrap__resource__delete_one(
            modelname = 'model.name',
            id = id,
            success_code = OUT__model_name__delete_one__SUCCESS_CODE
        )
    
    # Call method (with optional parameters):
    @http.route('/api/model.name/<id>/<method>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__model_name__id__method_PUT(self, id, method):
        return wrap__resource__call_method(
            modelname = 'model.name',
            id = id,
            method = method,
            success_code = OUT__model_name__call_method__SUCCESS_CODE
        )
    
