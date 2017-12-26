Support email: avs3.ua@gmail.com

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OVERVIEW
========

This module provide professional RESTful API (json) access to Odoo models with OAuth2 authentification (very simplified) and Redis token store.

The module has a predefined (and statically customizable) scheme of response Odoo fields for 'Read one', 'Read all' and 'Create one' methods.

The scheme of the response fields can have a **tree-like** structure with **any** level of **nesting**. See "Example #1" below.

The scheme of the request fields can have a **tree-like** structure with one (and more in some cases) level of **nesting**. See "Example #2" below.

Also this module allow to fetch any existing PDF report from Odoo.

Available models (the list is easily extensible):
    - account.invoice
    - account.invoice.line
    - product.template
    - report (only to fetching existing reports)
    - res.partner
    - sale.order
    - sale.order.line

**The procedure of adding any Odoo model is simple and not required of writing new code.**

Each model has the following methods:
    - Read all (with optional filters, offset, limit, order)
    - Read one
    - Create one (with optional default values)
    - Update one
    - Delete one
    - Call any method of Odoo model (with optional parameters)

This module works with standard and custom Odoo models.

Authentication consists of three methods:
    - Login in Odoo and get access tokens
    - Refresh access token
    - Delete access tokens from token store

'Access token' and 'Refresh token' have a certain lifetimes.

**This module requires a working 'Redis' server.**

Thanks to 'Redis', your REST sessions are not drops after the server reboot, and also authentication by access token is very fast.

This module requires sending 'Access token' inside the request header. **All other parameters of any requests (including GET requests) should be sent as json payload inside the request body. Each request must contain the header "Content-Type: text/html".**

|
**Example #1: 'sale.order - Read one' - response json**::

    {
        "create_date": "2016-06-02 18:42:48",
        "name": "SO001",
        "payment_term_id": {
            "id": 2,
            "name": "15 Days"
        },
        "order_line": [
            {
                "name": "Product 1",
                "price_unit": 111,
                "product_uom_qty": 11,
                "price_subtotal": 1221,
                "product_id": {
                    "barcode": "2400000032632",
                    "name": "Product 1",
                    "type": "consu",
                    "attribute_line_ids": [
                        {
                            "display_name": "Attribute 1",
                            "id": 1
                        },
                        {
                            "display_name": "Attribute 2",
                            "id": 2
                        }
                    ],
                    "categ_id": {
                        "id": 1,
                        "name": "All"
                    },
                    "id": 2
                },
                "id": 1,
                "tax_id": [
                    {
                        "id": 6,
                        "name": "ITAX X"
                    },
                    {
                        "id": 7,
                        "name": "Tax 15.00%"
                    }
                ]
            },
            {
                "name": "Product 2",
                "price_unit": 222,
                "product_uom_qty": 22,
                "price_subtotal": 4884,
                "product_id": {
                    "barcode": null,
                    "name": "Product 2",
                    "type": "consu",
                    "attribute_line_ids": [],
                    "categ_id": {
                        "id": 1,
                        "name": "All"
                    },
                    "id": 3
                },
                "id": 2,
                "tax_id": [
                    {
                        "id": 7,
                        "name": "Tax 15.00%"
                    }
                ]
            }
        ],
        "amount_tax": 915.75,
        "state": "manual",
        "user_id": {
            "id": 1,
            "name": "Admin"
        },
        "date_order": "2016-06-02 18:41:42",
        "partner_id": {
            "city": "City 1",
            "id": 6,
            "name": "Customer 1"
        },
        "id": 1,
        "amount_total": 7020.75
    }


