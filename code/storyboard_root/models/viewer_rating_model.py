import datetime
from datetime import datetime
from os.path import getsize
from xml.etree.ElementTree import tostring

import psycopg2
from click import DateTime
from flask_restful.fields import Boolean, DateTime, Integer
from psycopg2.extensions import Column
from sqlalchemy.sql.schema import Column, FetchedValue
from sqlalchemy.types import Integer
from storyboard_root.resources.database_resources.db_resource import db
from storyboard_root.models.rating_model import RatingModel


class ViewerRatingModel(db.Model):  

    __table_args__ = {"schema":"sch_storyboard"}
    __tablename__ = "tbl_viewer_rating" 

    viewer_id = db.Column( db.Integer )
    story_id = db.Column( db.Integer )
    latest_rating = db.Column( db.Float )
    viewer_rating_mapping_id = db.Column( db.Integer, primary_key = True )

        
    def __init__(self,i_viewer_id,i_story_id,i_latest_rating):
        self.viewer_id = i_viewer_id
        self.story_id = i_story_id
        self.latest_rating = i_latest_rating
        

    def json(self):
        return { "rating" : self.latest_rating }

    @classmethod
    def get_viewer_rating(self,in_story_id,in_user_id):
        try:
            viewer_rating = self.query.filter_by(story_id = in_story_id).filter_by( viewer_id = in_user_id ).first() # flask sqlalchemy requires self.column name to evaluate "!="" condition 
            return viewer_rating
        except:
            print("exception occured")

    @classmethod
    def upsert_viewer_rating_mapping(self,in_story_id,in_viewer_id,in_rating): #if the writer is the viewer then ignore,logic has been implemented in parent method. 
        try:
            viewer_rating = self.get_viewer_rating(in_story_id,in_viewer_id)
            if viewer_rating is None:
                new_viewer_rating_map = self(in_viewer_id,in_story_id,0)       
                db.session.add(new_viewer_rating_map)
                db.session.commit()
            else:
                if (in_rating != 0 ) :
                    previous_latest_rating = viewer_rating.latest_rating
                    viewer_rating.latest_rating = in_rating
                    db.session.commit()
                    RatingModel.update_rating(in_story_id,in_rating,previous_latest_rating)
        except:
            print("exception occured")
    

    @classmethod
    def delete_viewer_rating_mapping(self,in_story_id,in_viewer_id): #if the writer is the viewer then ignore,logic has been implemented in parent method. 
        try:
            self.query.filter_by(story_id = in_story_id).filter_by( viewer_id = in_viewer_id ).delete()
        except:
            print("exception occured")
        finally:
            db.session.commit()

    # @classmethod
    # def get_view_by_story(self,in_story_id):
    #     view = self.query.filter_by(story_id = in_story_id).first() # flask sqlalchemy requires self.column name to evaluate "!="" condition 
    #     return view

    # @classmethod
    # def get_view_by_writer(self, in_writer_id):
    #     view = self.query.filter_by(writer_id = in_writer_id).first()
    #     return view
    
    # @classmethod
    # def get_view_list_by_writer(self):
    #     view = self.query.all()
    #     return view

    # @classmethod
    # def get_view_list_by_story(self):
    #     view = self.query.all()
    #     return view


    

    

