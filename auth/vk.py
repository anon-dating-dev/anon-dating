import tornado.web
from vkmixin import VKMixin
from settings import Settings


class VkAuthHandler(tornado.web.RequestHandler, VKMixin):

    def initialize(self, login_url):
        self._login_url = login_url
        self._base_url = Settings.get('app')['base_url']
        self._port = Settings.get('app')['port']
        self._authSettings = Settings.get('auth')['vk']

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument("code", False)
        if not code:
            yield self.authorize_redirect(redirect_uri=self._get_redirect_uri(),
                                          client_id=self._authSettings['client_id'])
        else:
            user = yield self.get_authenticated_user(redirect_uri=self._get_redirect_uri(),
                                                     client_id=self._authSettings['client_id'],
                                                     client_secret=self._authSettings['client_secret'],
                                                     code=code)
            print "User %s" % user
            self.redirect('/')

    def _get_redirect_uri(self):
        return "%s:%s%s" % (self._base_url, self._port, self._login_url)