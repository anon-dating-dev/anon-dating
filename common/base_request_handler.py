import tornado.web
import momoko
from settings import Settings


class BaseRequestHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        """
        Lazy connect to db.
        """
        if not hasattr(self.application, 'db'):
            dsn = Settings.get('db')['dsn']
            self.application.db = momoko.Pool(dsn=dsn)
        return self.application.db
