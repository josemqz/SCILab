import tty
import sys
import termios

orig_settings=termios.tcgetattr(sys.stdin)
# tty.setcbreak(sys.stdin)
tty.setcbreak(sys.stdin.fileno())
x  = 0
cod = ""
try:
	while x != ord('\n'):

		x = ord(sys.stdin.read(1))
		if x == 127:
			print("del")
			if len(cod) > 1:
				cod = cod[:-1]
			elif len(cod) == 1:
				cod = ""
		else:
			cod += chr(x)
	
		if len(cod) < 10:
			print("pressed", chr(x))
		else:
			break
	print(repr(cod))
except KeyboardInterrupt:
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
	print(repr(cod))
	
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
