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

    def say(self, sentence, require_answer = False, choices = []):
        pepper_cmd.robot.say(sentence + " "*15)

        if require_answer:
            if choices == []:
                return self.listen(sentence)
            else:
                return self.listen_multi(sentence, choices)
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
    
    def listen_multi(self, sentence, choices):
        #answer = pepper_cmd.robot.asr(vocabulary = vocabulary, timeout = timeout)
        answer = self.api.call('get',  9000, ['req', GET_MULTI], ['sentence',sentence], ["choices", ",".join(choices)])["response"] #human answer
        if answer.lower() not in choices:
            answer = self.say(sentence = "Sorry I didn't understand, can you repeat please?", require_answer=True, choices=choices)
        return answer
