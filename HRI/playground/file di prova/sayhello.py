import os, sys, qi
# pip = os.getenv('PEPPER_IP')
# pport = 9559
# url = "tcp://" + pip + ":" + str(pport)
# app = qi.Application(["App", "--qi-url=" + url ])
# app.start() # non blocking
# session = app.session
# memory_service=app.session.service("ALMemory")
sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')
import pepper_cmd
from pepper_cmd import *
begin()

vocabulary = ["hi", "hello"]
timeout = 30
answer = pepper_cmd.robot.asr(vocabulary,timeout)
if answer!="":  # valid answer
    print(answer)
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
    pepper_cmd.robot.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

    loops = 0

    while loops!=4:
        
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
        pepper_cmd.robot.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)
        
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
        pepper_cmd.robot.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)
    
        # if loops == 4:
            #self.messageVision(self.vision, self.tts_service, self.typeImage, "rock")
        loops+=1

end()

