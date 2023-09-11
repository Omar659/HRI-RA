import os, sys


# To import api_call
import sys
sys.path.append('./utils')
sys.path.append('./../utils')
from api_call import *
from config import *

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin()

pepper_cmd.robot.asay("Hello!")


api_call = API_call(URL, "planner")
response = api_call.call("get", ("req", GET_JSON), ("json_path", "./data/game_status.json"))
print()
print(response)


api_call = API_call(URL, "chat")
response = api_call.call("get", ("req", GET_JSON), ("json_path", "./data/game_status.json"))
print()
print(response)

# def right():
#     response = requests.get(url + "right")
#     print(response.text)

# right()

# response = requests.get(url, headers={"Content-Type": "application/json"})
# print(response.status_code)
# print(response.text)

# url2 = "http://0.0.0.0:8081/"
# response = requests.get(url2 + "chat")
# print(response.text)

end()
