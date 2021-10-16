
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
    return sum(individual),
    
# registra la función que se va a evaluar
toolbox.register("evaluate", funcAptitud)

log.info('Funcion de Aptitud definida')

#@title ESTRUCTURA DEL CROMOSOMA

# indica que los individuos son una lista de genes que aplica la función antes definida
creator.create("Individual", list, fitness=creator.Fitness)

# indica que los genes son binarios ( 0 / 1 )
toolbox.register("attr_bin", random.randint, 0, 1)

# cantidad de genes que va a tener el cromosoma
cant_genesCromosoma = 10

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

##################################################################### FUNCIONES #####################################################################
# En esta seccion se encuentran todas las funciones a ser utilizadas en la seccion EJECUCION


##################################################################### EJECUCION #####################################################################
# En esta seccion se hacen las llamadas a las funciones definidas previamente para ejecutar el algoritmo genetico


