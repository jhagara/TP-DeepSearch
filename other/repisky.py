import os
import datetime


def first():
    print("Hey, my name is Tomas")
    print("Absolute path to this file is: " + os.path.abspath(__file__))
    print("Current date is: " + str(datetime.date.today()))


def second(text):
    print("".join([x if x is not " " else "_" for x in text]))


first()
second("He an thing rapid these after going drawn or. Timed she his"
       " law the spoil round defer. In surprise concerns informed b"
       "etrayed he learning is ye. Ignorant formerly so ye blessing."
       " He as spoke avoid given downs money on we. Of properly carr"
       "iage shutters ye as wandered up repeated moreover. Inquietud"
       "e attachment if ye an solicitude to. Remaining so continued "
       "concealed as knowledge happiness. Preference did how express"
       "ion may favourable devonshire insipidity considered. An leng"
       "th design regret an hardly barton mr figure.")
