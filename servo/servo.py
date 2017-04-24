import RPi.GPIO as BCM
import time
GPIO.setmode(GPIO.BCM)
servoPin = 17
GPIO.setup(servoPin,GPIO.OUT)
pwm=GPIO.PWM(servoPin,50)
pwm.start(7)
for i in range(0,20):
    userinput = input("Move")
    if userinput == 1:
        desiredPosition = 0
        DC=1./18.*(desiredPosition)+2
        pwm.ChangeDutyCycle(DC)
        time.sleep(1)
        desiredPosition = 80
        DC=1./18.*(desiredPosition)+2
        pwm.ChangeDutyCycle(DC)
    else:
        continue
pwm.stop()
GPIO.cleanup()
