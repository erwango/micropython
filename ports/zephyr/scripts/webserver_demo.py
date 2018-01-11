import socket
import machine


#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head> <title>ESP8266 LED ON/OFF</title> </head>
<center><h2>A simple webserver for turning HUZZAH Feather LED's on and off with Micropython</h2></center>
<center><h3>(for noobs to both the ESP8266 and Micropython)</h3></center>
<form>
LED0:
<button name="LED" value="ON0" type="submit">LED ON</button>
<button name="LED" value="OFF0" type="submit">LED OFF</button><br><br>
LED2:
<button name="LED" value="ON2" type="submit">LED ON</button>
<button name="LED" value="OFF2" type="submit">LED OFF</button>
</form>
</html>
"""

#Setup PINS
LED0 = machine.Pin(("GPIOB", 0), machine.Pin.OUT)
LED2 = machine.Pin(("GPIOB", 7), machine.Pin.OUT)

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    request = str(request)
    LEDON0 = request.find('/?LED=ON0')
    LEDOFF0 = request.find('/?LED=OFF0')
    LEDON2 = request.find('/?LED=ON2')
    LEDOFF2 = request.find('/?LED=OFF2')
    if LEDON0 == 6:
        print('TURN LED0 ON')
        LED0.off()
    if LEDOFF0 == 6:
        print('TURN LED0 OFF')
        LED0.on()
    if LEDON2 == 6:
        print('TURN LED2 ON')
        LED2.off()
    if LEDOFF2 == 6:
        print('TURN LED2 OFF')
        LED2.on()
    response = html
    conn.send(response)
    conn.close()
