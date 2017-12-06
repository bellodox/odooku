# -*- coding: utf-8 -*-
import redis
import logging
try:
    import simplejson as json
except ImportError:
    import json

_logger = logging.getLogger(__name__)


class RedisTokenStore(object):
    
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.rs = redis.StrictRedis(host=host, port=port, db=db, password=password)
        # Connection test
        try:
            res = self.rs.get('foo')
            _logger.info("<REDIS> Successful connect to Redis-server.")
        except:
            _logger.error("<REDIS> ERROR: Failed to connect to Redis-server!")
            print "<REDIS> ERROR: Failed to connect to Redis-server!"
    
    def save_all_tokens(self, access_token, expires_in,
                    refresh_token, refresh_expires_in, user_id):
        # access_token
        self.rs.set('access_' + access_token,
                    json.dumps({'user_id': user_id}),
                    expires_in
        )
        # refresh_token
        self.rs.set('refresh_' + refresh_token,
                    json.dumps({
                        'access_token': access_token,
                        'user_id':      user_id
                    }),
                    refresh_expires_in
        )
    
    def fetch_by_access_token(self, access_token):
        key = 'access_' + access_token
        _logger.info("<REDIS> Fetch by access token.")
        data = self.rs.get(key)
        if data:
            return json.loads(data)
        else:
            return None
    
    def fetch_by_refresh_token(self, refresh_token):
        key = 'refresh_' + refresh_token
        _logger.info("<REDIS> Fetch by refresh token.")
        data = self.rs.get(key)
        if data:
            return json.loads(data)
        else:
            return None
    
    def delete_access_token(self, access_token):
        self.rs.delete('access_' + access_token)
    
    def delete_refresh_token(self, refresh_token):
        self.rs.delete('refresh_' + refresh_token)
    
    def update_access_token(self, old_access_token,
                            new_access_token, expires_in,
                            refresh_token, user_id):
        # Delete old access token
        self.delete_access_token(old_access_token)
        # Write new access token
        self.rs.set('access_' + new_access_token,
                    json.dumps({'user_id': user_id}),
                    expires_in
        )
        # Rewrite refresh token
        refresh_token_key = 'refresh_' + refresh_token
        current_ttl = self.rs.ttl(refresh_token_key)
        self.rs.set(refresh_token_key,
                    json.dumps({
                        'access_token': new_access_token,
                        'user_id':      user_id
                    }),
                    current_ttl
        )
    
    def delete_all_tokens_by_refresh_token(self, refresh_token):
        refresh_token_data = self.fetch_by_refresh_token(refresh_token)
        if refresh_token_data:
            access_token = refresh_token_data['access_token']
            # Delete tokens
            self.delete_access_token(access_token)
            self.delete_refresh_token(refresh_token)
    
