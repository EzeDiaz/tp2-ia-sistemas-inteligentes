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

def cantidadDeTandas(diasDelDev):
    diaAnterior = 0
    sumaDeTandas = 0
    for dia in diasDelDev:
        if(dia == 1 and diaAnterior == 0):
            sumaDeTandas+=1

        diaAnterior = dia

    return sumaDeTandas

#################################################################### ESTRUCTURAS ####################################################################
# En esta seccion se encuentran las estructuras de datos a utilizar
class Desarrollador:

    def __init__(self, idDev, cantidadDeTandas, devsIncompatibles, semanas, cantidadDiasVacas):
        self.idDev = idDev
        self.cantidadDeTandas = cantidadDeTandas
        self.devsIncompatibles = devsIncompatibles
        self.semanas = semanas
        self.cantidadDiasVacas = cantidadDiasVacas

############################################################## FIXTURE DE DESARROLLADORES ##############################################################
# En esta seccion se inicializan las variables auxiliares y las correspondientes a la biblioteca a utilizar
# Tomado de: https://github.com/PGP-MachineLearning/IA/blob/master/AG-One-Max-Problem.ipynb
desarrolladores = []

# 15 porque queremos 15 devs
desarrolladores.append(Desarrollador(0,2,[1],[0,1,1,0,0],5))
desarrolladores.append(Desarrollador(1,1,[0],[1,1,0,0,0],8))
desarrolladores.append(Desarrollador(2,3,[13],[1,0,1,0,1],3))
desarrolladores.append(Desarrollador(3,3,[],[1,1,0,1,0],3))
desarrolladores.append(Desarrollador(4,2,[5,6],[0,0,1,1,0],3))
desarrolladores.append(Desarrollador(5,2,[4,6],[1,0,0,0,1],7))
desarrolladores.append(Desarrollador(6,1,[4,5],[1,1,0,0,0],10))
desarrolladores.append(Desarrollador(7,2,[],[0,0,1,1,0],4))
desarrolladores.append(Desarrollador(8,1,[],[0,0,1,0,0],4))
desarrolladores.append(Desarrollador(9,1,[10,11],[1,1,0,0,0],7))
desarrolladores.append(Desarrollador(10,2,[9,11],[0,0,0,1,1],7))
desarrolladores.append(Desarrollador(11,2,[9,10],[0,0,1,1,0],7))
desarrolladores.append(Desarrollador(12,2,[],[1,1,0,0,0],3))
desarrolladores.append(Desarrollador(13,3,[2],[0,0,0,1,0],3))
desarrolladores.append(Desarrollador(14,1,[],[1,1,1,0,0],12))


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
import matplotlib.pyplot as plt

from deap import base
from deap import creator
from deap import tools

log.info('Librerias importadas')

#@title Inicializa objeto Toolbox auxiliar
toolbox = base.Toolbox()

## OPERADORES GENÉTICOS
## (ver lista completa en https://deap.readthedocs.io/en/master/api/tools.html#operators )

# Registrar tipo de Selección a aplicar con sus parámetros
toolbox.register("select", tools.selTournament, tournsize=4)

# Registrar tipo de Cruzamiento a aplicar con sus parámetros
toolbox.register("mate", tools.cxTwoPoint)

# Registrar tipo de Mutación a aplicar con sus parámetros
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.5)

log.info('Operadores Geneticos definidos')

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
        sumaDeTandas = cantidadDeTandas(diasDelDev)

        # Si coincide lo ocurrido con lo esperado le ponemos 10
        puntajeTandas[i] = 10 if dev.cantidadDeTandas == sumaDeTandas else abs(dev.cantidadDeTandas - sumaDeTandas)
            
        #Coincidencia de desarrolladores
        listaDeListaDiasDevsIncompatibles = []
        flagPenalizacion = 0

        for incom in dev.devsIncompatibles:
            listaDeListaDiasDevsIncompatibles.append(obtenerDiasDeUnDev(incom, individual))

        # 22 porque itero sobre los dias habiles
        for indice in range(22):
            for listaDiasDelIncompatible in listaDeListaDiasDevsIncompatibles:
                if (diasDelDev[indice] + listaDiasDelIncompatible[indice]) == 2:
                    flagPenalizacion = 1

                if flagPenalizacion == 1:
                        break;
            
            if flagPenalizacion == 1:
                break;

        if flagPenalizacion == 1:
            puntajeCoincidencias[i] = -99
            break;
                        
        #Semanas
        semanasTomadas = [0, 0, 0, 0, 0]

        for semana in range(5):
            semanasTomadas[semana] = seTomoVacacionesEnCiertaSemana(semana, diasDelDev)

        # Si coincide lo ocurrido con lo esperado le ponemos 10
        puntajeSemanas[i] = 10 if dev.semanas == semanasTomadas else (-noCoincidencias(dev.semanas, semanasTomadas))

        #Cantidad de dias
        if  sum(diasDelDev) <= dev.cantidadDiasVacas:
            puntajeDias[i] = (sum(diasDelDev) * 20) / dev.cantidadDiasVacas

        if sum(diasDelDev) > dev.cantidadDiasVacas:
            puntajeDias[i] = -99

    #return (sum(puntajeTandas) + sum(puntajeCoincidencias) + sum(puntajeSemanas) + sum(puntajeDias))
    return (sum(puntajeTandas) + sum(puntajeCoincidencias) + sum(puntajeSemanas) + sum(puntajeDias),)

