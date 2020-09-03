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
#convert
from ast import literal_eval


class SimpleEcho(WebSocket):


    def handleConnected(self):
        print(self.address, 'open')

    def handleMessage(self):
        is_open = 0 #1일때 열려있음
        is_work = 0 #습도,스타일링 둘중 하나라도 일하고 있음 / 스타일링 중/ 습도 조절중
        
        #connect sensord
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
        time.sleep(2)
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
        p.start(0)
        p.ChangeDutyCycle(2.5) #0
        print("servo, humidity Ready..")
        time.sleep(2)
        
        requestObject = json.dumps(self.data)
        # requestString = '{'work':'ticket' || '1'}'
        # responseString = '{"work":"0(cam) || 2(dehumid)", "user":"name"}'

        requestString = literal_eval(requestObject)
        obj = json.loads(requestString)
        print(obj["work"])
        msg = obj["work"]



        #클라이언트 메세지에서 (ticket 혹은 1) is_work[1] on/off 결정(스타일링 여부) 
        if msg == "1":
            print("start sytling")
            is_work=1 #작동중임,,
            time.sleep(10)
            print("styling done")
            is_work=0
            responseString = '{"work":"", "username":""}'

        else : 
            try:
                while True:
                    ##PIR sensor
                    #Human detected && not working
                    if GPIO.input(PIR_sensor) == 1 and is_work==0:
                        GPIO.output(led_Y, 1)
                        GPIO.output(led_R, 0)
                        # type_=1
                        print("detected, count start..")
                        time.sleep(5)
                        print("count done")

                        if GPIO.input(PIR_sensor) == 1:
                            is_work=1
                            # 카메라 켜고 사람 인식 start
                            # send user name
                            responseString = '{"work":"0", "username":"name"}'
                            break
                        else:
                            #적외선 인식작업 재개
                            continue
                            
                    #Human not detected || working (door is opening , styling ...)
                    else:
                        GPIO.output(led_R, 1)
                        GPIO.output(led_Y, 0)
                        print("not detected !")
                        #survo motor
                        if is_work == 0 or is_open == 1:
                            print('door is opened or machine not working')
                            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
                            if humidity is not None and temperature is not None:
                                print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
                                humidity = math.floor(humidity)
                                print(humidity)
                                if humidity>70:
                                    #door is closed but humidity is high-> we should open
                                    if is_open==0:
                                        #open
                                        p.ChangeDutyCycle(7.5) #90
                                        is_open=1
                                        time.sleep(1)
                                        is_work = 1
                                        responseString = '{"work":"2", "username":"open"}'
                                        break
                                #we should close
                                else:
                                    if is_open==1:
                                        p.ChangeDutyCycle(5.0)
                                        is_open = 0
                                        is_work = 0
                                        responseString = '{"work":"2", "username":"close"}'
                                        break
                        else:
                            print("it is  working and it is closed")

            except KeyboardInterrupt:
                print("Stopped by User")
                p.stop()
                GPIO.cleanup()
                # type_=-1
                # responseString = '{"state":"disconnected", "type":"-1", "message":""}'
                # responseString = '{"state":"connected", "type":'+str(type_)+ '"message":'+str(successcnt)+'}'
                self.sendMessage(responseString)
        

        #메시지 내용: 인식한 사람 이름
        print("send message")
        # successcnt_dt=0
        print(responseString)
        self.sendMessage(responseString)
   
    def handleClose(self):
        print(self.address, 'closed')
server = SimpleWebSocketServer('',9999, SimpleEcho)
server.serveforever()
