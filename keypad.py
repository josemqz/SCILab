import RPi.GPIO as GPIO
import time

# these GPIO pins are connected to the keypad
# change these according to your connections!
L1 = 25
L2 = 8
L3 = 7
L4 = 1

C1 = 12
C2 = 16
C3 = 20
C4 = 21

# Initialize the GPIO pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Make sure to configure the input pins to use the internal pull-down resistors

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# The readLine function implements the procedure discussed in the article
# It sends out a single pulse to one of the rows of the keypad
# and then checks each column for changes
# If it detects a change, the user pressed the button that connects the given line
# to the detected column

def readLine(line, characters):
	GPIO.output(line, GPIO.HIGH)
	if(GPIO.input(C1) == 1):
		print(characters[0])
		return(characters[0])
	if(GPIO.input(C2) == 1):
		print(characters[1])
		return(characters[1])
	if(GPIO.input(C3) == 1):
		print(characters[2])
		return(characters[2])
	if(GPIO.input(C4) == 1):
		print(characters[3])
		return(characters[3])
	GPIO.output(line, GPIO.LOW)
	return("")


# EDIT: evitar que al mantener presionada una tecla 
# se seleccione la primera de la columna
def numpad_code():
	code = []
	while True:
		# call the readLine function for each row of the keypad
		ch1 = readLine(L1, ["1","2","3","A"])
		ch2 = readLine(L2, ["4","5","6","B"])
		ch3 = readLine(L3, ["7","8","9","C"])
		ch4 = readLine(L4, ["*","0","#","D"])

		for i in [ch1,ch2,ch3,ch4]:
			if i == "*":
				print("code:", code)
				return code

			elif i != "":
				print("i:", i)
				code.append(i)
				break

		time.sleep(0.1)

#except KeyboardInterrupt:
#	print("\nApplication stopped!")
