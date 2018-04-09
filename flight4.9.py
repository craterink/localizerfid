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

# TASK ONE: test going to different GPS coordinates and waiting
point1 = LocationGlobalRelative(30.384754, -97.730244, 10)
point2 = LocationGlobalRelative(30.384462, -97.730701, 10)
print("TASK 1: Going towards first GPS waypoint ...")
fal.simple_gotoloc(vehicle, point1,5)
print("TASK 1: Going to the second TASK 1 GPS waypoint ...")
fal.simple_gotoloc(vehicle, point2,5)

# TASK TWO: test going to different NED coordinates and waiting
print("TASK 2: Going 5m N and E...")
fal.goto(vehicle,5,5,None) 
print("TASK 2: Going 5m S and W...")
fal.goto(vehicle,-5,-5,None) 

# TASK THREE: test using velocity to control drone
print("TASK 3: Velocity to N and W 1m/s for 5 seconds")
fal.send_ned_velocity(vehicle, 1, -1, 0, 5)
print("TASK 3: Velocity to S and E 1m/s for 5 seconds")
fal.send_ned_velocity(vehicle, -1, 1, 0, 5)

# TASK FOUR: test RTL
print("TASK 4: Returning to Launch")
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
#print("\nClose vehicle object")
vehicle.close()