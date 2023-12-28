#!/usr/bin/python3

"""
    Program: LCD1602 Demo (lcd-hello.py)
    Author:  M. Heidenreich, (c) 2020

    Description:
    
    This code is provided in support of the following YouTube tutorial:
    https://youtu.be/DHbLBTRpTWM

    THIS SOFTWARE AND LINKED VIDEO TUTORIAL ARE PROVIDED "AS IS" AND THE
    AUTHOR DISCLAIMS ALL WARRANTIES INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
# Nota: Si se preguntan por qué el lcd imprime lento los mensajes 
# es debido a la longitud de los cables sumado al uso del protocolo I2C

from rpi_lcd import LCD

"""
Método para imprimir mensajes personalizados en pantalla LCD
---
lcd (obj): instancia de LCD()
msg1 (String): mensaje a imprimir en primera fila
msg2 (String): mensaje a imprimir en segunda fila
do_clear (bool): vaciar pantalla antes de imprimir
"""
def lcd_print(lcd, msg1, msg2="", do_clear=True):

    if do_clear:
        lcd.clear() 
    lcd.text(msg1.center(16), 1)
    lcd.text(msg2.center(16), 2)
