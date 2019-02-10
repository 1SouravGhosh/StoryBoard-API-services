import datetime
from optparse import Option
from os.path import getsize, join
from symbol import with_item
from typing import Text
from xml.etree.ElementTree import tostring

import psycopg2
from click import DateTime
from flask.globals import session
from flask_restful.fields import Boolean, DateTime, Integer
from psycopg2.extensions import Column
from pylint.pyreverse.diagrams import Relationship
from pylint.utils import category_id
from sqlalchemy.orm import backref, defer, load_only, relationship, undefer
from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.sql.operators import like_op
from sqlalchemy.sql.schema import FetchedValue, ForeignKey

from storyboard_root.models.storytext_model import StoryTextModel
from storyboard_root.models.writer_model import WriterModel
from storyboard_root.resources.database_resources.db_resource import db


class StoryModel(db.Model):  

    __table_args__ = {"schema":"sch_storyboard"}
    __tablename__ = "tbl_story" 

    story_id = db.Column( db.Integer , primary_key = True )
    category_id = db.Column( db.Integer )
    story_name = db.Column( db.Text )
    story_description = db.Column( db.Text )
    story_text_id = db.Column( db.Integer , db.ForeignKey("sch_storyboard.tbl_storytext.story_text_id") )
    writer_id = db.Column( db.Integer , db.ForeignKey("sch_storyboard.tbl_writer.writer_id"))
    created_date = db.Column( db.DateTime )
    updated_date = db.Column( db.DateTime )
    created_by = db.Column( db.Integer )
    updated_by = db.Column( db.Integer )
    total_view = db.Column( db.Integer )
    average_rating = db.Column( db.Integer )



    def __init__(self,i_story_id, i_category_id, i_story_name, 
                    i_story_description, i_created_date, 
                    i_updated_date, i_created_by, i_updated_by,i_total_view,i_average_rating,i_obj_writer,i_obj_storytext):        
        self.story_id = i_story_id  
        self.category_id = i_category_id  
        self.story_name = i_story_name  
        self.story_description = i_story_description 
        self.created_date = i_created_date  
        self.updated_date = i_updated_date  
        self.created_by = i_created_by  
        self.updated_by = i_updated_by  
        self.total_view = i_total_view
        self.average_rating = i_average_rating
        self.writer = i_obj_writer
        self.storytext = i_obj_storytext
 

    def json(self):
        return { 
            "story_id"  :  self.story_id , 
            "category_id"  :  self.category_id , 
            "story_name"  :  self.story_name , 
            "story_details"  :  self.story_description , 
            "storytext_id"  :   self.story_text_id ,
            "writer_id"  :  self.writer.user_id , 
            "writer_name" : self.writer.writer_first_name+" "+self.writer.writer_last_name,
            "created_date" : self.created_date.strftime("%Y-%m-%d %H:%M:%S") if self.created_date is not None else None ,
            "updated_date" : self.updated_date.strftime("%Y-%m-%d %H:%M:%S") if self.updated_date is not None else None , 
            "created_by"  :  self.created_by , 
            "updated_by"  :  self.updated_by , 
            "view" :        self.total_view ,
            "rating" :  self.average_rating 
        }



    @classmethod
    def get_story_list_by_writer(self,in_writer_id):
        try:
            print(in_writer_id)
            writer = WriterModel.query.filter_by(writer_id=in_writer_id).first()
            return writer.stories
        except:
            print("exception occured model")

    @classmethod
    def get_story_by_id(self,in_story_id):
        try:
            story = self.query.filter_by(story_id=in_story_id).first()
            return story
        except:
            print("exception occured")

    @classmethod
    def get_story_by_name(self,in_story_name,in_category_id):
        try:
            story = self.query.filter_by(story_name=in_story_name).filter_by(category_id=in_category_id).first()
            return story
        except:
            print("exception occured")

    
    @classmethod
    def get_story_list_by_category(self,in_category_id):
        try:
            stories = self.query.filter(self.category_id==in_category_id).all()
            return stories
        except:
            print("exception occured model")

    @classmethod
    def get_story_list_by_trend(self):
        try:
            stories = self.query.all()
            return stories
        except:
            print("exception occured")

    @classmethod
    def get_writer_list(self):
        try:
            writers = WriterModel.query.all()
            return writers
        except:
            print("exception occured")
    

    @classmethod
    def get_if_user_is_writer(self,in_story_id,in_user_id):
        try:
            iswriter = self.query.filter_by(story_id = in_story_id).filter_by(writer_id = in_user_id).first()
            if iswriter:
                return True
            else:
                return False
        except:
            print("exception occured")

    @classmethod
    def get_writer_name(self,in_story_id):
        try:
            story = self.query.filter_by(story_id = in_story_id).first()
            return story.writer
        except:
            print("exception occured")


    @classmethod
    def create_story(self, in_category_id, in_story_name, 
                    in_story_description, in_story, in_writer_userid,in_created_by):  #need to inlude story text model
        try:
            obj_writer = WriterModel.get_writer_by_userid(in_writer_userid)
            obj_storytext = StoryTextModel.create_storytext(in_story)   
            new_story = self(i_story_id=None,i_category_id=in_category_id, i_story_name=in_story_name, 
                           i_story_description=in_story_description, i_created_date=datetime.datetime.now(), 
                           i_created_by=in_created_by,i_total_view=0,i_average_rating=0,
                           i_updated_date=None,i_updated_by=None,i_obj_writer=obj_writer,i_obj_storytext=obj_storytext)         
            db.session.add(new_story)
            db.session.commit()
        except:
           print("exception occured story model")
            
        

    
    @classmethod
    def update_story(self,in_story_id,in_category_id, in_story_name, 
                            in_story_description, in_storytext, in_writer_userid, in_updated_by): 
        try:
            existing_story = self.get_story_by_id(in_story_id) # reusing the "get_storydetails_by_id" function of this class
            
            if in_category_id is not None:
                existing_story.category_id = in_category_id        
            
            if in_story_description is not None:
                existing_story.story_description = in_story_description

            if in_story_name is not None:
                existing_story.story_name = in_story_name        

            if in_writer_userid is not None:
                obj_writer = WriterModel.get_writer_by_userid(in_writer_userid)
                if obj_writer:
                    existing_story.writer=obj_writer

            if in_storytext is not None:
               StoryTextModel.update_storytext(existing_story.story_text_id,in_storytext)

            if in_updated_by is not None:
                existing_story.updated_by = in_updated_by

            existing_story.updated_date = datetime.datetime.now()
            db.session.commit()
        except:
            print("exception occured")
            

    
    @classmethod
    def delete_story_by_id(self,in_story_id):
        try:
            story = self.get_story_by_id(in_story_id)
            self.query.filter_by(story_id=in_story_id).delete()
            StoryTextModel.delete_story_by_id(story.story_text_id)
        except:
            print("exception occured")
        finally:
            db.session.commit()
