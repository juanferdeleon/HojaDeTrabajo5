#Programa de simulacion de procesos
#Rodrigo Garoz Carne 18102
#Juan Fernando De Leon Quezada Carne 17822

import simpy
import random
import math

class OS:

    def _init_(self, env, CPU_Amount, RAM_Capacity, ):
        self.CPU = simpy.Resource(env, capacity = CPU_Amount)
        self.RAM = simpy.Container(env, init = Ram_Capacity, capacity = RAM_Capacity)
        

class Process:

    def _init_(self, id, process_No, env, os):
        self.id = id
        self.process_No = process_No
        self.instructions = random.randint(1, 10)
        self.required_RAM = random.randint(1, 10)
        self.env = env
        self.terminated = False
        self.os = os
        self.initial_Time = 0
        self.end_Time = 0
        self.process = env.process(self.procesar(env, os))

    def procesar(self, env, os):
        self.initial_Time = env.now
        
