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


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""



def print_carga_de_datos_info(catalog):
    print("Cargando información de los archivos ....")
    print("Se han cargado un total de "+ str(gr.numEdges(catalog["connections"]))+" de arcos conectados")
    print("Se han cargado un total de "+str(gr.numVertices(catalog["connections"]))+" landing points (vertices)")
    
    print("Se han cargado un total de "+str(controller.mpsize(catalog["info_countries"]))+" paises")
    print("Primer landing pont cargado:")
    print("-identificador")
    print("-nombre")
    print("-latitud")
    print("-longitud")
    print("La ultima información cargada")



def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Cantidad de clusters dentro de la red de cables submarinos")


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
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()
        controller.loadData(catalog)
        print_carga_de_datos_info(catalog)
        
    elif int(inputs[0]) == 2:
        landing_point1=input("Escriba el nombre del landing point 1")
        landing_point2=input("Escriba el nombre del landing point 2")

    else:
        sys.exit(0)
sys.exit(0)
