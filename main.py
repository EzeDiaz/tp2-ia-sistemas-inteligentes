##################################################################### FUNCIONES #####################################################################
# En esta seccion se encuentran todas las funciones a ser utilizadas en la seccion EJECUCION

def obtenerDiasDeUnDev(indiceDev, individual):
    # Nos quedamos con una lista de los dias del dev
    # 22 elementos; 1 si se tomo vacaciones, 0 si trabajo - No estan los fines de semana
    diasDelDev = []

    for j in range(22):
        indiceDiaDelDev = indiceDev + 15 * j # indiceDev es el desarrollador, j es el dia
        diasDelDev.append(individual[indiceDiaDelDev])

    return diasDelDev

def seTomoVacacionesEnCiertaSemana(semana, diasDelDev):
    inicioRango = 5 * semana
    finRango = 22 if semana == 4 else semana * 5 + 5

    for i in range(inicioRango, finRango):
        if diasDelDev[i] == 1:
            return 1

    return 0

# Ojo, las listas tiene que tener la misma longitud
def noCoincidencias(unaLista, otraLista):
    contador = 0

    for i in range(len(unaLista)):
        if unaLista[i] != otraLista[i]:
            contador+=1

    return contador

##################################################################### SETUP INICIAL #####################################################################
# En esta seccion se inicializan las variables auxiliares y las correspondientes a la biblioteca a utilizar
# Tomado de: https://github.com/PGP-MachineLearning/IA/blob/master/AG-One-Max-Problem.ipynb


# https://docs.python.org/3/library/configparser.html
# config.get('loQueEstaEntre[]', 'cadaParametro')
# Leemos el config
import configparser
config = configparser.ConfigParser()
config.read('config.cfg') # Para usar otro config hay que cambiar este nombre

# Levantamos el log
#If you want to set the logging level from a command-line option such as:
#--log=INFO
# https://stackoverflow.com/questions/49580313/create-a-log-file
import datetime
import sys
import logging
# logging.info('your text goes here')
# logging.error('your text goes here')
# logging.debug('your text goes here')
log = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
nombreLog = 'log_' + datetime.datetime.now().strftime("%d%b%Y_%H-%M-%S") + config.get('log', 'formato') # Le ponemos fecha al log asi se van generando separados
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s {%(module)s} [%(funcName)s] %(message)s', encoding='utf-8', datefmt='%Y-%m-%d,%H:%M:%S', filename=nombreLog, level=logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
log.addHandler(consoleHandler)
log.info('Inicializando variables')


#@title
import random
import numpy as np
#import matplotlib.pyplot as plt

from deap import base
from deap import creator
from deap import tools

log.info('Librerias importadas')

#@title Inicializa objeto Toolbox auxiliar
toolbox = base.Toolbox()

## OPERADORES GENÉTICOS
## (ver lista completa en https://deap.readthedocs.io/en/master/api/tools.html#operators )

# Registrar tipo de Selección a aplicar con sus parámetros
toolbox.register("select", tools.selTournament, tournsize=2)

# Registrar tipo de Cruzamiento a aplicar con sus parámetros
toolbox.register("mate", tools.cxTwoPoint)

# Registrar tipo de Mutación a aplicar con sus parámetros
toolbox.register("mutate", tools.mutFlipBit, indpb=0.5)

log.info('Operadores Genaticos definidos')

#@title FUNCIÓN DE APTITUD

# indica que es la función de aptitud es para maximizar
creator.create("Fitness", base.Fitness, weights=(1.0,))

