from env import DATABASE_URL

from sqlalchemy import Column, BigInteger

from SayaStringSession.database import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(BigInteger, primary_key=True)

    def __init__(self, user_id, channels=None):
        if DATABASE_URL == "":
            return
        self.user_id = user_id
        self.channels = channels

    # def __repr__(self):
    #     return "<User {} {} {} ({})>".format(self.thumbnail, self.thumbnail_status, self.video_to, self.user_id)


if DATABASE_URL and SESSION is not None:
    Users.__table__.create(checkfirst=True)


async def num_users():
    if not DATABASE_URL or SESSION is None:
        return 0
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()
