# fuente: 
# maker.pro/raspberry-pi/tutorial/how-to-use-a-keypad-with-a-raspberry-pi-4

# This program allows a user to enter a Code.
# If the D-Button is pressed on the keypad, the input is reset.
# If the user hits the A-Button, the input is checked.

import RPi.GPIO as GPIO
import time
from src.lcd import *

# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 25
L2 = 8
L3 = 7
L4 = 1

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1

secretCode = "1780"
codigo = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

def checkSpecialKeys():
    global codigo
    pressed = False

    GPIO.output(L4, GPIO.HIGH)

    if (GPIO.input(C4) == 1):
        print("Input reset!");
        pressed = True
        GPIO.output(L4, GPIO.LOW)
        return "D"

    GPIO.output(L4, GPIO.LOW)
    GPIO.output(L1, GPIO.HIGH)

    if (not pressed and GPIO.input(C4) == 1):
        pressed = True
        if codigo == secretCode:
            print("Correct code !")
            return "1"
            
        else:
            print("Incorrect code!")
            return "0"
    
    GPIO.output(L4, GPIO.LOW)

    return ""

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def readLine(line, characters):
    global codigo
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        codigo = codigo + characters[0]
        print(codigo)
    if(GPIO.input(C2) == 1):
        codigo = codigo + characters[1]
        print(codigo)
    if(GPIO.input(C3) == 1):
        codigo = codigo + characters[2]
        print(codigo)
    if(GPIO.input(C4) == 1):
        codigo = codigo + characters[3]
        print(codigo)
    GPIO.output(line, GPIO.LOW)

# lcd: instancia de LCD()
def verificar_keypad(lcd):
    
    global keypadPressed
    global codigo
    specialKey = ""
    while True:
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
        # Otherwise, just read the input
        else:
            specialKey = checkSpecialKeys()
            if specialKey == "":
                readLine(L1, ["1","2","3","A"])
                readLine(L2, ["4","5","6","B"])
                readLine(L3, ["7","8","9","C"])
                readLine(L4, ["*","0","#","D"])
                if len(codigo) > 0:
                    lcd_print(lcd, "*"*len(codigo))
                else:
                    lcd_print(lcd, "Bienvenid@ a", "FabLab!", False)
                time.sleep(0.1)
            else:
                codigo = ""
                if specialKey == "1":
                    return True
                elif specialKey == "0":
                    return False
                # no deberia entrar aqui
                else:
                    time.sleep(0.1)
