import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
servoPin = 11
GPIO.setup(servoPin,GPIO.OUT)
pwm=GPIO.PWM(servoPin,50)
pwm.start(7)
for i in range(0,20):
    input("Move")
    desiredPosition = 0
    DC=1./18.*(desiredPosition)+2
    pwm.ChangeDutyCycle(DC)
    time.sleep(1)
    desiredPosition = 80
    DC=1./18.*(desiredPosition)+2
    pwm.ChangeDutyCycle(DC)
pwm.stop()
GPIO.cleanup()
