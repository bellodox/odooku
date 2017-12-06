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


print '\n 2. res.partner - Update one:'
r = requests.put(
    'http://localhost:8069/api/res.partner/41',  # fill 'id' here!
    headers = {
        'Content-Type': 'text/html; charset=utf-8',
        'Access-Token': access_token
    },
    data = json.dumps({
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
    }),
    #verify = False      # for TLS/SSL connection
)
print r.text
