from uuid import uuid4
from sqlalchemy.orm import relationship

from app.extensions import db
from app.services.github import GitHub


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    avatar_url = db.Column(db.String(255), nullable=True)
    github_id = db.Column(db.Integer(), nullable=True)
    photos = db.relationship(
        'Photo',
        cascade='all, delete',
        backref='owner',
        lazy=True
    )

    def __init__(self, id, username, avatar_url, github_id, photos):
        self.id = id
        self.username = username
        self.avatar_url = avatar_url
        self.github_id = github_id
        self.photos = photos

    @staticmethod
    def find_or_create_from_token(access_token):
        data = GitHub.get_user_from_token(access_token)

        """Find existing user or create new User instance"""
        instance = User.query.filter_by(github_id=data['id']).first()

        if not instance:
            instance = User(
                uuid4(),
                data['login'],
                data['avatar_url'],
                data['id'],
                []
            )
            db.session.add(instance)
            db.session.commit()

        return instance

    def __repr__(self):
        return "<User: {}>".format(self.username)
