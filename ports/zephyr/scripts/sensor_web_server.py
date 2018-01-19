import zsensor
try:
    import usocket as socket
except:
    import socket


hts221 = zsensor.Sensor("HTS221")
lis3mdl = zsensor.Sensor("LIS3MDL")

CONTENT = b"""\
HTTP/1.0 200 OK
<HTML>
<HEAD>
<meta http-equiv="refresh" content="5">
<TITLE>Hello #%d from MicroPython!</TITLE>
</HEAD>
<CENTER>
<H2>Welcome to Zephyr/Micropython Sensing Webserver</H2>
</CENTER>
<H2>HTS221 Sensor:</H2>
<P>Temperature: %.1f
<P>Humidity: %.1f
<H2>LIS3MDL Sensor:</H2>
<P>Magn_x: %.3f
<P>Magn_y: %.3f
<P>Magn_z: %.3f
</HTML>
"""

def main():
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]
    print("Address", addr)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:80/")

    counter = 0
    while True:

        res = s.accept()
        client_sock = res[0]

        hts221.measure()
        lis3mdl.measure()

        temp = hts221.get_float(zsensor.TEMP)
        humidity = hts221.get_float(zsensor.HUMIDITY) / 1000
        magn_x =lis3mdl.get_float(zsensor.MAGN_X)
        magn_y =lis3mdl.get_float(zsensor.MAGN_Y)
        magn_z =lis3mdl.get_float(zsensor.MAGN_Z)

        client_sock.write(CONTENT % (counter, temp, humidity,
                                            magn_x, magn_y, magn_z))

        client_sock.close()

        counter += 1
        print()


main()
