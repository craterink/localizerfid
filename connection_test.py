#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
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



def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(10)
print("Set default/target airspeed to 10")
vehicle.airspeed = 10

print("Going towards first point for 5 seconds ...")
point1 = LocationGlobalRelative(30.384754, -97.730244, 10)
vehicle.simple_goto(point1)
time.sleep(5)

print("Going to the second point for 5 seconds ...")
point2 = LocationGlobalRelative(30.384462, -97.730701, 10)
vehicle.simple_goto(point2)



time.sleep(5)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")



#Close vehicle object before exiting script
#print("\nClose vehicle object")
vehicle.close()