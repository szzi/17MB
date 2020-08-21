# humidity > 50% -> open the door
# humidity < 40% -> close the door

#!/usr/bin/python
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

servomotor_pin =18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servomotor_pin, GPIO.OUT)
p= GPIO.PWM(servomotor_pin, 50)  

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
flag=0
p.start(0)
p.ChangeDutyCycle(2.5) #0
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))       
        if humidity>69:
            if flag==0:
                flag=1
                cnt = 0
                p.ChangeDutyCycle(7.5) #90
                time.sleep(1)
                p.ChangeDutyCycle(5.0)
                time.sleep(1)
                p.ChangeDutyCycle(2.5) #0
                time.sleep(1)    
        elif humidity<=69:
            if flag == 1:
                p.ChangeDutyCycle(7.5) #0
            flag=0
        time.sleep(1)     
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)


if KeybordInterrupt:
    p.stop()
    GPIO.cleanup()



