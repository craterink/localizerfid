#!/usr/bin/env python`

import time
import pigpio

I2C_ADDR=112

def i2c(id, tick):
    global pi

    s, b, d = pi.bsc_i2c(I2C_ADDR)
    if b:
        if d[0] == 224: # 116 send 'HH:MM:SS*'
            print 'rr'
        elif d[0] == 225: # 100 send 'Sun Oct 30*'
            print 'lrv'
        elif d[0] == 81: # 100 send 'Sun Oct 30*'
            print '81'
        else:
            print str(d[0])

pi = pigpio.pi()

if not pi.connected:
    exit()

# Respond to BSC slave activity

e = pi.event_callback(pigpio.EVENT_BSC, i2c)

pi.bsc_i2c(I2C_ADDR) # Configure BSC as I2C slave

time.sleep(600)

e.cancel()

pi.bsc_i2c(0) # Disable BSC peripheral

pi.stop()
