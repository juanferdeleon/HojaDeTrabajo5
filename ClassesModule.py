#Programa de simulacion de procesos
#Rodrigo Garoz Carne 18102
#Juan Fernando De Leon Quezada Carne 17822

import simpy
import random
import math

random.seed(15)

#Componentes a utilizar (RAM Y No. DE CPU)
class Components:

    def __init__(self, env, CPU_Amount, RAM_Capacity):
        self.CPU = simpy.Resource(env, capacity = CPU_Amount)
        self.RAM = simpy.Container(env, init = RAM_Capacity, capacity = RAM_Capacity)
        

#Clase que define un proceso
class Process:

    #Atributos
    def __init__(self, id, env, components):
        self.id = id
        self.env = env
        self.components = components
        self.instructions = random.randint(1, 10)
        self.required_RAM = random.randint(1, 10)
        self.terminated = False
        self.initial_Time = 0
        self.end_Time = 0
        self.total_Time = 0

    #Proceso
    def procesar(self, env, components, instructions, ioTime):
        self.initial_Time = env.now
        print("%s: Proceso: %d" % (self.id, self.initial_Time))
        with components.RAM.get(self.required_RAM) as ram:
            yield ram

            #Proceso de RAM
            print('%s: RAM %d (Estado: Wait)' % (self.id, env.now))
            nxt = 0

            while not self.terminated:
                with component.CPU.request() as request:
                    print('%s: CPU %d (Estado: Wait)' % (self.id, env.now))
                    yield request

                    #Proceso CPU
                    print('%s: CPU %d (Estado: Running)' % (self.id, env.now))
                    
                    for i in range (instructions):
                        if self.instructions > 0:
                            self.instructions -= 1
                            nxt = random.randint(0, 1)

                    yield env.timeout(1)# Tiempo de espera de CPU

                    #Proceso Input/Output
                    if nxt == 1:
                        print('%s: I/O %d (Estado: I/O)' % (self.id, env.now))
                        yield env.timeout(ioTime)

                    # RAM terminated
                    if self.instructions == 0:
                        self.terminated = True

            print('%s: Terminado %d (Estado: Terminated)' % (self.id, env.now))
            components.RAM.put(self.required_RAM)  # Regresa la RAM que se utilizo

        self.end_Time = env.now
        self.total_Time = int(self.finishedTime - self.createdTime)
        
        return self.total_Time
            
        
        
