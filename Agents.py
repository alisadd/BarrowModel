import random

class Nomad:
    """ Initialise nomad of a certain age and social status. 
    """
    status = {14: "marginal", 70: "common_low", 185: "common", 300: "chief", 2000: "royal"}

    def __init__(self, age, agents):
        self.age = age
        self.agents = agents
        self.type = "Common"
        self.alive = True
        self.has_burial = False
    
    def set_energy(self, value):
        self.energy = value
        return self.energy
    
    def update_age(self):
        self.age += 1
       
    def set_status(self):
        probability = random.random()
        if probability > 0.91:
            self.status = Nomad.status[300]
        elif probability >= 0.58 and probability < 0.91:
            self.status = Nomad.status[185]
        elif probability >= 0.12 and probability < 0.58:
            self.status = Nomad.status[70]
        elif probability < 0.12:
            self.status = Nomad.status[14]
        return self.status
    
    def estimate_burial(self, dead, num_of_workers):
        total_effort = 0
        for hours, status in Nomad.status.items():
            if status == dead.status:
                total_effort = hours
#         add randomizing of individual effort.
        individual_contribution = total_effort/num_of_workers
        if self.energy < individual_contribution:
                individual_contribution = self.energy
        return individual_contribution
        
    def reproduce(self):
        new = Nomad(14, self.agents)
        new.set_status()
        new.set_energy(30)
        self.agents.append(new)
    
    def die(self):
        self.alive = False
        self.type = "Dead"
            
    def leave(self):
        self.agents.remove()
        
    def __str__(self):
        return "This %s %s nomad of age %s has %s points of energy" % (self.type, self.status, self.age, self.energy)
    
    
class Royal(Nomad):
    '''initialize a royal scythian'''
    def __init__(self, age, agents):
        Nomad.__init__(self, age, agents)
        self.type = "Royal"
        self.alive = True
        self.status = "royal"
        self.energy = 30
        
    def build_burial(self, dead):
        pass   
    
    def reproduce(self):
        pass
    
    def die(self):
        self.alive = False
        self.type = "Royal Dead"
    
    def __str__(self):
        return "This %s nomad of age %s has %s points of energy" % (self.status, self.age, self.energy)
    
