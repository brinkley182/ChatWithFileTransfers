# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 06:41:56 2019

@author: Xkalaber
"""

def usage(script_name):
    print('Usage: py ' + script_name + ' <port number>')
if __name__=="__main__":
    import sys
    import socket
    import server_globals
    from msg_relay import MsgRelay
    argc=len(sys.argv)
    if argc !=2:
        usage(sys.argv[0])
        sys.exit()
    serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    serversocket.bind(('localhost',int(sys.argv[1])))
    serversocket.listen(5)
    while True:
        sock,addr=serversocket.accept()
        print(sock.getsockname()[1])
        MsgRelay(sock).start()