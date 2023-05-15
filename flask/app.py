from flask import Flask
from flask_restful import Api
from mail import mail
from models import db
from auth import Register, Login, Refresh
from user import FollowUser, UnfollowUser, Following, Followers, ProfileInfo, SearchUser, UserExport
from post_ops import PostOps, Feed
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from workers import celery_app
from cache import cache


class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

app, api, celery = None, None, None

def create_app():

    app = Flask(__name__)
    app.config.from_object('config')
    
    api = Api(app)
    mail.init_app(app)
    jwt = JWTManager(app)
    app.app_context().push()

    CORS(app, resources={r'/*': {'origins': '*'}})
    cache.init_app(app)
    db.init_app(app)
    app.app_context().push()

    celery_app.conf.update(
        broker_url = app.config['CELERY_BROKER_URL'],
        result_backend = app.config['CELERY_RESULT_BACKEND'],
        timezone = app.config['CELERY_TIMEZONE']
    )
    celery_app.Task = ContextTask
    app.app_context().push()

    return app, api, celery

app, api, celery = create_app()

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Refresh, '/refresh')

api.add_resource(FollowUser, '/follow')
api.add_resource(UnfollowUser, '/unfollow')

api.add_resource(Following, '/<username>/following', '/<username>/following/<user_list>')
api.add_resource(Followers, '/<username>/followers', '/<username>/followers/<user_list>')

api.add_resource(ProfileInfo, '/<username>/info')
api.add_resource(SearchUser, '/search/<query>')

api.add_resource(PostOps, '/post')
api.add_resource(Feed, '/feed')

api.add_resource(UserExport, '/user/export')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
