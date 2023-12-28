import RPi.GPIO as GPIO

# Configuración de botón en RPi
# Métodos utilizados se encuentran en main.py
pin = 5
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#input()
#GPIO.cleanup()
