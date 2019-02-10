import datetime
from nt import replace
from xml.etree.ElementTree import tostring

import psycopg2
from flask import Flask, json, request
from flask_restful import Resource, reqparse
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.dialects.postgresql.dml import insert
from storyboard_root.models.user_model import UserModel


parser = reqparse.RequestParser()
parser.add_argument("userid", type = int, help ="Please pass a valid user name")
parser.add_argument("first_name", type = str, help ="Please pass a valid user name")  
parser.add_argument("last_name", type = str, help ="Please pass a valid user name")  
parser.add_argument("writer_alt_name", type = str, help ="Please pass a valid user name")
parser.add_argument("user_phone_number", type = str, help ="Please pass a valid user name")  
parser.add_argument("user_alternate_phone_number", type = str, help ="Please pass a valid user name")
parser.add_argument("email", type = str, help ="Please pass a valid user name")
parser.add_argument("writer", type = bool, help ="Please pass a valid user name")
parser.add_argument("new_password", type = str, help ="Please pass a valid user name")
parser.add_argument("password", type = str, help ="Please pass a valid user name")
parser.add_argument("sq1_answer", type = str, help ="Please pass a valid user name")
parser.add_argument("sq2_answer", type = str, help ="Please pass a valid user name")
parser.add_argument("sq3_answer", type = str, help ="Please pass a valid user name")



class User(Resource):

    def get(self):
        try:
            if request.args["requestcode"] == "0" : #log in
                user = UserModel.get_user_by_email_phone(request.args["phone"]) 
                if user:
                    user = UserModel.authenticate_user(user.json()["userid"],request.args["password"])
                    if user is None:
                        return {"message" :"password wrong" }
                    else:
                        return user.json()
                else:
                    return {"message" :"user doesn't exist" }

            elif request.args["requestcode"] == "1" : #get user details by id
                user = UserModel.get_user_by_id(request.args["userid"])
                if user is None:
                    return {"message" :"user doesn't exist" }
                else:
                    return user.json()
        except:
            print("exception occured")


        

    def post(self):   
        try:  
            data = parser.parse_args() 
            user = UserModel.get_user_by_email_phone(data["user_phone_number"])
            if user:
                return {"message" :"User already exists." }
            else:
                UserModel.create_user(
                    data["first_name"],data["last_name"],data["writer_alt_name"],data["user_phone_number"],
                    data["user_alternate_phone_number"],data["email"],data["writer"],data["password"],
                    data["sq1_answer"],data["sq2_answer"],data["sq3_answer"]
                )  
                user = UserModel.get_user_by_email_phone(data["user_phone_number"])
                if user is None:
                    return {"message" :"Something wet wrong! Please check again." }
                else:
                    return user.json()
        except:
            print("exception occured")
        
    
    def put(self): 
        try:
            data = parser.parse_args() 
            user = UserModel.get_user_by_id(data["userid"])
            if user.password.strip() != data["password"].strip():
                return {"message" : "password wrong"}
            if user is None:
                return {"message" :"User does not exist." }           
            else: 
                UserModel.update_user( data["userid"],
                    data["first_name"],data["last_name"],data["writer_alt_name"],data["user_phone_number"],
                    data["user_alternate_phone_number"],data["email"],data["writer"],data["new_password"],data["password"],
                    data["sq1_answer"],data["sq2_answer"],data["sq3_answer"]) 
            user = UserModel.get_user_by_id(data["userid"])
            return user.json() 
        except:
            print("exception occured")




    def delete(self):
        try:
            data = parser.parse_args() 
            user = UserModel.get_user_by_id(data["userid"])   
            if user is None:
                return {"message" :"record does not exist"} 
            elif user is not None:
                UserModel.delete_user_by_id(data["userid"]) 
                user = UserModel.get_user_by_id(data["userid"]) 
                if user is None:
                    return {"message" :"user deleted successfully"}  
        except:
            print("exception occured")

        
        


    