# definimos la función de aptitud
def funcAptitud(individual):
    puntajeTandas = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    puntajeCoincidencias = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    puntajeSemanas = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    puntajeDias = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for i in range(15):
        diasDelDev = obtenerDiasDeUnDev(i, individual)
        dev = desarrolladores[i]

        #Cantidad de tandas
        diaAnterior = 0
        sumaDeTandas = 0
        for dia in diasDelDev:
            if(dia == 1 and diaAnterior == 0):
                sumaDeTandas+=1

            diaAnterior = dia

        # Si coincide lo ocurrido con lo esperado le ponemos 10
        puntajeTandas[i] = 10 if dev.cantidadDeTandas == sumaDeTandas else abs(dev.cantidadDeTandas - sumaDeTandas)
            
        #Coincidencia de desarrolladores
        listaDeListaDiasDevsIncompatibles = []
        flagPenalizacion = 0

        for incom in dev.devsIncompatibles:
            listaDeListaDiasDevsIncompatibles.append(obtenerDiasDeUnDev(incom, individual))

        for indice in range(22):
            for listaDiasDelIncompatible in listaDeListaDiasDevsIncompatibles:
                if (diasDelDev[indice] + listaDiasDelIncompatible[indice]) == 2:
                    flagPenalizacion = 1

                if flagPenalizacion == 1:
                        break;
            
            if flagPenalizacion == 1:
                break;

        if flagPenalizacion == 1:
            puntajeCoincidencias[i] = -999999
            break;
                        
        #Semanas
        semanasTomadas = [0, 0, 0, 0, 0]

        for semana in range(5):
            semanasTomadas[semana] = seTomoVacacionesEnCiertaSemana(semana, diasDelDev)

        # Si coincide lo ocurrido con lo esperado le ponemos 10
        puntajeSemanas[i] = 10 if dev.semanas == semanasTomadas else (-noCoincidencias(dev.semana, semanasTomadas))

        #Cantidad de dias
        if dev.cantidadDiasVacas == sum(diasDelDev):
            puntajeDias[i] = 20

        if dev.cantidadDiasVacas < sum(diasDelDev):
            puntajeDias[i] = dev.cantidadDiasVacas - sum(diasDelDev)

        if sum(diasDelDev) > dev.cantidadDiasVacas:
            puntajeDias[i] = -999999

    return sum(puntajeTandas) + sum(puntajeCoincidencias) + sum(puntajeSemanas) + sum(puntajeDias)
    
# registra la función que se va a evaluar
toolbox.register("evaluate", funcAptitud)

log.info('Funcion de Aptitud definida')

#@title ESTRUCTURA DEL CROMOSOMA

# indica que los individuos son una lista de genes que aplica la función antes definida
creator.create("Individual", list, fitness=creator.Fitness)

# indica que los genes son binarios ( 0 / 1 )
toolbox.register("attr_bin", random.randint, 0, 1)

cant_genesCromosoma = 330 # Son 465 porque son 15 devs X 22 dias

# registra el tipo de individuo y población a usar
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bin, cant_genesCromosoma)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

log.info('Cromosoma definido')

#@title
### Parámetros de la Corrida

# Cantidad de Ciclos de la Corrida
CANT_CICLOS = 100  #@param {type:"integer"}

# Indica que finaliza corrida cuando se alcance una  Aptitud Mínima (opcional)
FINALIZA_CORRIDA_POR_MIN_APTITUD = True  #@param {type:"boolean"}
FINALIZA_CORRIDA_VAL_MIN_APTITUD = 10  #@param {type:"integer"}

# Cantidad de Individuos en la Población
CANT_INDIVIDUOS_POBLACION = 3  #@param {type:"integer"}

# Probabilidad del Cruzamiento (en AG 1 = 100%)
PROBAB_CRUZAMIENTO = 1 

# Probabilidad del Mutación 
PROBAB_MUTACION = 0.3 #@param {type:"slider", min:0, max:1, step:0.05}

# Indica si se muestra el detalle de las estadísticas en cada ciclo
MUESTRA_ESTADISTICAS = True  #@param {type:"boolean"}

log.info('Parametros de la Corrida definidos')

#################################################################### ESTRUCTURAS ####################################################################
# En esta seccion se encuentran las estructuras de datos a utilizar
class Desarrollador:

    def __init__(self, idDev, cantidadDeTandas, devsIncompatibles, semanas, cantidadDiasVacas):
        self.idDev = idDev
        self.cantidadDeTandas = cantidadDeTandas
        self.devsIncompatibles = devsIncompatibles
        self.semanas = semanas
        self.cantidadDiasVacas = cantidadDiasVacas


##################################################################### EJECUCION #####################################################################
# En esta seccion se hacen las llamadas a las funciones definidas previamente para ejecutar el algoritmo genetico

cal = toolbox.population(n=2)


dev1 = [1,0,1]
dev2 = [1,0,0]

log.info(dev1 + dev2)
