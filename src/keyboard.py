import tty
import sys
import termios

orig_settings=termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
x  = 0
num_chars = 0
while x != "\n":

	if num_chars < 10:
		x = sys.stdin.read(1)[0]
		print("pressed", x)
	else:
		break
	
	num_chars += 1
except KeyboardInterrupt:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
	
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
