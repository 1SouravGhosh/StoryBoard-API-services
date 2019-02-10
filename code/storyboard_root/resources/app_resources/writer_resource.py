import datetime
from nt import replace
from xml.etree.ElementTree import tostring
import psycopg2
from flask import Flask, json, request
from flask_restful import Resource, reqparse
from sqlalchemy.dialects.postgresql import json
from sqlalchemy.dialects.postgresql.dml import insert
from storyboard_root.models.writer_model import WriterModel


parser = reqparse.RequestParser()
parser.add_argument("writer_userid", type = int, help ="Please pass a valid writer name")
parser.add_argument("first_name", type = str, help ="Please pass a valid writer name")  
parser.add_argument("last_name", type = str, help ="Please pass a valid writer name")  
parser.add_argument("writerid", type = str, help ="Please pass a valid writer name")



class Writer(Resource):

    def get(self):
        try:
            if(request.args["request_code"]=="1"):
                print(request.args["writer_userid"])
                writer = WriterModel.get_writer_by_userid(request.args["writer_userid"])
                if writer:
                    return writer.json()
                else:
                    return {"message" : "writer doesn't exist"}
            else:
                pass #to be implemeted writer list
        except:
            print("exception occured")    

    
        


    