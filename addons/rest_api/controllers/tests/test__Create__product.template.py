import requests, json


print '\n 1. Login in Odoo and get access tokens:'
r = requests.post(
    'http://localhost:8069/api/auth/get_tokens',
    headers = {'Content-Type': 'text/html; charset=utf-8'},
    data = json.dumps({
        'db':       'testdb10',
        'username': 'admin',
        'password': 'admin',
    }),
    #verify = False      # for TLS/SSL connection
)
print r.text
access_token = r.json()['access_token']


print '\n 2. product.template - Create one:'
r = requests.post(
    'http://localhost:8069/api/product.template',
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Access-Token': access_token
    },
    data = json.dumps({
        
        # simple field (non relational)
        'name': 'TEST Product (with attributes)',
        
        # one2many field (list of dictionaries of new records)
        'attribute_line_ids': [
            {
                # Database data description:
                # "Color" is 'product.attribute' ID: 2
                # "White" is 'product.attribute.value' ID: 3
                # "Black" is 'product.attribute.value' ID: 4
                
                # many2one field (EXISTING 'id', NOT dictionary of new record!)
                'attribute_id': 2,  # "Color"
                
                # many2many field (list of EXISTING 'ids' with TECHNICAL PREFIX)
                'value_ids': [(6,0, [3, 4])],  # ["White", "Black"]
                # (or equivalent way)
                #'value_ids': [(4, 3), (4, 4)],
            },
            #...
        ],
        
    }),
    #verify = False      # for TLS/SSL connection
)
print r.text
