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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from App.controller import loadCountries
from typing import ClassVar
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.ADT.graph import gr
import haversine as hs
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """ Inicializa el analizador
   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        catalog = {
                    'stops': None,
                    'connections': None,
                    'components': None,
                    'paths': None
                    }
        #GRAFOS
        catalog['destinos'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)

        catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',#grafo adjacente
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareIds)

        #MAPAS
        catalog["info_countries"]=m.newMap(numelements=500,
                                            maptype="PROBING",
                                            comparefunction=compareIds)
        catalog["landing_point_id"]=m.newMap(numelements=500,
                                            maptype="PROBING",
                                            comparefunction=compareIds)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newCatalog')

# Funciones para agregar informacion al catalogo
# Funciones para hacer grafos
    
def addcountry(catalog,country):
        countries=country["CountryName"].split(",")
        for content in countries:
            addMap(catalog, content, country,"info_countries")


def addLanding_points(catalog,landing_point):
        lApoints=landing_point["landing_point_id"].split(",")
        for char in lApoints:
            addMap(catalog,char,landing_point,"landing_point_id")
        
def addConnection_graf(analyzer, lastservice, service):
 
    try:
        origin = vertex_name(lastservice)
        destination = vertex_name(service)
        distance = float(100)
        addpoint(analyzer, origin)
        addpoint(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        addRouteStop(analyzer, service)
        addRouteStop(analyzer, lastservice)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addConnection_graf')

def graf_country(catalog,lascontry, country):
    try: 
        origin = country_vertex(lastservice)
        destination = country_vertex(service)
        distance = float(hs.haversine(float(lascontry["CapitalLatitude"]),float(lascontry["CapitalLongitude"])))
        addpoint(catalog, origin)
        addpoint(catalog, destination)
        addConnection(catalog, origin, destination, distance)
        addnewpoint(catalog, lascontry)
        addnewpoint(catalog, country)
        return catalog


    except Exception as exp:
        error.reraise(exp, 'model:graf_country')


def country_vertex(country):
    name = country['CountryName'] + '-'
    name = name + country['CapitalName']
    return name

def addpoint(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], stopid):
            gr.insertVertex(analyzer['connections'], stopid)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addpoint')


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer

def addnewpoint(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
   
    entry = m.get(analyzer['destinos'], service['CountryName'])
    
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareIds)
        lt.addLast(lstroutes, service['CapitalName'])
        m.put(analyzer['destinos'], service['CountryName'], lstroutes)
    else:
        lstroutes = entry['value']
        
        info = service['CapitalName']
        
        if info not in lstroutes :
           
            lt.addLast(lstroutes, info)
        else:
            print(0)
           
    return analyzer


def addRouteStop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
   
    entry = m.get(analyzer['destinos'], service['\ufefforigin'])
    
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareIds)
        lt.addLast(lstroutes, service['cable_name'])
        m.put(analyzer['destinos'], service['\ufefforigin'], lstroutes)
    else:
        lstroutes = entry['value']
        
        info = service['cable_name']
        
        if info not in lstroutes :
           
            lt.addLast(lstroutes, info)
        else:
            print(0)
           
    return analyzer

def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = m.keySet(analyzer['destinos'])
    for key in lt.iterator(lststops):
        lstroutes = m.get(analyzer['destinos'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route




# Función para la creación de tablas de hash


def addMap(catalog, indexs, content,map_name):

    indices = catalog[map_name]
    existencia_indice = m.contains(indices, indexs)
    if existencia_indice:
        entry = m.get(indices, indexs)
        ind = me.getValue(entry)
    else:
        ind = estructure(indexs)
        m.put(indices, indexs, ind)
    lt.addLast(ind['song'], content)

"""ESTRUCTURAS"""


def vertex_name(service):
    """
    Nombre del vertice es la combinación del origen y el nombre del cable
    """
    name = service['\ufefforigin'] + '-'
    name = name + service['cable_name']
    return name

def length_sin_unidades(lastservice, service):
    """
        En caso que no exista un dato para la longitud del cable se remplaza por 0 y 
        se quita las unidades
    """

    if service['cable_length'] == 'n.a.':
        service['cable_length'] = 0
    elif service['cable_length'] != 'n.a.':
        numero_sin_units=service["cable_length"].split(" ")
        num=numero_sin_units[0].split(",")
        novo_num=""
        for char in num:
            novo_num+=char
        
        service["cable_length"]=novo_num
        
    if lastservice['cable_length'] == 'n.a.':
        lastservice['cable_length'] = 0
    elif lastservice['cable_length'] != 'n.a.':
        numero_sin_units=lastservice["cable_length"].split(" ")
        num=numero_sin_units[0].split(",")
        novo_num=""
        for char in num:
            novo_num+=char
        lastservice["cable_length"]=novo_num


def estructure(name):

    struct = {'name': "",
              "song": None,
              "Size": 0,
              }
    struct['name'] = name
    struct['song'] = lt.newList('ARRAY_LIST', compareIds )
    return struct




# Funciones de consulta

def mpsize(catalog):
    return m.size(catalog)

    



# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def compareIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1