# registra la función que se va a evaluar
toolbox.register("evaluate", funcAptitud)

log.info('Funcion de Aptitud definida')

#@title ESTRUCTURA DEL CROMOSOMA

# indica que los individuos son una lista de genes que aplica la función antes definida
creator.create("Individual", list, fitness=creator.Fitness)

# indica que los genes son binarios ( 0 / 1 )
listaBinaria = [0, 1]
toolbox.register("attr_bin", np.random.choice, listaBinaria, p=[0.9, 0.1])

cant_genesCromosoma = 330 # Son 330 porque son 15 devs X 22 dias

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
FINALIZA_CORRIDA_VAL_MIN_APTITUD = 500  #@param {type:"integer"}

# Cantidad de Individuos en la Población
CANT_INDIVIDUOS_POBLACION = 500  #@param {type:"integer"}

# Probabilidad del Cruzamiento (en AG 1 = 100%)
PROBAB_CRUZAMIENTO = 1 

# Probabilidad del Mutación 
PROBAB_MUTACION = 0.3 #@param {type:"slider", min:0, max:1, step:0.05}

# Indica si se muestra el detalle de las estadísticas en cada ciclo
MUESTRA_ESTADISTICAS = True  #@param {type:"boolean"}

log.info('Parametros de la Corrida definidos')

##################################################################### EJECUCION #####################################################################
# En esta seccion se hacen las llamadas a las funciones definidas previamente para ejecutar el algoritmo genetico

#@title EJECUCIÓN DE LA CORRIDA


## Define una función auxiliar para calcular estadísticas y guarda info en vectores auxiliares
def CalculoEstadisticas(ciclo, indivPobla, muestra, mejorMax = True):
    
    global mejorIndCorrida
    global ciclosMaxAptitud
    global ciclosPromAptitud
    global ciclosMinAptitud

    if len(indivPobla) == 0:
      return None, 0, 0, 0 

    auxMax = None
    auxMin = None
    auxSum = 0
    auxBestInd = None
    auxBestIndApt = None
    
    for ind in indivPobla:

        apt = round(ind.fitness.values[0], 2)
        auxSum = auxSum + apt

        if (auxMax == None) or (apt > auxMax):
            auxMax = apt
            if mejorMax:
              auxBestInd = ind
              auxBestIndApt = apt

        if (auxMin == None) or (apt < auxMin):
            auxMin = apt
            if not mejorMax:
              auxBestInd = ind
              auxBestIndApt = apt

    auxProm = round(auxSum / len(indivPobla),2)

    ciclosMaxIndiv.append( auxBestInd )
    ciclosMaxAptitud.append( auxMax )
    ciclosPromAptitud.append( auxProm )
    ciclosMinAptitud.append( auxMin )

    if muestra:          
        log.info('-- Ciclo  %d --', ciclo)
        log.info(' Mejor Individuo: %s { %d }', auxBestInd, auxBestIndApt)    
        log.info('   Max: %f / Promedio: %f / Min: %f ', auxMax, auxProm, auxMin)



    return auxBestInd, auxMax, auxProm, auxMin

# Define la población inicial
indivPobla = toolbox.population(n=CANT_INDIVIDUOS_POBLACION)

# Asigna el valor de aptitud a los individuos de la población inicial
fitnesses = list(map(toolbox.evaluate, indivPobla))
for ind, fit in zip(indivPobla, fitnesses):
    ind.fitness.values = fit

# vectores auxiliares 
ciclo = 1    
ciclosMaxIndiv = []
ciclosMaxAptitud = []
ciclosPromAptitud = []
ciclosMinAptitud = []

