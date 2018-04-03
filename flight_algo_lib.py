#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative, LocationLocal
from pymavlink import mavutil # Needed for command message definitions
import time
import math


#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Control Copter and send commands in GUIDED mode ')
parser.add_argument('--connect', 
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None

#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def wait_til_ready():
    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

def arm(mode):
    print("Arming motors")
    vehicle.mode = VehicleMode(mode)
    vehicle.armed = True

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

def takeoff(alt):
    print("Taking off!")
    vehicle.simple_takeoff(alt) # Take off to target altitude

    # Wait until the vehicle reaches a safe height
    #  before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=alt*0.95: 
            #Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)

def arm_and_takeoff_guided(alt):
    wait_til_ready()
    arm("GUIDED")
    takeoff(alt)

arm_and_takeoff_guided(5)


def goto_position_target_local_ned(north, east, down):
    """
    Send SET_POSITION_TARGET_LOCAL_NED command to request the vehicle fly to a specified
    location in the North, East, Down frame.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111111000, # type_mask (only positions enabled)
        north, east, down,
        0, 0, 0, # x, y, z velocity in m/s  (not used)
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)
    # send command to vehicle
    vehicle.send_mavlink(msg)


goto_position_target_local_ned(5,5,-5)
goto_position_target_local_ned(5,-5,-5)
goto_position_target_local_ned(-5,-5,-5)
goto_position_target_local_ned(-5,5,-5)
goto_position_target_local_ned(5,5,-5)

