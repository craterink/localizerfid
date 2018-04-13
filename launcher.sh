#!/bin/sh
#launcher/sh
#runs script upon startup

/usr/bin/sudo -u pi /usr/bin/screen -dmS ultra sudo python /home/pi/Documents/localizerfid/ultrasonic/ultra_read.py




cd /home/pi/Documents/localizerfid
sleep 20
/usr/bin/sudo -u pi /usr/bin/screen -dmS mavprox sudo mavproxy.py --master /dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00 --aircraft MyCopter
