import json
from common.model import Model
from tornado import  gen
from relationship import Relationship


class User(Model):

    def __init__(self, db, **kwargs):
        super(User, self).__init__(db)
        self._id = kwargs.get('id')
        self._external_id = kwargs.get('external_id')
        self._city_id = kwargs.get('city_id')
        self._city_name = kwargs.get('city_name')
        self._gender = kwargs.get('gender')
        self._profile = kwargs.get('profile')

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def external_id(self):
        return self.external_id

    @external_id.setter
    def external_id(self, value):
        self._external_id = value

    @property
    def city_id(self):
        return self._city_id

    @city_id.setter
    def city_id(self, value):
        self._city_id = value

    @property
    def city_name(self):
        return self._city_name

    @city_name.setter
    def city_name(self, value):
        self._city_name = value

    @property
    def gender(self):
        return self.external_id

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, value):
        self._profile = value

    @classmethod
    def _get_instance_from_cursor(cls, db, cursor):
        kwargs = {
            'id': cursor.id,
            'external_id': cursor.external_id,
            'city_id': cursor.city_id,
            'city_name': cursor.city_name,
            'gender': cursor.gender,
            'profile': cursor.profile
        }
        return super(User, cls)._get_instance_from_cursor(db, **kwargs)

    @gen.coroutine
    def save(self):
        insert_query = """
            INSERT INTO users
                (external_id, city_id, city_name, gender, profile)
            VALUES (%s, %s, %s, %s, %s)
        """
        update_query = """
            UPDATE users SET
                city_id = %s,
                city_name = %s,
                profile = %s
            WHERE id = %s
        """
        inset_params = (self._external_id,
                        self._city_id,
                        self._city_name,
                        self._gender,
                        json.dumps(self._profile))
        update_params = (self._city_id,
                         self._city_name,
                         json.dumps(self._profile),
                         self._id)
        yield super(User, self).save(insert_query, update_query, inset_params, update_params)

    @classmethod
    @gen.coroutine
    def get_by_id(cls, db, user_id):
        query = """
            SELECT * FROM users
            WHERE id = %s
        """
        users = yield cls.select(db, query, (user_id,))
        raise gen.Return(None if len(users) == 0 else users[0])

    @classmethod
    @gen.coroutine
    def get_by_external_id(cls, db, external_id):
        query = """
            SELECT * FROM users
            WHERE external_id = '%s'
        """
        users = yield cls.select(db, query, (external_id,))
        raise gen.Return(None if len(users) == 0 else users[0])

    @classmethod
    #@gen.coroutine
    def get_by_city_id_and_gender(cls, db, city_id, gender):
        query = """
            SELECT * FROM users
            WHERE city_id=%s AND gender = %s
        """
        cls.select(query, (city_id, gender))

    def get_related_users(self):
        query = """
            SELECT * FROM users
            INNER JOIN relationships AS r
                ON (r.first_id == id OR r.second_id = id)
            WHERE id = %s
        """
        self.__class__.select(query, (self.id, ))

    def create_new_relationship(self, user_id):
        relationship = Relationship(self._db, first_id=self._id, second_id=user_id)
        relationship.save()

    def remove_relationship(self, user_id):
        relationship = Relationship.get_by_ids(self._db, self._id, user_id)
        relationship.remove()

    def set_relationship_level(self, user_id, value):
        relationship = Relationship.get_by_ids(self._db, self._id, user_id)
        relationship.level = value
