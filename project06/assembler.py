#!/usr/bin/python
import sys

if len(sys.argv) < 2:
    print "You must supply the name of the file to assemble"
    exit(1)

file=open(sys.argv[1])


