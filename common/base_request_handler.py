import tornado.web
import momoko
from psycopg2.extras import NamedTupleConnection
from settings import Settings


class BaseRequestHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        """
        Lazy connect to db.
        """
        if not hasattr(self.application, 'db'):
            dsn = Settings.get('db')['dsn']
            self.application.db = momoko.Pool(dsn=dsn, connection_factory=NamedTupleConnection)
        return self.application.db
