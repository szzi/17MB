#PIR sensor

import RPi.GPIO as GPIO
import time

led_R=20
led_Y=21
sensor=4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_R, GPIO.OUT)
GPIO.setup(led_Y, GPIO.OUT)
GPIO.setup(sensor, GPIO.IN)

print("PIR Ready..")
time.sleep(5)
successcnt = 0
notcnt = 0
try:
    while True:
        print(sensor)
        if GPIO.input(sensor) == 1:
            GPIO.output(led_Y, 1)
            GPIO.output(led_R, 0)
            print("Motion Detected !")
            successcnt += 1
            time.sleep(1)
            
        if GPIO.input(sensor) == 0:
            GPIO.output(led_R, 1)
            GPIO.output(led_Y, 0)  
            print("not detected !")
            time.sleep(1)
            notcnt = 1

        if successcnt == 5: 
            print("start say hello")
            successcnt = 0
        if notcnt == 1:
            notcnt = 0 
            successcnt = 0

except KeyboardInterrupt:
    print("Stopped by User")
    GPIO.cleanup()

