'''
This class is used to interface with a single Magnetometer
on I2c pins 3 and 5 on the RPi3.
To use this class, instantiate and instance of the class (with no parameters).
Call read_mag() to get new readings or get_last_readings() to see most recent.
'''
import smbus as smbus
import RPi.GPIO as GPIO

class Magnetometer(object):

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(0x0E, 0x10, 0x01)
        self.last_read = (0,0,0)
        self.last_five = []

    def __add_last_five(self, reading):
        ''' Helper function
            (Private)
        '''
        self.last_five.append(reading)
        if len(self.last_five) > 5:
            self.last_five.pop(0)
            

    def read_mag(self):
        try:
            data = self.bus.read_i2c_block_data(0x0E, 0x01, 6)
        except:
            data = [0,0,0,0,0,0]

        xMag = data[0] * 256 + data[1]
        if xMag > 32767 :
            xMag -= 65536

        yMag = data[2] * 256 + data[3]
        if yMag > 32767 :
            yMag -= 65536

        zMag = data[4] * 256 + data[5]
        if zMag > 32767 :
            zMag -= 65536

        self.last_read = (xMag, yMag, zMag)
        self.__add_last_five((xMag, yMag, zMag))
        return self.last_read

    def get_last_reading(self):
        return self.last_read

    def get_aggregate(self):
        ret_val = (0,0,0)
        x_avg = 0
        y_avg = 0
        z_avg = 0
        for reading in self.last_five:
            x_avg += reading[0]
            y_avg += reading[1]
            z_avg += reading[2]

        num_readings = len(self.last_five)
        if len(self.last_five) > 0:
            x_avg /= num_readings
            y_avg /= num_readings
            z_avg /= num_readings
            ret_val = (x_avg, y_avg, z_avg)
        else:
            ret_val = (0,0,0)

        return ret_val

'''
myMag = Magnetometer()
reading = myMag.read_mag()
print reading
'''


        
