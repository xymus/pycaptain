#!/usr/bin/python

from sys import argv, exit

from server.server import Server
from common import config

# usage text
usage = """Usage: %s [-h|--help] [-a addresse] [-p port] [-s scenario] [-private] [-admin password]
\taddresse\tNetwork addreses to open ports on. Can use multiples -a.
\tport\tPort to be used. (Yet to be implemented)
\tscenario\tScenario name to load.
\tprivate\tOnly players already registered by admin are accepted. (Yet to be implemented)
\tadmin pw\tSet password for administrator interface. (Yet to be implemented)
default is: %s""" % (argv[0], "%s -a localhost -p %s -s Sol"%(argv[0], config.port) )

# help!
if "--help" in argv or "-h" in argv:
    print usage
    exit()

# defaults
addresses = ["localhost"]
port = config.port
scenario = "Sol"
private = False
adminPassword = None

# walk in arguments
last = None
if len( argv ) > 1:
  for v in argv[1:]:
    if last:
        if last == "-a":
            addresses.append( v )
        elif last == "-p":
            ports.append( v )
        elif last == "-s":
            scenario = v
        elif last == "-admin":
            adminPassword = v
        last = None
    elif v == "-private":
        private = True
    else:
        last = v

# error in arguments
if last:
    print usage
    exit()

# init and run server
server = Server( addresses=addresses, port=port, scenarioName=scenario, private=private, adminPassword=adminPassword )
server.run()

