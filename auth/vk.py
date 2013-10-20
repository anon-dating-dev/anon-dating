import tornado.web
from vkmixin import VKMixin
from settings import Settings


class VkAuthHandler(tornado.web.RequestHandler, VKMixin):

    def __init__(self, *args, **kwargs):
        super(VkAuthHandler, self).__init__(*args, **kwargs)
        self._authSettings = Settings.get('auth')

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument("code", False)
        if not code:
                yield self.authorize_redirect(redirect_uri='http://localhost:8888/login',
                                              client_id=self._authSettings['vk']['client_id'])
        else:
            user = yield self.get_authenticated_user(redirect_uri='http://localhost:8888/login',
                                                     client_id=self._authSettings['vk']['client_id'],
                                                     client_secret=self._authSettings['vk']['client_secret'],
                                                     code=code)
            print "User %s" % user
            self.redirect('/')