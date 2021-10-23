import wiringpi
import time

led_pin = 17
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode( led_pin, 1 )
 
while True:
    wiringpi.digitalWrite( led_pin, 1 )
    time.sleep(0.5)
    wiringpi.digitalWrite( led_pin, 0 )
    time.sleep(0.5)
