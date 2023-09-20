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
            with open("./data/actual_user.json", 'r') as f:
                user = json.load(f)["user"]
            with open("./data/registered_users.json", 'r') as f:
                user_info = json.load(f)
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
                json.dump(data, f, indent=4)
            return {"message": "POST request succeed", "error": False}
        return {"message": "POST request failed", "error": True}

    def get(self):
        if self.req == GET_JSON:
            if self.json_path == None:
                return {"message": "Missing the json path", "error": True}
            with open(self.json_path, 'r') as f:
                data = json.load(f)
            return {"message": "JSON file returned", "error": False, "response": data}
        if self.req == GET_ROBOT_MOVES:
            with open("./data/game_status.json", 'r') as f:
                data = json.load(f)
            difficult = data["difficult"]
            slide_tile_pddl = Slide_tile_PDDL(difficult=difficult, optimal_plan=True, verbose=False)
            slide_tile_pddl.slide_tile.generate_tiles_from_mat(data["tiles"], data["bx"], data["by"])
            slide_tile_pddl.create_problem()
            slide_tile_pddl.solve_problem()
            new_actions = [str(action).split("(")[0].split(" ")[1] for action in slide_tile_pddl.plan.actions]
            old_actions = data["plan"]
            user_moves = data["user_moves"]
            new_plan = new_actions
            interaction = "neutral"
            if old_actions[:USER_MOVES] == user_moves:
                interaction = "good"
                if len(new_actions) < len(old_actions) - USER_MOVES:
                    new_plan = new_actions
                else:
                    new_plan = old_actions[USER_MOVES:]
            elif len(new_actions) >= len(old_actions):
                interaction = "bad"
            robot_moves = new_plan if len(new_plan) < ROBOT_MOVES else new_plan[:ROBOT_MOVES]
            gesture = {
                "win": False,
                "robot_moves": robot_moves,
                "interaction": interaction
            }
            with open("./data/game_pepper_interaction.json", 'w') as f:
                json.dump(gesture, f, indent=4)
            return {"message": "GET request succeed", "error": False, "response": {"new_plan": new_plan, "robot_moves": robot_moves, "interaction": interaction}}
        return {"message": "GET request failed", "error": True}

    def put(self):
        if self.req == PUT_GAME_STATUS:
            with open("./data/game_status.json", 'r') as f:
                data = json.load(f)
            for key, value in request.json.items():
                data[key] = value
            with open("./data/game_status.json", 'w') as f:
                json.dump(data, f, indent=4)
            return {"message": "PUT request succeed", "error": False}
        if self.req == PUT_WIN:
            with open("./data/game_pepper_interaction.json", 'r') as f:
                game_pepper_interaction = json.load(f)
            with open("./data/registered_users.json", 'r') as f:
                registered_users = json.load(f)
            with open("./data/actual_user.json", 'r') as f:
                actual_user = json.load(f)["user"]

            game_pepper_interaction["win"] = True
                
            win_info = request.json
            win_difficult = win_info["difficult"].lower()
            win_victory_time = win_info["victory_time"].split(":")
            win_victory_moves = win_info["victory_moves"]

            registered_users[actual_user]["Games"][win_difficult]["num_games_won"] += 1
            registered_users[actual_user]["Games"]["last_difficulty"] = win_difficult

            if registered_users[actual_user]["Games"][win_difficult]["record_moves"] == "-":
                registered_users[actual_user]["Games"][win_difficult]["record_moves"] = int(win_victory_moves)
            elif int(registered_users[actual_user]["Games"][win_difficult]["record_moves"]) > int(win_victory_moves):
                registered_users[actual_user]["Games"][win_difficult]["record_moves"] = int(win_victory_moves)

            record_time = registered_users[actual_user]["Games"][win_difficult]["record_time"].split(":")
            record_minutes = 999 if record_time[0] == "--" else int(record_time[0])
            record_seconds = 59 if record_time[1] == "--" else int(record_time[1])
            win_minutes = int(win_victory_time[0])
            win_seconds = int(win_victory_time[1])
            if (record_minutes > win_minutes) or (record_minutes == win_minutes and record_seconds > win_seconds):
                registered_users[actual_user]["Games"][win_difficult]["record_time"] = ":".join([str(win_minutes).zfill(2), str(win_seconds).zfill(2)])

            with open("./data/game_pepper_interaction.json", 'w') as f:
                json.dump(game_pepper_interaction, f, indent=4)
            with open("./data/registered_users.json", 'w') as f:
                json.dump(registered_users, f, indent=4)            
            return {"message": "PUT request succeed", "error": False}
        return {"message": "PUT request failed", "error": True}

    def delete(self):
        return {"message": "DELETE request failed", "error": True}