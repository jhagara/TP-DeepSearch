import time
import os
import sys

__author__ = "Jakub Hagara"

# --help - vypise meno, datum a absolutnu cestu k programu
# --string <string> - prepise medzery ' ' na '_'

argv = sys.argv

if len(argv) == 1:
    print __author__
    print "Current date & time " + time.strftime("%c")
    print os.getcwd()

for i, a in enumerate(argv):
    if a == "--string":
        print argv[i+1].replace(' ', '_')
    elif a == "--help":
        print "Jakub Hagara"
        print "Current date & time " + time.strftime("%c")
        print os.getcwd()
