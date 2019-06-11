# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 06:27:36 2019

@author: Xkalaber
"""

def displayMenu():
    print("Enter an option ('m', 'f', 'x'):\n (M)essage (send)\n (F)ile (request) \n e(X)it")
def getOption():
    response=sys.stdin.readline()
    if not response:
        return None
    return response[0]
def sendMessage(sock):
    msg= sys.stdin.readline()
    if not msg:
        return None
    try:
        sock.send(msg.encode())
    except:
        return None
    return 1
#needs to send uname to server and server needs to return port of requested uname
def requestFile(hostname,sock):
    print('Which user would you like to request a file from? ')
    uname=sys.stdin.readline().rstrip()
    print('sending name')
    sock.send(uname.encode())
    print('waiting to receive client port')
    client_port=sock.recv(1500).decode()
    print('receiving client port')
    print(client_port)
    if client_port=='0':
        print('is empty')
        return None
    else:
        print('What is the file name? ')
        filename=sys.stdin.readline().rstrip()
        if not filename:
            return None
        RetrieveFile(hostname,client_port,filename).start()
    return 1
def usage(script_name):
    print('Usage: py ' + script_name + ' <port number>')
def send_name(sock):
    print('waiting for request from server')
    msg_bytes=sock.recv(1024)
    print(msg_bytes.decode())
    name=sys.stdin.readline().rstrip()
    print('sending name to server')
    sock.send(name.encode())
if __name__=="__main__":
    import sys, os
    import socket
    argc=len(sys.argv)
    if argc != 5:
        usage(sys.argv[0])
        sys.exit()
    import getopt
    optlist, non_option_args=getopt.getopt(sys.argv[1:],'l:p:')
    listen_port=None
    connect_port=None
    for opt, arg in optlist:
        if opt=='-l':
            listen_port=arg
        if opt=='-p':
            connect_port=arg
    if not listen_port:
        usage(sys.argv[0])
        sys.exit()
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect(('localhost',int(connect_port)))
    sock.send(listen_port.encode())
    send_name(sock)
    from recv_messages import RecvMessages
    RecvMessages(sock).start()
    from file_request_listener import FileRequestListener
    FileRequestListener(sock).start()
    from retrieve_file import RetrieveFile
    while True:
        displayMenu()
        option=getOption()
        if not option:
            break
        if option=='m':
            sock.send(option.encode())
            if not sendMessage(sock):
                break
        elif option=='f':
            sock.send(option.encode())
            if not requestFile('localhost',sock):
                break
        elif option =='x':
            sock.send(option.encode())
            break
        else:
            print('Invalid option')
    try:
        sock.shutdown(socket.SHUT_WR)
        sock.close()
        os._exit(0)
    except:
        pass