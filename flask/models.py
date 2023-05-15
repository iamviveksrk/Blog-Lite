from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String(), nullable=False)
    lastseen = db.Column(db.Float())
    email = db.Column(db.String())
    posts = db.relationship('Post', backref='users', lazy=True)
    userinfo = db.relationship('UserInfo', back_populates='user', lazy=True, uselist=False)

class UserInfo(db.Model):
    __tablename__ = 'userinfo'
    username = db.Column(db.String(), db.ForeignKey('users.username'))
    profile_id = db.Column(db.Integer(), primary_key=True)
    bio = db.Column(db.String())
    skin = db.Column(db.String())
    top = db.Column(db.String())
    hairColor = db.Column(db.String())
    eyes = db.Column(db.String())
    eyebrows = db.Column(db.String())
    mouth = db.Column(db.String())
    facialHair = db.Column(db.String())
    facialHairColor = db.Column(db.String())
    clothing = db.Column(db.String())
    clothingColor = db.Column(db.String())
    accessories = db.Column(db.String())
    accessoriesColor = db.Column(db.String())

    user = db.Relationship('User', back_populates='userinfo', lazy=True)


class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), db.ForeignKey('users.username'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    caption = db.Column(db.String())
    image = db.Column(db.String())
    timestamp = db.Column(db.Float())
    private = db.Column(db.Integer())

class Follow(db.Model):
    __tablename__ = 'follows'

    follower = db.Column(db.String(), db.ForeignKey('users.username'), primary_key=True)
    following = db.Column(db.String(), db.ForeignKey('users.username'), primary_key=True)
    timestamp = db.Column(db.Float())
