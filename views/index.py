import tornado.web
from common.base_request_handler import BaseRequestHandler
from models.user import User

class IndexHandler(BaseRequestHandler):
    """
    Render main page.
    """
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        print 'uid', self.get_secure_cookie('uid')
        #user = yield User.get_by_id(self.db, 11)
        #print 'User model', user
        self.render('index.html')