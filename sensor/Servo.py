import RPi.GPIO as GPIO
import time

pin =18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p= GPIO.PWM(pin, 50)  #PMW:펄스 폭 변조
p.start(0)
cnt = 0

try:

    while True:
        a = float(input('Humidity: '))

        if a > 50:
            p.ChangeDutyCycle(12.5)
            time.sleep(1)
        else if a < 40:
            p.ChangeDutyCYcle(7.5)
            time.sleep(1)

        """p.ChangeDutyCycle(12.5) #최댓값
        time.sleep(1)
        p.ChangeDutyCycle(10.0)
        time.sleep(1)
        p.ChangeDutyCycle(7.5) #0
        time.sleep(1)
        p.ChangeDutyCycle(5.0)
        time.sleep(1)
        p.ChangeDutyCycle(2.5) #최솟값
        time.sleep(1)"""

except KeybordInterrupt:
     p.stop()
    
GPIO.cleanup()
