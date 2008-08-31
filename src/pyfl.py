#!/usr/bin/python

from sys import argv

from client.client import Client

client = Client()

try:
  if "-s" in argv:
    try:
        client.run()
    except Exception, ex:
        print ex
  else:
    client.run()
except KeyboardInterrupt:
  print "KeyboardInterrupt"
  if client.run:
      client.run = False

