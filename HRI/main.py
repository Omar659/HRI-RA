from __future__ import division

import argparse
from re import T
from gestures import Gesture
from pepper_commands import *
import os
import qi
import os
import subprocess
import sys

sys.path.append("./utils")
sys.path.append("./../utils")

sys.path.append("./")
sys.path.append("./../")

import random
import operator
from cd import *
from chat import *  #from utils
import webbrowser

#from database import Database
from numpy.random import choice
tablet = "./tablet/"
scripts = "scripts/"


global session
global index
global database
index = 1

global ALDialog
global topic_name
global topic_path
global doGesture
global name


doGesture = True
name = ""

begin()

def launch_application(app):
    with cd(os.path.join(app, scripts)):
        os.system("python game.py --user "+name)

    return

def connection():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot's IP address. If on a robot or a local Naoqi - use '127.0.0.1' (this is the default value).")
    parser.add_argument("--port", type=int, default=9559,
                        help="port number, the default value is OK in most cases")
    session = pepper_cmd.robot.session


def main(session):
    connection()
   

    # Gestures, Vision and Sensors
    touch = Touch()
    gesture = Gesture(True)
    #Chat
    chat = Dialogue() 
    # Motion
    motion = Motion()
    # Sonar
    sonar = Sonar(robot_position)
    sonar.set_sonar()    
    # Database
    database = Database(filename="registered_users", timeout=10)

    # Get ALDialog service    
    robot_position = (0,0)


    pepper_cmd.robot.normalPosture()

    chat.say("Searching for humans...")
    
    gesture.gestureSearching()
    time.sleep(2)

    chat.say("Human Found!")
    distances = sonar.get_distances()
    print("Distances: ", distances)
    min_distance, id = motion.selectMinDistance(distances) #id is the person id
    print("Min distance: ", min_distance)
    motion.forward(sonar, min_distance)
    print("Robot position", sonar.robot_position)
    sonar.robot_position = tuple(map(operator.sub, sonar.humans_positions[id], (0.5, 0)))
    print("Robot position", sonar.robot_position)
    pepper_cmd.robot.normalPosture()

    chat.say("Scanning human...")
    gesture.gestureAnalyzing()
    chat.say("Human Scanned!")

    chat.say("Hello! I'm Pepper.\nI'm here to play with you.")
    gesture.doHello()
    time.sleep(2)  
    chat.say("You can talk with me or interact by clicking the tablet.") 

    chat.say("Let us know each other")
    database.create_db()
    name = database.detect_user()


    
    

    database.create_db()
    database.detect_user()
    
    # Interaction with the game
    while True:
        time.sleep(0.1)
        if os.path.exists("./data/game_pepper_interaction.json"):
            with open("./data/game_pepper_interaction.json", 'r') as f:
                interaction = json.load(f)
            if interaction["win"]:
                gesture.doWin()
                pepper_cmd.robot.normalPosture()
                break
            if interaction["robot_moves"] != []:
                if interaction["interaction"] == "neutral":
                    gesture.getThinkingPose()
                elif interaction["interaction"] == "good":
                    gesture.doYes()
                elif interaction["interaction"] == "bad":
                    gesture.doNo()
                pepper_cmd.robot.normalPosture()
                for robot_move in interaction["robot_moves"]:
                    if robot_move == "Right":
                        gesture.movetileRight()
                    elif robot_move == "Left":
                        gesture.movetileLeft()
                    elif robot_move == "Up":
                        gesture.movetileUp()
                    elif robot_move == "Down":
                        gesture.movetileDown()
                    pepper_cmd.robot.normalPosture()
                with open("./data/game_pepper_interaction.json", 'w') as f:
                    json.dump({
                        "win": False,
                        "robot_moves": [],
                        "interaction": ""
                    }, f)

    return 0


if __name__ == "__main__":
    main(session)

end()




    # project_path = args.project_path

    # try:
    #     session.connect("tcp://{}:{}".format(args.ip, args.port))
    # except RuntimeError:
    #     print ("\nCan't connect to Naoqi at IP {} (port {}).\nPlease check your script's arguments."
    #            " Run with -h option for help.\n".format(args.ip, args.port))
    #     sys.exit(1)


    #min_distance = motion.selectMinDistance(humans_positions) -> prendo la distanza minima tra quelle nel sonar (per il momento solo humans frontali)
    #possiamo fare anche che l'umano sta in diagonale rispetto al robot, questo richiederebbe di calcolare l'angolo alpha tra il robot e l'umano 
    #usando l'arcotangente e far poi ruotare il robot di quell'angolo alpha
    #motion.forward(min_distance, sonar)


    # gesture.movetileRight()
    # pepper_cmd.robot.normalPosture()
    # time.sleep(1.0)
    # gesture.movetileLeft()
    # pepper_cmd.robot.normalPosture()
    # time.sleep(1.0)
    # gesture.movetileUp()
    # pepper_cmd.robot.normalPosture()
    # time.sleep(1.0)
    # gesture.movetileDown()
    # launch_application(tablet)
    # gesture.doNo()
    # gesture.doWin()
    # gesture.doRock()
   
    # gesture.doNo()
    # gesture.doWin()
    #gesture.getThinkingPose()


    # parser.add_argument("--project-path", type=str, required=True,
    #                     help="path of the project folder, for instance: /home/sveva/playground/Pepper-Interaction/project-pepper")
   
    # args = parser.parse_args()


    #Sounds
    # audio_player = session.service("ALAudioPlayer")
    #audio_player.playFile("/home/simone/playground/HRI-RA/HRI/sounds/rock1.wav", _async=True)