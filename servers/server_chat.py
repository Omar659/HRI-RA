# To import config
import sys
sys.path.append('./')
sys.path.append('./..')
from utils.config import *
from inputimeout import inputimeout

from flask import request
from flask_restful import Resource

'''
    POST (CREATE) create a resourse. 
    GET (lettura) return a representation of a resourse. 
    PUT (UPDATE) update a resorse. 
    DELETE remove a resourse.
'''

class Server_chat(Resource):
    def __init__(self):
        self.req = request.args.get("req") # Mandatory
        self.sentence = request.args.get("sentence") #sentence from pepper

    def post(self):
        return {"message": "POST request failed", "error": True}

    def get(self):
        if self.req == GET_JSON:
            nome = input("scrivi qualcosa per prova: ")
            return {"message": "JSON file returned", "error": False, "response": nome}
        if self.req == GET_ANS:
            print("Pepper says: ", self.sentence)
            try:
                nome = inputimeout("Human answer: ", timeout=TIMEOUT)
            except Exception:
                return {"message": str(Exception), "error": True}
            return {"message": "Answer returned", "error": False, "response": nome}
        if self.req == GET_MSG:
            print("Pepper says: ", self.sentence)
            return {"message": "Pepper message returned", "error": False}
        
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        return {"message": "DELETE request failed", "error": True}