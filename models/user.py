import json
import momoko


class User(object):
    def __init__(self):
        super(User, self).__init__()

    @classmethod
    def create(cls, db=None, **args):
        query = "INSERT INTO users" \
                "(city_id, city_name, gender, profile)"\
                "VALUES (%s, %s, %s, %s)"
        params = (args['city_id'],
                  'test',
                  args['gender'],
                  json.dumps(args['profile']))
        return momoko.Op(db.execute, query, params)