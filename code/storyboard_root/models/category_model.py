import datetime
from os.path import getsize
from xml.etree.ElementTree import tostring
import psycopg2
from flask_restful.fields import Boolean, DateTime, Integer
from psycopg2.extensions import Column
from sqlalchemy.sql.schema import FetchedValue
from storyboard_root.resources.database_resources.db_resource import db
import json


class CategoryModel(db.Model):  

    __table_args__ = {"schema":"sch_storyboard"}
    __tablename__ = "tbl_category" 

    category_id = db.Column( db.Integer , primary_key = True )
    category_name = db.Column( db.String(100) )
    category_description = db.Column( db.String(100) )
    created_date = db.Column( db.DateTime )
    updated_date = db.Column( db.DateTime )
    created_by = db.Column( db.Integer )
    updated_by = db.Column( db.Integer )
        

    def __init__(self,i_category_id,i_category_name,i_category_description,i_created_date,i_updated_date,i_created_by,i_updated_by):
            self.category_id = i_category_id
            self.category_name = i_category_name 
            self.category_description = i_category_description
            self.created_date = i_created_date
            self.updated_date = i_updated_date
            self.created_by = i_created_by
            self.updated_by = i_updated_by
    
    def json(self):
        return { 
            'category_id' : self.category_id if self.category_id else None,
            'category_name'  : self.category_name if self.category_name else None,
            'category_description' : self.category_description if self.category_description else None,
            'created_date' : self.created_date.strftime("%Y-%m-%d %H:%M:%S") if self.created_date else None,
            'updated_date' : self.updated_date.strftime("%Y-%m-%d %H:%M:%S") if self.updated_date else None,
            'created_by' : self.created_by if self.created_by else None,
            'updated_by' : self.updated_by if self.updated_by else None,
            'selected' : False #this is used in front end. to reduce mobile app resource usage it is sent from api
        }
            


    @classmethod
    def get_categorydetails_by_name(self,in_category_name):
        try:
            category = self.query.filter_by(category_name = in_category_name).first()
            return category
        except:
            print("exception occured")

    @classmethod
    def get_categorydetails_by_id(self,in_category_id):
        try:
            category = self.query.filter_by(category_id=in_category_id).first()
            return category
        except:
            print("exception occured")
    
    @classmethod
    def get_category_list(self):
        try:
            categorylist = self.query.all()
            return categorylist
        except:
            print("exception occured")


    @classmethod
    def create_category(self,in_category_name,in_category_description,in_created_by):
        try:
            new_category = self(None,in_category_name,in_category_description,datetime.datetime.now(),None,in_created_by,None)        
            db.session.add(new_category)
        except:
            print("exception occured")
        finally:            
            db.session.commit()


    
    @classmethod
    def update_category_details(self,in_category_id,in_category_name,in_category_description,in_updated_by): 
        try:
            existing_category = self.get_categorydetails_by_id(in_category_id) # reusing the "get_categorydetails_by_id" function of this class

            if in_category_name is not None:
                existing_category.category_name = in_category_name        
            
            if in_category_description is not None:
                existing_category.category_description = in_category_description

            if in_updated_by is not None:
                existing_category.updated_by = in_updated_by

            existing_category.updated_date = datetime.datetime.now()
        except:
            print("exception occured")
        finally:
            db.session.commit()


    
    @classmethod
    def delete_category_by_id(self,in_category_id):
        try:
            self.query.filter_by(category_id=in_category_id).delete()
            db.session.commit()
        except:
            print("exception occured")
            

    

