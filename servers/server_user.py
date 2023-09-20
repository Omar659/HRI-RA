# To import config
import sys
sys.path.append('./')
sys.path.append('./..')
from utils.config import *
from inputimeout import inputimeout

from flask import request
from flask_restful import Resource
import json

'''
    POST (CREATE) create a resourse. 
    GET (lettura) return a representation of a resourse. 
    PUT (UPDATE) update a resorse. 
    DELETE remove a resourse.
'''

class Server_user(Resource):
    def __init__(self):
        self.req = request.args.get("req") # Mandatory
        self.name = " " #sentence from pepper
        self.survey = {}

    def post(self):
        self.name = request.args.get("name")
        self.survey = request.json
        if self.req == POST_SURVEY:
            with open("./data/registered_users.json", 'r') as f:
                data = json.load(f)
            for key, value in self.survey.items():
                data[self.name]["Survey"][key] = value
            with open("./data/registered_users.json", 'w') as f:
                json.dump(data, f, indent=4)
            return {"message": "User preferences modified", "error": False}
        return {"message": "POST request failed", "error": True}

    def get(self):        
        if self.req == GET_ANS:
            print("Pepper says: ", self.sentence)
            try:
                nome = inputimeout("Human answer: ", timeout=TIMEOUT)
            except Exception:
                return {"message": str(Exception), "error": True}
            return {"message": "Answer returned", "error": False, "response": nome}    
        if self.req == GET_USER:
            with open("./data/actual_user.json", 'r') as f:
                data = json.load(f)
            return {"message": "User returned", "error": False, "response": data}        
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        return {"message": "DELETE request failed", "error": True}