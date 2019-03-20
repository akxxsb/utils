# -*- coding: utf-8 -*-
import sys
import argparse
import socket

def scan_port(ser=None, begin=None, end=None, timeout=None, verbose=True):
    ser = ser or 'localhost'
    begin = begin or 0
    end = end or 65536
    timeout = timeout or 0.1

    rv = []
    c = socket.socket()
    begin = max(begin, 1)
    end = min(end, 65536)
    for port in range(begin, end):
        if verbose:
            msg = "\rchecking on (%15s, %5s), avaliable port: %4d  " % (ser, port, len(rv))
            sys.stderr.write(msg)
        c.__init__()
        c.settimeout(timeout)
        ret = c.connect_ex((ser, port))
        if ret == 0:
            rv.append((ser, port))
        c.close()

    return rv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="qsc 自制端口扫描工具")
    parser.add_argument("--host", dest="host", type=str, help="host, eg: localhost, www.baidu.com, 127.0.0.1")
    parser.add_argument("--begin", '-b', dest="begin", type=int, help="扫描端口的起始端口")
    parser.add_argument("--end", '-e', dest="end", type=int, help="扫描端口的结束端口")
    parser.add_argument("--timeout", '-t', dest="timeout", type=float, help="连接超时时间")

    args = parser.parse_args()
    print(args)
    rv = scan_port(args.host, args.begin, args.end, args.timeout)

    print()
    for item in rv:
        print(item)

