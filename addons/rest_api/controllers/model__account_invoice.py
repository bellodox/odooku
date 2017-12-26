# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)


# List of REST resources in current file:
#   (url prefix)                    (method)     (action)
# /api/account.invoice                GET     - Read all (with optional filters, offset, limit, order)
# /api/account.invoice/<id>           GET     - Read one
# /api/account.invoice                POST    - Create one
# /api/account.invoice/<id>           PUT     - Update one
# /api/account.invoice/<id>           DELETE  - Delete one
# /api/account.invoice/<id>/<method>  PUT     - Call method (with optional parameters)


# List of IN/OUT data (json data and HTTP-headers) for each REST resource:

# /api/account.invoice  GET  - Read all (with optional filters, offset, limit, order)
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
OUT__account_invoice__read_all__SUCCESS_CODE = 200  # editable
#   JSON:
#       {
#           "count":   XXX,     # number of returned records
#           "results": [
OUT__account_invoice__read_all__JSON = (            # editable
    # simple fields (non relational):
    'id',
    'date_invoice',
    'number',
    'date_due',
    'residual',
    'amount_untaxed',
    'amount_total',
    'state',
    # many2one fields:
    ('partner_id', (
        'id',
        'name',
    )),
    ('user_id', (
        'id',
        'name',
    )),
)
#           ]
#       }

# /api/account.invoice/<id>  GET  - Read one
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (optional parameter 'search_field' for search object not by 'id' field)
#           {"search_field": "some_field_name"}     # editable
# OUT data:
OUT__account_invoice__read_one__SUCCESS_CODE = 200  # editable
OUT__account_invoice__read_one__JSON = (            # editable
    # (The order of fields of different types maybe arbitrary)
    # simple fields (non relational):
    'id',
    'number',
    'date_invoice',
    'date_due',
    'amount_untaxed',
    'amount_tax',
    'amount_total',
    'residual',
    'state',
    # many2one fields:
    ('partner_id', (
        'id',
        'name',
        'city',
    )),
    ('user_id', (
        'id',
        'name',
    )),
    ('payment_term_id', (
        'id',
        'name',
    )),
    ('fiscal_position_id', (
        'id',
        'name',
    )),
    ('journal_id', (
        'id',
        'display_name',
    )),
    ('account_id', (
        'id',
        'display_name',
    )),
    # one2many fields:
    ('invoice_line_ids', [(
        'id',
        ('product_id', (  # many2one
            'id',
            'name',
        )),
        'name',
        ('account_id', (  # many2one
            'id',
            'display_name',
        )),
        'quantity',
        'price_unit',
        ('invoice_line_tax_ids', [(  # many2many
            'id',
            'name',
        )]),
        'price_subtotal',
    )]),
)

# /api/account.invoice  POST  - Create one
# IN data:
#   HEADERS:
#       'access_token'
#   DEFAULTS:
#       (optional default values of fields)
DEFAULTS__account_invoice__create_one__JSON = {     # editable
            #"some_field_1": some_value_1,
            #"some_field_2": some_value_2,
            #...
}
#   JSON:
#       (fields and its values of created object;
#        don't forget about model's mandatory fields!)
#           ...                                     # editable
# OUT data:
OUT__account_invoice__create_one__SUCCESS_CODE = 200  # editable
OUT__account_invoice__create_one__JSON = (          # editable
    'id',
)

# /api/account.invoice/<id>  PUT  - Update one
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (fields and new values of updated object)   # editable
#           ...
# OUT data:
OUT__account_invoice__update_one__SUCCESS_CODE = 200  # editable

# /api/account.invoice/<id>  DELETE  - Delete one
# IN data:
#   HEADERS:
#       'access_token'
# OUT data:
OUT__account_invoice__delete_one__SUCCESS_CODE = 200  # editable

# /api/account.invoice/<id>/<method>  PUT  - Call method (with optional parameters)
# IN data:
#   HEADERS:
#       'access_token'
#   JSON:
#       (named parameters of method)                # editable
#           ...
# OUT data:
OUT__account_invoice__call_method__SUCCESS_CODE = 200  # editable


# HTTP controller of REST resources:

class ControllerREST(http.Controller):
    
    # Read all (with optional filters, offset, limit, order):
    @http.route('/api/account.invoice', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__account_invoice__GET(self):
        return wrap__resource__read_all(
            modelname = 'account.invoice',
            default_domain = [],
            success_code = OUT__account_invoice__read_all__SUCCESS_CODE,
            OUT_fields = OUT__account_invoice__read_all__JSON
        )
    
    # Read one:
    @http.route('/api/account.invoice/<id>', methods=['GET'], type='http', auth='none')
    @check_permissions
    def api__account_invoice__id_GET(self, id):
        return wrap__resource__read_one(
            modelname = 'account.invoice',
            id = id,
            success_code = OUT__account_invoice__read_one__SUCCESS_CODE,
            OUT_fields = OUT__account_invoice__read_one__JSON
        )
    
    # Create one:
    @http.route('/api/account.invoice', methods=['POST'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__account_invoice__POST(self):
        return wrap__resource__create_one(
            modelname = 'account.invoice',
            default_vals = DEFAULTS__account_invoice__create_one__JSON,
            success_code = OUT__account_invoice__create_one__SUCCESS_CODE,
            OUT_fields = OUT__account_invoice__create_one__JSON
        )
    
    # Update one:
    @http.route('/api/account.invoice/<id>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__account_invoice__id_PUT(self, id):
        return wrap__resource__update_one(
            modelname = 'account.invoice',
            id = id,
            success_code = OUT__account_invoice__update_one__SUCCESS_CODE
        )
    
    # Delete one:
    @http.route('/api/account.invoice/<id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__account_invoice__id_DELETE(self, id):
        return wrap__resource__delete_one(
            modelname = 'account.invoice',
            id = id,
            success_code = OUT__account_invoice__delete_one__SUCCESS_CODE
        )
    
    # Call method (with optional parameters):
    @http.route('/api/account.invoice/<id>/<method>', methods=['PUT'], type='http', auth='none', csrf=False)
    @check_permissions
    def api__account_invoice__id__method_PUT(self, id, method):
        return wrap__resource__call_method(
            modelname = 'account.invoice',
            id = id,
            method = method,
            success_code = OUT__account_invoice__call_method__SUCCESS_CODE
        )
    
