import datetime
from nt import replace

import psycopg2
from flask import Flask, request
from flask_restful import Resource, reqparse
from pylint.checkers.strings import get_args
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.dialects.postgresql.dml import insert
from storyboard_root.models.story_model import StoryModel
from storyboard_root.models.user_model import UserModel


parser = reqparse.RequestParser()
parser.add_argument("story_id", type = int, help = "Please pass a valid story name")
parser.add_argument("category_id", type = int, help = "Please pass a valid story name")
parser.add_argument("story_name", type = str, help = "Please pass a valid story name")  
parser.add_argument("story_details", type = str, help = "Please pass a valid story name")  
parser.add_argument("story", type = str, help = "Please pass a valid story name")
parser.add_argument("writer_userid", type = int, help = "Please pass a valid story name")  
parser.add_argument("userid", type = int, help = "Please pass a valid story name")


class Story(Resource):

    def get(self):
        try:
            story = StoryModel.get_story_by_id(request.args["story_id"])
            if story is None:
                return { "message" : "Story doesn't exist" }
            else:
                return story.json()
        except:
            print("exception occured")

        

    def post(self):   
        try:  
            data = parser.parse_args() 
            StoryModel.create_story(
                data["category_id"] or None, data["story_name"] or None, data["story_details"] or None,
                data["story"] or None, data["writer_userid"] or None,data["userid"] or None) 
            story = StoryModel.get_story_by_name(data["story_name"],data["category_id"])
            if story is None:
                return { "message" : "Something went wrong! Please check the again" }
            else:
                return story.json()
        except:
            print("exception occured")


    def put(self):   
        try:  
            data = parser.parse_args() 
            story = StoryModel.get_story_by_id(data["story_id"])
            if story is None:
                return { "message" : "story does not exist" }
            else:
                StoryModel.update_story(data["story_id"] or None,
                    data["category_id"] or None, data["story_name"] or None, data["story_details"] or None,
                    data["story"] or None, data["writer_userid"] or None,data["userid"] or None) 
                story = StoryModel.get_story_by_id(data["story_id"])
                if story is None:
                    return { "message" : "Something went wrong! Please check the again" }
                else:
                    return story.json()
        except:
            print("exception occured in resource module")



    def delete(self):
        try:
            data = parser.parse_args() 
            story = StoryModel.get_story_by_id(data["story_id"])    
            if story is None:
                return {"message" : "record does not exist"}
            elif story is not None:
                StoryModel.delete_story_by_id(data["story_id"])
                story = StoryModel.get_story_by_id(data["story_id"])
                if story is None:
                    return {"message" : "record deleted successfully"}  
        except:
            print("exception occured")

        
        


class Story_List(Resource):

    def get(self):
        try:
            storylist_json={}
            #print(request.args["category_id"])
            print(request.args["writer_id"])
            print(request.args["category_id"])
            if request.args["writer_id"]=="0" and request.args["category_id"]=="0":
                stories = StoryModel.get_story_list_by_trend()
            elif request.args["writer_id"] == "0": # if value 0 then don't return by the respective id 
                stories = StoryModel.get_story_list_by_category(request.args["category_id"])
            else:
                stories = StoryModel.get_story_list_by_writer(request.args["writer_id"])

            if stories is None:
                return { "message" : "Story doesn't exist" }
            else:
                for story in stories:
                    storylist_json.update(
                        {story.story_id : { "story_name":story.story_name, "story_details":story.story_description, 
                                            "writer_id":story.writer.user_id if story.writer else "error", 
                                            "view":story.total_view, "rating":story.average_rating, 
                                            "writer_name": ( story.writer.writer_first_name if story.writer else "error" ) + " " + ( story.writer.writer_last_name if story.writer else "error" ) }})
                return storylist_json
        except:
            print("exception occured resource")
    

    

class Writer_List(Resource): #need to be modified

    def get(self):
        # try:
            writerlist_json={}
            writers = StoryModel.get_writer_list()
            if writers is None:
                return { "message" : "data doesn't exist" }
            else:
                for writer in writers:
                    if(writer.user_id is not None and writer.writer_first_name is not None or writer.writer_last_name is not None):
                        writerlist_json.update({writer.writer_id : { "writer_name": writer.writer_first_name+" "+writer.writer_last_name }})
                
                return writerlist_json
        # except:
            # print("exception occured")