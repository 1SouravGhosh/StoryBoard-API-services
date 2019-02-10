import datetime
from optparse import Option
from os.path import getsize
from symbol import with_item
from tokenize import String
from typing import Text
from xml.etree.ElementTree import tostring

import psycopg2
from click import DateTime
from flask.globals import session
from flask_restful.fields import Boolean, DateTime, Integer
from psycopg2.extensions import Column
from sqlalchemy.orm import backref, defer, load_only, undefer
from sqlalchemy.sql.operators import like_op
from sqlalchemy.sql.schema import FetchedValue, ForeignKey
from storyboard_root.resources.database_resources.db_resource import db


class WriterModel(db.Model):
    __table_args__ = {"schema":"sch_storyboard"}
    __tablename__ = "tbl_writer" 

    writer_id = db.Column( db.Integer , primary_key = True )
    writer_display_id = db.Column( db.String )
    writer_first_name = db.Column( db.String )
    writer_last_name = db.Column( db.String )
    user_id = db.Column( db.Integer )
    stories = db.relationship("StoryModel" , backref="writer" )
    

    def __init__(self, i_writer_id, i_writer_display_id, i_writer_first_name, i_writer_last_name, in_user_id):
        self.writer_id = i_writer_id
        self.writer_display_id = i_writer_display_id
        self.writer_first_name = i_writer_first_name
        self.writer_last_name = i_writer_last_name
        self.user_id = in_user_id

    def json(self):
        return { 
            "userid" : self.user_id ,
            "writerid" : self.writer_id,
            "first_name"  : self.writer_first_name ,
            "last_name" : self.writer_last_name     
        }

    @classmethod
    def get_writer_by_id(self,in_writer_id):
        try:
            #print(in_writer_id)
            writer = self.query.filter(self.writer_id==in_writer_id).first()
            return writer
        except:
            print("exception occured")
    
    @classmethod
    def get_writer_by_userid(self,in_user_id):
        # try:
            print(in_user_id)
            writer = self.query.filter(self.user_id==in_user_id).first()
            return writer
        # except:
            # print("exception occured")


    # @classmethod
    # def get_writer_list(self,in_writer_id):
    #     try:
    #         #print(in_writer_id)
    #         writer = self.query.filter(self.writer_id==in_writer_id).first()
    #         return writer
    #     except:
    #         print("exception occured")
    
    


    