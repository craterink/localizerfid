import RPi.GPIO as GPIO
import time

import wiringpi2 as wiringpi #for openning the serial port
import math
import signal
import serial



class timeoutError(Exception):
    def __init__(self):
        pass
    

class TimeoutError(Exception):
    def __init__(self, value = "Timed Out"):
        self.value = value
    def __str__(self):
        return repr(self.value)

def timeout(seconds_before_timeout):

    def decorate(f):     
        def handler(signum, frame):

            print "timed out"
            raise timeoutError
        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds_before_timeout)
            try:
                result = f(*args, **kwargs)
            finally:
                signal.signal(signal.SIGALRM, old)
            signal.alarm(0)
            return result
        new_f.func_name = f.func_name
        return new_f
    return decorate

GPIO.setmode(GPIO.BCM) 
TRIG_0 = 23
ECHO_0 = 24
#set mode and define GPIO variables
def init_ultrasonic():
                 
    GPIO.setup(TRIG_0,GPIO.OUT)
    GPIO.setup(ECHO_0,GPIO.IN)
    #setup pins
    GPIO.output(TRIG_0, False)
    print("Settling sensor")
    time.sleep(2)

def time_to_distance(time):
    distance = time * 17150             #distance = speed * time/2, speed = 343 m/s
    distance = round(distance, 2)
    return distance

@timeout(2)
def read_ultrasonic():
    pulse_distances = []
    GPIO.output(TRIG_0, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_0, False)
    while(GPIO.input(ECHO_0) is 0):
        pass
    pulse_start_0 = time.time()
    while(GPIO.input(ECHO_0) is 1):
        pass
    pulse_end_0 = time.time()
    return time_to_distance(pulse_end_0-pulse_start_0)


init_ultrasonic()
ser = serial.Serial(
          
   port='/dev/ttyAMA0',
   baudrate = 115200,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   #timeout=1

)

def convToHundredthsOfInches(val):
    val = val*(10000.0/254.0)
    rng = math.trunc(val)
    return rng
    

def convToSendStr(rng):
    rng_str = str(rng)
    if len(rng_str) == 1:
        rng_str = '00' + rng_str
    if len(rng_str) == 2:
        rng_str = '0' + rng_stri
    send = ('R%s%s') % (rng_str,chr(13))
    return send

HIMAX_INTERPRET = 25800
testVal = 0
while(1):
    cmVal = read_ultrasonic()
    hiVal = convToHundredthsOfInches(cmVal)
    if(hiVal > HIMAX_INTERPRET):
        # clip signal
        hiVal = HIMAX_INTERPRET
    sendStr = convToSendStr(hiVal)
    print sendStr
    ser.write(sendStr)

