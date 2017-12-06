# -*- coding: utf-8 -*-
from main import *

_logger = logging.getLogger(__name__)


# List of REST resources in current file:
#   (url prefix)            (method)     (action)
# /api/auth/get_tokens        POST    - Login in Odoo and get access tokens
# /api/auth/refresh_token     POST    - Refresh access token
# /api/auth/delete_tokens     POST    - Delete access tokens from token store


# List of IN/OUT data (json data and HTTP-headers) for each REST resource:

# /api/auth/get_tokens  POST  - Login in Odoo and get access tokens
# IN data:
#   JSON:
#       {
#           "db":       "XXXX",     # Odoo db name
#           "username": "XXXX",     # Odoo username
#           "password": "XXXX"      # Odoo user password
#       }
# OUT data:
OUT__auth_gettokens__SUCCESS_CODE = 200             # editable
#   JSON:
#       {
#           "uid":                  XXX,
#           "user_context":         {....},
#           "company_id":           XXX,
#           "access_token":         "XXXXXXXXXXXXXXXXX",
#           "expires_in":           XXX,
#           "refresh_token":        "XXXXXXXXXXXXXXXXX",
#           "refresh_expires_in":   XXX
#       }

# /api/auth/refresh_token  POST  - Refresh access token
# IN data:
#   JSON:
#       {"refresh_token": "XXXXXXXXXXXXXXXXX"}
# OUT data:
OUT__auth_refreshtoken__SUCCESS_CODE = 200          # editable
#   JSON:
#       {"access_token": "XXXXXXXXXXXXXXXXX"}

# /api/auth/delete_tokens  POST  - Delete access tokens from token store
# IN data:
#   JSON:
#       {"refresh_token": "XXXXXXXXXXXXXXXXX"}
# OUT data:
OUT__auth_deletetokens__SUCCESS_CODE = 200          # editable


# HTTP controller of REST resources:

class ControllerREST(http.Controller):
    
    # Login in Odoo database and get access tokens:
    @http.route('/api/auth/get_tokens', methods=['POST'], type='http', auth='none', csrf=False)
    def api_auth_gettokens(self):
        # Convert http data into json:
        jdata = json.loads(request.httprequest.stream.read())
        
        db = jdata['db']
        username = jdata['username']
        password = jdata['password']
        
        # Compare dbname (from HTTP-request vs. Odoo config):
        if db and (db != db_name):
            error_descrip = "Wrong 'dbname'!"
            error = 'wrong_dbname'
            _logger.error(error_descrip)
            return error_response(400, error, error_descrip)
        
        # Empty 'db' or 'username' or 'password:
        if not db or not username or not password:
            error_descrip = "Empty value of 'db' or 'username' or 'password'!"
            error = 'empty_db_or_username_or_password'
            _logger.error(error_descrip)
            return error_response(400, error, error_descrip)
        
        # Login in Odoo database:
        try:
            request.session.authenticate(db, username, password)
        except:
            # Invalid database:
            error_descrip = "Invalid database!"
            error = 'invalid_database'
            _logger.error(error_descrip)
            return error_response(400, error, error_descrip)
        
        uid = request.session.uid
        
        # Odoo login failed:
        if not uid:
            error_descrip = "Odoo User authentication failed!"
            error = 'odoo_user_authentication_failed'
            _logger.error(error_descrip)
            return error_response(401, error, error_descrip)
        
        # Generate tokens
        access_token = generate_token()
        expires_in = access_token_expires_in
        refresh_token = generate_token()
        refresh_expires_in = refresh_token_expires_in
        
        # Save all tokens in store
        _logger.info("Save OAuth2 tokens of user in Redis store...")
        token_store.save_all_tokens(
            access_token = access_token,
            expires_in = expires_in,
            refresh_token = refresh_token,
            refresh_expires_in = refresh_expires_in,
            user_id = uid)
        
        # Successful response:
        return werkzeug.wrappers.Response(
            status = OUT__auth_gettokens__SUCCESS_CODE,
            content_type = 'application/json; charset=utf-8',
            headers = [ ('Cache-Control', 'no-store'),
                        ('Pragma', 'no-cache')  ],
            response = json.dumps({
                'uid':                  uid,
                'user_context':         request.session.get_context() if uid else {},
                'company_id':           request.env.user.company_id.id if uid else 'null',
                'access_token':         access_token,
                'expires_in':           expires_in,
                'refresh_token':        refresh_token,
                'refresh_expires_in':   refresh_expires_in, }),
        )
    
    # Refresh access token:
    @http.route('/api/auth/refresh_token', methods=['POST'], type='http', auth='none', csrf=False)
    def api_auth_refreshtoken(self):
        # Try convert http data into json:
        try:
            jdata = json.loads(request.httprequest.stream.read())
        except:
            jdata = {}
        # Get and check refresh token
        refresh_token = jdata.get('refresh_token')
        if not refresh_token:
            error_descrip = "No refresh token was provided in request!"
            error = 'no_refresh_token'
            _logger.error(error_descrip)
            return error_response(400, error, error_descrip)
        
        # Validate refresh token
        refresh_token_data = token_store.fetch_by_refresh_token(refresh_token)
        if not refresh_token_data:
            return error_response_401__invalid_token()
        
        old_access_token = refresh_token_data['access_token']
        new_access_token = generate_token()
        uid = refresh_token_data['user_id']
        
        # Update access (and refresh) token in store
        token_store.update_access_token(
            old_access_token = old_access_token,
            new_access_token = new_access_token,
            expires_in = access_token_expires_in,
            refresh_token = refresh_token,
            user_id = uid)
        
        # Successful response:
        return werkzeug.wrappers.Response(
            status = OUT__auth_refreshtoken__SUCCESS_CODE,
            content_type = 'application/json; charset=utf-8',
            headers = [ ('Cache-Control', 'no-store'),
                        ('Pragma', 'no-cache')  ],
            response = json.dumps({
                'access_token': new_access_token,
            }),
        )
    
    # Delete access tokens from token store:
    @http.route('/api/auth/delete_tokens', methods=['POST'], type='http', auth='none', csrf=False)
    def api_auth_deletetokens(self):
        # Try convert http data into json:
        try:
            jdata = json.loads(request.httprequest.stream.read())
        except:
            jdata = {}
        # Get and check refresh token
        refresh_token = jdata.get('refresh_token')
        if not refresh_token:
            error_descrip = "No refresh token was provided in request!"
            error = 'no_refresh_token'
            _logger.error(error_descrip)
            return error_response(400, error, error_descrip)
        
        token_store.delete_all_tokens_by_refresh_token(refresh_token)
        
        # Successful response:
        return successful_response(
            OUT__auth_deletetokens__SUCCESS_CODE,
            {}
        )
    
