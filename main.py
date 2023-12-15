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

# como importar automaticamente desde src
#from src.keypad import *
from src.lcd import *
from src.relay import *
from src.button import *
from src.threads import *

# import re
import requests
from datetime import datetime
from time import sleep
import pandas as pd

# manejar interrupciones a programa
def safe_exit(signum, frame):
	lcd.clear()
	print("\n\n- - - Sistema detenido. - - -\n")
	exit(1)

from signal import signal, SIGTERM, SIGHUP, SIGINT
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
signal(SIGINT, safe_exit)

lcd = LCD()

server_url = "http://127.0.0.1:5000"

# horarios de funcionamiento de laboratorio
# hora_min = datetime.strptime("10:55","%H:%M").time()
# hora_max = datetime.strptime("17:00","%H:%M").time()


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
	#print(response[response['Rut']==rut])
	persona = data[data['Rut'] == rut].to_dict(orient='records')
	#response = requests.get(url=server_url+"/get_persona", 
	#						params={'rut':rut})
	# esta parte del codigo depende de la implementacion del server del fablab
	# puede variar el valor de retorno en caso de no encontrar a nadie
	#json.loads(response.decode('utf-8'))
	#persona = response.json()
	print("[get_persona] persona:", persona)
	return persona
#	return persona

# post ingreso a BD
def add_ingreso(id):
	# lo mismo, depende del funcionamiento del server cuando haya que obtener el tiempo
	#tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#print(tiempo)
	response = requests.post(url=server_url+"/add_ingreso", 
							params={'id':id})


# acciones al verificar identidad
# autorizacion: bool, indica si se debe permitir el ingreso
def ingreso(autorizacion, do_lcd_print=True):
	if autorizacion:
		if do_lcd_print:
			lcd_print(lcd, "Acceso", "- autorizado -")
		print("Acceso autorizado.")

		# senial a relay
		print("Relay activado.")
		open_relay(True)

		sleep(5)
		open_relay(False)
		if do_lcd_print:
			lcd.clear()
		
	else:
		if do_lcd_print:
			lcd_print(lcd, "Acceso", "- denegado -")
		print("Acceso denegado.")
		# deberia solo mantenerse activado el bloqueo
		print("Relay desactivado.")
		open_relay(False)

		sleep(3)
		if do_lcd_print:
			lcd.clear()


# funcion de thread de lector qr
def ingreso_qr(lock):
	# check QR
	qr = input()
	
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
	if len(qr) > 0:
		with lock:
			
			# flag global para indicar bloqueo
			global runningQR
			runningQR = True
			
			# verificar codigo de numpad
			if len(qr) == 4:
				if qr == "1780":
					print("Contraseña correcta")
					ingreso(1)
					return
					
				else:
					print("Contraseña incorrecta")
					ingreso(0)
					return
					
			# verificacion tipo de tarjeta
			# TUI: 87004 (codigo 5 digitos) (RUT sin digito verificador)
			# RUT: https://portal.sidivregistrocivil.cl/docstatus&RUN=(RUT)&type=CEDULA&...
			cod_card = qr[:5]
			#print("qr:", qr)
			#print("cod_card:", cod_card)
			
			# TUI
			if cod_card == "87004":
				
				lcd_print(lcd, "Verificando", "TUI...")
				# num_tui = qr[5:10]
				rut = qr[10:]
				
				# obtener digito verificador
				rut += "-"+dig_verificador(rut)
				print("rut:", rut)
				
				sleep(1)

			# CI
			elif cod_card == "https":
				
				lcd_print(lcd, "Verificando", "CI...")
				rut = qr.split('RUN=')[1].split('&')[0]
				print("rut:", rut)
				sleep(1)

			# Tarjeta sin formato valido
			else:
				
				lcd_print(lcd, "Tarjeta", "invalida.")
				print("Tarjeta invalida.\n")
				sleep(3)
				
				runningQR = False
				return
				# continue

			# HTTP GET request
			try:
				persona = get_persona(rut)
			except:
				print("Error de conexion a servidor")

				runningQR = False
				return
				# continue

			# modificar segun comportamiento de server real
			#if persona['status'] == 200:
			if len(persona) > 0:
				
				print("Coincidencia de RUT!")
				persona = persona[0]
				ingreso(1)

				# HTTP POST request para registrar visita y hora
				#add_ingreso(persona['Rut'])

			else:
				print("RUT no encontrado.")
				ingreso(0)
			print("\n")

			runningQR = False


# funcion de thread de keypad
"""
def ingreso_keypad(lock):
	global runningKeypad
	print("\nEsperando codigo en keypad...")
	
	# se realiza ingreso dependiendo del codigo ingresado en keypad
	vk = verificar_keypad(lcd)
	if vk:
		with lock:
			runningKeypad = True
			ingreso(1)
			runningKeypad = False
"""

# funcion de thread de boton
def ingreso_boton(lock):
	global pressedButton
	
	# no funciona un while
	while not pressedButton:
		pass
	
	with lock:
		global runningButton
		runningButton = True
		ingreso(1)  	#, do_lcd_print=False)
		runningButton = False
		pressedButton = False

# - configuración threads -
lock = threading.Lock()

# flag para thread de cada operacion
runningButton = False
#runningKeypad = False
runningQR = False

threadButton = threading.Thread(target=ingreso_boton, args=(lock,))
#threadKeypad = threading.Thread(target=ingreso_keypad, args=(lock,))
threadQR = threading.Thread(target=ingreso_qr, args=(lock,))

threads = [threadButton, threadQR] #, threadKeypad]

for t in threads:
	t.start()

lcd_print(lcd, "Bienvenid@ a", "FabLab!", False)

# loop
#l = 0 # TEST
while(1):
	#l+=1 # TEST

	hora_act = datetime.now().time()
	#print(hora_act) # TEST
	
	
	# cambiar comportamiento por horario o codigo en numpad
	# if (hora_act >= hora_min and hora_act <= hora_max):
	
	# usar qr y teclado al mismo tiempo (y botón)
	
	if not threadQR.is_alive():
		print("creating new instance threadQR")
		lcd_print(lcd, "Bienvenid@ a", "FabLab!")
		threadQR = threading.Thread(target=ingreso_qr, args=(lock,))
		threadQR.start()
	
	"""	
	if not threadKeypad.is_alive():
		print("creating new instance threadKeypad")
		threadKeypad = threading.Thread(target=ingreso_keypad, args=(lock,))
		threadKeypad.start()
	"""

	if not threadButton.is_alive():
		print("creating new instance threadButton")
		lcd_print(lcd, "Bienvenid@ a", "FabLab!")
		threadButton = threading.Thread(target=ingreso_boton, args=(lock,))
		threadButton.start()
