import sys 
import os
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *
from math import *

sys.path.append("./utils")
sys.path.append("./../utils")

from chat import *
import random
import threading

      
class Gesture:
    def __init__(self, doGesture, typeImage = "happyImage", favourite=None):
        self.ALMotion = pepper_cmd.robot.motion_service
        self.doGesture = doGesture
        self.tts_service = pepper_cmd.robot.tts_service
        self.typeImage = typeImage
        self.favourite = favourite
        self.chat = Dialogue()
        # Good moves sentences
        self.yes_sentence = [
            "Wow, what brilliant moves!",
            "You couldn't have done better.",
            "These moves are incredible!",
            "Very good!",
            "Simply amazing!",
            "There is nothing to say but 'perfect'.",
            "Great moves!"
        ]
        # Bad moves sentences
        self.no_sentence = [
            "Not an optimal choice.",
            "I think you could have considered better alternatives.",
            "Perhaps you should have planned this move differently.",
            "It was not the most strategic move you could make.",
            "This move might not be your best."
        ]
        # Neutral moves sentences
        self.neutral_sentence = [
            "Hmm...",
            "Hmm... I see.",
            "Let me think...",
            "Okay okay..."
        ]
        # Game won sentences
        self.win_sentence = [
            "We won!",
            "A wonderful victory! We are champions!",
            "Victory!",
            "Well done! We won!"
        ]


    def doHello(self):
        '''
        Hello animation
        '''
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch"]
        angles = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07]
        times  = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
        isAbsolute = True
        self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        for i in range(2):
            jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
            angles = [1.7, -0.07, -0.07]
            times  = [0.8, 0.8, 0.8]
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
            angles = [1.3, -0.07, -0.07]
            times  = [0.8, 0.8, 0.8]
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)
        return
    
    def movetileRight(self):
        '''
            Move robot arm to the right to obtain a move to the right in the game.
        '''
        isAbsolute = True

        # First motion
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
        jointValues = [1.57, -0.33, 1.75, 1.23, -0.1, 0.70]
        times = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]        
        self.ALMotion.angleInterpolation(jointNames, jointValues, times, isAbsolute)

        # Second motion
        jointNames = ["RElbowRoll", "RElbowYaw", "RShoulderRoll", "RWristYaw"]
        jointValues = [1.38, 1.23, -0.25, -0]
        times = [0.6, 0.6, 0.6, 0.6]
        self.ALMotion.angleInterpolation(jointNames, jointValues, times, isAbsolute)
    
    def movetileLeft(self):
        '''
            Move robot arm to the left to obtain a move to the left in the game.
        '''
        isAbsolute = True

        # First motion
        jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand"]
        jointValues = [1.57, 0.33, -1.75, -1.23, 0.1, 0.70]
        times = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        self.ALMotion.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        
        # Second motion
        jointNames = ["LElbowRoll", "LElbowYaw", "LShoulderRoll", "LWristYaw"]
        jointValues = [-1.38, -1.23, -0.25, -0]
        times = [0.6, 0.6, 0.6, 0.6]
        self.ALMotion.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        
    def movetileUp(self):
        '''
            Move robot arm up to get a move up in the game.
        '''
        isAbsolute = True
        
        # First motion
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
        jointValues = [1.57, -0.20, 1.75, 1.23, -0.1, 0.70]
        times = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        self.ALMotion.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        
        # Second motion
        jointNames = ["RShoulderPitch",  "RElbowYaw", "RWristYaw"]
        jointValues = [0.2, 1.50, 1.16]
        times = [0.6, 0.6, 0.6, 0.6]
        self.ALMotion.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    def movetileDown(self):
        '''
            Move robot arm down to get a move down in the game.
        '''
        isAbsolute = True
        
        # First motion
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"]
        jointValues = [1.0, -0.26, 1.75, 1.23, -0.1, 0.70]
        times = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
        
        self.ALMotion.angleInterpolation(jointNames, jointValues, times, isAbsolute)
        
        # Second motion
        jointNames = ["RShoulderPitch", "RElbowYaw", "RWristYaw", "RElbowRoll", "RHand"]
        jointValues = [1.50, 1.50, -1.16, 0.4, 0.70]
        times = [0.6, 0.6, 0.6, 0.6, 0.6]
        self.ALMotion.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    def gestureSearching(self):
        pepper_cmd.robot.headPose(0.5, -0.07, 2.0)        
        pepper_cmd.robot.headPose(-0.5, -0.07, 2.0)
        pepper_cmd.robot.headPose(0, -0.2, 2.0)
    
    def gestureAnalyzing(self):     
        pepper_cmd.robot.headPose(0, -0.5, 2.0)        
        pepper_cmd.robot.headPose(0, 0.5, 2.0)
        pepper_cmd.robot.headPose(0.0, -0.2, 2.0)

    def doYes(self):
        '''
            The robot does yes with the head. This animation is used when the user does good moves in the game
        '''
        # Good sentence in parallel with the animation
        yes_thread = threading.Thread(target=self.chat.say, args=(random.choice(self.yes_sentence),))
        yes_thread.start()
        for _ in range(2):
            # First motion
            jointNames = ["HeadPitch"]
            angles = [-0.3]
            times  = [1.0]
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)
            # Second motion
            jointNames = ["HeadPitch"]
            angles = [0.1]
            times  = [1.0]
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        return
    
    def doNo(self):
        '''
            The robot does no with the head. This animation is used when the user does bad moves in the game
        '''
        # Bad sentence in parallel with the animation
        no_thread = threading.Thread(target=self.chat.say, args=(random.choice(self.no_sentence),))
        no_thread.start()
        self.ALMotion.angleInterpolation(["HeadYaw", "HeadPitch"], [0.30, 0.08], 0.4, True)
        self.ALMotion.angleInterpolation("HeadYaw", -0.40, 0.5, True)
        self.ALMotion.angleInterpolation("HeadYaw", 0.40, 0.5, True)

    def doRock(self, reps = 5):
        '''
            Play guitar animation
        '''
        jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "HeadPitch"]

        angles = [1.10, 0.52, -1.36, -1.48, 
                 -1.41, 0.27, 1.29, -0.07,
                 0.68, 0.70, -0.26, 0.31,
                 -0.15, -0.17, 0.28]

        times = [1.0, 1.0, 1.0, 1.0, 
                 1.0, 1.0, 1.0, 1.0, 
                 1.0, 1.0, 1.0, 1.0,
                 1.0, 1.0, 1.0]
        
        isAbsolute = True
        self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        loops = 0
        while loops!=reps:
            
            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "HeadPitch"]

            angles = [1.10, 0.52, -1.36, -1.48, 
                    -1.41, 0.27, 1.29, -0.07,
                    0.68, 1.48, -0.26, 0.60,
                    0.15, -0.17, -0.43]
                    
            times = [0.5, 0.5,0.5, 0.5, 
                    0.5, 0.5, 0.5, 0.5, 
                    0.5, 0.5, 0.5, 0.5,
                    0.5, 0.5, 0.5]
            
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)
            
            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "HeadPitch"]

            angles = [1.10, 0.52, -1.36, -1.48, 
                    -1.41, 0.27, 1.29, -0.07,
                    0.68, 0.70, -0.26, 0.70,
                    -0.15, -0.17, 0.43]
            
            times = [0.5, 0.5,0.5, 0.5, 
                    0.5, 0.5, 0.5, 0.5, 
                    0.5, 0.5, 0.5, 0.5,
                    0.5, 0.5, 0.5]

            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)
        
            loops+=1

    def getThinkingPose(self, game=True):
        '''
            The robot does a thinking pose. This animation is used when the user 
            does neutral moves in the game if the parameter game is True
        '''
        if game:
            # Neutral sentence in parallel with the animation
            neutral_thread = threading.Thread(target=self.chat.say, args=(random.choice(self.neutral_sentence),))
            neutral_thread.start()
        for _ in range(5):
            HeadYaw = radians(0)
            HeadPitch = radians(-11.4)
            LShoulderPitch = radians(-50.0)
            LShoulderRoll = radians(10.0)
            LElbowYaw = radians(-40)
            LElbowRoll = radians(-85)
            LWristYaw = radians(-60.0)
            RShoulderPitch = radians(81.3)
            RShoulderRoll = radians(-33.1)
            RElbowYaw = radians(32.4)
            RElbowRoll = radians(70.4)
            RWristYaw = radians(21.4)
            LHand = 0.5
            RHand = 0.98
            HipRoll = radians(0)
            HipPitch = radians(-6.8)
            KneePitch = radians(-0.1)

            jointValues = [HeadYaw, HeadPitch,
                LShoulderPitch, LShoulderRoll, LElbowYaw, LElbowRoll, LWristYaw,
                RShoulderPitch, RShoulderRoll, RElbowYaw, RElbowRoll, RWristYaw,
                LHand, RHand, HipRoll, HipPitch, KneePitch]
            
            jointNames = ["HeadYaw", "HeadPitch",
                    "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
                    "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
                    "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]
            
            self.ALMotion.angleInterpolation(jointNames, jointValues, 1.0, True)

         
    def doWin(self):
        '''
            The robot does a win animation. This animation is used when the game is won
        '''
        # Neutral sentence in parallel with the animation
        win_thread = threading.Thread(target=self.chat.say, args=(random.choice(self.win_sentence),))
        win_thread.start()
        HeadYaw = radians(0)
        HeadPitch = radians(-11.4)
        LShoulderPitch = radians(36)
        LShoulderRoll = radians(7.8)
        LElbowYaw = radians(-90.3)
        LElbowRoll = radians(-70.1)
        LWristYaw = radians(-101.4)
        RShoulderPitch = radians(37.1)
        RShoulderRoll = radians(-8.6)
        RElbowYaw = radians(92.2)
        RElbowRoll = radians(70.4)
        RWristYaw = radians(96.1)
        LHand = 0.04
        RHand = 0.03
        HipRoll = radians(0.1)
        HipPitch = radians(-0.5)
        KneePitch = radians(-0.4)

        jointValues = [HeadYaw, HeadPitch,
                LShoulderPitch, LShoulderRoll, LElbowYaw, LElbowRoll, LWristYaw,
                RShoulderPitch, RShoulderRoll, RElbowYaw, RElbowRoll, RWristYaw,
                LHand, RHand, HipRoll, HipPitch, KneePitch]
        
        jointNames = ["HeadYaw", "HeadPitch",
                    "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw",
                    "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw",
                    "LHand", "RHand", "HipRoll", "HipPitch", "KneePitch"]            
        self.ALMotion.angleInterpolation(jointNames, jointValues, 1.0, True)

        LShoulderPitch = radians(80)
        LShoulderRoll = radians(7.8)
        LElbowYaw = radians(-90.3)
        LElbowRoll = radians(-89.1)
        LWristYaw = radians(-101.4)
        RShoulderPitch = radians(80)
        RShoulderRoll = radians(-7.8)
        RElbowYaw = radians(92.2)
        RElbowRoll = radians(89)
        RWristYaw = radians(96.1)
        LHand = 0.04
        RHand = 0.03
        HipRoll = radians(0.1)
        HipPitch = radians(-0.5)
        KneePitch = radians(-0.4)

        jointValues = [HeadYaw, HeadPitch,
                LShoulderPitch, LShoulderRoll, LElbowYaw, LElbowRoll, LWristYaw,
                RShoulderPitch, RShoulderRoll, RElbowYaw, RElbowRoll, RWristYaw,
                LHand, RHand, HipRoll, HipPitch, KneePitch]        
        self.ALMotion.angleInterpolation(jointNames, jointValues, 0.4, True)
        
        LShoulderPitch = radians(36)
        LShoulderRoll = radians(7.8)
        LElbowYaw = radians(-90.3)
        LElbowRoll = radians(-80.1)
        LWristYaw = radians(-101.4)
        RShoulderPitch = radians(37.1)
        RShoulderRoll = radians(-8.6)
        RElbowYaw = radians(92.2)
        RElbowRoll = radians(80.4)
        RWristYaw = radians(96.1)

        jointValues = [HeadYaw, HeadPitch,
                LShoulderPitch, LShoulderRoll, LElbowYaw, LElbowRoll, LWristYaw,
                RShoulderPitch, RShoulderRoll, RElbowYaw, RElbowRoll, RWristYaw,
                LHand, RHand, HipRoll, HipPitch, KneePitch]
        self.ALMotion.angleInterpolation(jointNames, jointValues, 0.4, True)
