import time
from machine import Pin
LED = Pin(("GPIO_A1", 3), Pin.OUT)
LED.value(1)
LED.value(0)
while True:
	LED.value(1)
	time.sleep(0.5)
	LED.value(0)
	time.sleep(0.5)
