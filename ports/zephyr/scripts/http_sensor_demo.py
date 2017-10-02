import usocket as socket
import time
import tmp006

DWEET_IO_IPV4_ADDR="34.229.35.198"

POST_MSG_PREFIX = "POST /dweet/for/cc32xx?Temp="
POST_MSG_POSTFIX = "\r\nConnection: keep-alive\r\n\r\n"

addr = (DWEET_IO_IPV4_ADDR, 80)

s = socket.socket()

# Connect to dweet.io
s.connect(addr)

try:
    while True:
        temp = tmp006.read_temp()

        temp_str = ("%0.2f" % temp)
        post_msg = POST_MSG_PREFIX + temp_str + POST_MSG_POSTFIX
        post_bytes = bytes(post_msg,"utf-8")
        print("\nSending...\n" + post_msg)

        s.send(post_bytes)

        time.sleep(5)

        print("Response...")
        print(s.recv(4096))

except:
    s.close()

