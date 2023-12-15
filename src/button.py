import RPi.GPIO as GPIO

pin = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressedButton = False

def button_callback(channel):
	global pressedButton
	pressedButton = True

GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback)

"""
while 1:
	while not pressedButton:
		pass
	
	print("ciclo", end="")
	pressedButton = False
"""

#GPIO.cleanup()
