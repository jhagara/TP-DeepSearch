#
from time import strftime
import os
import sys
import getopt

# variables
abs_path = os.path.dirname(os.path.abspath(__file__))
name = "Jozef Sitarcik"


#
def signature():
    print "\n" +\
          (name.replace(" ", "_") +
           "\n" +
           strftime("%H:%M:%S %d-%m-%Y") +
           "\n" +
           abs_path)


def main(argv):
    input_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", "inputfile=")
    except getopt.GetoptError:
        print 'sitarcik.py -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'sitarcik.py -i <inputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
    file = open(input_file, 'r')
    for line in file:
        print(line.replace(" ", "_")),


main(sys.argv[1:])
signature()
