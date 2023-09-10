import os, sys


import requests

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin()

pepper_cmd.robot.asay("Hello!")

url = "http://0.0.0.0:8080/"

def right():
    response = requests.get(url + "right")
    print(response.text)

right()



url2 = "http://0.0.0.0:8081/"
response = requests.get(url2 + "chat")
print(response.text)

end()
