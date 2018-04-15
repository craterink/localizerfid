#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
import flight_algo_lib as fal
from pymavlink import mavutil


vehicle = connect('/dev/serial/by-id/usb-3D_Robotics_PX4_FMU_v2.x_0-if00', wait_ready=True)

fal.arm_and_takeoff(vehicle, 1)
time.sleep(60)
print('STARTING FIRST RTL')
vehicle.mode = VehicleMode("RTL")
time.sleep(20)
print('STARTING SECOND TAKEOFF')
fal.arm_and_takeoff(vehicle, 1)
vehicle.mode = VehicleMode("RTL")
time.sleep(20)
fal.arm_and_takeoff(vehicle, 3)
vehicle.mode = VehicleMode("RTL")
time.sleep(20)
fal.arm_and_takeoff(vehicle, 5)
print("Set default/target airspeed to 10")
vehicle.airspeed = 10

# RTL
print("TASK 4: Returning to Launch")
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
#print("\nClose vehicle object")
vehicle.close()
