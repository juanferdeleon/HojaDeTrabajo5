#Programa de simulacion de procesos
#Rodrigo Garoz Carne 18102
#Juan Fernando De Leon Quezada Carne 17822

import simpy
import random
import math
from ClassesModule import Components
from ClassesModule import Process

# Modificar caracteristicas

CPU_Amount = 2 #CPUS
RAM_Capacity = 100 #Capacidad de RAM
process_Amount = 200 # Cantidad de procesos
Interval = 10 # Intervalo de los procesos
instructions = 6  # Instrucciones realizadas por tiempo
ioTime = 1  # I/O Time
ProcessTimes = []  # Tiempos
random.seed(15)


#Main

# Generador de procesos
def proceso_generator(env, components, instructions, ioTime):
    n = 0
    for i in range(process_Amount):
        creating_Time = math.exp(1.0/Interval)
        process = Process('Proceso %d' % i, env, components)
        ProcessTimes.insert(n, process.procesar(env, components, instructions, ioTime))
        n += 1
        print(n)
        yield env.timeout(creating_Time)  # Tiempo que tardara en crearse cada proceso

env = simpy.Environment()  # Environment
components = Components(env, CPU_Amount, RAM_Capacity)  # Componentes (RAM Y CPUS)
env.process(proceso_generator(env, components, instructions, ioTime))  # Se crean procesos
env.run()

        

#------Se calcula el Promedio de tiempo que esta cada proceso en la computadora y desviacion estandar------#

def avarage(ProcessTimes):
    return (sum(ProcessTimes) * (1.0 / len(ProcessTimes)))

tiempo_promedio_total = avarage(ProcessTimes)  # Se obtiene el tiempo promedio
varianza_tiempo_total = map(lambda x: (x - tiempo_promedio_total) ** 2, TiemposDeProcesos)
desvest_tiempo_total = math.sqrt(avarage(varianza_tiempo_total))  # Se obtiene la desviacion estandar

print ("El promedio de tiempo es de: ", tiempo_promedio_total, ", y su desviacion estandar es de: ", \
      desvest_tiempo_total)

