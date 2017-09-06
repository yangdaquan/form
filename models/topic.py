import time

from models.mongo_model import Mongo_Model
from models.user import User


class Topic(Mongo_Model):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('views', int, 0),
            ('title', str, ''),
            ('content', str, ''),
            ('user_id', int, 0),
            ('board_id', int, 0),
        ]
        return names


    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m


    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m

    def user(self):
        u = User.find(self.user_id)
        return u

    @classmethod
    def topic_sort(cls, user_id):
        ms = Topic.find_all(user_id=user_id)
        l = []
        if ms != [None]:
            ms = sorted(ms, key=lambda x: x.created_time, reverse=True)
            if len(ms) >= 1:
                for i in range(len(ms)):
                    l.append(ms[i])
            else:
                return ms
        return l



