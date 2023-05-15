from flask import request, jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import User, db, UserInfo
import time

defaultInfo = {
    'bio' : 'Hey there! I am using Sandigram.',
    'skin' : 'pale',
    'top' : 'shaggyMullet',
    'hairColor' : 'black',
    'eyes' : 'closed',
    'eyebrows' : 'defaultNatural',
    'mouth' : 'serious',
    'facialHair' : 'beardMedium',
    'facialHairColor' : 'black',
    'clothing' : 'shirtVNeck',
    'clothingColor' : 'pastelYellow',
    'accessories' : 'prescription01',
    'accessoriesColor' : 'gray02'
}

class Register(Resource):

    def post(self):

        username = request.json['username']
        password = request.json['password']
        email = request.json['email']

        if username is None:
            return abort(400, message='Username not provided.')

        if password is None:
            return abort(400, message='Password not provided.')

        user = db.session.query(User).get(username)

        if user:
            return abort(401, message=f'Username already exists! {user.username} , {user.password}')

        hashed_pw = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_pw,
            email=email,
            lastseen = time.time()
        )
        db.session.add(user)

        userinfo = UserInfo(
            username = username,
            bio = defaultInfo['bio'],
            skin = defaultInfo['skin'],
            top = defaultInfo['top'],
            hairColor = defaultInfo['hairColor'],
            eyes = defaultInfo['eyes'],
            eyebrows = defaultInfo['eyebrows'],
            mouth = defaultInfo['mouth'],
            facialHair = defaultInfo['facialHair'],
            facialHairColor = defaultInfo['facialHairColor'],
            clothing = defaultInfo['clothing'],
            clothingColor = defaultInfo['clothingColor'],
            accessories = defaultInfo['accessories'],
            accessoriesColor = defaultInfo['accessoriesColor'],
        )
        db.session.add(userinfo)

        db.session.commit()

        access_token = create_access_token(identity=username, expires_delta=False)
        refresh_token = create_refresh_token(identity=username)
        avatar = user.userinfo.__dict__
        del avatar['_sa_instance_state']
        del avatar['profile_id']
        del avatar['username']
        bio = avatar.pop('bio')

        response = jsonify({'message' : f'User <{username}> has been successfully registered.',
                            'access_token' : access_token,
                            'refresh_token' : refresh_token,
                            'username' : username,
                            'avatar' : avatar,
                            'bio' : bio
                            })
        response.status_code = 201

        return response

class Login(Resource):

    def post(self):

        username = request.json['username']
        password = request.json['password']

        if username is None:
            return abort(400, message='Username not provided.')

        if password is None:
            return abort(400, message='Password not provided.')

        user = db.session.query(User).get(username)

        if not user:
            return abort(401, message='Username provided does not exist.')

        if not check_password_hash(user.password, password):
            return abort(401, message='Wrong Password')

        user.lastseen = time.time()
        db.session.commit()

        access_token = create_access_token(identity=username, expires_delta=False)
        refresh_token = create_refresh_token(identity=username)
        avatar = user.userinfo.__dict__
        del avatar['_sa_instance_state']
        del avatar['profile_id']
        del avatar['username']
        bio = avatar.pop('bio')


        response = jsonify({'message' : f'User <{username}> has been logged in successfully!',
                            'access_token' : access_token, 
                            'refresh_token' : refresh_token, 
                            'username': username,
                            'avatar' : avatar,
                            'bio' : bio
                            })
        response.status_code = 201

        return response


class Refresh(Resource):

    @jwt_required(refresh=True)
    def get(self):
        username = get_jwt_identity()
        user = db.session.query(User).filter_by(username=username).first()
        access_token = create_access_token(identity=username)

        response = jsonify({'access_token' : access_token, 'refresh_token' : refresh_token})
        response.status_code = 201

        return response
