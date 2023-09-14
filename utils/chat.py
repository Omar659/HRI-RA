from numpy.random import choice

import time
import math
import os, sys
import csv
import json 

sys.path.append('./utils')
sys.path.append('./../utils')
from api_call import *
from config import *

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *


class Dialogue:

    def __init__(self):
        self.api = API_call(URL, "chat")

    def say(self, sentence, require_answer = False, sleeping_time = 0.0):
        pepper_cmd.robot.say(sentence)

        if require_answer:
            return self.listen(sentence)
        else:
            self.api.call('get',  TIMEOUT, ['req', GET_MSG], ['sentence',sentence]) #pepper sentence

        if sleeping_time:
            time.sleep(sleeping_time)

    def listen(self, sentence):
        try:
        #answer = pepper_cmd.robot.asr(vocabulary = vocabulary, timeout = timeout)
            answer = self.api.call('get',  TIMEOUT, ['req', GET_ANS], ['sentence',sentence])["response"] #human answer
            #print(answer)
        except:
            answer = self.say(sentence = "Sorry, I did not hear you, repeat please.", require_answer = True)
        return answer
    
class Database:
    def __init__(self, filename, timeout=30):

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
                       
        return name
    
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