import tornado.web
from vkmixin import VKMixin
from common.base_request_handler import BaseRequestHandler
from settings import Settings
from models.user import User


class VkAuthHandler(BaseRequestHandler, VKMixin):
    """
    Auth users with vk.com OAuth2.
    """
    def initialize(self, login_url):
        self._login_url = login_url
        self._base_url = Settings.get('app')['base_url']
        self._port = Settings.get('app')['port']
        self._authSettings = Settings.get('auth')['vk']

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument("code", False)
        #@todo: catch AuthError
        if not code:
            yield self.authorize_redirect(redirect_uri=self._get_redirect_uri(),
                                          client_id=self._authSettings['client_id'])
        else:
            vk_user = yield self.get_authenticated_user(redirect_uri=self._get_redirect_uri(),
                                                     client_id=self._authSettings['client_id'],
                                                     client_secret=self._authSettings['client_secret'],
                                                     code=code)
            user = yield User.get_by_external_id(self.db, vk_user['uid'])
            user = User(self.db) if user is None else user
            user.external_id = vk_user['uid']
            user.city_id = vk_user['city']
            user.city_name = 'foooo'
            user.gender = vk_user['sex']
            user.profile = {'first_name': vk_user['first_name'],
                            'last_name': vk_user['last_name'],
                            'user_pic_small': vk_user['photo_50'],
                            'user_pic_big': vk_user['photo_max_orig']}
            yield user.save()
            self.set_secure_cookie('uid', str(user.id))
            self.redirect('/')

    def _get_redirect_uri(self):
        return "%s:%s%s" % (self._base_url, self._port, self._login_url)