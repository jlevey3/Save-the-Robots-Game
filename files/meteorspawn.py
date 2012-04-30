from meteors import *
from random import randrange
import math


spawnticker = 60

class MeteorGroup(Group):
    meteors = Group()
    
    
	    

class MeteorSpawner(object):
    
    # spawnticker will increase by one every frame.  It does not get reset.  
    # this means we can wait for a certain number of seconds before introducing harder meteors
    spawnticker = 1
    spawntime = 60
    bounds = None
    
    #frequency = how many frames between each meteor
    frequency_rock = 40
    frequency_ice = 60
    frequency_iron = 70
    frequency_radiation = 71
    frequency_fire = 40
    frequency_gold = 200
    
    delay_rock = 0
    delay_ice = 180
    delay_iron = 300
    delay_radiation = 400
    delay_fire = 700
    delay_gold = 800
    
    
    def spawn(self):
        self.spawnticker += 1
        self.spawn_rock()
        self.spawn_ice()
        self.spawn_iron()
        self.spawn_radiation()
        self.spawn_fire()
        self.spawn_gold()
        
    # Meteor formatting is
    # MeteorGroup.meteors.add(<MeteorType>Meteor((<x coordinate>,<y coordinate>), self.bounds, <frames until impact>, "<string of Meteor Type>"))
        
    def spawn_rock(self):
	if self.spawnticker >= delay_rock:
            if self.spawnticker % self.frequency_rock == 0:
                MeteorGroup.meteors.add(RockMeteor((randrange(0,800),randrange(0,600)),self.bounds, 100, "rock"))
            #optional: self.frequency_rock += (randrange(-3,3)).  Provides variation.
            
    
    def spawn_ice(self):
        if self.spawnticker % self.frequency_ice == 0:
            MeteorGroup.meteors.add(IceMeteor((randrange(0,800),randrange(0,600)),self.bounds, 100, "ice"))

    
    def spawn_iron(self):
        if self.spawnticker  % self.frequency_iron == 0: 
            MeteorGroup.meteors.add(IronMeteor((randrange(0,800),randrange(0,600)),self.bounds, 1000, "iron"))
    
    def spawn_radiation(self):
        if self.spawnticker  % self.frequency_radiation == 0: 
            MeteorGroup.meteors.add(RadiationMeteor((randrange(0,800),randrange(0,600)),self.bounds, 100, "radiation"))
    
    def spawn_fire(self):
	if self.spawnticker  % self.frequency_fire == 0: 
            MeteorGroup.meteors.add(FireMeteor((randrange(0,800),randrange(0,600)),self.bounds, 100, "fire"))
    
    def spawn_gold(self):
        return 8