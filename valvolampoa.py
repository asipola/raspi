#!/usr/bin/python
# -*- coding: UTF-8 -*-
import RPi.GPIO as GPIO
import spidev
import time
import picamera

ledipinninumero=21
# A0 = 0, A1 = 1, A2 = 2, A3 =3 
temp_channel = 2
rajalampo = 24
print ("\nKytke liittimeen A%1d\n" % temp_channel)
#time.sleep(1)
spi = spidev.SpiDev()
kamera = picamera.PiCamera()
spi.open(0,0)
spi.max_speed_hz=1000000
def readadc(adcnum):
# read SPI data from MCP3004 chip, 4 possible adc's (0 thru 3)
    if adcnum > 3 or adcnum < 0:
        return -1
    r = spi.xfer2([1,8+adcnum <<4,0])
    adcout = ((r[1] &3) <<8)+r[2]
    return adcout

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledipinninumero, GPIO.OUT)


i = 1
while True:
	value = readadc(temp_channel) 
	volts = (value * 3.3) / 1024
	temperature_C = (volts - 0.5) * 100	
	print("%4.1f Celsiusastetta C" % temperature_C)
	print("-------------------------")
        if temperature_C > rajalampo:
           GPIO.output(ledipinninumero, True)
           print("YLILÄMPÖ HÄLYTYS!!! - Otetaan kuva")
           kamera.capture('kuva%03i.jpg' %i)
           i += 1
           if i > 3:
               i = 1
        else:
           GPIO.output(ledipinninumero, False)
	time.sleep(5)

