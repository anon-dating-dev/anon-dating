from common.model import Model


class Message(Model):
    def __init__(self, db, **kwargs):
        super(Message, self).__init__(db)
        self._id = kwargs.get('id')
        self._recipient_id = kwargs.get('recipient_id')
        self._sender_id = kwargs.get('sender_id')
        self._text = kwargs.get('text')
        self._creation_date = kwargs.get('creation_date')

    @classmethod
    def _get_instance_from_cursor(cls, db, cursor):
        kwargs = {
            'id': cursor.id,
            'recipient_id': cursor.recipient_id,
            'sender_id': cursor.sender_id,
            'text': cursor.text,
            'creation_date': cursor.creation_date
        }
        return super(db, **kwargs)

    def save(self):
        insert_query = """
            INSERT INTO messages
                (recipient_id, sender_id, text, creation_date)
            VALUES (%s, %s, %s, NOW())
        """
        insert_params = (self._recipient_id, self._sender_id, self._text)
        super(insert_query, None, insert_params)
