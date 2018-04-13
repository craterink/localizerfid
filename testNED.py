#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
import flight_algo_lib as fal
from pymavlink import mavutil


vehicle = connect('/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00', wait_ready=True)
vehicle.channels.overrides = {'5':None, '6':None,'3':0}
fal.arm_and_takeoff(vehicle, 10)
print("Set default/target airspeed to 10")
vehicle.airspeed = 10

#TASK 1: test goto_NED with treshold detection
print "Testing goto_position_target_local_ned\n"
print "North 5, East 5, Up 5"
fal.goto_position_target_local_ned(vehicle,5,5,-5)
print "South 5, West 5, Down 5"
fal.goto_position_target_local_ned(vehicle,-5,-5,5)

# TASK FOUR: test RTL
print("TASK 4: Returning to Launch")
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
#print("\nClose vehicle object")
vehicle.close()
