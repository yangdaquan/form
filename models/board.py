import time
from models.mongo_model import Mongo_Model


class Board(Mongo_Model):

    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('title', str, ''),
        ]
        return names
