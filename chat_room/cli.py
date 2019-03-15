#-*- encoding: utf-8 -*-
import sys
import time
import socket
import select

try:
    ser, port = sys.argv[1], int(sys.argv[2])
except Exception as ex:
    ser, port = "0.0.0.0", 8015

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((ser, port))

fds = [sys.stdin, c]

BUFF_SIZE = 1024

def gen_prompt():
    sys.stdout.write('You say: ')
    sys.stdout.flush()

def clear_prompt():
    sys.stdout.write('\r'*100)
    sys.stdout.flush()

def event_loop():
    while True:
        gen_prompt()
        r_list, _, _ = select.select(fds, [], [])
        for r in r_list:
            if r == sys.stdin:
                line = sys.stdin.readline().strip()
                if len(line) == 0:
                    continue
                c.send(line)
            else:
                clear_prompt()
                data = r.recv(BUFF_SIZE)
                if len(data) == 0:
                    print("服务器关闭了聊天，聊天结束")
                    r.close()
                    sys.exit(0)
                print(data)

if __name__ == '__main__':
    event_loop()
