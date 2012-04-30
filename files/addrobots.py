from robots import *
from random import randrange
import math

foo = "pingas"
def addrobots(bounds):
    #Here's how to add robots.  the format is:
    # RoboGroup.robots.add(<Familymember>bot((<x coordinate>,<y coordinate>), bounds))
    
    RoboGroup.robots.add(Brotherbot((randrange(0,800),randrange(0,600)), bounds))
    RoboGroup.robots.add(Fatherbot((randrange(0,800),randrange(0,600)), bounds))
    RoboGroup.robots.add(Motherbot((randrange(0,800),randrange(0,600)), bounds))
    RoboGroup.robots.add(Sisterbot((randrange(0,800),randrange(0,600)), bounds))
    print "ROBOT GROUP SIZE: "+ str(len(RoboGroup.robots))
