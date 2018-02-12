try:
    import usocket as socket
except:
    import socket
import utime
import urandom
import zsensor
import math

from R import R

hts221 = zsensor.Sensor("HTS221")
lis3mdl = zsensor.Sensor("LIS3MDL")
lps25hb = zsensor.Sensor("LPS25HB")
lsm6ds0 = zsensor.Sensor("LSM6DS0")

def resp_header(resp, content_type):
        resp.write("HTTP/1.0 200 OK\r\n")
        resp.write("Content-Type: %s\r\n" % content_type)
        resp.write("\r\n")


def handle(resp, path):
    if path == b"/":
        resp_header(resp, "text/html")
        resp.write(R["static/dashboard.html"])

    elif path.startswith(b"/static/"):
        if path.endswith(b".js"):
            resp_header(resp, "text/html")
        else:
            resp_header(resp, "application/javascript")
        resp.write(R[str(path[1:], "utf-8")])

    elif path == b"/events":
        resp_header(resp, "text/event-stream")

        i=0
        try:
            while True:
                # LIS3MDL
                if ((i % 2) == 0):
                    lis3mdl.measure()
                    magn_x = lis3mdl.get_float(zsensor.MAGN_X)
                    magn_y = lis3mdl.get_float(zsensor.MAGN_Y)
                    magn_z = lis3mdl.get_float(zsensor.MAGN_Z)
                    max_magn = max(math.fabs(magn_x), math.fabs(magn_y), math.fabs(magn_z))
                    resp.write('data: {"widget": "dynamicWidget", "field": "magn_value", "value": "%s"}\n\n' % max_magn)
                if ((i % 10) == 0):
                    resp.write('data: {"widget": "lis3mdl", "field": "magn_x", "value": "%s"}\n\n' % magn_x)
                    resp.write('data: {"widget": "lis3mdl", "field": "magn_y", "value": "%s"}\n\n' % magn_y)
                    resp.write('data: {"widget": "lis3mdl", "field": "magn_z", "value": "%s"}\n\n' % magn_z)

                # HTS221
                if ((i % 5) == 0):
                    hts221.measure()
                    temp = hts221.get_int(zsensor.TEMP)
                    humidity = hts221.get_float(zsensor.HUMIDITY)
                    resp.write('data: {"widget": "dynamicWidget", "field": "temp", "value": "%s"}\n\n' % temp)
                    resp.write('data: {"widget": "dynamicWidget", "field": "humidity", "value": "%s"}\n\n' % humidity)
                if ((i % 10) == 0):
                    resp.write('data: {"widget": "hts221", "field": "temp", "value": "%s"}\n\n' % temp)
                    resp.write('data: {"widget": "hts221", "field": "humidity", "value": "%s"}\n\n' % humidity)

                # LPS25HB
                if ((i % 10) == 0):
                    lps25hb.measure()
                    press = lps25hb.get_float(zsensor.PRESS) * 10
                    temp2 = lps25hb.get_int(zsensor.TEMP)
                    resp.write('data: {"widget": "lps25hb", "field": "press", "value": "%s"}\n\n' % press)
                    resp.write('data: {"widget": "lps25hb", "field": "temp2", "value": "%s"}\n\n' % temp2)

                # LSM6DS0
                lsm6ds0.measure()
                accel_x =lsm6ds0.get_float(zsensor.ACCEL_X)
                accel_y =lsm6ds0.get_float(zsensor.ACCEL_Y)
                accel_z =lsm6ds0.get_float(zsensor.ACCEL_Z)
                gyro_x =lsm6ds0.get_float(zsensor.GYRO_X)
                gyro_y =lsm6ds0.get_float(zsensor.GYRO_Y)
                gyro_z =lsm6ds0.get_float(zsensor.GYRO_Z)
                if ((i % 10) == 0):
                    resp.write('data: {"widget": "lsm6ds0", "field": "accel_x", "value": "%s"}\n\n' % accel_x)
                    resp.write('data: {"widget": "lsm6ds0", "field": "accel_y", "value": "%s"}\n\n' % accel_y)
                    resp.write('data: {"widget": "lsm6ds0", "field": "accel_z", "value": "%s"}\n\n' % accel_z)
                    resp.write('data: {"widget": "lsm6ds0", "field": "gyro_x", "value": "%s"}\n\n' % gyro_x)
                    resp.write('data: {"widget": "lsm6ds0", "field": "gyro_y", "value": "%s"}\n\n' % gyro_y)
                    resp.write('data: {"widget": "lsm6ds0", "field": "gyro_z", "value": "%s"}\n\n' % gyro_z)
                    i = 0
                if accel_x == 0:
                    accel_x = 0.0001
                rad = math.atan(accel_z/accel_x)
                if (accel_x  > 0):
                    angle = math.degrees(rad) - 90
                elif (accel_x  < 0):
                    angle = math.degrees(rad) + 90
                if ( angle < 2 and angle > -2):
                    # Avoid moves when board is stable
                    angle = 0
                resp.write('data: {"widget": "dynamicWidget", "field": "angle", "value": "%s"}\n\n' % angle)

                utime.sleep(0.1)
                i += 1
        except OSError:
            print("Event source connection closed")
            return

    else:
        assert 0, path


def main():
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8080/")

    while True:
        res = s.accept()
        client_sock = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        client_stream = client_sock

        print("Request:")
        req = client_stream.readline()
        method, path, proto = req.split(None, 2)
        print(method, path, proto)
        while True:
            h = client_stream.readline()
            if h == b"" or h == b"\r\n":
                break
            print(h)

        handle(client_stream, path)

        client_stream.close()
        print()


main()
