#@todo: replace with tornado.escape
import json
from tornado.auth import OAuth2Mixin, _auth_return_future, return_future, AuthError
from tornado.httpclient import AsyncHTTPClient


class VKMixin(OAuth2Mixin):
    _OAUTH_ACCESS_TOKEN_URL = "https://oauth.vk.com/access_token?"
    _OAUTH_AUTHORIZE_URL = "https://oauth.vk.com/authorize?"
    _API_REQUEST_URL = "https://api.vk.com/method/"

    @return_future
    def authorize_redirect(self, redirect_uri=None, client_id=None,
                           client_secret=None, extra_params=None, callback=None):
        if extra_params is None:
            extra_params = {}
        extra_params.update({'scope': 'PERMISSIONS',
                             'response_type': 'code'})
        super(VKMixin, self).authorize_redirect(redirect_uri, client_id,
                                                client_secret, extra_params, callback)

    @_auth_return_future
    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                               code, callback, extra_params=None):
        client = self.get_auth_http_client()
        if extra_params is None:
            extra_params = {}
        extra_params.update({'response_type': 'token', 'redirect_uri': redirect_uri})
        token_url = self._oauth_request_token_url("https://oauth.vk.com/blank.html",
                                                  client_id,
                                                  client_secret,
                                                  code,
                                                  extra_params)
        client.fetch(token_url, self.async_callback(self._on_access_token,
                                                    callback))

    def _on_access_token(self, callback, response):
        if response.error:
            callback.set_exception(AuthError('Vk auth error: %s' % str(response)))
            return
        body = json.loads(response.body)
        access_token = body['access_token']
        user_id = body['user_id']
        self._get_user_info(user_id, access_token, callback)

    def _get_user_info(self, user_id, access_token, callback):
        client = self.get_auth_http_client()
        fields = ['sex', 'bdate', 'city', 'country', 'photo_50', 'photo_max_orig']
        url = "%susers.get?user_ids=%s&fields=%s&ACCESS_TOKEN=%s" % (self._API_REQUEST_URL,
                                                                     user_id,
                                                                     ','.join(fields),
                                                                     access_token)
        client.fetch(url, self.async_callback(self._on_user_info, callback))

    def _on_user_info(self, callback, response):
        body = json.loads(response.body)
        user_info = body['response'][0]
        callback.set_result(user_info)

    def get_auth_http_client(self):
        return AsyncHTTPClient()
