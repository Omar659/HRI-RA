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

    def say(self, sentence, require_answer = False):
        pepper_cmd.robot.say(sentence + " "*15)

        if require_answer:
            return self.listen(sentence)
        else:
            self.api.call('get',  TIMEOUT, ['req', GET_MSG], ['sentence',sentence]) #pepper sentence


    def listen(self, sentence):
        try:
        #answer = pepper_cmd.robot.asr(vocabulary = vocabulary, timeout = timeout)
            answer = self.api.call('get',  TIMEOUT, ['req', GET_ANS], ['sentence',sentence])["response"] #human answer
            #print(answer)
        except:
            answer = self.say(sentence = "Sorry, I did not hear you, repeat please.", require_answer = True)
        return answer