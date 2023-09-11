# To import config
import sys
sys.path.append('./')
sys.path.append('./..')
from utils.config import *

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

    def post(self):
        return {"message": "POST request failed", "error": True}

    def get(self):
        if self.req == GET_JSON:
            nome = input("scrivi qualcosa per prova: ")
            return {"message": "JSON file returned", "error": False, "response": nome}
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delet(self):
        return {"message": "DELETE request failed", "error": True}