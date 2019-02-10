import datetime
from nt import replace
import psycopg2
from flask import Flask, request
from flask_restful import Resource, reqparse
from storyboard_root.models.view_model import ViewModel
from storyboard_root.models.story_model import StoryModel
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.dialects.postgresql.dml import insert


class View(Resource):

    def get(self):
        try:
            view = ViewModel.get_view_by_story(request.headers["story_id"])
            if view is None:
                return { "message" : "Something went wrong! Please check the again" }
            else:
                return view.json()
        except:
            print("exception occured")

        

    def post(self):     
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("story_id", type = int, help = "Please pass a story id")
            parser.add_argument("writer_id", type = int, help = "Please pass a writer id")
            parser.add_argument("user_id", type = int, help = "Please pass a writer id")    
            data = parser.parse_args() 
            if StoryModel.get_if_user_is_writer(data["story_id"],data["user_id"]):
                return { "message" : "You are the writer! Sit back and Relax." }
            else:
                ViewModel.create_view(data["story_id"] or None,data["writer_id"] or None) #creating view 
                view = ViewModel.get_view_by_story(data["story_id"]) #checking above has been created or not
                if view is None:
                    return { "message" : "Something went wrong! Please check the again" }
                else:
                    return view.json()  
        except:
            print("exception occured")


    def delete(self): #has to be ordered properly
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("story_id", type = int, help = "Please pass a valid view id") 
            data = parser.parse_args() 
            view = ViewModel.get_view_by_story(data["story_id"])    
            if view is None:
                return {"message" : "record does not exist"}
            elif view is not None:
                    ViewModel.delete_view_by_story(data["story_id"])
                    view = ViewModel.get_view_by_story(data["story_id"])
                    if view is None:
                        return {"message" : "record deleted successfully"}
                    else:
                        return {"message" : "something went wrong. Please check again"} 
        except:
            print("exception occured")
        
        


    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("story_id", type = int, help = "Please pass a story id")
            parser.add_argument("user_id", type = int, help = "Please pass a writer id")    
            data = parser.parse_args() 
            if StoryModel.get_if_user_is_writer(data["story_id"],data["user_id"]) == False:    
                ViewModel.update_view(data["story_id"] or 0)  
            view = ViewModel.get_view_by_story(data["story_id"])
            if view is None:
                return { "message" : "Something went wrong! Please check the again" }
            else:
                return view.json() 
        except:
            print("exception occured")




# class view_List(Resource):
#     def get(self):
#         viewlist = ViewModel.get_view_list()
#         viewlist_json = {}
#         if viewlist:
#             for view in viewlist:
#                 viewlist_json.update( {view.json()["view_name"] : view.json()} )
#         else:
#             return {"Message": "Record does not exist"}
            
#         return viewlist_json