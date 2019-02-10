import datetime
from datetime import datetime
from os.path import getsize
from xml.etree.ElementTree import tostring
import psycopg2
from click import DateTime
from flask_restful.fields import Boolean, DateTime, Integer
from psycopg2.extensions import Column
from sqlalchemy.sql.schema import FetchedValue
from storyboard_root.resources.database_resources.db_resource import db


class ViewModel(db.Model):  

    __table_args__ = {"schema":"sch_storyboard"}
    __tablename__ = "tbl_view" 

    view_id = db.Column( db.Integer , primary_key = True )
    view_number = db.Column( db.Integer )
    story_id = db.Column( db.Integer )
    writer_id = db.Column( db.Integer ) 



        
    def __init__(self,i_view_id,i_view_number,i_story_id,i_writer_id):
        self.view_id = i_view_id
        self.view_number = i_view_number 
        self.story_id = i_story_id
        self.writer_id = i_writer_id
        

    def json(self):
        return { 
            "view_id" : self.view_id ,
            "view"  : self.view_number ,
            "story_id" : self.story_id ,
            "writer_id" : self.writer_id 
        }


    @classmethod
    def get_view_by_story(self,in_story_id):
        try:
            view = self.query.filter_by(story_id = in_story_id).first() # flask sqlalchemy requires self.column name to evaluate "!="" condition 
            return view
        except:
            print("exception occured")

    @classmethod
    def get_viewlist_by_writer(self, in_writer_id):
        try:
            view = self.query.filter_by(writer_id = in_writer_id).first()
            return view
        except:
            print("exception occured")
    

    @classmethod
    def get_view_list_by_story(self):
        try:
            view = self.query.all()
            return view
        except:
            print("exception occured")


    @classmethod
    def create_view(self,in_story_id,in_writer_id): #if the writer is the viewer then ignore,logic has been implemented in parent method. 
        try:
            new_view = self(None,1,in_story_id,in_writer_id)        
            db.session.add(new_view)
        except:
            print("exception occured")
        finally:
            db.session.commit()

    
    @classmethod
    def update_view(self,in_story_id): #if user is writer then don't increament the view
        try:
            view = self.get_view_by_story(in_story_id) # reusing the "get_view_by_story" function of this class     
            view.view_number = view.view_number + 1
        except:
            print("exception occured")
        finally:
            db.session.commit()

    @classmethod
    def delete_view_by_story(self,in_story_id):
        try:
            self.query.filter_by(story_id = in_story_id).delete()
        except:
            print("exception occured")
        finally:
            db.session.commit()

    

    

