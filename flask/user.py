from flask import request, jsonify
from flask_restful import Resource, abort
from models import User, Follow, Post, db, UserInfo
from flask_jwt_extended import jwt_required, get_jwt_identity
from tasks import user_export
import time


class FollowUser(Resource):

    @jwt_required()
    def post(self):
        
        follower = get_jwt_identity()
        following = request.json['username']
        timestamp = time.time()
        print(follower, following)

        if following is None:
            return abort(400, message='Username cannot be empty.')

        if follower == following:
            return abort(400, message="Cannot follow yourself.")

        follow = db.session.query(Follow).get((follower, following))

        if follow:
            return abort(401, message=f'Such a follow already exists')

        follow = Follow(follower=follower, following=following, timestamp=timestamp)
        db.session.add(follow)
        db.session.commit()

        response = jsonify({'message' : f'Success. {follower} is now following {following}'})
        response.status_code = 201

        return response

class UnfollowUser(Resource):

    @jwt_required()
    def post(self):

        follower = get_jwt_identity()
        following = request.json['username']

        if following is None:
            return abort(400, message='Username cannot be empty.')

        if follower == following:
            return abort(400, message="Cannot unfollow yourself.")

        follow = db.session.query(Follow).get((follower, following))

        if not follow:
            return abort(401, message=f'Such a follow does not exist')

        db.session.delete(follow)
        db.session.commit()

        response = jsonify({'message' : f'Success. {follower} has unfollowed {following}'})
        response.status_code = 201

        return response

class Following(Resource):

    def get(self, username, user_list=None):

        query = db.session.query(Follow).filter_by(follower=username)

        if user_list is None:
            following_count = query.count()
            return jsonify({'following_count' : following_count})

        followings = []
        for i in query:
            following = i.following
            user_obj = db.session.query(User).get(following)
            avatar = user_obj.userinfo.__dict__.copy()
            del avatar['_sa_instance_state']
            del avatar['profile_id']
            del avatar['username']
            bio = avatar.pop('bio')

            followings.append({'username':following, 'bio':bio, 'avatar':avatar})

        response = jsonify({'following' : followings})
        response.status_code = 201

        return response

class Followers(Resource):

    def get(self, username, user_list=None):

        query = db.session.query(Follow).filter_by(following=username)

        if user_list is None:
            follower_count = query.count()
            return jsonify({'follower_count' : follower_count})

        followers = []

        for i in query:
            follower = i.follower
            user_obj = db.session.query(User).get(follower)
            avatar = user_obj.userinfo.__dict__.copy()
            del avatar['_sa_instance_state']
            del avatar['profile_id']
            del avatar['username']
            bio = avatar.pop('bio')

            followers.append({'username':follower, 'bio':bio, 'avatar':avatar})

        response = jsonify({'followers' : followers})
        response.status_code = 201

        return response

class ProfileInfo(Resource):

    @jwt_required(optional=True)
    def get(self, username):

        user = db.session.query(User).get(username)
        token_username = get_jwt_identity()

        if not user:
            return abort(400, message='Username does not exist.')

        if username == token_username:
            post_ids = [i.post_id for i in user.posts]
        else:
            post_ids = [i.post_id for i in user.posts if not i.private]
            print(username, token_username)
        avatar = user.userinfo.__dict__
        del avatar['_sa_instance_state']
        del avatar['profile_id']
        del avatar['username']
        bio = avatar.pop('bio')
        response = jsonify({'post_ids' : post_ids, 'bio' : bio, 'avatar' : avatar})
        response.status_code = 201

        return response

    
    def put(self, username):

        data = request.json
        userinfo = db.session.query(User).get(username).userinfo

        userinfo.bio = data['bio']
        userinfo.skin = data['avatar']['skin']
        userinfo.top = data['avatar']['top']
        userinfo.hairColor = data['avatar']['hairColor']
        userinfo.eyes = data['avatar']['eyes']
        userinfo.eyebrow = data['avatar']['eyebrows']
        userinfo.mouth = data['avatar']['mouth']
        userinfo.facialHair = data['avatar']['facialHair']
        userinfo.facialHairColor = data['avatar']['facialHairColor']
        userinfo.clothing = data['avatar']['clothing']
        userinfo.clothingColor = data['avatar']['clothingColor']
        userinfo.accessories = data['avatar']['accessories']
        userinfo.accessoriesColor = data['avatar']['accessoriesColor']
        
        db.session.commit()
        return jsonify({'message':'Edited successfully!'})


class SearchUser(Resource):

    def get(self, query):

        users = db.session.query(User).filter(User.username.like(query + '%')).all()
        user_list = []
        for user in users:
            if len(user_list) > 3:
                break
            avatar = user.userinfo.__dict__
            del avatar['_sa_instance_state']
            del avatar['profile_id']
            del avatar['username']
            bio = avatar.pop('bio')
            user_list.append({'username' : user.username, 'bio' : bio, 'avatar' : avatar})
        
        response = jsonify({'users':user_list})
        response.status_code = 201

        return response

class UserExport(Resource):

    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        job = user_export.delay(username)

        return jsonify({'message':'Task called successfully!', 'job_id':str(job)})