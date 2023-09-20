

from numpy.random import choice

import time
import math
import os
import json 

import sys
sys.path.append("./utils")
sys.path.append("./../utils")

from chat import *

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

fakeASRkey = 'FakeRobot/ASR'
fakeASRevent = 'FakeRobot/ASRevent'
fakeASRtimekey = 'FakeRobot/ASRtime'

class Database:
    def __init__(self, filename, timeout=30):
        self.file = "./data/" + filename + ".json"
        self.timeout = timeout
        self.chat = Dialogue()
        self.is_new = False
        
    def create_db(self):
        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                json.dump({}, f, indent=4)
        with open("./data/game_pepper_interaction.json", 'w') as f:
            json.dump({
                "win": False,
                "robot_moves": [],
                "interaction": ""
            }, f, indent=4)
    
    def name_user(self):
        name = self.chat.say("What is your name?", require_answer=True)
        self.save_user(name)
        print("Name is "+ name)
        return name
    
    def save_user(self, name):
        with open("./data/actual_user.json", 'w') as f:
            json.dump({"user": name}, f, indent=4)


    def detect_user(self):
        data = {}
        if os.path.exists(self.file):            
            name = self.name_user()
            with open(self.file, 'r') as f:
                data = json.load(f)
                if name in data.keys(): # Already registered user 
                    print("{} exists in the database".format(name))
                    self.chat.say("Glad to see you again {}!".format(name))
                else:
                    print("{} not exists in the database".format(name))
                    self.chat.say("Nice to meet you {}!".format(name))
                    self.is_new = True            
            if self.is_new:
                self.register_user(data, name)                       
        return name
    
    def register_user(self, data, name):                
        if os.path.exists(self.file):
            with open(self.file, 'w') as f:                
                data[name] = {
                    "Games": {
                        "easy": {
                            "record_moves": "-",
                            "record_time": "--:--",
                            "num_games_won": 0
                        },
                        "medium": {
                            "record_moves": "-",
                            "record_time": "--:--",
                            "num_games_won": 0
                        },
                        "hard": {
                            "record_moves": "-",
                            "record_time": "--:--",
                            "num_games_won": 0
                        },
                        "last_difficulty": "easy"
                    },
                    "Survey": {}
                } # Create an entry with user data                
                json.dump(data, f, indent=4)
        else:
            print("No Database has been created")
    
    def update_result(self, name, result):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                data = json.load(f)            
            with open(self.file, 'w') as f:
                data[name]["Max_level"] = result
                json.dump(data, f, indent=4)

class Motion:
    def __init__(self):
        self.motion_service = pepper_cmd.robot.motion_service

    def setSpeed(self, lin_vel, ang_vel, dtime, sonar):
        self.motion_service.move(lin_vel, 0, ang_vel)
        time.sleep(dtime)
        self.motion_service.stopMove()

    def forward(self, sonar, s, lin_vel=0.2, ang_vel=0):
        print("Sonar Values", sonar.sonarValues)
        self.setSpeed(lin_vel, ang_vel, abs((s-0.5)/lin_vel), sonar)
    
    def detect_person(self, sonar):
        for i in range(len(sonar.sonarValues)):
            if sonar.sonarValues[i] <= 0.75:
                if i==0:
                    print("Person detected with sonar SonarFront")
                else:
                    print("Person detected with sonar SonarBack")
                return True
        return False

    def selectMinDistance(self, distances):
        min_distance = float("inf")
        index = 0
        for i in range(len(distances)):
            if distances[i] < min_distance:
                min_distance = distances[i]
                index = i
        return min_distance, index    

class Sonar:
    def __init__(self, robot_position, sensor= "SonarFront", duration = 3.0):
        self.sensor = sensor
        self.memory_service = pepper_cmd.robot.memory_service
        self.duration = duration
        self.sonarValueList = ['Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value',
                               'Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value' ]
        self.robot_position = robot_position
        self.humans_positions = self.get_positions()
        
    def set_sonar(self):
        distances = self.get_distances()
        mkey = self.sonarValueList[0]
        self.memory_service.insertData(mkey,distances)
        mkey = self.sonarValueList[1]
        self.memory_service.insertData(mkey,None) # Disabled
        time.sleep(self.duration)
        self.sonarValues =  self.memory_service.getListData(self.sonarValueList)
        print(self.sonarValues)

    def get_positions(self):
        '''
            We use only the frontal sonar, so it will discover only humans in front of him
        '''
        human1_position = (1,0)
        human2_position = (2,0)
        humans_positions = [human1_position, human2_position]
        return humans_positions

    def get_distances(self):
        distances = []
        for pos in self.humans_positions:
            distance = math.sqrt((self.robot_position[0]-pos[0])**2 + (self.robot_position[1]-pos[1])**2)
            distances.append(distance)
        return distances