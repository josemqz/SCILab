import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

RELAIS_1_GPIO = 17
GPIO.setwarnings(False)
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
#GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
#GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on 

"""
Método para controlar activación de relay
switch (bool): variable que define activación al pasar a True,
				y viceversa con False.
"""
def open_relay(switch):
	if switch:
		GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
	else:
		GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on

#GPIO.cleanup()
