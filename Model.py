import random
import numpy as np
import pandas as pd
from Agents import Nomad, Royal 

class Model:
    '''initialize agent based model'''
    def __init__(self, num_of_nomads, num_of_royals, num_of_iterations):
        self.agents = []
        self.dead_agents = []
        self.burials = []
        self.num_of_nomads = num_of_nomads
        self.num_of_royals = num_of_royals
        self.num_of_iterations = num_of_iterations
        

    def step(self):
#       shuffle the agents list
        random.shuffle(self.agents)
#       every agent ages 1 year each step, if adult with some probability reproduces
#       and with some probability dies (probability to die increases if agent is old).
        for i, _ in enumerate(self.agents, 0):
            if self.agents[i].alive == True:
                self.agents[i].set_energy(30)
                self.agents[i].update_age()
                if random.random() > 0.82:
                    self.agents[i].reproduce()
                if self.agents[i].age > 50 and random.random() > 0.3:
                    self.agents[i].die()
                elif random.random() > 0.82:
                    self.agents[i].die()
        if len(self.agents) >= 100 and sum(isinstance(item, Royal) for item in self.agents) == 0:
            print("royal appeared")
            self.add_royal(1)
        if len(self.agents) == 0:
            print("new group")
            self.setup()
#       check if someone died and doesn't have a burial, build the burial and add it to the list.
        dead_in_step = {"royal": [], "chief": [], "common": [], "common_low": [], "marginal": []}
        community = [x for x in self.agents if x.type == "Common"]
        dead_agents = [x for x in self.agents if x.type == "Dead"]
        dead_royals = [x for x in self.agents if x.type == "Royal Dead"]
#             first check if there are any dead royals
        resettle = []
        for dead in dead_royals:
            if dead.has_burial == False:
                for hours, status in Nomad.status.items():
                    if status == dead.status:
                        effort_for_royal = hours 
                individual_effort = effort_for_royal/len(community)
                for i in community:
                    i.energy -= individual_effort
                for key, value in dead_in_step.items():
                    if key == dead.status:
                        value.append(round(effort_for_royal))
                dead.has_burial == True
                self.dead_agents.append(dead)
                self.agents.remove(dead)
#                 then check if there are common dead
        for dead in dead_agents:
            if dead.has_burial == False:
                num_of_workers = self.get_num_of_workers(dead.status)
                try:
                    workers = random.sample(community, num_of_workers)
                except ValueError:
                    print("all community works")
                    num_of_workers = len(community)
                    workers = community
                collective_effort = 0
                collective_energy = 0
                for i in workers:
                        collective_effort += i.estimate_burial(dead, num_of_workers)
                        collective_energy += i.energy
                while collective_energy < collective_effort and collective_effort > 0:
                    collective_effort -= 1
                try:
                    individual_effort = collective_effort/num_of_workers
                except ZeroDivisionError:
                    print("no workers left")
                    individual_effort = 0
                for i in workers:
                    i.energy -= individual_effort
                    if i.energy < 0:
                        print(i)
                        resettle.append(i)
                for key, value in dead_in_step.items():
                    if key == dead.status:
                        value.append(round(collective_effort))
                dead.had_burial = True
                self.dead_agents.append(dead)
                self.agents.remove(dead)
        self.burials.append(dead_in_step)         
        self.agents[:] = [x for x in self.agents if x.type != "Dead" or x.type !="Royal Dead"]
        
    def get_num_of_workers(self, status):
        community = [x for x in self.agents if x.type == "Common"]
        if status == "marginal":
            num_of_workers = 2
        elif status == "common_low":
            num_of_workers = 5
        elif status == "common":
            num_of_workers = 30
        elif status == "chief":
            num_of_workers = round(len(community) / 2)
        return num_of_workers
    
    def set_agents(self):
        '''generate agents'''
        for i in range(0, self.num_of_nomads):
            self.agents.append(Nomad(random.randint(14, 50), self.agents))
        for i in range(0, len(self.agents)):
            self.agents[i].set_status()
            self.agents[i].set_energy(30)
        
        for i in range(0, self.num_of_royals):
            self.agents.append(Royal(random.randint(14, 50), self.agents))
            
            
    def add_royal(self, num):
        for i in range(0, num):
            self.agents.append(Royal(random.randint(14, 50), self.agents))
        
    def reset(self):
        self.agents = []
        
    def setup(self):
        self.reset()
        self.set_agents()

        
    def get_data(self):
        '''plots the model. x = step count, y = number of burials'''
        means = []
        sums = []
        for i in self.burials:
            j = {k:round(np.mean(v)) for k,v in i.items()}
            means.append(j)
        df = pd.DataFrame(means)
        df = df.fillna(0)
        df.to_csv("/home/alisk/means.csv", sep='\t', encoding='utf-8')


    def iter_step(self, iterations):
        for i in range(0, iterations):
            for num in range(0, self.num_of_iterations):
                self.step()
            print(len(self.agents))    
            self.setup()

    def get_number_of_burials(self, burials):
        all_bur = {"royal": 0, "chief": 0, "common": 0, "common_low": 0, "marginal": 0}
        for i in test.burials:
            for key, value in i.items():
                if key == all_bur.keys:
                    all_bur.add(value)
