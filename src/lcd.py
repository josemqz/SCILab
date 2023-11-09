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

from rpi_lcd import LCD

"""
lcd: instancia de LCD()
msg1: mensaje a imprimir en primera fila
msg2: mensaje a imprimir en segunda fila
do_clear: vaciar pantalla antes de imprimir
"""

def lcd_print(lcd, msg1, msg2="", do_clear=True):

    if do_clear:
        lcd.clear() 
    lcd.text(msg1.center(16), 1)
    lcd.text(msg2.center(16), 2)
