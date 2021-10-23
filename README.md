# TP2-IA-Sistemas-Inteligentes GRUPO 12
Trabajo Práctico 2 - Inteligencia Artificial - Sistemas Inteligentes

## Integrantes del grupo
- Arrascaeta, Ignacio
- Cueli, Juan Francisco
- Diaz, Ezequiel
- Marchesotti, Nicolás
- Messuti, Claudio
- Oviedo, Facundo

## Enunciado
[Enunciado Sistemas Inteligentes - 2do Cuatrimestre 2021](https://drive.google.com/file/d/18Wz3wD0k8PnrjpACX-vVBbVzKHncLakK/view?usp=sharing)

## Ejecución del programa
Para poder correr el ejecutable `Ejecutar algoritmo - Con instalacion de dependencias` se debe contar con la versión 3.9.7 de Python instalada (visitar https://www.python.org/downloads/). 

- Realizar las modificaciones necesarias en el archivo `config.cfg` para ejecutar con los parametros deseados
  - Seccion `log`
    - `formato` especifica el formato deseado para la generacion del log
      - Valores permitidos: .log - .csv
  - Seccion `opearadores_geneticos`
    - `participantes_torneo` especifica cuantos participantes tendra el torneo
      - Valores permitidos: numeros enteros
    - `metodo_cruzamiento` especifica el metodo de cruzamiento
      - Valores permitidos: multipunto - simple
    - `metodo_mutacion` especifica el metodo de mutacion
      - Valores permitidos: shuffle - flip_bit
  - Seccion `corrida`
    - `ciclos` especifica cuantos ciclos correra el algoritmo
      - Valores permitidos: numeros enteros
    - `umbral_aptitud` especifica el minimo valor de aptitud para que corte el algoritmo
      - Valores permitidos: numeros enteros
    - `cantidad_individuos_poblacion` especifica la cantidad de individuos de la poblacion
      - Valores permitidos: numeros enteros
    - `probabilidad_de_mutacion` especifica la probabilidad de mutacion
      - Valores permitidos: numeros flotantes entre 0 y 1 (0.1 - 0.2 - etc) 
- Doble click en `Ejecutar algoritmo - Con instalacion de dependencias`
- Revisar el log y el grafico generados (se genera con la fecha y hora de ejecucion) para analizar los resultados obtenidos
