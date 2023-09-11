# To import config
import sys
sys.path.append('./')
sys.path.append('./..')
from utils.config import *

from flask import request
from flask_restful import Resource
import json

'''
    POST (CREATE) create a resourse. 
    GET (lettura) return a representation of a resourse. 
    PUT (UPDATE) update a resorse. 
    DELETE remove a resourse.
'''

class Server_planner(Resource):
    def __init__(self):
        self.req = request.args.get("req") # Mandatory
        self.json_path = request.args.get("json_path")

    def post(self):
        return {"message": "POST request failed", "error": True}

    def get(self):
        if self.req == GET_JSON:
            if self.json_path == None:
                return {"message": "Missing the json path", "error": True}
            with open(self.json_path, 'r') as file_json:
                data = json.load(file_json)
            return {"message": "JSON file returned", "error": False, "response": data}
        return {"message": "GET request failed", "error": True}

    def put(self):
        return {"message": "PUT request failed", "error": True}

    def delet(self):
        return {"message": "DELETE request failed", "error": True}




















# #Flask
# app = Flask(__name__)
# api = Api(app)
# api.add_resource(Server_planner, "/planner")
# api.add_resource(Server_chat, "/chat")

# if __name__ == '__main__':
#     print("Starting api...")
#     app.run(host="0.0.0.0", port="8080")


# server_planner = Flask("")

# # VANNO RIVISTE #
# @server_planner.route("/left")
# def left(self):
#     return "left"

# @server_planner.route("/right")
# def right():
#     return {"move":"right", "altro":3}
# # VANNO RIVISTE #

# @server_planner.route("/read_json")
# def read_json():
#     language = request.args.get('language')
#     print(path)
#     # with open(path, 'r') as json_file:
#     #     return json.load(json_file)


# Qui definisco le classi (o forse le importo e le definisco in ./RA)

# if __name__ == "__main__":
#     # Qui creo le varie classi che saranno leggibili da server
#     server_planner.run(host="0.0.0.0",port=8080)