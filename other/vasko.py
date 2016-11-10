import time
import sys
import os

print "Martin Vasko"
print time.strftime("%d.%m.%Y")
print os.path.abspath(sys.argv[0])
if (len(sys.argv) > 1):
    print sys.argv[1].replace(" ", "_")
