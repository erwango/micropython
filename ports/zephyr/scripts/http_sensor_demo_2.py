import usocket as socket
import time
import hts221

DWEET_IO_IPV4_ADDR="34.231.80.209"

POST_MSG_PREFIX = "POST /dweet/for/nucleo_f429zi?Temp="
POST_MSG_POSTFIX = "\r\nConnection: keep-alive\r\n\r\n"

addr = (DWEET_IO_IPV4_ADDR, 80)

s = socket.socket()
print("\nSocket:" + str(s))

# Connect to dweet.io
try:
    s.connect(addr)
    print("connect ok\n")
except:
    print("connect error\n")

try:
    while True:
        temp = hts221.read_temp()

        temp_str = ("%.1f" % temp)
        post_msg = POST_MSG_PREFIX + temp_str + POST_MSG_POSTFIX
        post_bytes = bytes(post_msg,"utf-8")
        print("\nSending...\n" + post_msg)

        s.send(post_bytes)

        time.sleep(5)

        print("Response...")
        print(s.recv(4096))

except:
    s.close()
