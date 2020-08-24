import RPi.GPIO as GPIO
import time
#servo motor
import sys
import Adafruit_DHT
#webSocket
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
#humidity
import math
curHum=0
successcnt = 0
class SimpleEcho(WebSocket):
    def handleMessage(self):
        requestString = json.dumps(self.data)
        print(requestString)
        type_=0
        # responseString = '{"state":"connected", "type":"0", "message":""}'
        #connect sensor
        led_R=20
        led_Y=21
        PIR_sensor=17
        servomotor_pin =18
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(led_R, GPIO.OUT)
        GPIO.setup(led_Y, GPIO.OUT)
        GPIO.setup(PIR_sensor, GPIO.IN)
        GPIO.setup(servomotor_pin, GPIO.OUT)
        print("PIR Ready..")
        # time.sleep(2)
        #PMW: change pulse
        p= GPIO.PWM(servomotor_pin, 50)
        sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
        if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
            sensor = sensor_args[sys.argv[1]]
            pin = sys.argv[2]
        else:
            #ERROR occurs HERE!!!
            print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
            print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
            sys.exit(1)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        flag=0
        p.start(0)
        p.ChangeDutyCycle(2.5) #0
        print("servo, humidity Ready..")
        is_break = 0
        type_=0
        successcnt_dt=0
        successcnt_ndt=0
        try:
            while True:
                ##PIR sensor
                #DETECTED
                if GPIO.input(PIR_sensor) == 1:
                    GPIO.output(led_Y, 1)
                    GPIO.output(led_R, 0)
                    # is_break=1
                    # print("type 1",successcnt)
                    type_=1
                    successcnt_dt = successcnt_dt+1
                    print("detected!",successcnt_dt)
                    time.sleep(1)
                    # responseString = '{"state":"connected", "type":'+''str(type_)+ "message":"'+str(successcnt)+'"}'
                    if successcnt_dt>20:
                        successcnt_dt=0
                        break
                    else:
                        continue
                #NOT DETECTED
                else:
                    successcnt_dt=0
                    GPIO.output(led_R, 1)
                    GPIO.output(led_Y, 0)
                    print("not detected !")
                    #survo motor
                    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                    if humidity is not None and temperature is not None:
                        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                        humidity = math.floor(humidity)
                        print(humidity)
                        if humidity>70:
                        # if flag==0:
                            type_=2
                            # flag=1
                            p.ChangeDutyCycle(7.5) #90
                            time.sleep(1)
                            p.ChangeDutyCycle(5.0)
                            while humidity>70:
                                humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                                time.sleep(1)
                            p.ChangeDutyCycle(2.5) #0
                            # time.sleep(1)
                            print("///////////////////STOP HERE/////////////")
                            time.sleep(5)
                            # print("is_break:",is_break,"flag:",flag)
                            # if is_break!=1:
                            #     is_break=1
                                # print("type 2")
                            # type_=2
                            break
                                # responseString = '{"state":"connected", "type":"2", "message":""}'
                        else:
                        # if flag == 1:
                            p.ChangeDutyCycle(7.5) #0
                            # flag=0
                    # time.sleep(1)
                    else:
                        print('Failed to get reading. Try again!')
                        sys.exit(1)
                # if is_break==1:
                #     is_break=0
                #     break
                # if successcnt < 1000:
                #     successcnt += 1
        except KeyboardInterrupt:
            print("Stopped by User")
            p.stop()
            GPIO.cleanup()
            type_=-1
            # responseString = '{"state":"disconnected", "type":"-1", "message":""}'
            responseString = '{"state":"connected", "type":'+str(type_)+ '"message":'+str(successcnt)+'}'
            self.sendMessage(responseString)
        print("I will send msg & initialize variable~")
        successcnt_dt=0
        responseString = '{"state":"connected", "type":'+str(type_)+ '"message":'+str(successcnt)+'}'
        print(responseString)
        self.sendMessage(responseString)
    def handleConnected(self):
        print(self.address, 'open')
    def handleClose(self):
        print(self.address, 'closed')
server = SimpleWebSocketServer('',9999, SimpleEcho)
server.serveforever()