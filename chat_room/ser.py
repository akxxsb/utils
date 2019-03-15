# -*- coding: utf-8 -*-
import sys
import socket
import select

try:
    ser, port = sys.argv[1], int(sys.argv[2])
except Exception as ex:
    ser, port = "0.0.0.0", 8015

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ser, port))

s.listen(5)
print("listen on {}".format((ser, port)))

fds = [s, sys.stdin]
BUFF_SIZE = 1024
name_map = {}
num = 1

def get_name(c):
    global name_map
    global num
    if c in name_map:
        return name_map[c]
    name_map[c] = "client [{}]".format(num)
    num += 1
    return name_map[c]

def send_board_cast(fds, no_send_list, msg):
    for fd in (fd for fd in fds if fd not in no_send_list):
        fd.send(msg)

def add_prefix_suffix(msg):
    prefix = "=" * 40
    suffix = "=" * 40
    msg = "{} {} {}".format(prefix, msg, suffix)
    return msg

def show_user_msg():
    msg = "当前用户数:%s" % (len(fds)-2)
    msg = add_prefix_suffix(msg)
    print(msg)

def event_loop():
    show_user_msg()
    while True:
        r_list, _, _ = select.select(fds, [], [])
        for r in r_list:
            if r == sys.stdin:
                line = sys.stdin.readline().strip()
                if len(line) == 0:
                    continue
                data = "[System message]: {}".format(line)
                send_board_cast(fds, [s, sys.stdin], data)
            elif r == s:
                c, addr = s.accept()
                name = get_name(c)
                fds.append(c)
                data = "[System message]: {} 加入了聊天".format(name)
                print(data)
                show_user_msg()
                send_board_cast(fds, [s, sys.stdin, c], data)
            else:
                data = r.recv(BUFF_SIZE)
                name = get_name(r)
                if len(data) == 0:
                    fds.remove(r)
                    r.close()
                    data = "[System message]: {} 离开了聊天".format(name)
                    print(data)
                    show_user_msg()
                    send_board_cast(fds, [s, sys.stdin, r], data)
                    continue

                data = "{} say: {}".format(name, data)
                print(data)
                send_board_cast(fds, [s, sys.stdin, r], data)

if __name__ == '__main__':
    event_loop()
