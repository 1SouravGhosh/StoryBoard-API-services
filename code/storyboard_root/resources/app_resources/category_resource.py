import datetime
from nt import replace
import psycopg2
from flask import Flask, request
from flask_restful import Resource, reqparse
from storyboard_root.models.category_model import CategoryModel
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.dialects.postgresql.dml import insert

parser = reqparse.RequestParser()
parser.add_argument("category_id", type = int, help = "Please pass a valid category id")
parser.add_argument("category_name", type = str, help = "Please pass a valid category name")
parser.add_argument("category_details", type = str, help = "Please pass a valid category detail")  
parser.add_argument("user_id", type = int, help = "Please pass a valid user id")  


class Category(Resource):

    def get(self):
        try:
            category = CategoryModel.get_categorydetails_by_id(request.headers["category_id"])
            if category is None:
                return { "message" : "Something went wrong! Please check the again" }
            else:
                return category.json()
        except:
            print("exception occured")

        

    def post(self):
        try:
            data = parser.parse_args() 
            print(data["category_name"] + data["category_details"])
            CategoryModel.create_category(data["category_name"] or None,data["category_details"] or None,data["user_id"] or None)  
            category = CategoryModel.get_categorydetails_by_name(data["category_name"])
            if category is None:
                return { "message" : "Something went wrong! Please check the again" }
            else:
                return category.json(),400 
        except:
            print("exception occured")


    def delete(self):
        try:
            category = CategoryModel.get_categorydetails_by_id(request.headers["category_id"])    
            if category is None:
                return {"message" : "record does not exist"}
            elif category is not None:
                CategoryModel.delete_category_by_id(request.headers["category_id"])
                category = CategoryModel.get_categorydetails_by_id(request.headers["category_id"])
                if category is None:
                    return {"message" : "record deleted successfully"}  
        except:
            print("exception occured")        
        


    def put(self):
        try:            
            data = parser.parse_args()
            category = CategoryModel.get_categorydetails_by_id(data["category_id"])   
            if category is None:
                return {"message" : "record does not exist"} 
            elif(data["category_id"] != 0 and data["category_name"] != ""):
                CategoryModel.update_category_details( data["category_id"],
                    data["category_name"] or None,data["category_details"] or None,data["user_id"] or None ) 
            else:
                return { "Message": "there is a problem in request" }

            category = CategoryModel.get_categorydetails_by_id(data["category_id"])
            if category is None:
                return { "message" : "Something went wrong! Please check the again" }
            else:
                return category.json()
        except:
            print("exception occured")


class Category_List(Resource):
    def get(self):
        try:
            categorylist = CategoryModel.get_category_list()
            categorylist_json = {}
            if categorylist:
                for category in categorylist:
                    categorylist_json.update( {category.json()["category_name"] : category.json()} )
            else:
                return {"Message": "Record does not exist"}
                
            return categorylist_json
        except:
            print("exception occured")