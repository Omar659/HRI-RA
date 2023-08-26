import os, sys
import pepper_cmd
from pepper_cmd import *

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

begin()

pepper_cmd.robot.say('Hello')

end()
