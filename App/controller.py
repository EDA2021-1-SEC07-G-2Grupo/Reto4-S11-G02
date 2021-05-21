"""
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
               
            model.addConnection_graf(catalog, service)
            
        
    model.addRouteConnections(catalog)

    return catalog 


def loadCountries(catalog):
    servicesfile = cf.data_dir + "countries.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice=None
    for country in input_file:
        model.addcountry(catalog,country)
        if lastservice is not None:
            sameservice = lastservice['CountryName'] == country['CountryName']
            samedirection = lastservice['CapitalName'] == country['CapitalName']
            samebusStop = lastservice['CapitalName'] == country['CapitalName']
            if sameservice and samedirection and not samebusStop:
                model.addConnection_graf(catalog, lastservice, country)
        lastservice = country
    model.addRouteConnections(catalog)

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

# Funciones de consulta sobre el catálogo
def mpsize(catalog):
    return model.mpsize(catalog)
def first_map_element(catalog):
    return model.first_map_element(catalog)

def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)