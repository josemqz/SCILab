import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressedButton = False

def button_callback(channel):
	global pressedButton
	pressedButton = True

GPIO.add_event_detect(15, GPIO.RISING, callback=button_callback)

#input()

#GPIO.cleanup()
