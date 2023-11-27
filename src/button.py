import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressedButton = False

def button_callback(channel):
	global pressedButton
	pressedButton = True

GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback)

# input()

# GPIO.cleanup()
