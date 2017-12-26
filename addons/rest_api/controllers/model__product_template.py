# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)


# List of REST resources in current file:
#   (url prefix)                     (method)     (action)
# /api/product.template                GET     - Read all (with optional filters, offset, limit, order)
# /api/product.template/<id>           GET     - Read one
# /api/product.template                POST    - Create one
# /api/product.template/<id>           PUT     - Update one
# /api/product.template/<id>           DELETE  - Delete one
# /api/product.template/<id>/<method>  PUT     - Call method (with optional parameters)


# List of IN/OUT data (json data and HTTP-headers) for each REST resource:

# /api/product.template  GET  - Read all (with optional filters, offset, limit, order)
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
OUT__product_template__read_all__SUCCESS_CODE = 200 # editable
#   JSON:
#       {
#           "count":   XXX,     # number of returned records
#           "results": [
OUT__product_template__read_all__JSON = (           # editable
    'id',
    'name',
)
#           ]
#       }

# /api/product.template/<id>  GET  - Read one
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (optional parameter 'search_field' for search object not by 'id' field)
#           {"search_field": "some_field_name"}     # editable
# OUT data:
OUT__product_template__read_one__SUCCESS_CODE = 200 # editable
OUT__product_template__read_one__JSON = (           # editable
    # (The order of fields of different types maybe arbitrary)
    # simple fields (non relational):
    'id',
    'name',
    'type',
    'sale_ok',
    'barcode',
    # many2one fields:
    ('categ_id', (
        'id',
        'name',
    )),
    # one2many fields:
    ('attribute_line_ids', [(
        'id',
        'display_name',
    )]),
    ('seller_ids', [(
        'id',
        ('name', (
            'id',
            'name',
            'phone',
            ('child_ids', [(
                'id',
                'name',
                'mobile',
            )]),
        )),
        'min_qty',
        'delay',
    )]),
    # many2many fields:
    #('supplier_taxes_id', [(    # need install 'account' module
        #'id',
        #'name',
        #'type',
        #'amount',
        #'price_include',
    #)]),
    #('taxes_id', [(             # need install 'account' module
        #'id',
        #'name',
        #'type',
        #'amount',
        #'price_include',
    #)]),
)

# /api/product.template  POST  - Create one
# IN data:
#   HEADERS:
#       'access_token'
#   DEFAULTS:
#       (optional default values of fields)
DEFAULTS__product_template__create_one__JSON = {    # editable
            #"some_field_1": some_value_1,
            #"some_field_2": some_value_2,
            #...
}
#   JSON:
#       (fields and its values of created object;
#        don't forget about model's mandatory fields!)
#           ...                                     # editable
# OUT data:
OUT__product_template__create_one__SUCCESS_CODE = 200 # editable
OUT__product_template__create_one__JSON = (         # editable
    'id',
)

# /api/product.template/<id>  PUT  - Update one
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (fields and new values of updated object)   # editable
#           ...
# OUT data:
OUT__product_template__update_one__SUCCESS_CODE = 200 # editable

# /api/product.template/<id>  DELETE  - Delete one
# IN data:
#   HEADERS:
#       'access_token'
# OUT data:
OUT__product_template__delete_one__SUCCESS_CODE = 200 # editable

# /api/product.template/<id>/<method>  PUT  - Call method (with optional parameters)
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (named parameters of method)                # editable
#           ...
# OUT data:
OUT__product_template__call_method__SUCCESS_CODE = 200  # editable


# HTTP controller of REST resources:

class ControllerREST(http.Controller):
    
    # Read all (with optional filters, offset, limit, order):
    @http.route('/api/product.template', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__product_template__GET(self):
        return wrap__resource__read_all(
            modelname = 'product.template',
            default_domain = [],
            success_code = OUT__product_template__read_all__SUCCESS_CODE,
            OUT_fields = OUT__product_template__read_all__JSON
        )
    
    # Read one:
    @http.route('/api/product.template/<id>', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__product_template__id_GET(self, id):
        return wrap__resource__read_one(
            modelname = 'product.template',
            id = id,
            success_code = OUT__product_template__read_one__SUCCESS_CODE,
            OUT_fields = OUT__product_template__read_one__JSON
        )
    
    # Create one:
    @http.route('/api/product.template', methods=['POST'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__product_template__POST(self):
        return wrap__resource__create_one(
            modelname = 'product.template',
            default_vals = DEFAULTS__product_template__create_one__JSON,
            success_code = OUT__product_template__create_one__SUCCESS_CODE,
            OUT_fields = OUT__product_template__create_one__JSON
        )
    
    # Update one:
    @http.route('/api/product.template/<id>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__product_template__id_PUT(self, id):
        return wrap__resource__update_one(
            modelname = 'product.template',
            id = id,
            success_code = OUT__product_template__update_one__SUCCESS_CODE
        )
    
    # Delete one:
    @http.route('/api/product.template/<id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__product_template__id_DELETE(self, id):
        return wrap__resource__delete_one(
            modelname = 'product.template',
            id = id,
            success_code = OUT__product_template__delete_one__SUCCESS_CODE
        )
    
    # Call method (with optional parameters):
    @http.route('/api/product.template/<id>/<method>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__product_template__id__method_PUT(self, id, method):
        return wrap__resource__call_method(
            modelname = 'product.template',
            id = id,
            method = method,
            success_code = OUT__product_template__call_method__SUCCESS_CODE
        )
    
