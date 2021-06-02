﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros




def initCatalog():
    """

    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    yeah=loadLanding_points(catalog)
    loadCountries(catalog)
    
    loadConnections(catalog)
    
    
    
   
    return catalog,yeah

  

def loadConnections(catalog):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.
    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + "connections.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice=None
    for service in input_file:
        model.addconnections(catalog,service) 
               
        model.addConnection_graf(catalog, service)
      
     
        
  

    return catalog 


def loadCountries(catalog):
    servicesfile = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")

    for country in input_file:
        model.addcountry(catalog,country)
      

    #for country in servicesfile:
    return catalog 


def loadLanding_points(catalog):
    servicesfile = cf.data_dir + "landing_points.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for char in input_file:
        inicial=char
        break 
   
    for landing_pointss in input_file:
        model.addLanding_points(catalog,landing_pointss)
    
    
    final=landing_pointss
    

    
    
    return catalog,inicial,final

# Funciones de ordenamiento
#REQUERIMIENTOS

# Funciones de consulta sobre el catálogo
def mpsize(catalog):
    return model.mpsize(catalog)


def first_map_element(catalog):
    return model.first_map_element(catalog)

def consulta_conexion_criticos(catalog):
    return model.consulta_conexion_criticos (catalog) 


    

def req1(catalog,v1,v2):

    cantidad=model.connectedComponents(catalog)
    cantidad="El número total de componentes conectados es: "+str(cantidad)
    v1=model.vertices_buscables(catalog,v1)
    v2=model.vertices_buscables(catalog,v2)
    

    T_f= model.strongly_conected(catalog,v1,v2)
    if  T_f==True:
        texto= ("Los componentes están en el mismo cluster.")
        return texto,cantidad
    elif T_f==0:
        texto= ("los componentes no están en el mismo cluster.")
        return texto,cantidad
    elif T_f== False:
        texto=("No existe/existen los vertices mencionados")
        return texto,cantidad
        

def req3(catalog,pais1,pais2):
    ciudad1=model.getcity(catalog,pais1)
    ciudad2=model.getcity(catalog,pais2)
   
    if ciudad2 != None or ciudad1 != None:

        model.dijkstra_path(catalog,ciudad1)
        min_cost_to_2= model.dijkstra_llegada(catalog,ciudad2)
        return min_cost_to_2
    else:
        return "No se ha encontrado los/el pais que está buscando "