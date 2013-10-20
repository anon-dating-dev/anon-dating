import tornado.web
import momoko
from vkmixin import VKMixin
from settings import Settings
from models.user import User

class VkAuthHandler(tornado.web.RequestHandler, VKMixin):

    def initialize(self, login_url):
        self._login_url = login_url
        self._base_url = Settings.get('app')['base_url']
        self._port = Settings.get('app')['port']
        self._authSettings = Settings.get('auth')['vk']

    @property
    def db(self):
        if not hasattr(self.application, 'db'):
            dsn = 'dbname=%s user=%s password=%s host=%s port=%s' % ('anon_dating',
                                                                     'anon_dating_admin',
                                                                     'anon',
                                                                     'localhost',
                                                                     5433)
            self.application.db = momoko.Pool(dsn=dsn)
        return self.application.db

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument("code", False)
        #@todo: catch AuthError
        if not code:
            yield self.authorize_redirect(redirect_uri=self._get_redirect_uri(),
                                          client_id=self._authSettings['client_id'])
        else:
            user = yield self.get_authenticated_user(redirect_uri=self._get_redirect_uri(),
                                                     client_id=self._authSettings['client_id'],
                                                     client_secret=self._authSettings['client_secret'],
                                                     code=code)
            print "User %s" % user
            args = {
                'city_id': user['city'],
                'profile': {'first_name': user['first_name'],
                            'last_name': user['last_name'],
                            'user_pic_small': user['photo_50'],
                            'user_pic_big': user['photo_max_orig']},
                'gender': user['sex']
            }
            cursor = yield User.create(db=self.db, **args)
            print "Saved"
            self.redirect('/')

    def _get_redirect_uri(self):
        return "%s:%s%s" % (self._base_url, self._port, self._login_url)