from psycopg2._psycopg import ProgrammingError
from tornado import gen
import momoko


class Model(object):

    def __init__(self, db):
        super(Model, self).__init__()
        self._db = db

    @gen.coroutine
    def save(self, insert_query, update_query, insert_params, update_params):
        if self._id is None:
            query = "%s RETURNING id" % insert_query
            params = insert_params
        else:
            query = update_query
            params = update_params
        cursor = yield self.__class__._execute(self._db, query, params)
        try:
            cursor = cursor.fetchone()
            self._id = cursor.id
        except ProgrammingError:
            return

    @classmethod
    def _execute(cls, db, query, params):
        """
        Execute db query
        @param db: db connection instance
        @param query: str
        @param params: tuple
        """
        return momoko.Op(db.execute, query, params)

    @classmethod
    def _get_instance_from_cursor(cls, db, **kwargs):
        return cls(db, **kwargs)

    @classmethod
    @gen.coroutine
    def create(cls, db, **args):
        instance = cls(db, **args)
        yield instance.save()
        raise gen.Return(instance)

    @classmethod
    @gen.coroutine
    def select(cls, db, query, params):
        cursor = yield cls._execute(db, query, params)
        instance_list = []
        for row in cursor.fetchall():
            instance_list.append(cls._get_instance_from_cursor(db, row))
        raise gen.Return(instance_list)
