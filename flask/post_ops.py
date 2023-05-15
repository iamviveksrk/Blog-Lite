from flask import request, jsonify
from flask_restful import Resource, abort
from models import User, Post, db, Follow
from flask_jwt_extended import jwt_required, get_jwt_identity
import time
import os
from cache import cache, cache_key, ClearCache


class PostOps(Resource, ClearCache):

    @jwt_required(optional=True)
    @cache.cached(timeout=300, key_prefix=cache_key)
    def get(self):

        post_id = request.args.get('post_id')
        post_record = db.session.query(Post).get(post_id)

        username = get_jwt_identity()

        if post_record:
            if not post_record.private or username == post_record.username:
                response = jsonify({'post_id':post_record.post_id,
                                    'username':post_record.username,
                                    'title':post_record.title,
                                    'caption':post_record.caption,
                                    'image':post_record.image,
                                    'timestamp':post_record.timestamp,
                                    'private':post_record.private})
                response.status_code = 201

                return response
        print(username, post_record.username)
        return abort(400, message="Nonetype")

    @jwt_required()
    def post(self):
        username = get_jwt_identity()
        title = request.form['title']
        caption = request.form['caption']
        timestamp = time.time()
        private = request.form['private']
        
        generated_post = Post(username=username, title=title, caption=caption, timestamp=timestamp, private=private)
        db.session.add(generated_post)
        db.session.commit()

        generated_post.image = os.getcwd().replace('flask', 'vue\\public\\posts\\') + f'{generated_post.post_id}.png'
        db.session.commit()
        
        image = request.files['image']
        image.save(generated_post.image)

        print('added post!')

        response = jsonify({'message' : f'Post created successfully! id: {generated_post.post_id}'})
        response.status_code = 201

        return response

    @jwt_required()
    def put(self):
        username = get_jwt_identity()
        post_id = request.form['post_id']

        post_record = db.session.query(Post).get(post_id)
        if post_record.username != username:
            return abort(400, 'Unauthorized. Post id out of scope for logged in account.')

        post_record.title = request.form['title']
        post_record.caption = request.form['caption']
        post_record.timestamp = time.time()
        post_record.private = request.form['private']
        db.session.commit()

        self.clear_cache_post(post_id)

        response = jsonify({'message' : f'Post updated successfully! id: {post_record.post_id}'})
        response.status_code = 201

        return response
    
    @jwt_required()
    def delete(self):
        username = get_jwt_identity()

        post_id = request.args.get('post_id')
        post_record = db.session.query(Post).get(post_id)
        if post_record.username != username:
            return abort(400, 'Unauthorized. Post id out of scope for logged in account.')
        
        try:
            os.remove(f'C:/Users/iamvi/github/Blog-Lite/vue/public/posts/{post_id}.png')
        except:
            print('No image found!')
        db.session.delete(post_record)
        db.session.commit()

        self.clear_cache_post(post_id)

        return jsonify({'message' : f'Post {post_id} deleted successfully!'})


class Feed(Resource):

    @jwt_required()
    @cache.cached(timeout=30)
    def get(self):
        username = get_jwt_identity()
        posts_with_timestamps = []

        for i in db.session.query(Follow).filter_by(follower=username):
            following = i.following
            for j in db.session.query(User).get(following).posts:
                if not j.private:
                    posts_with_timestamps.append((j.post_id, j.timestamp))
        
        posts_with_timestamps.sort(key=lambda i: i[1], reverse=True)
        post_ids = [i[0] for i in posts_with_timestamps]
        print([i[1] for i in posts_with_timestamps])

        return jsonify({'post_ids' : post_ids})

