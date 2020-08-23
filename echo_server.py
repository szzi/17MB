#PIR sensor

import RPi.GPIO as GPIO
import time

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json


socketList = dict()
is_open=0

class SimpleEcho(WebSocket):

    def handleMessage(self):
        requestString = json.dumps(self.data)
        responseString = '{"state":"connected", "type":"1", "message":""}'

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
                    break

                if notcnt == 1:
                    notcnt = 0
                    successcnt = 0
                
                
        except KeyboardInterrupt:
            print("Stopped by User")
            GPIO.cleanup()
            responseString = '{"state":"disconnected", "user" : "true"}'
            self.sendMessage(responseString)
        
        self.sendMessage(responseString)
        print("sent message")

    def handleConnected(self):
        is_open=1
        print(self.address, 'connected')

    def handleClose(self):
        is_open=0
        print(self.address, 'closed')

server = SimpleWebSocketServer('',9999, SimpleEcho)
while True:
    server.serveforever()
    if is_open==0:
        break
