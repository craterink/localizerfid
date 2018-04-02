print('test')












#import serial
#import time
ser = serial.Serial()
ser.baudrate = 57600
ser.port = 'COM8'
ser.xonxoff=1;
print(ser)
ser.open()
data='Idn\r'.encode('utf-8')
print(data)
ser.write(data)
time.sleep(0.01)
i=ser.in_waiting
print(i)
out = ser.read(i)
print(out)
time.sleep(1)
