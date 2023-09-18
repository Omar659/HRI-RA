# To import config
import sys
sys.path.append('./')
sys.path.append('./..')
from utils.config import *
from inputimeout import inputimeout

from flask import request
from flask_restful import Resource
import subprocess

'''
    POST (CREATE) create a resourse. 
    GET (lettura) return a representation of a resourse. 
    PUT (UPDATE) update a resorse. 
    DELETE remove a resourse.
'''

class Server_chat(Resource):
    def __init__(self):
        self.req = request.args.get("req") # Mandatory
        self.sentence = request.args.get("sentence") # sentence from pepper
        self.choices = request.args.get("choices") # choices for answer
        self.user_name = request.args.get("user_name") # choices for answer
        self.page = request.args.get("page") # html page

    def post(self):
        return {"message": "POST request failed", "error": True}

    def get(self):
        if self.req == GET_JSON:
            nome = input("scrivi qualcosa per prova: ")
            return {"message": "JSON file returned", "error": False, "response": nome}
        if self.req == GET_ANS:
            print("Pepper says: ", self.sentence)
            try:
                nome = inputimeout(self.user_name + " answer: ", timeout=TIMEOUT)
            except Exception:
                return {"message": str(Exception), "error": True}
            return {"message": "Answer returned", "error": False, "response": nome}
        if self.req == GET_MSG:
            print("Pepper says: ", self.sentence)
            return {"message": "Pepper message returned", "error": False}
        if self.req == GET_MULTI:
            print("Pepper says: ", self.sentence, self.choices.split(","))
            try:
                answer = inputimeout(self.user_name + " answer: ", timeout=9000)
            except Exception:
                return {"message": str(Exception), "error": True}
            return {"message": "Answer returned", "error": False, "response": answer}
        if self.req == GET_HTML:
            subprocess.check_output("firefox " + self.page, shell=True, universal_newlines=True)
            return {"message": "Pepper message returned", "error": False}
        
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        return {"message": "DELETE request failed", "error": True}