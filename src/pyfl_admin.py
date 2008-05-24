#!/usr/bin/python

from socket import SocketType
from sys import argv, exit
from md5 import md5

from common import config

class Admin:
    def __init__( self, server="localhost", port=config.port, password=None ):
        self.server = server
        self.port = port
        if password:
            self.password = md5(password).hexdigest()
        else:
            self.password = None
        self.socket = SocketType()

    def connect( self ):
        self.socket.connect( ( self.server, self.port ) )

    def sendMessage( self, message ):
        if self.password:
            self.socket.send( message+" "+self.password+"\n" )
        else:
            self.socket.send( message+"\n" )

    def quit( self ):
        self.socket.close()

def usage():
    print """Usage: %s [-i] [-s server] [-p port] [-w password] [-m message]
    Options:
    \t-i\tInteractive mode, othewise uses default values.
    \tserver\tServer ip address or hostname.
    \tport\tServer port to use.
    \tpassword\tServer admin password.
    \tmessage\tMessage (string) to send to the server."""
    exit()

if __name__ == '__main__':
  server = "localhost"
  port = config.port
  password = None
  message = None # "shutdown"+"\n"

  specServer = specPort = specPassword = specMessage = False

  if argv.count( "-h" ) or argv.count( "--help" ):
      usage()

  if argv.count( "-s" ):
    p = argv.index( "-s" )
    if len(argv) > p:
        server = argv[ p+1 ]
        specServer = True

  if argv.count( "-p" ):
    p = argv.index( "-p" )
    if len(argv) > p:
        port = int(argv[ p+1 ])
        specPort  = True

  if argv.count( "-w" ):
    p = argv.index( "-w" )
    if len(argv) > p:
        password = argv[ p+1 ]
        specPassword = True


  if argv.count( "-m" ):
    p = argv.index( "-m" )
    if len(argv) > p:
        message = argv[ p+1 ]
        specMessage = True

  if argv.count( "-i" ): # interactive!
    if not specServer:
        server = raw_input( "server: " )

    if not specPort:
        port = int(raw_input( "port: " ))

    if not specPassword:
        password = raw_input( "password: " )

  #  if not specMessage:
  #      message = raw_input( "message: " )

  if not message:
    usage()

  admin = Admin( server, port, password )
  admin.connect()

  #if argv.count( "-i" ): # interactive!
  #  option = None
  #  os = ["sysmsg: Send a system message.", "code: send python code to be executed", "shutdown: "]
  #  while option != "quit":
  #      print "\nOptions":
  #      for o in os
  #          print " "+o
  #      option = raw_input( 'enter your choice or "quit": ' )

  #      if option == "sysmsg":
  #          message = raw_input( 'system message to send: ' )
  #          admin.sendMessage( message )
  #else:
  admin.sendMessage( message )

  admin.quit()



