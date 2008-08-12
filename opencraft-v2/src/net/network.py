import socket

def init():
    global s
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(("",9547))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setblocking(False)
    
def sendp(data,view):
    s.sendto(data,("<broadcast>",9547))
    
