#!/usr/bin/python

from sys import argv

from server.server import Server

if len( argv ) > 1:
    server = Server( argv[1:] )
else:
    server = Server()
server.run()

