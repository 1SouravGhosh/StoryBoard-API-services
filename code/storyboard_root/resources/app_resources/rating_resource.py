import datetime
from nt import replace
import psycopg2
from flask import Flask, request
from flask_restful import Resource, reqparse
from storyboard_root.models.rating_model import RatingModel
from storyboard_root.models.story_model import StoryModel
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.dialects.postgresql.dml import insert

parser = reqparse.RequestParser()
parser.add_argument("story_id", type = int, help = "Please pass a story id")
parser.add_argument("writer_id", type = int, help = "Please pass a writer id")
parser.add_argument("user_id", type = int, help = "Please pass a writer id")  
parser.add_argument("rating", type = int, help = "Please pass a valid rating")  

class Rating(Resource):

    def get(self):
        try:
            rating = RatingModel.get_rating_by_story(request.headers["story_id"])
            if rating is None:
                return { "message" : "Something went wrong! Please check the again" }
            else:
                return rating.json()
        except:
            print("exception occured")

        

    # def post(self):     
    #     data = parser.parse_args() 
    #     RatingModel.create_rating(data["story_id"] or None,data["writer_id"] or None,data["rating"] or None) #creating rating 
    #     rating = RatingModel.get_rating_by_story(data["story_id"]) #checking above has been created or not
    #     if rating is None:
    #         ViewerRatingModel.delete_viewer_rating_mapping(data["story_id"],data["user_id"]) #deleting viewer rating mapping
    #         return { "message" : "Something went wrong! Please check the again" }
    #     else:
    #         return rating.json()  


    # def delete(self): #has to be ordered properly
    #     parser = reqparse.RequestParser()
    #     parser.add_argument("story_id", type = int, help = "Please pass a valid rating id") 
    #     parser.add_argument("user_id", type = int, help = "Please pass a valid rating id") 
    #     data = parser.parse_args() 
    #     rating = RatingModel.get_rating_by_story(data["story_id"])    
    #     if rating is None:
    #         return {"message" : "record does not exist"}
    #     elif rating is not None:
    #         if ViewerRatingModel.get_if_viewer_rating_present(data["story_id"],data["user_id"]):
    #             ViewerRatingModel.delete_viewer_rating_mapping(data["story_id"],data["user_id"])
    #             RatingModel.delete_rating_by_story(data["story_id"])
    #             rating = RatingModel.get_rating_by_story(data["story_id"])
    #             if rating is None:
    #                 return {"message" : "record deleted successfully"}
    #         else:
    #             return {"message" : "something went wrong. Please check again"}
  

        
        


    # def put(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument("story_id", type = int, help = "Please pass a story id")
    #     parser.add_argument("user_id", type = int, help = "Please pass a writer id")  
    #     parser.add_argument("rating", type = int, help = "Please pass a valid rating")  
    #     data = parser.parse_args() 
    #     if ViewerRatingModel.get_if_viewer_rating_present(data["story_id"],data["user_id"]):
    #         RatingModel.update_rating(data["story_id"] or None,data["rating"] or 0)  
    #         rating = RatingModel.get_rating_by_story(data["story_id"])
    #         if rating is None:
    #             return { "message" : "Something went wrong! Please check the again" }
    #         else:
    #             return rating.json() 
    #     else:
    #         return { "message" : "Something went wrong! Please check the again" }


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