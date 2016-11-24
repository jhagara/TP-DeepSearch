#
from time import strftime
import os

# variables
abs_path = os.path.dirname(os.path.abspath(__file__))
name = "Jozef Sitarcik"

#pep8 correct?
print (name.replace(" ", "_") +
       "\n" +
       strftime("%H:%M:%S %d-%m-%Y") +
       "\n" +
       abs_path)