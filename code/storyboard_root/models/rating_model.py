import datetime
from datetime import datetime
from os.path import getsize
from xml.etree.ElementTree import tostring

import psycopg2
from click import DateTime
from flask_restful.fields import Boolean, DateTime, Integer
from psycopg2.extensions import Column
from sqlalchemy.sql.schema import Column, FetchedValue
from sqlalchemy.sql.sqltypes import Integer
from storyboard_root.resources.database_resources.db_resource import db


class RatingModel(db.Model):  

    __table_args__ = {"schema":"sch_storyboard"}
    __tablename__ = "tbl_rating" 

    rating_id = db.Column( db.Integer , primary_key = True )
    rating_number = db.Column( db.Integer )
    story_id = db.Column( db.Integer )
    writer_id = db.Column( db.Integer ) 
    rating = db.Column( db.Float )




        
    def __init__(self,i_rating_id,i_rating_number,i_story_id,i_writer_id,i_rating):
        self.rating_id = i_rating_id
        self.rating_number = i_rating_number 
        self.story_id = i_story_id
        self.writer_id = i_writer_id
        self.rating = i_rating
        

    def json(self):
        return { 
            "rating_id" : self.rating_id ,
            "rating_number"  : self.rating_number ,
            "story_id" : self.story_id ,
            "writer_id" : self.writer_id ,
            "rating" : self.rating
        }


    @classmethod
    def get_rating_by_story(self,in_story_id):
        try:
            rating = self.query.filter_by(story_id = in_story_id).first() # flask sqlalchemy requires self.column name to evaluate "!="" condition 
            return rating
        except:
            print("exception occured")

    @classmethod
    def get_rating_by_writer(self, in_writer_id):
        try:
            rating = self.query.filter_by(writer_id = in_writer_id).all()
            return rating  
        except:
            print("exception occured")

    @classmethod
    def get_rating_list_by_story(self): #need to be changed
        try:
            rating = self.query.all()
            return rating
        except:
            print("exception occured")


    @classmethod
    def create_rating(self,in_story_id,in_writer_id): #if the writer is the viewer then ignore,logic has been implemented in parent method. 
        try:
            new_rating = self(None,1,in_story_id,in_writer_id,0.001)    #calculating average by division. So putting 0 on numerator is avoided    
            db.session.add(new_rating)
        except:
            print("exception occured")
        finally:
            db.session.commit()

    
    @classmethod
    def update_rating(self,in_story_id,in_rating,in_user_rating=0): #if user is writer then don't increament the rating     
        try:
            new_rating = self.get_rating_by_story( in_story_id ) # reusing the "get_ratingdetails_by_id" function of this class
            new_rating.rating_number = new_rating.rating_number + 1
            new_rating.rating = ((new_rating.rating * (new_rating.rating_number - 1) - in_user_rating) + in_rating) / new_rating.rating_number
            print(new_rating.rating)
            print(new_rating.rating_number)
        except:
            print("exception occured")
        finally:
            db.session.commit() ##the db session is getting commited in the calling method in ViewerRatingModel
    

    

    @classmethod
    def delete_rating_by_story(self,in_story_id):
        try:
            self.query.filter_by(story_id = in_story_id).delete() # flask sqlalchemy requires self.column name to evaluate "!="" condition 
        except:
            print("exception occured")
        finally:
            db.session.commit()