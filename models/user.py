import json
from common.model import Model


class User(Model):

    def __init__(self, db, **kwargs):
        super(User, self).__init__(db)
        self._external_id = kwargs.get('external_id')
        self._city_id = kwargs.get('city_id')
        self._city_name = kwargs.get('city_name')
        self._gender = kwargs.get('gender')
        self._profile = kwargs.get('profile')

    @classmethod
    def create(cls, db, **args):
        query = "INSERT INTO users" \
                "(external_id, city_id, city_name, gender, profile)" \
                "VALUES (%s, %s, %s, %s, %s)"
        params = (args['external_id'],
                  args['city_id'],
                  'test',
                  args['gender'],
                  json.dumps(args['profile']))
        return cls._execute(db, query, params)

    @classmethod
    def get_by_id(cls, db, user_id):
        pass

    @classmethod
    def get_by_city_id_and_gender(cls, db, city_id, gender):
        query = "SELECT * FROM users" \
                "WHERE city_id=%s AND gender = %s"
        return cls._execute(db, query, (city_id, gender))
