import time
from models.mongua import Mongua
from models.topic import Topic
from models.user import User


class Reply(Mongua):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names = names + [
            ('content', str, ''),
            ('topic_id', int, 0),
            ('user_id', int, 0),
        ]
        return names

    def user(self):
        u = User.find(self.user_id)
        return u


    @classmethod
    def topic_of_reply(cls,user_id):
        rs = Reply.find_all(user_id=user_id)
        ts = []
        for r in rs:
            t = Topic.find(r.topic_id)
            if t not in ts:
                ts.append(t)
        return ts


    @classmethod
    def topic_of_reply_sort(cls, user_id):
        ts = Reply.topic_of_reply(user_id)
        l = []
        if ts != [None]:
            ts = sorted(ts, key=lambda x: x.created_time, reverse=True)
            if len(ts) >= 1:
                for i in range(len(ts)):
                    l.append(ts[i])
            else:
                return ts
        return l

