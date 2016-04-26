from flask.ext.login import UserMixin

from app import db

class User(UserMixin, db.Model):
    '''Represents users'''
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), nullable=True, index=True, unique=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.nickname)

    @property
    def is_authenticated(self):
        '''Should return True unless the user should not be allowed to
        authenticate. (Method name is a bit misleading but needs to be
        implemented for login)'''
        return True

    @property
    def is_active(self):
        '''Should return True unless a user is inactive (e.g. banned)'''
        return True

    @property
    def is_anonymous(self):
        '''Should return True only for fake users that are not supposed to log
        in'''
        return False

    def get_id(self):
        '''Returns a unique identifier for the user, in unicode'''
        return str(self.id)

class Post(db.Model):
    '''Represents blog posts written by users'''
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}'.format(self.body)
