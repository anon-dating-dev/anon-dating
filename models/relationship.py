from common.model import Model


class Relationship(Model):
    """
    Relation between two users.
    """
    def __init__(self, db, **kwargs):
        super(Relationship, self).__init__(db)
        self._db = db
        self._first_id = kwargs.get('first_id')
        self._second_id = kwargs.get('second_id')
        self._level = kwargs.get('level')

    @property
    def first_id(self):
        return self._first_id

    @property
    def second_id(self):
        return self._second_id

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        query = "UPDATE relationships" \
                "SET level=%s" \
                "WHERE first_id=%s AND second_id=%s"
        return self.__class__._execute(self._db, query, (value, self.first_id, self.second_id))

    def remove(self):
        query = "DROP FROM relationships" \
                "WHERE first_id=%s AND second_id=%s"
        return self.__class__._execute(self._db, query, (self.first_id, self.second_id))

    @classmethod
    def create(cls, db, first_id, second_id):
        query = "INSERT INTO relationships" \
                "(first_id, second_id)" \
                "VALUES (%s, %s)"
        return cls._execute(db, query, (first_id, second_id))
