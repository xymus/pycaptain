#!/usr/bin/python

from sys import argv, exit

from server.server import Server
from common import config

# usage text
usage = """Usage: %s [-h|--help] [-a addresse] [-p port] [-s scenario] [--private] [-w password] [-l language] [--save path]
\t-a --address\tNetwork addreses to open ports on. Can be used more than once.
\t-p --port\t\tPort to be used.
\t-s --scenario\tScenario name to load.
\t--pw\t\tSet password for administrator interface.
\t-l --language\tSet language for server, use en, fr, de, etc.
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
savePath = None

# walk in arguments
last = None
if len( argv ) > 1:
    for v in argv[1:]:
        if last:
            if last == "-a":
                addresses.append( v )
            elif last == "-p":
                port = int( v )
            elif last == "-s":
                scenario = v
            elif last == "--pw":
                adminPassword = v
            elif last == "-l":
                language = v
            elif last == "--save":
                savePath = v
            last = None
        elif v == "--private":
            private = True
        elif v == "--address":
            last = "-a"
        elif v == "--port":
            last = "-p"
        elif v == "--scenario":
            last = "-s"
        elif v == "--language":
            last = "-l"
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
server = Server(addresses=addresses, port=port, scenarioName=scenario, private=private, adminPassword=adminPassword, savePath=savePath)
server.run()

