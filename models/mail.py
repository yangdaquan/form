
from models.mongo_model import Mongo_Model


class Mail(Mongo_Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
            ('content', str, ''),
            ('sender_id', int, 0),
            ('receiver_id', int, 0),
            ('read', bool, False),
        ]
        return names

    def mark_read(self):
        self.read = True
        self.save()
