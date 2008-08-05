import socket

def init(p):
  global s
  s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  s.bind(("",p))
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  #s.setblocking(False)

def send(d, data):
  s.sendto(data,0,("<broadcast>",d))

def get():
  return s.recv(2**16)
