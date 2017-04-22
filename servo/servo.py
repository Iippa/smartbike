import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
servoPin = 11
GPIO.setup(servoPin,GPIO.OUT)
pwm=GPIO.PWM(servoPin,50)
pwm.start(7)
for i in range(0,20):
    desiredPosition = input("Asento 0-18")
    DC=1./18.*(desiredPosition)+2
    pwm.ChangeDutyCycle(DC)
pwm.stop()
GPIO.cleanup()
