import datetime
from nt import replace
import psycopg2
from flask import Flask, request
from flask_restful import Resource, reqparse
from storyboard_root.models.viewer_rating_model import ViewerRatingModel
from storyboard_root.models.story_model import StoryModel
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.dialects.postgresql.dml import insert

parser = reqparse.RequestParser()
parser.add_argument("story_id", type = int, help = "Please pass a story id")
parser.add_argument("user_id", type = int, help = "Please pass a writer id")  
parser.add_argument("rating", type = float, help = "Please pass a valid rating")
parser.add_argument("mode", type = str, help = "Please pass a valid rating")


class ViewerRatingMapping(Resource):

    def get(self):
        try:
            rating = ViewerRatingModel.get_viewer_rating(request.headers["storyid"],request.headers["userid"])
            if rating is None:
                return { "message" : "Something went wrong! Please check the again" }
            else:
                return rating.json()
        except:
            print("exception occured")

        

    def post(self):      #db rollback to implemented 
        try:
            data = parser.parse_args() 
            if StoryModel.get_if_user_is_writer(data["story_id"],data["user_id"]):
                return { "message" : "You are the writer! Sit back and Relax." }
            else:
                ViewerRatingModel.upsert_viewer_rating_mapping(data["story_id"],data["user_id"],data["rating"])
                viewer_rating_mapping = ViewerRatingModel.get_viewer_rating(data["story_id"],data["user_id"])
                if viewer_rating_mapping is None:
                    return { "message" : "Something went wrong! Please check the again" }
                else:
                    return viewer_rating_mapping.json() 
        except:
            print("exception occured")
        


# class Rating_List(Resource):
#     def get(self):
#         ratinglist = RatingModel.get_rating_list()
#         ratinglist_json = {}
#         if ratinglist:
#             for rating in ratinglist:
#                 ratinglist_json.update( {rating.json()["rating_name"] : rating.json()} )
#         else:
#             return {"Message": "Record does not exist"}
            
#         return ratinglist_json

# def delete(self): #has to be ordered properly
#         parser = reqparse.RequestParser()
#         parser.add_argument("story_id", type = int, help = "Please pass a valid rating id") 
#         parser.add_argument("user_id", type = int, help = "Please pass a valid rating id") 
#         data = parser.parse_args() 
#         rating = RatingModel.get_rating_by_story(data["story_id"])    
#         if rating is None:
#             return {"message" : "record does not exist"}
#         elif rating is not None:
#             if ViewerRatingModel.get_if_viewer_rating_present(data["story_id"],data["user_id"]):
#                 ViewerRatingModel.delete_viewer_rating_mapping(data["story_id"],data["user_id"])
#                 RatingModel.delete_rating_by_story(data["story_id"])
#                 rating = RatingModel.get_rating_by_story(data["story_id"])
#                 if rating is None:
#                     return {"message" : "record deleted successfully"}
#             else:
#                 return {"message" : "something went wrong. Please check again"}
  