**Example #2: 'res.partner - Update one' - request json**::

    {
        # simple fields (non relational):
        'name':         'TEST Name~~',
        'street':       'TEST Street~~',
        'street2':      'TEST Street2~~',
        'city':         'TEST City~~',
        'zip':          '123~~',
        'phone':        '+123456789~~',
        'email':        'a@b.com~~',
        # many2one fields (existing 'id', not dictionary of new record!):
        'state_id':     6,
        'country_id':   14,
        # one2many fields (list of dictionaries of records):
        'bank_ids': [
            {                                   # this record will be updated (because 'id' is specified)
                'id':           56,
                'acc_number':   'acc_number 1~~',
                'bank_bic':     'bank_bic 1~~',
            },
            {                                   # this record will be removed (because 'id' is specified and record is empty)
                'id':           57,
            },
            {                                   # this record will be created (because 'id' is not specified but record is not empty)
                'acc_number':   'acc_number 4',
                'bank_bic':     'bank_bic 4',
            },
        ],
        # many2many fields (list of dictionaries of existing 'ids'):
        'category_id': [  # field's values will be replaced by this 'ids'
            {'id': 3},
            {'id': 4},
        ],
    }


The composition and structure of the request and response fields **can have a tree-like structure** with almost any level of **nesting**. Also, the fields in this structure are very **easy to add or delete, without writing or deleting code.**

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DETAILED DESCRIPTION
====================
|

**Full list of REST resources**::

    (url prefix)                      (method)    (action)

       (authentication):

    /api/auth/get_tokens                POST    - Login in Odoo and get access tokens
    /api/auth/refresh_token             POST    - Refresh access token
    /api/auth/delete_tokens             POST    - Delete access tokens from token store

       (models):

    /api/account.invoice                GET     - Read all (with optional filters, offset, limit, order)
    /api/account.invoice/<id>           GET     - Read one
    /api/account.invoice                POST    - Create one
    /api/account.invoice/<id>           PUT     - Update one
    /api/account.invoice/<id>           DELETE  - Delete one
    /api/account.invoice/<id>/<method>  PUT     - Call method (with optional parameters)

    /api/account.invoice.line               GET     - Read all (with optional filters, offset, limit, order)
    /api/account.invoice.line/<id>          GET     - Read one
    /api/account.invoice.line               POST    - Create one
    /api/account.invoice.line/<id>          PUT     - Update one
    /api/account.invoice.line/<id>          DELETE  - Delete one
    /api/account.invoice.line/<id>/<method> PUT     - Call method (with optional parameters)

    /api/product.template               GET     - Read all (with optional filters, offset, limit, order)
    /api/product.template/<id>          GET     - Read one
    /api/product.template               POST    - Create one
    /api/product.template/<id>          PUT     - Update one
    /api/product.template/<id>          DELETE  - Delete one
    /api/product.template/<id>/<method> PUT     - Call method (with optional parameters)

    /api/report/<method>                PUT     - Call method (with optional parameters)

    /api/res.partner                    GET     - Read all (with optional filters, offset, limit, order)
    /api/res.partner/<id>               GET     - Read one
    /api/res.partner                    POST    - Create one
    /api/res.partner/<id>               PUT     - Update one
    /api/res.partner/<id>               DELETE  - Delete one
    /api/res.partner/<id>/<method>      PUT     - Call method (with optional parameters)

    /api/sale.order                     GET     - Read all (with optional filters, offset, limit, order)
    /api/sale.order/<id>                GET     - Read one
    /api/sale.order                     POST    - Create one
    /api/sale.order/<id>                PUT     - Update one
    /api/sale.order/<id>                DELETE  - Delete one
    /api/sale.order/<id>/<method>       PUT     - Call method (with optional parameters)

    /api/sale.order.line                GET     - Read all (with optional filters, offset, limit, order)
    /api/sale.order.line/<id>           GET     - Read one
    /api/sale.order.line                POST    - Create one
    /api/sale.order.line/<id>           PUT     - Update one
    /api/sale.order.line/<id>           DELETE  - Delete one
    /api/sale.order.line/<id>/<method>  PUT     - Call method (with optional parameters)


The detailed description of IN/OUT data (json data and HTTP-headers) for each REST resource presents in appropriate models files like '/controllers/model__xxxxxxxxxx.py' and in file '/controllers/auth.py'.

By default this model's resources are disabled:
    - account.invoice
    - account.invoice.line
    - product.template
    - sale.order
    - sale.order.line

To enable one of them - you need to install appropriate standard module - 'account' or 'product' or 'sale', and then uncomment **one** appropriate import line in file '/controllers/resources.py'.

