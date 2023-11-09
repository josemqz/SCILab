#!/usr/bin/python3

#SCILab
# Sistema de Control de Ingreso FabLab
# 2023

# configurar registro para personas nuevas (Forms o Classroom)

# desactivar interfaz grafica predeterminadamente

# Configuracion lector QR *
# Configuracion sensor NFC (later)

# como importar automaticamente desde src
from src.keypad import *
from src.lcd import *
from src.relay import *

import re
import requests
from datetime import datetime
from time import sleep

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

# HTTP requests a server con datos de usuarios
def get_persona(rut):
	response = requests.get(url=server_url+"/get_persona", 
							params={'rut':rut})
	# esta parte del codigo depende de la implementacion del server del fablab
	# puede variar el valor de retorno en caso de no encontrar a nadie
	#json.loads(response.decode('utf-8'))
	persona = response.json()

	print("[get_persona] persona:", persona)
	return persona

def add_ingreso(id):
	# lo mismo, depende del funcionamiento del server cuando haya que obtener el tiempo
	#tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	#print(tiempo)
	response = requests.post(url=server_url+"/add_ingreso", 
							params={'id':id})


# acciones al verificar identidad
def ingreso(autorizacion):
	if autorizacion:
		lcd_print(lcd, "Acceso", "- autorizado -")
		print("Acceso autorizado.")

		# senial a relay
		print("Relay activado.")
		open_relay(True)

		sleep(5)
		open_relay(False)
		lcd.clear()
		
	else:
		lcd_print(lcd, "Acceso", "- denegado -")
		print("Acceso denegado.")
		

		# deberia solo mantenerse activado el bloqueo
		print("Relay desactivado.")
		open_relay(False)

		sleep(3)
		lcd.clear()


# obtener digito verificador para caso de TUI
def dig_verificador(rut):
	secuencia = [2,3,4,5,6,7,2,3,4]
	df = 0
	rut = rut[::-1]
	for i,r in enumerate(rut):
		df += int(r)*secuencia[i]
	df %= 11
	return str(11-df)


# horarios de funcionamiento de laboratorio
hora_min = datetime.strptime("10:55","%H:%M").time()
hora_max = datetime.strptime("17:00","%H:%M").time()

# loop
#l = 0 # TEST
while(1):
	#l+=1 # TEST
	
	hora_act = datetime.now().time()
	print(hora_act) # TEST
	
	lcd_print(lcd, "Bienvenid@ a", "FabLab!", False)
	
	# cambiar comportamiento por horario o codigo en numpad
	if (hora_act >= hora_min and hora_act <= hora_max):
		
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
		
		if len(qr) > 0:

			# verificacion tipo de tarjeta
			# TUI: 87004 (codigo 5 digitos) (RUT sin digito verificador)
			# RUT: https://portal.sidivregistrocivil.cl/docstatus&RUN=(RUT)&type=CEDULA&...
			cod_card = qr[:5]
			#print("qr:", qr)
			#print("cod_card:", cod_card)
			
			# TUI
			if cod_card == "87004":
				
				lcd_print(lcd, "Verificando", "TUI...")
				num_tui = qr[5:10]
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
				continue


			# HTTP GET request
			try:
				persona = get_persona(rut)
			except:
				print("Error de conexion a servidor")
				continue

			# modificar segun comportamiento de server real
			if persona['status'] == 200:
				
				print("Coincidencia de RUT!")
				ingreso(1)

				# HTTP POST request para registrar visita y hora
				add_ingreso(persona['id'])

			else:
				print("RUT no encontrado.")
				ingreso(0)
			print("\n")


	# funcionamiento por keypad (fuera de horario de funcionamiento de FabLab) 
	else:
		print("\nEsperando codigo en keypad...")
		
		# se realiza ingreso dependiendo del codigo ingresado en keypad
		ingreso(verificar_keypad(lcd))