# Cálcula estadísticas y guarda info en vectores auxiliares
auxBestInd, auxMax, auxProm, auxMin = CalculoEstadisticas(0, indivPobla, MUESTRA_ESTADISTICAS)
      
        # criterio de paro
while (ciclo < CANT_CICLOS) and (not(FINALIZA_CORRIDA_POR_MIN_APTITUD) or (auxMax < FINALIZA_CORRIDA_VAL_MIN_APTITUD)):

    # Realiza la Selección
    indivSelecc = toolbox.select(indivPobla, len(indivPobla))

    # Inicializa a los hijos clonando a los seleccionados
    indivHijos = list(map(toolbox.clone, indivSelecc))
    
    # Realiza el Cruzamiento
    for hijo1, hijo2 in zip(indivHijos[::2], indivHijos[1::2]):
        if random.random() < PROBAB_CRUZAMIENTO:
            toolbox.mate(hijo1, hijo2)
            del hijo1.fitness.values
            del hijo2.fitness.values

    # Realiza la Mutación
    for mutant in indivHijos:
        if random.random() < PROBAB_MUTACION:
            toolbox.mutate(mutant)
            del mutant.fitness.values
              
    # Evalua a los individuos que salen de la Mutación
    #  para determinar si son válidos y su valor de aptitud
    invalid_ind = [ind for ind in indivHijos if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    
    # Reemplaza la población actual con los hijos
    indivPobla[:] = indivHijos
    
    # Cálcula estadísticas y guarda info en vectores auxiliares
    auxBestInd, auxMax, auxProm, auxMin = CalculoEstadisticas(ciclo, indivPobla, MUESTRA_ESTADISTICAS)


    ciclo = ciclo + 1

log.info('---- Corrida Finalizada en %d ciclos ----', ciclo )

mejorCiclo = np.argmax( ciclosMaxAptitud )

log.info('== Mejor Individuo de la Corrida: %s { %f }', ciclosMaxIndiv[mejorCiclo], ciclosMaxAptitud[mejorCiclo])

log.info('Mejor individuo encontrado en el ciclo %d', mejorCiclo )

log.info('--- Datos del mejor individuo ---')
log.info('--- Id desarrollador | Tandas: (deseadas, tomadas) | Coincidencias: (prohibidas, ocurridas) | Semanas: (deseadas, tomadas) | Dias: (deseados, tomados) ---')
for i in range(15):
    diasDelDev = obtenerDiasDeUnDev(i, ciclosMaxIndiv[mejorCiclo])

    #Tandas
    sumaDeTandas = cantidadDeTandas(diasDelDev)

    #Coincidencia de desarrolladores
    listaDeListaDiasOtrosDevs = []
    devsQueSeCruzo = []

    for j in range(15):
        listaDeListaDiasOtrosDevs.append(obtenerDiasDeUnDev(j, ciclosMaxIndiv[mejorCiclo]))

    # 22 porque itero sobre los dias habiles
    for indice in range(22):
        indicadorDeDev = 0
        for listaDiasDelOtro in listaDeListaDiasOtrosDevs:
            if (diasDelDev[indice] + listaDiasDelOtro[indice]) == 2:
                devsQueSeCruzo.append(indicadorDeDev)

            indicadorDeDev+=1

    devsQueSeCruzoSinRepetidos = set(devsQueSeCruzo)

    #Semanas
    semanasTomadas = [0, 0, 0, 0, 0]

    for semana in range(5):
        semanasTomadas[semana] = seTomoVacacionesEnCiertaSemana(semana, diasDelDev)

    #Dias tomados
    diasTomados = sum(diasDelDev)

    log.info(' %d | Tandas: (%d, %d) | Coincidencias: (%s, %s) | Semanas: (%s, %s) | Dias: (%d, %d) ', i, desarrolladores[i].cantidadDeTandas, sumaDeTandas, desarrolladores[i].devsIncompatibles, devsQueSeCruzoSinRepetidos, desarrolladores[i].semanas, semanasTomadas, desarrolladores[i].cantidadDiasVacas, diasTomados)

#@title MOSTRAR GRAFICO DE LA CORRIDA
plt.figure(figsize=(15,8)) 
plt.plot(ciclosPromAptitud)
plt.plot(ciclosMinAptitud)
plt.plot(ciclosMaxAptitud)

plt.title('Resultados de la Corrida')
plt.xlabel('Ciclos')
plt.ylabel('Aptitud')
plt.legend(['Promedio', 'Mínima', 'Máxima'], loc='lower right')

plt.show()