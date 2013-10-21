import momoko


class Model(object):

    def __init__(self, db):
        super(Model, self).__init__()
        self._db = db

    @classmethod
    def _execute(cls, db, query, params):
        """
        Execute db query
        @param db: db connection instance
        @param query: str
        @param params: tuple
        """
        return momoko.Op(db.execute, query, params)
