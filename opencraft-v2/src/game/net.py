import socket

import simplejson

class Connection(object):
    def __init__(self, dest, stype="tcp", _socket=None):
        assert stype in ("tcp", "udp")
        self.dest = dest
        if _socket is not None:
            self.socket = _socket
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if stype == "tcp" else socket.SOCK_DGRAM)
            self.socket.connect(self.dest)
        self.socket.setblocking(False)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.buf = ""
    def fileno(self):
        return self.socket.fileno()
    def send(self, message):
        s = simplejson.dumps(message)
        r = str(len(s))+":"+s
        self.socket.send(r)
    def recv(self):
        try:
            self.buf += self.socket.recv(2**16)
        except socket.error:
            return []
        r = []
        while True:
            try:
                first_colon = self.buf.index(":")
            except ValueError:
                break
            l = int(self.buf[:first_colon])
            m = self.buf[first_colon+1:first_colon+1+l]
            if len(m) < l:
                break
            assert len(m) == l
            o = simplejson.loads(m)
            self.buf = self.buf[first_colon+1+l:]
            r.append(o)
        return r

class Listener(object):
    def __init__(self, port, type="tcp"):
        assert type in ("tcp", "udp")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM if type == "tcp" else socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(False)
        self.socket.bind(("", port))
        self.socket.listen(5)
    def fileno(self):
        return self.socket.fileno()
    def accept(self):
        l = []
        while True:
            try:
                s = self.socket.accept()
            except socket.error:
                break
            l.append(Connection(s[1], "tcp", s[0]))
        return l

if __name__ == "__main__":
    import select
    listen = Listener(2410)
    clients = []
    while True:
        need_update = select.select([listen]+clients, [], [])[0]
        for conn in need_update:
            if conn is listen:
                clients.extend(listen.accept())
            else:
                for msg in conn.recv():
                    for client in clients:
                        client.send(msg)
