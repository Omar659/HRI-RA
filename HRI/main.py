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

import threading

sys.path.append("./utils")
sys.path.append("./../utils")

sys.path.append("./")
sys.path.append("./../")

from api_call import *
from config import *

import random
import operator
from cd import *
from chat import *  #from utils
import webbrowser

#from database import Database
from numpy.random import choice
tablet = "./tablet/"
scripts = "scripts/"


# global session
# global index
# global database
# index = 1

# global ALDialog
# global topic_name
# global topic_path
# global doGesture
# global name


# doGesture = True
# name = ""

begin()

def launch_application(page):
    api = API_call(URL, "chat")
    api.call("get", TIMEOUT, ("req", GET_HTML), ("page", page))
    return

def connection():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot's IP address. If on a robot or a local Naoqi - use '127.0.0.1' (this is the default value).")
    parser.add_argument("--port", type=int, default=9559,
                        help="port number, the default value is OK in most cases")
    # session = pepper_cmd.robot.session

def init_values():
    # Starting position
    robot_position = (0,0)

    # CLASSES
    # Gestures
    gesture = Gesture(True)
    # Chat
    chat = Dialogue() 
    # Motion
    motion = Motion()
    # Sonar
    sonar = Sonar(robot_position)
    sonar.set_sonar()    
    # Database
    database = Database(filename="registered_users", timeout=10)
    return robot_position, gesture, chat, motion, sonar, database

def approach(chat, gesture, sonar, motion, database):
    # pepper_cmd.robot.normalPosture()
    # chat.say("Searching for humans...")
    
    # gesture.gestureSearching()
    # time.sleep(2)

    # chat.say("Human Found!")
    # distances = sonar.get_distances()
    # print("Distances: ", distances)
    # min_distance, id = motion.selectMinDistance(distances) #id is the person id
    # print("Min distance: ", min_distance)
    # motion.forward(sonar, min_distance)
    # print("Robot position", sonar.robot_position)
    # sonar.robot_position = tuple(map(operator.sub, sonar.humans_positions[id], (0.5, 0)))
    # print("Robot position", sonar.robot_position)
    # pepper_cmd.robot.normalPosture()

    # chat.say("Scanning human...")
    # gesture.gestureAnalyzing()
    # chat.say("Human Scanned!")

    # chat.say("Hello! I'm Pepper.\nI'm here to play with you.")
    # gesture.doHello()
    # time.sleep(2)  
    # chat.say("You can talk with me or interact by clicking the tablet.") 

    chat.say("Let us know each other")
    database.create_db()
    user_name = database.detect_user()

    answer = chat.say("Do you want to play with me?", True, ["yes", "no"])
    if answer == "yes":
        return user_name
    else:
        return None

def game(gesture):
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


def main():
    # Connect pepper
    connection()

    # Initialize values
    robot_position, gesture, chat, motion, sonar, database = init_values()
   
    # The robot start moving searching for a human and ask him what is his/her name
    user_name = approach(chat, gesture, sonar, motion, database)
    if user_name is None:
        bye_thread = threading.Thread(target=chat.say, args=("Ok, sorry to have bothered you.",))
        bye_thread.start()
        gesture.doHello()
        pepper_cmd.robot.normalPosture()
        return 0

    # The rotbot through some questions, select the difficulty
    # Se non ti conosce
    if database.is_new:
        answer = chat.say("Do you like puzzle games?", True, ["yes", "no"])
        if answer == "yes":
            yes_thread = threading.Thread(target=chat.say, args=("Perfect!",))
            yes_thread.start()
            gesture.doRock(2)
            pepper_cmd.robot.normalPosture()
        else:
            no_thread = threading.Thread(target=chat.say, args=("Hmm... maybe, I'll try to change your mind.",))
            no_thread.start()
            gesture.getThinkingPose(False)
            pepper_cmd.robot.normalPosture()
        answer = chat.say("Do you know Slide Puzzle game?", True, ["yes", "no"])
        if answer == "yes":
            launch_application("./HRI/tablet/HTML/starting_page/select_difficulty.html")
            chat.say("These are the difficulties. You can start a game at any of these, but I suggest you to start with the easy mode.")
        else:
            launch_application("./HRI/tablet/HTML/starting_page/tutorial.html")
            chat.say("The goal of the game is to sort the tiles in ascending order.")
            chat.say("Highlighted in green are the tiles you can move.")
            chat.say("At the bottom there is the elapsed time and the current number of moves and their records")
            chat.say("The purpose of the tutorial is to explain the rules to you, so you act on your own. In a normal game we will alternate between four of your moves and two of mine")
        return 0
    # Se ti conosce
    else:
        launch_application("./HRI/tablet/HTML/starting_page/select_difficulty.html")
        with open("./data/registered_users.json", 'r') as f:
            registered_users = json.load(f)
        
        chat.say("These are the difficulties. You can start a game at any of these, but I suggest you to start with the easy mode.")
        # pagina difficolta

    launch_application()

    game(gesture)

    # TASTO CONTINUA DA RISOLVERE

    # Piaciuto il gioco?
    # Risposta qualsiasi
    # Vuoi fare un altra partita?
        # si -> pagina difficolta
        # no -> pagina questionario (Puoi aiutarmi a capire cosa pensi di me e del gioco compilando questo breve questionario sulla tua esperienza)
 
    # ciao   

    return 0


if __name__ == "__main__":
    main()
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