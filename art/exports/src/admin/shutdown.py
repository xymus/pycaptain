#!/usr/bin/python

from sys import argv
import config

from admin import Admin

server = "localhost"
port = config.port
message = "shutdown"
password = None

if argv.count( "-s" ):
    p = argv.index( "-s" )
    if len(argv) > p:
        server = argv[ p+1 ]

if argv.count( "-p" ):
    p = argv.index( "-p" )
    if len(argv) > p:
        port = int(argv[ p+1 ])

if argv.count( "-w" ):
    p = argv.index( "-w" )
    if len(argv) > p:
        password = argv[ p+1 ]

if argv.count( "-m" ):
    p = argv.index( "-m" )
    if len(argv) > p:
        message = argv[ p+1 ]

admin = Admin( server, port, password )
admin.connect()
admin.sendMessage( message )
admin.quit()

