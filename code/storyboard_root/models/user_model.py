import datetime
from datetime import datetime
from os.path import getsize
from re import compile
from xml.etree.ElementTree import tostring

import psycopg2
from click import DateTime
from flask_restful.fields import Boolean, DateTime, Integer
from psycopg2.extensions import Column
from sqlalchemy.sql.schema import Column, FetchedValue

from storyboard_root.resources.database_resources.db_resource import db


class UserModel(db.Model):  

    __table_args__ = {"schema":"sch_storyboard"}
    __tablename__ = "tbl_user" 

    user_id = db.Column( db.Integer , primary_key = True )
    user_first_name = db.Column( db.String )
    user_last_name = db.Column( db.String )
    writer_alt_name = db.Column( db.String )
    user_phone_number_1 = db.Column( db.String )
    user_phone_number_2 = db.Column( db.String )
    email_id = db.Column( db.String )
    is_writer = db.Column( db.Boolean ) 
    password = db.Column( db.String )
    secret_question_1 = db.Column( db.String )
    secret_question_2 = db.Column( db.String )
    secret_question_3 = db.Column( db.String )



        
    def __init__(self, i_user_id, i_user_first_name, i_user_last_name, i_writer_alt_name,
                i_user_phone_number_1, i_user_phone_number_2, i_email_id, i_is_writer,i_password,
                i_secret_question_1,i_secret_question_2,i_secret_question_3):
        self.user_id = i_user_id
        self.user_first_name = i_user_first_name
        self.user_last_name = i_user_last_name
        self.writer_alt_name = i_writer_alt_name
        self.user_phone_number_1 = i_user_phone_number_1
        self.user_phone_number_2 = i_user_phone_number_2 
        self.email_id = i_email_id
        self.is_writer = i_is_writer
        self.password = i_password
        self.secret_question_1 = i_secret_question_1
        self.secret_question_2 = i_secret_question_2
        self.secret_question_3 = i_secret_question_3
        

    def json(self):
        return { 
            "userid" : self.user_id ,
            "first_name"  : self.user_first_name ,
            "last_name" : self.user_last_name ,
            "writer_altname" : self.writer_alt_name ,
            "user_phone_number" : self.user_phone_number_1 ,
            "user_altphone_number"  : self.user_phone_number_2 ,
            "emailid" : self.email_id ,
            "writer" : self.is_writer
        }


    @classmethod
    def authenticate_user(self,in_user_id = None, in_password = None): # or condition nto be added for mail id
        try:
            #print(in_password)
            user = self.query.filter_by(user_id = in_user_id).filter_by(password = in_password).first() # flask sqlalchemy requires self.column name to evaluate "!="" condition 
            
            return user
        except:
            print("exception occured")

    @classmethod
    def get_user_by_id(self,in_user_id):
        try:
            user = self.query.filter_by(user_id = in_user_id).first() # flask sqlalchemy requires self.column name to evaluate "!="" condition 
            return user
        except:
            print("exception occured")

    @classmethod
    def get_user_by_email_phone(self,in_user_phone_number = None): # or condition nto be added for mail id
        try:
            user = self.query.filter_by(user_phone_number_1 = in_user_phone_number).first() 
            return user
        except:
            print("exception occured")

    
    @classmethod
    def create_user(self,in_first_name,in_last_name,in_writer_alt_name,
                    in_user_phone_number_1,in_user_phone_number_2,in_email_id,in_is_writer,in_password,
                    i_secret_question_1,i_secret_question_2,i_secret_question_3): #if the writer is the userer then ignore,logic has been implemented in parent method. 
        try:
            new_user = self(None,in_first_name,in_last_name,in_writer_alt_name,in_user_phone_number_1,in_user_phone_number_2,
                            in_email_id,in_is_writer,in_password.strip(),i_secret_question_1,i_secret_question_2,i_secret_question_3)        
            db.session.add(new_user)
        except:
            print("exception occured")
        finally:
            db.session.commit()

    
    @classmethod
    def update_user(self,in_user_id,in_first_name,in_last_name,in_writer_alt_name,
                    in_user_phone_number_1,in_user_phone_number_2,in_email_id,in_is_writer,in_new_password,in_password,
                    i_secret_question_1,i_secret_question_2,i_secret_question_3): #if user is writer then don't increament the user
        try:
            update_user = self.get_user_by_id(in_user_id) # reusing the "get_user_by_story" function of this class 
    
            if update_user:   
                if in_first_name:    
                    update_user.user_first_name = in_first_name 
                if in_last_name:
                    update_user.user_last_name = in_last_name 
                if in_writer_alt_name:
                    update_user.writer_alt_name = in_writer_alt_name 
                if in_user_phone_number_1:
                    update_user.user_phone_number_1 = in_user_phone_number_1 
                if in_user_phone_number_2:
                    update_user.user_phone_number_2 = in_user_phone_number_2 
                if in_email_id:
                    update_user.email_id = in_email_id 
                if in_is_writer:
                    update_user.is_writer = in_is_writer 
                if (in_new_password and update_user.secret_question_1 == i_secret_question_1 and update_user.secret_question_2 == i_secret_question_2 and update_user.secret_question_3 == i_secret_question_3):
                    update_user.password = in_new_password.strip() 
                if in_new_password:
                    if (update_user.password.strip() == in_password.strip()):
                        update_user.password = in_new_password.strip()
        except:
            print("exception ocuured")
        finally:
            db.session.commit()


    @classmethod
    def delete_user_by_id(self,in_user_id):
        try:
            self.query.filter_by( user_id = in_user_id ).delete()
        except:
            print("exception occured")
        finally:
            db.session.commit()

    

    

