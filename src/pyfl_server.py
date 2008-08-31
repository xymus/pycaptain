#!/usr/bin/python

from sys import argv, exit

from server.server import Server
from common import config

# usage text
usage = """Usage: %s [-h|--help] [-a addresse] [-p port] [-s scenario] [-private] [-w password] [-l language]
\taddresse\tNetwork addreses to open ports on. Can use multiples -a.
\tport\t\tPort to be used. (Yet to be implemented)
\tscenario\tScenario name to load.
\tprivate\t\tOnly players already registered by admin are accepted. 
\t\t\t\t(Yet to be implemented)
\tw pw\t\tSet password for administrator interface.
\tlanguage\tSet language for server, use en, fr, de, etc.
default is: %s""" % (argv[0], "%s -a localhost -p %s -s Sol -l en"%(argv[0], config.port) )

# help!
if "--help" in argv or "-h" in argv:
    print usage
    exit()

# defaults
addresses = ["localhost"]
port = config.port
scenario = "Sol"
language = "en"
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
                port = int( v )
                #ports.append( v )
            elif last == "-s":
                scenario = v
            elif last == "-w":
                adminPassword = v
            elif last == "-l":
                language = v
            last = None
        elif v == "-private":
            private = True
        else:
            last = v

# error in arguments
if last:
    print usage
    exit()
    
# load language
exec( "from languages.%s import %s as Language" % ( language.lower(), language.capitalize() ) )
language = Language()
language.install()

# init and run server
server = Server( addresses=addresses, port=port, scenarioName=scenario, private=private, adminPassword=adminPassword )
server.run()

