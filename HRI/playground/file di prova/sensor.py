import os, sys

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin()

# Motion
# Read sensors

pepper_cmd.robot.startSensorMonitor()  # non-blocking
pepper_cmd.robot.startLaserMonitor()   # non-blocking

p = pepper_cmd.robot.sensorvalue() 
# [frontlaser, frontsonar, rearsonar, headtouch, lefthandtouch, righthandtouch]
print(p)

pepper_cmd.robot.stopSensorMonitor()
pepper_cmd.robot.stopLaserMonitor()


end()