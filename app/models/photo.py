from uuid import uuid4

from app.extensions import db


class Photo(db.Model):
    __tablename__ = 'photo'

    id = db.Column(db.String(255), primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    user_id = db.Column(
        db.String(255),
        db.ForeignKey('user.id'),
        nullable=False
    )

    def __init__(self, image_url, id=uuid4()):
        self.image_url = image_url
        self.id = id

    def __repr__(self):
        return "<Image: {}>".format(self.image_url)
