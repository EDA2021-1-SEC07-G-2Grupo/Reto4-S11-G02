"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import stack
import time
import tracemalloc



"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def print_separador_sensillo():
    print("---------------------------------------------------------------------------")
def print_separador_gigante():
    print("===========================================================================")

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory











def print_carga_de_datos_info(catalog,elemets):
    

    print("Cargando información de los archivos ....")
    print_separador_gigante()
    print("Se ha cargado un total de "+ str(gr.numEdges(catalog["connections"]))+" de conexiones entre arcos")
    print("Se ha cargado un total de "+str(gr.numVertices(catalog["connections"]))+" landing points conectados")
    print("Se ha cargado un total de "+str(controller.mpsize(catalog["info_countries"]))+" paises")
    print_separador_sensillo()
    print(("primer landing point cargado").upper())
    print_separador_sensillo()
    primer_elemeto=elemets[1][1]
    print("-identificador: "+str(primer_elemeto["landing_point_id"]))
    print("-nombre: "+str(primer_elemeto["name"]))
    print("-latitud: "+str(primer_elemeto["latitude"]))
    print("-longitud: "+str(primer_elemeto["longitude"]))
    print_separador_sensillo()
    elemento_final=elemets[1][2]
    print(("La ultimo landing point cargado:").upper())
    print_separador_sensillo()
    print("-identificador: "+str(elemento_final["landing_point_id"]))
    print("-nombre: "+str(elemento_final["name"]))
    print("-latitud: "+str(elemento_final["latitude"]))
    print("-longitud: "+str(elemento_final["longitude"]))
    print_separador_gigante()
   
    


# --------------------------------------------------------------------------------------
def print_req1(catalog,v1,v2):
    print_separador_gigante()
    elementos_imprimir=controller.req1(catalog,v1,v2)
    print(elementos_imprimir[1])
    print_separador_sensillo()
    print(elementos_imprimir[0])
    print_separador_sensillo()
    print_separador_gigante()

# --------------------------------------------------------------------------------------
def print_req2(catalog):


    print("Encontrando los landing point que sirven como punto de interconexión a más cables en la red...")
    lista_puntos_criticos=controller.req2(catalog)
    elementos=0
    for element in lt.iterator(lista_puntos_criticos):
        elementos+=1
        if elementos==11:
            break
        print("Nombre: "+str(element["name"]))
        print("País: "+str(element["Pais"]))
        print("Identificador: "+str(element["identificador"]))
        print("Conexiones a landing_point de diferentes cables: "+str(element["conectados"]))
        print_separador_sensillo()
    


 # --------------------------------------------------------------------------------------   
    
def print_req3(catalog, pais1, pais2):



    path=controller.req3(catalog,pais1,pais2)
    recorrido=0
    print_separador_gigante()
    print("Ruta:")
    print_separador_sensillo()
    if path is not None:
        if "No se ha encontrado los/el pais que está buscando " not in path:
            
            while (not stack.isEmpty(path)):
                point = stack.pop(path)
                recorrido+=int(point["weight"])
                print( "Landig Point A: "+str(controller.des_vertice(point["vertexA"]))+", "+" Landig Point B: "+str(controller.des_vertice(point["vertexB"]))+", "+" Distancia: "+str(point["weight"])+" km")
                print_separador_sensillo()
            print("El recorrido total es de: "+str(recorrido)+" km")
            print_separador_gigante()
        else:
            
            print(path)
            print_separador_gigante
           
            
    else:
        print_separador_sensillo()
        print("No se ha encontrado un camino")
        print_separador_gigante()

# --------------------------------------------------------------------------------------
def print_req4(catalog):
    info=controller.req4(catalog["connections"])
    print("Numero de nodos conectados:"+str(info[0]))
    print_separador_sensillo()
    print("Costo total de la red de expanción minima: "+str(info[1]))
    print_separador_sensillo()
    print("La conexión más larga es en dirección a "+str(info[2]["key"])+" con un costo de "+str(info[2]["value"]))
    print_separador_sensillo()
    print("La conexión más corta es en dirección a "+str(info[3]["key"])+" con un costo de "+str(info[3]["value"]))
    print_separador_sensillo()

# --------------------------------------------------------------------------------------
def print_req5(landing_point,catalog):
   
    datos=controller.req5(landing_point,catalog)
    print_separador_sensillo()
    if datos ==False:
        print("No existe el vertice que acaba de escribir")
        print_separador_sensillo()
    else:
        
        print(str(datos[0])+" paises serían afectados si el landing point "+str(landing_point)+" llega a fallar")
        print_separador_sensillo()
        print("Los paises directamente afectados serian: ")
        print_separador_sensillo()
        
        for element in lt.iterator(datos[1]):
            
                print("-"+str(element["Pais"])+", que está a: "+str(element["Distancia"]+"km"))
                print_separador_sensillo()
               
# --------------------------------------------------------------------------------------
def print_req6(catalog,country):
    pass
def printMenu():
    print("Bienvenido")
    print("1- Cargar Datos")
    print("2- Indentificación de clusters de comunicación ")
    print("3- Identificar los puntos de conexión críticos de la red")
    print("4- La ruta de menor distancia")
    print("5- Identificar la Infraestructura Crítica de la Red")
    print("6- Análisis de fallas")
 


def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog)


catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
                
     

        catalog = controller.initCatalog()
        elments=controller.loadData(catalog)
        print_carga_de_datos_info(catalog,elments)
        



    elif int(inputs[0]) == 2:
        landing_point1=input("Escriba el nombre del landing point 1: ")
        landing_point2=input("Escriba el nombre del landing point 2: ")

     




        print_req1(catalog,landing_point1,landing_point2)



    elif int(inputs[0]) == 3:

  


        print_req2(catalog)#FUNCIONA





    elif int (inputs[0])==4:
        pais1=str(input("Escriba el primer país "))
        pais2=str(input("Escriba el segundo país "))


        print_req3(catalog,pais1,pais2)
 


    elif int (inputs[0])==5:
        


        print_req4(catalog)
       

    elif int(inputs[0])==6:
        landing_point=str(input("Escriba la ciudad en la que se encuentra el landing point a consultar: "))




        print_req5(landing_point,catalog)



    else:
        sys.exit(0)
sys.exit(0)
