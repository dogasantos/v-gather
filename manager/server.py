#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# server.py
 
from multiprocessing.connection import Listener
from common import *
from datahandler import *

def StartServer():
    server_sock = Listener((BINDIP, PORTA))
    conn = server_sock.accept()
    data = conn.recv()
    print type(data)
    print "tamanho: %d"%(len(data))
    print Deserialize(data)

if __name__ == "__main__":
    StartServer()



    
