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


print '\n 2. res.partner - Create one:'
r = requests.post(
    'http://localhost:8069/api/res.partner',
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Access-Token': access_token
    },
    data = json.dumps({
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
    }),
    #verify = False      # for TLS/SSL connection
)
print r.text
