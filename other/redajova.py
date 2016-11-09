import os
import time

def details():
    my_name = 'Martina Redajova\n'
    my_dir = os.path.dirname(os.path.realpath(__file__))
    curr_date = time.strftime("%d.%m.%Y")
    print("My names is " + my_name)
    print("Directory: " + my_dir)
    print(curr_date)

def string_replacement(s):
    s = s.replace(' ', '_')
    print(s)

details()
str_to_replace = '\nCollege degree promises opportunities, not mental health.'
string_replacement(str_to_replace)
