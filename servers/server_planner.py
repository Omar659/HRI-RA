# To import config
import sys
sys.path.append('./')
sys.path.append('./..')
from utils.config import *
from RA.planner import *

from flask import request
from flask_restful import Resource
import json
import os
import random

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
        if self.req == POST_GAME_STATUS:
            difficult = request.json["difficult"]
            image_names_root = "./HRI/tablet/HTML/images/tiles/"
            image_names = os.listdir(image_names_root)
            image_name = random.choice(image_names)
            if difficult.lower() not in ["easy", "medium", "hard"]:
                {"message": "Difficult not present", "error": True}

            with open("./data/actual_user.json", 'r') as file_json:
                user = json.load(file_json)["user"]
            with open("./data/registered_users.json", 'r') as file_json:
                user_info = json.load(file_json)
            record_moves = user_info[user]["Games"][difficult]["record_moves"]
            record_time = user_info[user]["Games"][difficult]["record_time"]
            slide_tile_pddl = Slide_tile_PDDL(difficult=difficult, optimal_plan=True, verbose=False)
            tiles = slide_tile_pddl.slide_tile.return_tiles()
            plan = []
            for action in slide_tile_pddl.plan.actions:
                plan.append(str(action).split("(")[0].split(" ")[1])
            data = {
                "image_name": "./../images/tiles/" + image_name,
                "difficult": difficult,
                "tiles": tiles,
                "bx": slide_tile_pddl.slide_tile.b_x,
                "by": slide_tile_pddl.slide_tile.b_y,
                "user_turn": True,
                "plan": plan,
                "user_moves": [],
                "record_moves": record_moves,
                "record_time": record_time

            }
            with open("./data/game_status.json", 'w') as f:
                json.dump(data, f)
            return {"message": "POST request succeed", "error": False}
        return {"message": "POST request failed", "error": True}

    def get(self):
        if self.req == GET_JSON:
            if self.json_path == None:
                return {"message": "Missing the json path", "error": True}
            with open(self.json_path, 'r') as file_json:
                data = json.load(file_json)
            return {"message": "JSON file returned", "error": False, "response": data}

        if self.req == GET_ROBOT_MOVES:
            with open("./data/game_status.json", 'r') as file_json:
                data = json.load(file_json)
            difficult = data["difficult"]
            slide_tile_pddl = Slide_tile_PDDL(difficult=difficult, optimal_plan=True, verbose=False)
            slide_tile_pddl.slide_tile.generate_tiles_from_mat(data["tiles"], data["bx"], data["by"])
            slide_tile_pddl.create_problem()
            slide_tile_pddl.solve_problem()
            new_actions = [str(action).split("(")[0].split(" ")[1] for action in slide_tile_pddl.plan.actions]
            old_actions = data["plan"]
            user_moves = data["user_moves"]
            new_plan = new_actions
            if old_actions[:USER_MOVES] == user_moves:
                print("mosse migliori") # possibile
                if len(new_actions) < len(old_actions) - USER_MOVES:
                    new_plan = new_actions
                    print("Grazie alle tue mosse mi sono venute in mente nuove idee!")
                else:
                    print("Grazie alle tue mosse mi sono venute in mente nuove idee brutte! Continuo il piano precedente!")
                    new_plan = old_actions[USER_MOVES:]
            else:
                if len(new_actions) < len(old_actions) - USER_MOVES:
                    if len(old_actions) - len(new_actions) > USER_MOVES:
                        print("Hai fatto delle mosse migliori di quelle che pensavo io stesso!")
                    else:
                        print("Mosse buone ma non le migliori") # possibile
                else:
                    print("Pessime mosse") # possibile
            '''
            creo il json con robot moves e l'interazione del robot con l'utente in base alle mosse fatte
            '''
            robot_moves = new_plan if len(new_plan) < ROBOT_MOVES else new_plan[:ROBOT_MOVES]
            return {"message": "GET request succeed", "error": False, "response": {"new_plan": new_plan, "robot_moves": robot_moves}}
        return {"message": "GET request failed", "error": True}

    def put(self):
        if self.req == PUT_GAME_STATUS:
            with open("./data/game_status.json", 'r') as file_json:
                data = json.load(file_json)
            for key, value in request.json.items():
                data[key] = value
            with open("./data/game_status.json", 'w') as f:
                json.dump(data, f)
            return {"message": "PUT request succeed", "error": False}
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