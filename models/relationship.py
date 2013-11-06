from common.model import Model


class Relationship(Model):
    """
    Relation between two users.
    """
    def __init__(self, db, **kwargs):
        super(Relationship, self).__init__(db)
        self._id = kwargs.get('id')
        self._first_id = kwargs.get('first_id')
        self._second_id = kwargs.get('second_id')
        self._level = kwargs.get('level')

    @classmethod
    def _get_instance_from_cursor(cls, db, cursor):
        kwargs = {
            'id': cursor.id,
            'first_id': cursor.first_id,
            'second_id': cursor.second_id,
            'level': cursor.level
        }
        return super(db, **kwargs)

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
        self._level = value
        self.save()

    def save(self):
        insert_query = """
            INSERT INTO relationships
                (first_id, second_id)
            VALUES (%s, %s)
        """
        update_query = """
            UPDATE relationships
                SET level=%s
                WHERE first_id=%s AND second_id=%s
        """
        inset_params = (self._first_id, self._second_id)
        update_params = (self._level, self._first_id, self._second_id)
        super(insert_query, update_query, inset_params, update_params)

    def remove(self):
        query = "DROP FROM relationships" \
                "WHERE first_id=%s AND second_id=%s"
        self.__class__._execute(self._db, query, (self.first_id, self.second_id))

    @classmethod
    def get_by_ids(cls, db, first_id, second_id):
        query = """
            SELECT FROM relationships
            WHERE
                (first_id = %s AND second_id = %s) OR
                (first_id = %s AND second_id = %s)
        """
        cls.select(db, query, (first_id, second_id, second_id, first_id))
