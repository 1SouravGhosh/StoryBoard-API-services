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
from sqlalchemy.orm import backref, defer, load_only, relationship, undefer
from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.sql.operators import like_op
from sqlalchemy.sql.schema import FetchedValue, ForeignKey
from storyboard_root.resources.database_resources.db_resource import db


class StoryTextModel(db.Model):  

    __table_args__ = {"schema":"sch_storyboard"}
    __tablename__ = "tbl_storytext" 

    story_text_id = db.Column( db.Integer , primary_key = True )
    story_text = db.Column( db.Text )
    story_table = db.relationship( "StoryModel" , backref='storytext')



    def __init__(self,i_story_text_id, i_story_text):        
        self.story_text_id = i_story_text_id  
        self.story_text = i_story_text  
 

    def json(self):
        return { 
            "storytextid"  :  self.story_text_id , 
            "storytext"  :  self.story_text 
        }


    @classmethod
    def get_storytext_by_id(self,in_storytext_id):
        try:
            storytext = self.query.filter_by(story_text_id=in_storytext_id).first()
            return storytext
        except:
            print("exception occured storytext model")
    
    

    @classmethod
    def create_storytext(self, in_storytext):  #need to inlude story text model
        try:
            new_storytext = self(i_story_text_id=None,i_story_text=in_storytext)         
            db.session.add(new_storytext)
            db.session.commit()
            storytext = self.query.order_by(self.story_text_id.desc()).first()
            return storytext
        except:
           print("exception occured")
        

    
    @classmethod
    def update_storytext(self, in_storytext_id, in_storytext): 
        try:
            existing_storytext = self.get_storytext_by_id(in_storytext_id) # reusing the "get_storydetails_by_id" function of this class

            if in_storytext is not None:
                existing_storytext.story_text = in_storytext        
        except:
            print("exception occured")
        finally:
            db.session.commit()

    
    @classmethod
    def delete_story_by_id(self,in_storytext_id):
        try:
            self.query.filter_by(story_text_id=in_storytext_id).delete()
        except:
            print("exception occured")
        finally:
            db.session.commit()
