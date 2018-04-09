#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
import flight_algo_lib
from pymavlink import mavutil


# Connect to the Vehicle
#print('Connecting to vehicle on: %s' % connection_string)

vehicle = connect('/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00', wait_ready=True)
vehicle.channels.overrides = {'5':None, '6':None,'3':0}
#print "Armed: %s" % vehicle.armed

##vehicle.armed = True

# Get all original channel values (before override)
##print("Channel values from RC Tx:", vehicle.channels)

##time.sleep(1)

##vehicle.channels.overrides = {'5':None, '6':None,'3':1500}
#print " Ch3: %s" % vehicle.channels['3']
##time.sleep(3)

#print("Clear all overrides")
##vehicle.channels.overrides = {}
##vehicle.channels.overrides = {'5':None, '6':None,'3':0}
#print(" Channel overrides: %s" % vehicle.channels.overrides) 


arm_and_takeoff(vehicle, 10)
print("Set default/target airspeed to 10")
vehicle.airspeed = 10

print("Going towards first point for 5 seconds ...")
point1 = LocationGlobalRelative(30.384754, -97.730244, 10)
vehicle.goto(vehicle, point1)

print("Going to the second point for 5 seconds ...")
point2 = LocationGlobalRelative(30.384462, -97.730701, 10)
vehicle.goto(vehicle, point2)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
#print("\nClose vehicle object")
vehicle.close()