If you want to disable any model - you need to comment out **one** appropriate import line in file '/controllers/resources.py'.

|
**The procedure of adding any Odoo model in REST API:**

1. Clone and rename the template file "/controllers/model__TEMPLATE.py" - replace the word "TEMPLATE" by "your_model_name".
For example::
    "model__TEMPLATE.py" >> "model__res_partner.py"

2. Make some mechanical work in that file: replace all substrings "model.name" and "model_name" by substrings "your.model.name" and "your_model_name" respectively.
For example::
    "model.name" >> "res.partner"
    "model_name" >> "res_partner"

3. (most important) Fill the three lists of response Odoo fields for "Read one", "Read all" and "Create one" methods in that file in three variables - "OUT__your_model_name__read_one__JSON", "OUT__your_model_name__read_all__JSON" and "OUT__your_model_name__create_one__JSON".
Example of fields list::

    (
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

There can be any level of nesting of inner fields.

If you'll want to add or remove some Odoo field in REST API in the future, you'll need just add or remove/comment out a field in this list.

4. If necessary (but not mandatory), change the values of some variables which are labeled by tag "# editable" in that file.
There are such variables::
    - successful response codes in all methods;
    - default values in "Create one" method.

5. Add one import line of your new file in the file '/controllers/resources.py'.
For example::
    import model__your_model_name

6. Restart Odoo server.

|
**More examples of the request and response fields:**


**Example #3: 'sale.order - Read one' - response fields list**::

    (
        # (The order of fields of different types maybe arbitrary)
        # simple fields (non relational):
        'id',
        'name',
        'date_order',
        'create_date',
        'amount_tax',
        'amount_total',
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
        # one2many fields:
        ('order_line', [(
            'id',
            ('product_id', (  # many2one
                'id',
                'name',
                'type',
                'barcode',
                ('categ_id', (  # many2one
                    'id',
                    'name',
                )),
                ('attribute_line_ids', [(  # one2many
                    'id',
                    'display_name',
                )]),
            )),
            'name',
            'product_uom_qty',
            'price_unit',
            ('tax_id', [(  # many2many
                'id',
                'name',
            )]),
            'price_subtotal',
        )]),
    )


**Example #4: 'res.partner - Read all' - response json**::

    {
        "count": 11,
        "results": [
            {
                "id": 3,
                "name": "Admin"
            },
            {
                "id": 6,
                "name": "Customer 1"
            },
            {
                "id": 8,
                "name": "Customer 2"
            },
            {
                "id": 7,
                "name": "Customer 3"
            },
            {
                "id": 1,
                "name": "Our Company 1"
            },
            {
                "id": 9,
                "name": "Supplier 1"
            },
            {
                "id": 11,
                "name": "Contact 1"
            },
            {
                "id": 12,
                "name": "Contact 2"
            },
            {
                "id": 10,
                "name": "Supplier 2"
            },
            {
                "id": 5,
                "name": "Template User"
            },
            {
                "id": 41,
                "name": "TEST Name~~"
            }
        ]
    }


**Example #5: 'res.partner - Create one' - request json**::

    {
        # simple fields (non relational):
        'name':         'TEST Name',
        'street':       'TEST Street',
        'street2':      'TEST Street2',
        'city':         'TEST City',
        'zip':          '123',
        'phone':        '+123456789',
        'email':        'a@b.com',
        # many2one fields (existing 'id', not dictionary of new record!):
        'state_id':     10,
        'country_id':   235,
        # one2many fields (list of dictionaries of new records):
        'bank_ids': [
            {
                'acc_number':   'acc_number 1',
                'bank_bic':     'bank_bic 1',
            },
            {
                'acc_number':   'acc_number 2',
                'bank_bic':     'bank_bic 2',
            },
            {
                'acc_number':   'acc_number 3',
                'bank_bic':     'bank_bic 3',
            },
        ],
        # many2many fields (list of dictionaries of existing 'ids'):
        'category_id': [
            {'id': 1},
            {'id': 2},
        ],
    }


Other examples it can see in the existing different models files like '/controllers/model__xxxxxxxxxx.py'.


Before running this module, you need to install, setup and run 'Redis' server, something like this:
    - $ sudo yum install redis python-redis
    - $ redis-server

Useful 'Redis' links:

    - https://pypi.python.org/pypi/redis
    - http://redis.io/topics/quickstart

This module adds the following 'System Parameters' in Odoo:
    - oauth2_access_token_expires_in (600)
    - oauth2_refresh_token_expires_in (7200)
    - redis_host (localhost)
    - redis_port (6379)
    - redis_db (0)
    - redis_password (None)

**This module requires the 'db_name' and 'dbfilter' Odoo config parameters (or command line options) with only one database!**

**After the installation of this module it need to restart Odoo server!**

|
**To test REST resources can be used 'curl', like this**::

    (Linux syntax)

    1. Login in Odoo and get access tokens:
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/auth/get_tokens   -X POST   -d '{"db":"testdb10", "username":"admin", "password":"admin"}'

    2. Refresh access token:
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/auth/refresh_token   -X POST   -d '{"refresh_token":"XXXXXXXXXXXXXXXXX"}'

    3. Delete access tokens from token store:
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/auth/delete_tokens   -X POST   -d '{"refresh_token":"XXXXXXXXXXXXXXXXX"}'

    4. res.partner - Read all (without filters):
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/res.partner   -X GET   -H "Access-Token: XXXXXXXXXXXXXXXXX"

    5. res.partner - Read all (with two filters):
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/res.partner   -X GET   -H "Access-Token: XXXXXXXXXXXXXXXXX"   -d '{"filters": "[(\"name\", \"like\", \"ompany\"), (\"id\", \"<=\", 50)]"}'

    6. res.partner - Read one:
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/res.partner/3   -X GET   -H "Access-Token: XXXXXXXXXXXXXXXXX"

    7. res.partner - Create one:
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/res.partner   -X POST   -H "Access-Token: XXXXXXXXXXXXXXXXX"   -d '{"name": "TEST Name", "street": "TEST Street", "city": "TEST City"}'

    8. res.partner - Update one:
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/res.partner/2361   -X PUT   -H "Access-Token: XXXXXXXXXXXXXXXXX"   -d '{"name": "TEST Name~~", "street": "TEST Street~~", "city": "TEST City~~"}'

    9. res.partner - Delete one:
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/res.partner/2361   -X DELETE   -H "Access-Token: XXXXXXXXXXXXXXXXX"

    10. res.partner - Call method 'address_get' (without parameters):
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/res.partner/2361/address_get   -X PUT   -H "Access-Token: XXXXXXXXXXXXXXXXX"

    11. res.partner - Call method '_email_send' (with parameters):
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/res.partner/2361/_email_send   -X PUT   -H "Access-Token: XXXXXXXXXXXXXXXXX"   -d '{"email_from": "test@test.com", "subject": "TEST Subject", "body": "TEST Body"}'

    12. report - Call method 'get_pdf' (with parameters):
    curl -v -i -k -H "Content-Type: text/html"   http://localhost:8069/api/report/get_pdf   -X PUT   -H "Access-Token: XXXXXXXXXXXXXXXXX"   -d '{"report_name": "account.report_invoice", "docids": [3]}'


There are also some files in Python for examples and testing purpose:
    - /controllers/tests/test__Auth_GetTokens.py
    - /controllers/tests/test__Create__product.template.py (with attributes)
    - /controllers/tests/test__Create__res.partner.py
    - /controllers/tests/test__Update__res.partner.py


CHANGELOG
=========
|

version 1.3 (2017-10-25):
    - added the ability to fetch any existing PDF report from Odoo

version 1.2 (2017-02-08):
    - added the ability to customize response Odoo fields returned by 'Create one' method (see changes in file "/controllers/model__TEMPLATE.py")

version 1.1 (2017-01-03):
    - added **call any method** of Odoo model

version 1.0 (2016-06-25):
    - initial release (for Odoo v8/9)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Support email: avs3.ua@gmail.com

