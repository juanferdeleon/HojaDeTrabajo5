#Programa de simulacion de procesos
#Rodrigo Garoz Carne 18102
#Juan Fernando De Leon Quezada Carne 17822

import simpy
import random
import math
import statistics

# Modificar caracteristicas

CPU_Amount = 1 #CPUS
RAM_Capacity = 100 #Capacidad de RAM
process_Amount = 100 # Cantidad de procesos
Interval = 1 # Intervalo de los procesos
instructions = 6  # Instrucciones realizadas por tiempo
ioTime = 1  # I/O Time
ProcessTimes = []  # Tiempos
random.seed(15)


#Componentes a utilizar (RAM Y CPU)
class Components:

    def __init__(self, env):
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
        self.proceso = env.process(self.procesar(env, components))


    #Proceso
    def procesar(self, env, components):
        self.initial_Time = env.now
        print("Proceso: %s: Creado: %d" % (self.id, self.initial_Time))
        with components.RAM.get(self.required_RAM) as ram:
            yield ram

            #Proceso de RAM
            print('Proceso: %s: RAM: %d (Wait)' % (self.id, env.now))
            nxt = 0

            while not self.terminated:
                with components.CPU.request() as request:
                    print('Proceso: %s: Espera de CPU: %d (Wait)' % (self.id, env.now))
                    yield request
                    
                    for i in range (instructions):
                        if self.instructions > 0:
                            self.instructions -= 1
                            nxt = random.randint(1, 2)

                    yield env.timeout(1)# Tiempo de espera de CPU

                    #Proceso Input/Output
                    if nxt == 1:
                        print('Proceso: %s: Interaccion I/O %d (I/O)' % (self.id, env.now))
                        yield env.timeout(ioTime)

                    # RAM terminated
                    if self.instructions == 0:
                        self.terminated = True

            print('Procecso: %s: Finalizado en: %d (Estado: Terminated)' %(self.id, env.now))
            components.RAM.put(self.required_RAM)  # Regresa la RAM que se utilizo

        self.end_Time = env.now
        self.total_Time = int(self.end_Time - self.initial_Time)
        ProcessTimes.insert(self.id, self.total_Time)
        

#Main
#Crea los procesos
def processes(env, components):
    for i in range(process_Amount):
        creating_Time = math.exp(1.0/Interval)
        Process(i, env, components)
        yield env.timeout(creating_Time)  # Tiempo que tardara en crearse cada proceso

env = simpy.Environment()  # Environment
components = Components(env)  # Componentes (RAM Y CPUS)
env.process(processes(env, components))  # Se crean procesos
env.run()
        
avar = statistics.mean(ProcessTimes)  # Tiempo promedio       
desvEst = statistics.stdev(ProcessTimes)  # Desviacion Estandar

print ("\nTiempo promedio: ", avar, ", Desviacion Estandar: ", desvEst, "\n\n")

