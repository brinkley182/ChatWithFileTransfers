# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 06:48:54 2019

@author: Xkalaber
"""

import threading
import server_globals

class MsgRelay(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection=connection
        self.name=None
    def get_name(self):
        request ='What is your name?'
        self.connection.send(request.encode())
        name_bytes=self.connection.recv(1024)
        self.name=name_bytes.decode()
        server_globals.connections.setdefault(self.name,[])
        server_globals.connections[self.name].append(self.connection)

    def run(self):
        client_port=self.connection.recv(1024).decode()
        print('client port: ' +client_port)
        self.get_name()
        server_globals.connections.setdefault(self.name,[])
        server_globals.connections[self.name].append(client_port)
        print(server_globals.connections)
        while True:
            opt=self.connection.recv(1024).decode()
            print(opt)
            if opt == 'm':
                print('hitting the message')
                msg_bytes=self.connection.recv(1024)
                if len(msg_bytes):
                    pass
                else:
                    self.connection.close()
                    server_globals.connections.pop(self.name)
                    break
                name_msg=str(self.name)+': '
                for conn in server_globals.connections:
                    if server_globals.connections[conn][0] is not self.connection:
                       server_globals.connections[conn][0].send(name_msg.encode())
                       server_globals.connections[conn][0].send(msg_bytes)
            elif opt == 'f':
                file_owner=self.connection.recv(1500).decode()
                print(file_owner)
                if file_owner in server_globals.connections:
                    print('exists %s'%(server_globals.connections[file_owner][1]))
                    self.connection.send(server_globals.connections[file_owner][1].encode())
                    print('sent port')
                else:
                    self.connection.send('0'.encode())
                    print('doesnt exist')
                    pass
            elif opt == 'x':
                server_globals.connections.pop(self.name)
                print(server_globals.connections)
                break
            else:
                pass