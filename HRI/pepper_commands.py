

from numpy.random import choice

import time
import math
import os, sys
import csv
import json 
import pickle

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *


# self.memory_service  = self.session.service("ALMemory")
# self.motion_service  = self.session.service("ALMotion")
# self.tts_service = self.session.service("ALTextToSpeech")
# self.anspeech_service = self.session.service("ALAnimatedSpeech")
# self.leds_service = self.session.service("ALLeds")
# self.asr_service = self.session.service("ALSpeechRecognition")
# self.touch_service = self.session.service("ALTouch")

#begin()

class Configure():
    def __init__(self, alive = True, speed = 50):
        pepper_cmd.robot.setAlive(alive)
        pepper_cmd.robot.tts_service.setParameter("speed", speed)


class Dialogue:

    def __init__(self, speed = 1.0):
        Configure(speed = speed)

    def say(self, sentence, require_answer = False, sleeping_time = 0.0):
        pepper_cmd.robot.say(sentence)
        if require_answer:
            return self.listen(timeout = 30)
        if sleeping_time:
            time.sleep(sleeping_time)

    def listen(self, vocabulary = ['simone', 'omar', 'cristiano', 'iocchi', 'yes', 'no'], timeout = 15):
        answer = pepper_cmd.robot.asr(vocabulary = vocabulary, timeout = timeout)
        while not answer:
            answer = self.say(sentence = "Sorry, I did not hear you, repeat please.", require_answer = True)
        return answer
    
class Database:
    def __init__(self, filename, timeout=30):
        Configure()
        self.file = filename+".json"
        self.timeout = timeout
        self.chat = Dialogue()
        #self.items = {} #a dictionary where the name is the key and the value will the user data
        
    def create_db(self):
        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                # writer = csv.DictWriter(f, delimiter=",", fieldnames=header)
                # writer.writeheader()
                json.dump({}, f)
                #pickle.dump(self.items, f)
    
    def name_user(self):
        name = self.chat.say("What is your name?"+" "*5, require_answer=True)
        print("Name is "+ name)
        #self.chat.say("Perfect! Nice to meet you {}".format(name)+ " "*5)
        return name

    def detect_user(self, register=True, is_new=False):
        data = {}

        if os.path.exists(self.file):
            
            name = self.name_user()
            with open(self.file, 'r') as f:
                data = json.load(f)
                print(data)
                #data = pickle.load(f)
                if name in data.keys(): #already registered user 
                    print("{} exists in the database".format(name))
                    self.chat.say("Glad to see you again {}!".format(name)+ " "*8)
                else:
                    print("{} not exists in the database".format(name))
                    self.chat.say("Nice to meet you {}!".format(name)+ " "*8)
                    is_new = True
            
            if is_new:
                self.register_user(data, name)
                       
        return is_new, name
    
    def register_user(self, data, name):
                
        if os.path.exists(self.file):
            with open(self.file, 'w') as f:
                
                data[name] = {"Max_level":0} #create an entry with user data
                
                json.dump(data, f)
                #pickle.dump(data)
        else:
            print("No Database has been created")
    
    def update_result(self, name, result):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                data = json.load(f)
            
            with open(self.file, 'w') as f:
                data[name]["Max_level"] = result
                json.dump(data, f)








class Touch:
    def __init__(self, touched = False):
        self.jointNames = ["HeadYaw", "HeadPitch",
               "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
               "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
               "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]
        self.sensors = {'HeadMiddle': 'Device/SubDeviceList/Head/Touch/Middle/Sensor/Value' ,
                        'LHand':      'Device/SubDeviceList/LHand/Touch/Back/Sensor/Value' ,
                        'RHand':      'Device/SubDeviceList/RHand/Touch/Back/Sensor/Value' }
        self.touched = touched
    
    def isTouched(self, sensor):
        try:
            sensor_key = self.sensors[sensor]
            print("Touching %s ..." %sensor)
            pepper_cmd.robot.memory_service.insertData(sensor_key,1.0)
            time.sleep(2)
            pepper_cmd.robot.memory_service.insertData(sensor_key,0.0)
            print("Touching %s ... done" %sensor)
            return True
        except:
            print("ERROR: Sensor %s unknown" %sensor)
            return False
    
    def change_pose(self, indices, values, pose, sleeping_time = 0.5):
        joint_list = []
        for i, v in zip(indices, values):
            pose[i] = v
            joint_list.append(self.jointNames[i])

        pepper_cmd.robot.setPosture(pose)
        time.sleep(sleeping_time)
        print("Pose changed in joints: {}".format(joint_list))

        return pose
    
    def monitor_touch(self, sensor, monitoring_time = 20.0):
        
        curr_time = time.time() #start timer
        pepper_cmd.robot.startSensorMonitor()
        print("Waiting a touch to start during {} seconds...".format(monitoring_time))
        while not self.touched and (time.time() - curr_time < monitoring_time):
            p = pepper_cmd.robot.sensorvalue()
            self.touched = (p[3] >0)
        pepper_cmd.robot.stopSensorMonitor()
        if self.touched:
            print("A touch is detected.")
            pose = pepper_cmd.robot.getPosture()
            self.change_pose([0, 1], [0.0, -0.5], pose, sleeping_time = 1.0)
            pepper_cmd.robot.say("aja")
            pepper_cmd.robot.normalPosture()
            print("Pose is back to normal")

        return self.touched

    
    
class Vision:
    def __init__(self):
        pass

    
    def cnnForEmotionRecognition(self, image):
        classes = ["Neutral", "Happy", "Sad", "Surprise"]

        prediction = self.forward(image)

        return classes[prediction]


    def forward(self, image):
        list_of_candidates = [0, 1, 2, 3]

        if image == "happyImage":
            weights = [0.1, 0.5, 0.05, 0.35]
        elif image == "neutralImage":
            weights = [0.7, 0.1, 0.1, 0.1]  
        elif image == "sadImage":
            weights = [0.1, 0.05, 0.8, 0.05]  
        elif image == "surpriseImage":
            weights = [0.1, 0.35, 0.05, 0.5]  
        
        output = choice(list_of_candidates, 1, p=weights)[0]

        return output

class Motion:
    def __init__(self):
        self.motion_service = pepper_cmd.robot.motion_service

    def setSpeed(self, lin_vel, ang_vel, dtime, sonar):
        self.motion_service.move(lin_vel, 0, ang_vel)
        time.sleep(dtime)
        self.motion_service.stopMove()
        return 

    def forward(self, sonar, s, lin_vel=0.2, ang_vel=0):
        print("Sonar Values", sonar.sonarValues)
        self.setSpeed(lin_vel, ang_vel, abs((s-0.5)/lin_vel), sonar)
        # aggiornare la nuova posizione del robot

    
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
        self.robot_position = robot_position # tuple (int, int)
        self.humans_positions = self.get_positions()
        
    def set_sonar(self):

        distances = self.get_distances()

        mkey = self.sonarValueList[0]
        self.memory_service.insertData(mkey,distances)
        mkey = self.sonarValueList[1]
        self.memory_service.insertData(mkey,None) #disabled
        time.sleep(self.duration)
        self.sonarValues =  self.memory_service.getListData(self.sonarValueList)
        print(self.sonarValues)


    #we use only the frontal sonar, so it will discover only humans in front of him
    def get_positions(self):
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


#end()
