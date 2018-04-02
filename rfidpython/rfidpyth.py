import serial
import time
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM8'
print(ser)
ser.open()
print(ser)

data='Iso15 43211570C0 crc'#.encode('utf-8')
print(data)
ser.write(data)
time.sleep(.5)
i=ser.in_waiting
print(i)
out = ser.read(i)
print(out)
time.sleep(1)
