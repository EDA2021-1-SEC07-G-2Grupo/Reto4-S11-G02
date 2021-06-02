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


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def print_separador_sensillo():
    print("___________________________________________________________________________")
def print_separador_gigante():
    print("===========================================================================")


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
   
    



def print_req1(catalog,v1,v2):
    
    print('El número total de componentes conectados es: ' +
        str(controller.connectedComponents(catalog)))
  
    print(str(controller.strongly_conected(catalog["connections"],v1,v2)))


def print_req2(catalog):




    print("Encontrando los landing point que sirven como punto de interconexión a más cables en la red...")
    lista_puntos_criticos=controller.consulta_conexion_criticos(catalog)
    for element in lt.iterator(lista_puntos_criticos):
        print("Nombre: "+str(element["name"]))
        print("País: "+str(element["Pais"]))
        print("Identificador: "+str(element["identificador"]))
        print("Conexiones a landing_point de diferentes cables: "+str(element["conectados"]))
        print_separador_sensillo()


    
    
def print_req3(catalog, pais1, pais2):



    path=controller.req3(catalog,pais1,pais2)
    
    if path is not None:
        if "No se ha encontrado los/el pais que está buscando " not in path:
            pathlen = stack.size(path)
            print('El camino es de : ' + str(pathlen)+' km. ')
            while (not stack.isEmpty(path)):
                point = stack.pop(path)
                print(point)
        else:
            print(path)
    else:
        print("No se ha encontrado un camino")


    
def print_req4(catalog):
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
    else:
        sys.exit(0)
sys.exit(0)
