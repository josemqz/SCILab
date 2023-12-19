#!/usr/bin/python3

#SCILab
# Sistema de Control de Ingreso FabLab
# 2023

# configurar registro para personas nuevas (Forms o Classroom)

# desactivar interfaz grafica predeterminadamente
# crontab: systemctl stop lightdm ?

# Configuracion lector QR *
# Configuracion sensor NFC (later)

# arreglar funcionamiento boton
# arreglar cableado teclado
# cambiar threading por multiprocessing

# - Parametros -
DEBUG = True
# direccion de server con BD de personas registradas
server_url = "http://127.0.0.1:5000"


# - Modulos -
from src.lcd import *
from src.relay import *
from src.button import *
from src.threads import *

import requests					# HTTP requests
from datetime import datetime	# tiempo
from time import sleep			# tiempo de espera
import pandas as pd				# pandas :)

import tty
import sys
import termios


lcd = LCD()

# manejar interrupciones a programa
def safe_exit(signum, frame):
	lcd.clear()
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
	if DEBUG:
		print("\n\n- - - Sistema detenido. - - -\n")
	exit(1)

from signal import signal, SIGTERM, SIGHUP, SIGINT
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
signal(SIGINT, safe_exit)


# horarios de funcionamiento de laboratorio (legacy)
# hora_min = datetime.strptime("10:55","%H:%M").time()
# hora_max = datetime.strptime("17:00","%H:%M").time()


# - Funciones -

# obtener digito verificador para caso de TUI
def dig_verificador(rut):
	secuencia = [2,3,4,5,6,7,2,3,4]
	df = 0
	rut = rut[::-1]
	for i,r in enumerate(rut):
		df += int(r)*secuencia[i]
	df %= 11
	return str(11-df)


# - HTTP requests a server con datos de usuarios -
def get_persona(rut):
	data = pd.read_csv("ruts.csv")
	
	#if DEBUG:
		#print(response[response['Rut']==rut])
	
	persona = data[data['Rut'] == rut].to_dict(orient='records')
	#response = requests.get(url=server_url+"/get_persona", 
	#						params={'rut':rut})

	# esta parte del codigo depende de la implementacion del server del fablab
	# puede variar el valor de retorno en caso de no encontrar a nadie
	#json.loads(response.decode('utf-8'))
	#persona = response.json()
	if DEBUG:
		print("[get_persona] persona:", persona)
	return persona

# post ingreso a BD
def add_ingreso(id):
	# lo mismo, depende del funcionamiento del server cuando haya que obtener el tiempo
	#tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#print(tiempo)
	response = requests.post(url=server_url+"/add_ingreso", 
							params={'id':id})

	"""
	if response == "200":
		print("Ingreso añadido.")
	else:
		print("Fallo al añadir Ingreso en BD.")
	"""

# acciones al verificar identidad
# autorizacion: bool, indica si se debe permitir el ingreso
# do_lcd_print: indica si debe imprimir en lcd estado de ingreso
def ingreso(autorizacion, do_lcd_print=True):
	
	if autorizacion:
		
		# senial a relay
		if DEBUG:
			print("Relay activado.")
		open_relay(True)
		
		if do_lcd_print:
			lcd_print(lcd, "Ingreso", "- autorizado -")
		if DEBUG:
			print("Ingreso autorizado.")	

		sleep(5)
		open_relay(False)
		if do_lcd_print:
			lcd.clear()
		
	else:
		
		open_relay(False)
		if do_lcd_print:
			lcd_print(lcd, "Ingreso", "- denegado -")
		if DEBUG:
			print("Ingreso denegado.")
			# deberia solo mantenerse activado el bloqueo
			print("Relay desactivado.")

		sleep(3)
		
		if do_lcd_print:
			lcd.clear()


# - Input QR y numpad

# configuracion original de input
orig_settings=termios.tcgetattr(sys.stdin)

