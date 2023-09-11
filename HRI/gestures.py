import sys 
import os
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

      
class Gesture:
    def __init__(self, doGesture, vision, typeImage = "happyImage", favourite=None):
        self.ALMotion = pepper_cmd.robot.motion_service
        self.doGesture = doGesture
        self.vision = vision
        self.tts_service = pepper_cmd.robot.tts_service
        self.typeImage = typeImage
        self.favourite = favourite


    def doHello(self):
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
    
    def gestureSearching(self):
        pepper_cmd.robot.headPose(0.5, -0.07, 2.0)
        
        pepper_cmd.robot.headPose(-0.5, -0.07, 2.0)

        pepper_cmd.robot.headPose(0, -0.2, 2.0)
    
    def gestureAnalyzing(self):
     
        pepper_cmd.robot.headPose(0, -0.5, 2.0)
        
        pepper_cmd.robot.headPose(0, 0.5, 2.0)

        #set to normal
        pepper_cmd.robot.headPose(0.0, -0.2, 2.0)
            # jointNames = ["HeadYaw", "HeadPitch"]
            # angles = [-0.5, -0.07]
            # times  = [2.0, 2.0]
            # isAbsolute = True
            # self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        return


    def doYes(self):
        for i in range(2):
            jointNames = ["HeadPitch"]
            angles = [-0.3]
            times  = [1.0]
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["HeadPitch"]
            angles = [0.1]
            times  = [1.0]
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        return


    def doRock(self):
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

        while self.doGesture:
            
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
        
            if loops == 4:
                self.messageVision(self.vision, self.tts_service, self.typeImage, "rock")
            loops+=1


    def doJazz(self):
        jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "KneePitch", "HeadPitch"]

        angles = [1.20, 0.008, -0.65, -1.20, 
                 -0.05, 0.30, 0.33, -0.19,
                 0.40, 1.36, 0.99, 0.60,
                 -0.22, -0.26, -0.14, 0.05]

        times = [1.0, 1.0, 1.0, 1.0, 
                 1.0, 1.0, 1.0, 1.0, 
                 1.0, 1.0, 1.0, 1.0,
                 1.0, 1.0, 1.0, 1.0 ]
        
        isAbsolute = True
        self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        loops = 0
        
        while self.doGesture:
            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "KneePitch", "HeadPitch"]

            angles = [1.20, 0.008, -0.65, -1.20, 
                    -0.05, 0.30, 0.33, -0.19,
                    0.40, 1.36, 0.99, 0.60,
                    0.22, 0.26, 0.05, 0.05]

            times = [1.0, 1.0, 1.0, 1.0, 
                    1.0, 1.0, 1.0, 1.0, 
                    1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0 ]
        
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "KneePitch", "HeadPitch"]

            angles = [1.20, 0.008, -0.65, -1.20, 
                    -0.05, 0.30, 0.33, -0.19,
                    0.40, 1.36, 0.99, 0.60,
                    -0.12, -0.26, -0.14, 0.05]

            times = [1.0, 1.0, 1.0, 1.0, 
                    1.0, 1.0, 1.0, 1.0, 
                    1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0 ]
            
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            if loops == 2:
                self.messageVision(self.vision, self.tts_service, self.typeImage, "jazz")
            loops+=1

    
    def doClassical(self):
        
        jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "KneePitch", "HeadPitch"]

        angles = [0.85, 0.92, -2.07, -0.85, 
                -1.29, 0.43, -0.05, -0.01,
                -0.38, 0.71, 0.99, 0.60,
                0.2, -0.26, -0.14, 0.05]

        times = [1.0, 1.0, 1.0, 1.0, 
                1.0, 1.0, 1.0, 1.0, 
                1.0, 1.0, 1.0, 1.0,
                1.0, 1.0, 1.0, 1.0 ]
              
        
        isAbsolute = True
        self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        loops = 0

        while self.doGesture:
            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "KneePitch", "HeadPitch"]

            angles = [0.85, 0.92, -2.07, -0.85, 
                    -1.29, 0.43, -0.05, -0.01,
                    0, 0.71, 0.99, 0.60,
                    0.2, -0.26, -0.14, 0.05]

            times = [1.0, 1.0, 1.0, 1.0, 
                    1.0, 1.0, 1.0, 1.0, 
                    1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0 ]
                
            
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw","LElbowRoll", 
                      "LWristYaw", "LHand", "RShoulderPitch", "RShoulderRoll", 
                      "RElbowYaw","RElbowRoll", "RWristYaw", "RHand", 
                      "HipRoll", "HipPitch", "KneePitch", "HeadPitch"]

            angles = [0.85, 0.92, -2.07, -0.85, 
                    -1.29, 0.43, -0.05, -0.01,
                    -0.38, 0.71, 0.99, 0.60,
                    0.2, -0.26, -0.14, 0.05]

            times = [1.0, 1.0, 1.0, 1.0, 
                    1.0, 1.0, 1.0, 1.0, 
                    1.0, 1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0, 1.0 ]
                
            
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            if loops == 2:
                self.messageVision(self.vision, self.tts_service, self.typeImage, "classical")
            loops+=1

    
    def doPop(self):
        jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll"]

        angles = [0.64, 1.55, 0.64, -1.55]

        times = [1.0, 1.0, 1.0, 1.0]
              
        
        isAbsolute = True
        self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        loops = 0

        while self.doGesture:
            jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll", "HipRoll"]
            
            angles = [0.34, 1.25, 1, -1.25, 0.15]
            
            times = [1.0, 1.0, 1.0, 1.0, 1.0]
                
            
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll", "HipRoll"]
            
            angles = [1, 1.85, 0.34, -1.85, 0.15]
            
            times = [1.0, 1.0, 1.0, 1.0, 1.0]
                
            
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)


            angles = [0.34, 1.25, 1, -1.25, -0.15]
            
            times = [1.0, 1.0, 1.0, 1.0, 1.0]
                
            
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll", "HipRoll"]
            
            angles = [1, 1.85, 0.34, -1.85, -0.15]
            
            times = [1.0, 1.0, 1.0, 1.0, 1.0]
                
            
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            if loops == 1:
                self.messageVision(self.vision, self.tts_service, self.typeImage, "pop")
            loops+=1

    
    def messageVision(self, vision, tts_service, imageType, current_music):
        prediction = vision.cnnForEmotionRecognition(imageType)

        if (imageType == "sadImage" or imageType == "neutralImage") and current_music == self.favourite:
            tts_service.say("I see that you no longer like this music that you really liked in the past. Tell me stop if you want to change."+" "*5, _async=True)
        elif prediction == "Happy" or prediction == "Surprise":
            tts_service.say("I see your smile! I'm happy that you like the music!"+" "*5, _async=True)
        elif prediction == "Neutral" or prediction == "Sad":
            tts_service.say("It seems you don't like this song... Tell me stop if you want to change it."+" "*5, _async=True)

        

        return
    
