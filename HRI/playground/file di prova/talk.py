import os, sys

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *
begin()

# speech recognition
# vocabulary = list of keywords, e.g. ["yes", "no", "please"]
vocabulary = ["yes", "no", "hi"]
timeout = 30 # seconds after function returns
answer = pepper_cmd.robot.asr(vocabulary,timeout)
if answer!="":  # valid answer
    print(answer)
    # speech synthesis
    pepper_cmd.robot.say("Hello. How are you?")

end()