from flask import Flask
from flask_restful import Api
from storyboard_root.resources.app_resources.category_resource import Category,Category_List
from storyboard_root.resources.app_resources.story_resource import Story ,Story_List, Writer_List
from storyboard_root.resources.app_resources.rating_resource import Rating
from storyboard_root.resources.app_resources.viewer_rating_resources import ViewerRatingMapping
from storyboard_root.resources.app_resources.view_resource import View
from storyboard_root.resources.app_resources.user_resource import User
from storyboard_root.resources.app_resources.writer_resource import Writer
from storyboard_root.resources.database_resources.db_resource import db,DB_URL


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

#app.config['SQLALCHEMY_ECHO'] = True


api.add_resource(Category,'/category')
api.add_resource(Category_List,'/categorylist')
api.add_resource(Story,'/story')
api.add_resource(Story_List,'/storylist')
api.add_resource(Writer_List,'/writerlist')
api.add_resource(Rating,'/rating')
api.add_resource(ViewerRatingMapping,'/viewerrating')
api.add_resource(View,'/view')
api.add_resource(User,'/user')
api.add_resource(Writer,'/writer')



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000)