# funcion de thread de lector qr y numpad
def ingreso_cod(lock):

	# identificar teclas presionadas
	# source: stackoverflow.com/questions/34497323/what-is-the-easiest-way-to-detect-key-presses-in-python-3-on-a-linux-machine
	tty.setcbreak(sys.stdin.fileno()) # tty en raw mode
	key_input = ""				# codigo a almacenar
	x = 0						# input recibido
	is_code = True				# es un codigo si len < 8
	
	# lectura de input
	x = ord(sys.stdin.read(1))
	
	# ord convierte a ASCII
	while x != ord('\n'):
		
		# boton de borrado (127 es backspace en ASCII)
		if x == 127:
			if DEBUG:
				print("char borrado")
			if len(key_input) > 1:
				key_input = key_input[:-1]
			elif len(key_input) == 0 or len(key_input) == 1:
				key_input = ""
			continue

		else:
			if DEBUG:
				print("pressed", chr(x))
			key_input += chr(x) # chr convierte ASCII a caracter
			
		# si son <8 caracteres, es un codigo de ingreso
		if len(key_input) > 8:
			is_code = False
			
			# TODO: resolver problema de velocidad de impresion en lcd
			# ya que imprime los caracteres del codigo demasiado lento
			#lcd_print(lcd, len(key_input) * "*")
		
		# en caso que se borren caracteres hasta llegar a <8
		else:
			is_code = True
		
		# lectura de input
		x = ord(sys.stdin.read(1))

	# retornar configuracion de input a original
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
	key_input = key_input[:-1]
	if DEBUG:
		print("input:",key_input)

	
	"""
	# BEGIN TEST v v v
	if l%8== 0:
		qr = "87004123457524654"
	elif l%10 == 0:
		qr = "https://gob.cl/q?RUN=7524654-K&type=CEDULA&serial=123456"
	elif l%4 == 0:
		qr ="https://gob.cl/q?RUN=19948797-3&type=CEDULA&serial=123456"
	elif l%5 == 0:
		qr = "87004123459773126"
	else:
		qr=""
	# END TEST
	"""
	
	# bloquear thread si hay input
	len_input = len(key_input)
	if len_input > 0:
		with lock:
			
			# flag global para indicar bloqueo
			global runningCod
			runningCod = True
			
			# verificar codigo de numpad
			if is_code:
				if key_input == "1780":
					if DEBUG:
						print("Contraseña correcta")
					ingreso(1)
					
				else:
					if DEBUG:
						print("Contraseña incorrecta")
					ingreso(0)

			# verificar codigo QR
			else:
						
				# Verificacion tipo de tarjeta

				# TUI: 87004 (codigo 5 digitos) (RUT sin digito verificador)
				# RUT: https://portal.sidivregistrocivil.cl/docstatus&RUN=(RUT)&type=CEDULA&...
				cod_card = key_input[:5]
				
				# TUI
				if cod_card == "87004":
					
					lcd_print(lcd, "Verificando", "TUI...")
					# num_tui = key_input[5:10]
					rut = key_input[10:]
					
					# obtener digito verificador
					rut += "-"+dig_verificador(rut)
					if DEBUG:
						print("rut:", rut)
					
					sleep(1)

				# CI
				elif cod_card == "https":
					
					lcd_print(lcd, "Verificando", "CI...")
					rut = key_input.split('RUN=')[1].split('&')[0]
					if DEBUG:
						print("rut:", rut)

					sleep(1)

				# Tarjeta sin formato valido
				else:
					
					#lcd_print(lcd, "Tarjeta", "invalida.")
					ingreso(0)
					if DEBUG:
						print("Tarjeta invalida.\n")
					sleep(3)
					
					runningCod = False
					return

				# HTTP GET request
				try:
					persona = get_persona(rut)
				except:
					if DEBUG:
						print("Error de conexion a servidor")
					
					lcd_print(lcd, "Error de", "conexion")
					runningCod = False
					return

				# modificar segun comportamiento de server real
				#if persona['status'] == 200:
				if len(persona) > 0:
					
					if DEBUG:
						print("Coincidencia de RUT!")
					persona = persona[0]
					ingreso(1)

					# HTTP POST request para registrar visita y hora
					#add_ingreso(persona['Rut'])

				else:
					if DEBUG:
						print("RUT no encontrado.")
					ingreso(0)
				
				if DEBUG:
					print("\n")

			runningCod = False


# - Boton -
# tuve que mover estas variables a main, porque al estar en 
# button.py se generaba una dependencia ciclica

pressedButton = False # variable que indica si boton ha sido presionado

def button_callback(channel):
	global pressedButton
	if DEBUG:
		print("Apertura por boton")
	pressedButton = True

GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback)

# funcion de thread de boton
def ingreso_boton(lock):
	global pressedButton
	while not pressedButton:
		pass
	
	with lock:
		global runningButton
		runningButton = True
		
		# TODO: matar thread de cod
		ingreso(1)# do_lcd_print=False)
		
		runningButton = False
		pressedButton = False

# - Configuración threads -
lock = threading.Lock()

# flag para thread de cada operacion
runningButton = False
runningCod = False

threadButton = threading.Thread(target=ingreso_boton, args=(lock,))
threadCod = threading.Thread(target=ingreso_cod, args=(lock,))

threads = [threadButton, threadCod]

for t in threads:
	t.start()


# print inicial en LCD
lcd_print(lcd, "Bienvenid@ a", "FabLab!", False)


# - LOOP -
#l = 0 # TEST
hora_inicio = datetime.now()
while(1):
	#l+=1 # TEST

	# tiempo total de ejecucion
	t_ejecucion = datetime.now() - hora_inicio
	#if DEBUG:
		#print(datetime.now().time()) # TEST
	
	# refrescar lcd cada 5 minutos (en caso de bugs)
	if int(t_ejecucion.total_seconds()) % 300 == 0:
		#print("sec:", int(t_ejecucion.total_seconds()))
		lcd_print(lcd, "Bienvenid@ a", "FabLab!")
	
	# cambiar comportamiento por horario o codigo en numpad
	# if (hora_act >= hora_min and hora_act <= hora_max):
	
	if not threadCod.is_alive():
		if DEBUG:
			print("creating new instance threadCod")
		if not runningButton:
			lcd_print(lcd, "Bienvenid@ a", "FabLab!")
		threadCod = threading.Thread(target=ingreso_cod, args=(lock,))
		threadCod.start()
	
	if not threadButton.is_alive():
		if DEBUG:
			print("creating new instance threadButton")
		if not runningCod:
			lcd_print(lcd, "Bienvenid@ a", "FabLab!")
		threadButton = threading.Thread(target=ingreso_boton, args=(lock,))
		threadButton.start()
