import os, sys

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *
begin()
pepper_cmd.robot.startSensorMonitor()

# wait until head touched
headTouched = False
while not headTouched:
  p = pepper_cmd.robot.sensorvalue()
  headTouched = p[3]>0   # head sensor

pepper_cmd.robot.say("Aja la testa!")

# wait until front sonar detect something (range < 1.0)
personHere = False
while not personHere:
  p = pepper_cmd.robot.sensorvalue()
  personHere = p[1]<1.0   # front sonar

pepper_cmd.robot.say("Oh ciao!")


pepper_cmd.robot.stopSensorMonitor()

end()