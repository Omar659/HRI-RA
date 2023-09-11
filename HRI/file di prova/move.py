import os, sys

sys.path.append(os.getenv('PEPPER_TOOLS_HOME')+'/cmd_server')

import pepper_cmd
from pepper_cmd import *

begin()

# Motion
d = 1
a = 45
vx = 1
vy = 1
vth = 1
tm = 2
# Position control
pepper_cmd.robot.forward(d)   # [m] blocking
pepper_cmd.robot.backward(d)  # [m] blocking
pepper_cmd.robot.turn(a)      # [deg] blocking

# Speed control
pepper_cmd.robot.setSpeed(vx,vy,vth,tm,stopOnEnd=True)   # blocking
# vx: x vel [m/s], vy: y vel [m/s], vth: th vel [rad/s], tm: time [s]
# stopOnEnd: if stop after tm time

pepper_cmd.robot.asay("Hello bro")

end()