# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)


# List of REST resources in current file:
#   (url prefix)               (method)     (action)
# /api/company.member                GET     - Read all (with optional filters, offset, limit, order)
# /api/company.member/<id>           GET     - Read one
# /api/company.member                POST    - Create one
# /api/company.member/<id>           PUT     - Update one
# /api/company.member/<id>           DELETE  - Delete one
# /api/company.member/<id>/<method>  PUT     - Call method (with optional parameters)


# List of IN/OUT data (json data and HTTP-headers) for each REST resource:

# /api/company.member  GET  - Read all (with optional filters, offset, limit, order)
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (optional filters (Odoo domain), offset, limit, order)
#           {                                       # editable
#               "filters": "[('some_field_1', '=', some_value_1), ('some_field_2', '!=', some_value_2), ]",
#               "offset":  XXX,
#               "limit":   XXX,
#               "order":   "list_of_fields"  # default 'name asc'
#           }
# OUT data:
OUT__company_member__read_all__SUCCESS_CODE = 200       # editable
#   JSON:
#       {
#           "count":   XXX,     # number of returned records
#           "results": [
OUT__company_member__read_all__JSON = (                 # editable
    'id',
    'name',
    'birthday',
    ('parent_id', (
        'id',
        'name',
        'legal_name',
        'client_export_id',
        'copago_amount',
        'outstanding',
    )),
    'relationship',
    'allergies',
    'prev_ailments',
    'user_active',

)
#           ]
#       }

# /api/company.member/<id>  GET  - Read one
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (optional parameter 'search_field' for search object not by 'id' field)
#           {"search_field": "some_field_name"}     # editable
# OUT data:
OUT__company_member__read_one__SUCCESS_CODE = 200       # editable
OUT__company_member__read_one__JSON = (                 # editable
    # (The order of fields of different types maybe arbitrary)
    'id',
    'name',
    'birthday',
    ('parent_id', (
        'id',
        'name',
        'legal_name',
        'client_export_id',
        'copago_amount',
        'outstanding',
    )),
    'relationship',
    'allergies',
    'prev_ailments',
    'user_active',

)

# /api/company.member  POST  - Create one
# IN data:
#   HEADERS:
#       'access_token'
#   DEFAULTS:
#       (optional default values of fields)
DEFAULTS__company_member__create_one__JSON = {          # editable
            #"some_field_1": some_value_1,
            #"some_field_2": some_value_2,
            #
}
#   JSON:
#       (fields and its values of created object;
#        don't forget about model's mandatory fields!)
#                                                # editable
# OUT data:
OUT__company_member__create_one__SUCCESS_CODE = 200     # editable
OUT__company_member__create_one__JSON = (               # editable
    'id',
)

# /api/company.member/<id>  PUT  - Update one
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (fields and new values of updated object)   # editable
#
# OUT data:
OUT__company_member__update_one__SUCCESS_CODE = 200     # editable

# /api/company.member/<id>  DELETE  - Delete one
# IN data:
#   HEADERS:
#       'access_token'
# OUT data:
OUT__company_member__delete_one__SUCCESS_CODE = 200     # editable

# /api/company.member/<id>/<method>  PUT  - Call method (with optional parameters)
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (named parameters of method)                # editable
#
# OUT data:
OUT__company_member__call_method__SUCCESS_CODE = 200    # editable


# HTTP controller of REST resources:

class ControllerREST(http.Controller):

    # Read all (with optional filters, offset, limit, order):
    @http.route('/api/company.member', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__company_member__GET(self):
        return wrap__resource__read_all(
            modelname = 'company.member',
            default_domain = [],
            success_code = OUT__company_member__read_all__SUCCESS_CODE,
            OUT_fields = OUT__company_member__read_all__JSON
        )

    # Read one:
    @http.route('/api/company.member/<id>', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__company_member__id_GET(self, id):
        return wrap__resource__read_one(
            modelname = 'company.member',
            id = id,
            success_code = OUT__company_member__read_one__SUCCESS_CODE,
            OUT_fields = OUT__company_member__read_one__JSON
        )

    # Create one:
    @http.route('/api/company_member', methods=['POST'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__company_member__POST(self):
        return wrap__resource__create_one(
            modelname = 'company.member',
            default_vals = DEFAULTS__company_member__create_one__JSON,
            success_code = OUT__company_member__create_one__SUCCESS_CODE,
            OUT_fields = OUT__company_member__create_one__JSON
        )

    # Update one:
    @http.route('/api/company.member/<id>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__company_member__id_PUT(self, id):
        return wrap__resource__update_one(
            modelname = 'company.member',
            id = id,
            success_code = OUT__company_member__update_one__SUCCESS_CODE
        )

    # Delete one:
    @http.route('/api/company.member/<id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__company_member__id_DELETE(self, id):
        return wrap__resource__delete_one(
            modelname = 'company.member',
            id = id,
            success_code = OUT__company_member__delete_one__SUCCESS_CODE
        )

    # Call method (with optional parameters):
    @http.route('/api/company.member/<id>/<method>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__company_member__id__method_PUT(self, id, method):
        return wrap__resource__call_method(
            modelname = 'company.member',
            id = id,
            method = method,
            success_code = OUT__company_member__call_method__SUCCESS_CODE
        )

