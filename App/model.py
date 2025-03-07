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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.ADT.indexminpq import size
from DISClib.DataStructures.arraylist import addLast, firstElement, newList
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
from DISClib.Algorithms.Graphs import prim as prim
from DISClib.Algorithms.Graphs import bfs 
from DISClib.Utils import error as error
from DISClib.ADT.graph import gr
import haversine as hs
from DISClib.Algorithms.Sorting import mergesort as merg
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
        #Datos
        catalog["original_info"]=lt.newList(datastructure="ARRAY_LIST")
        #GRAFOS
        catalog['destinos'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)

        catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',#grafo adjacente
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIds)
        catalog["stos_cable_name"]= m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)

        #MAPAS
        catalog["info_countries"]=m.newMap(numelements=500,
                                            maptype="PROBING",
                                            comparefunction=compareIds)
        catalog["landing_point_id"]=m.newMap(numelements=500,
                                            maptype="PROBING",
                                            comparefunction=compareIds)
        catalog["ciudad_id"]=m.newMap(numelements=500,
                                            maptype="PROBING",
                                            comparefunction=compareIds)
        catalog["capital"]=m.newMap(numelements=500,
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
        ciudad=country["CapitalName"].split(",")
      
            
        if len(ciudad)==3:
            ciudad=(str(ciudad[0])+","+str(ciudad[1])+","+str(ciudad[2]))
        elif len(ciudad)==2:
            ciudad=(str(ciudad[0])+","+str(ciudad[1]))
        else:
            ciudad=str(ciudad[0])
       
        addMap(catalog, ciudad, country,"capital")


def addLanding_points(catalog,landing_point):
        lApoints=landing_point["landing_point_id"]
        
        addMap(catalog,lApoints,landing_point,"landing_point_id")
        ciudad=landing_point["name"].split(",")
        if len(ciudad)==5:
            ciudad=(str(ciudad[0])+","+str(ciudad[1])+","+str(ciudad[2])+","+str(ciudad[3]))
        elif len(ciudad)==4:
            ciudad=(str(ciudad[0])+","+str(ciudad[1])+","+str(ciudad[2]))
        elif len(ciudad)==3:
            ciudad=(str(ciudad[0])+","+str(ciudad[1]))
        elif len(ciudad)==2:
            ciudad=(str(ciudad[0]))
        else:
            ciudad=str(ciudad[0])
  
        
        addMap(catalog,ciudad,landing_point,"ciudad_id")





def addconnections(catalog,service):
    lt.addLast(catalog["original_info"],service)
        
def addConnection_graf(analyzer, service):
 
    try:
        pont1=pais(analyzer,service["\ufefforigin"])#PUNTO GRANDE QUE ES UN PAÍS
        pont2=pais(analyzer,service["destination"])#PUNTO GRANDE QUE ES EL POSIBLE SEGUNDO PAÍS
        
      

        ciudad1=ciudad(analyzer,service["\ufefforigin"])
        ciudad2=ciudad(analyzer,service["destination"])
       

        origin = vertex_name( ciudad1,service["\ufefforigin"])
        destination = vertex_name(ciudad2,service["destination"])

     

        distance = distance_haversine(analyzer,origin,destination)#Entre los 2 puntos
        distance=abs(distance)
        
       


        addpoint(analyzer, origin,"connections")
        addpoint(analyzer, destination,"connections")

        #PUNTOS ESPECIALES 
        addpoint(analyzer, pont1,"connections")
        addpoint(analyzer,pont2,"connections")

        #CONEXIONES
        addConnection(analyzer, origin, destination, distance,"connections")#conexion en las 2 rutas
       
        distance1=abs(distance_haversine_special(analyzer,origin,pont1))
       
        
       
        distance2=abs(distance_haversine_special(analyzer,origin,pont2))
    
       
        addConnection(analyzer, origin, pont1, distance1,"connections")
        addConnection(analyzer, destination, pont2, distance2,"connections")
        addConnection(analyzer, pont1,origin,  distance1,"connections")
        addConnection(analyzer, pont2,destination,  distance2, "connections")
        


        addnewpoint(analyzer, origin, destination)#TRABAJANDO EN ESTE PUNTO
        
        addnewpoint(analyzer, pont1,origin)
        addnewpoint(analyzer, pont2, destination)
        addnewpoint(analyzer,origin, pont1 )
        addnewpoint(analyzer, destination,pont2 )
        
        addRouteStop(analyzer, service["\ufefforigin"],service["cable_name"],"stos_cable_name")
        addRouteStop(analyzer, service["destination"],service["cable_name"],"stos_cable_name")
        
        #COMIENZO DEL GRAFO 2 ------------------------------------------------
       
       


        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addConnection_graf')




def addpoint(analyzer, stopid,name_analyzer):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer[name_analyzer], stopid):
            gr.insertVertex(analyzer[name_analyzer], stopid)
            
          
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addpoint')



def addConnection(analyzer, origin, destination, distance,name_analyzer):#CREO CONECCIONES PARA EL GRAFO CONNECTIONS

    """
    Adiciona un arco entre dos estaciones
    """
    
    if  "No city" in origin or "No Country" in destination or "No city" in destination:
    
        return analyzer
    
    else:
        edge = gr.getEdge(analyzer[name_analyzer], str(origin), str(destination))
     

        if edge is None:
            
        
            gr.addEdge(analyzer[name_analyzer], str(origin), str(destination), (distance))
    return analyzer

def addnewpoint(analyzer, service,conexion):

    
   
    entry = m.get(analyzer['destinos'], service)
  
    
    if entry is None:
        lstroutes = lt.newList(datastructure="ARRAY_LIST",cmpfunction=compareIds)
        lt.addLast(lstroutes, conexion )
        m.put(analyzer['destinos'], service, lstroutes)
    else:
        lstroutes = entry['value']
        
        info = str(service)
      
        if info not in lstroutes["elements"]:
           
            lt.addLast(lstroutes, info)
        
           
    return analyzer




def addRouteStop(analyzer, service,name,diccionario):#PARA AÑADIR EN LOS DICCIONARIOS DIRECTOS DE ID PAIS
    """

    """

    entry = m.get(analyzer[diccionario], service)

    
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareIds)
        lt.addLast(lstroutes, name)
        m.put(analyzer[diccionario], service, lstroutes)
    else:
        lstroutes = entry['value']
        
        info = name
        lt.addLast(lstroutes, info)
      
           
    return analyzer








# Función para la creación de tablas de hash


def addMap(catalog, indexs, content,map_name):#PARA CREAR MAPAS
  
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


def vertex_name(service,ciudad_name):#PARA EL GRAFO DE ID Y PAÍS
    """
    Nombre del vertice es la combinación del codio  y la ciudad 
    """


    name = service + '-'
    name = name+ciudad_name

    return name


def ciudad(catalog,service):#PARA ENCONTRAR EL PAÍS
    if m.contains(catalog["landing_point_id"],service)==True:
        lista=m.get(catalog["landing_point_id"],service)
        elemnto=lt.getElement(lista["value"]["song"],1)
        city=elemnto["name"].split(", ")
        if len(city)==3:
            ciudad_name=str(city[0])+", "+str(city[1])
        elif len(city)==4:
            ciudad_name=str(city[0])+", "+str(city[1]+", "+str(city[2]))
        else:
            ciudad_name=str(city[0])
    else:
        ciudad_name="No city"
       

    
    return ciudad_name


def pais(catalog,service):#PARA ENCONTRAR EL PAÍS

    if m.contains(catalog["landing_point_id"],service)==True:
        lista=m.get(catalog["landing_point_id"],service)
        elemnto=lt.getElement(lista["value"]["song"],1)
        city=elemnto["name"].split(", ")
        if len(city)==4:
                ciudad_name=city[3]
        elif len(city)==3:
                ciudad_name=city[2]
        elif len(city)==2:
                ciudad_name=city[1]
        else:
                ciudad_name=city[0]
        elementosss=m.get(catalog["info_countries"],ciudad_name)
        if elementosss==None:
            print(ciudad_name)
            return "No Country"
            
        else:
    
            especifico=lt.firstElement(elementosss["value"]["song"])
            ciudad_name=especifico["CapitalName"]
        
    else:
        ciudad_name="No Country"
        
        
   

    
    return ciudad_name

def length_sin_unidades( service):#TRANSFORMACIÓN COSTO DE GRAFO ID PAIS
    """
        En caso que no exista un dato para la longitud del cable se remplaza por 0 y 
        se quita las unidades
    """
  
    if service == 'n.a.':
        service = float(1000000)
    elif service != 'n.a.':
        numero_sin_units=service.split(" ")
        num=numero_sin_units[0].split(",")
        novo_num=""
        for char in num:
            novo_num+=char
        
        service =novo_num
      
        return float(service)
        
  


def estructure(name):#ESTRUCTURA MAPA

    struct = {'name': "",
              "song": None,
              "Size": 0,
              }
    struct['name'] = name
    struct['song'] = lt.newList('ARRAY_LIST', compareIds )
    return struct


def distance_haversine(catalog,lugar1,lugar2):
    lugar1=des_vertice(lugar1)
    lugar2=des_vertice(lugar2)
    datos_1=m.get(catalog["ciudad_id"],lugar1)
 

    datos_2=m.get(catalog["ciudad_id"],lugar2)

  
    if datos_1==None or datos_2==None:
    
        return  1000000000000000000
    else:
        dato1= lt.firstElement(datos_1["value"]["song"])
        dato2= lt.firstElement(datos_2["value"]["song"])

        lugar1=(float(dato1["latitude"]),float(dato1["longitude"]))
        lugar2=(float(dato2["latitude"]),float(dato2["longitude"]))
        return float(hs.haversine(lugar1,lugar2))
def des_vertice(v):
    
    v=v.split("-")
    if len(v)==3:
        
        return(v[0]+"-"+v[1])
    elif len(v)==4:
        
        return(v[0]+"-"+v[1]+"-"+v[2])
    elif len(v)==5:
        
        return(v[0]+"-"+v[1]+"-"+v[2]+"-"+v[3])
            
    else:
        return str(v[0])
    

          
def distance_haversine_special(catalog,lugar1,lugar2):
    

    lugar1=des_vertice(lugar1)
    lugar2=lugar2
    datos_1=m.get(catalog["ciudad_id"],lugar1)
    datos_2=m.get(catalog["capital"],lugar2)
    
    
    if datos_1==None or datos_2==None:
   
        return  1
    else:
        dato1= lt.firstElement(datos_1["value"]["song"])
        dato2= lt.firstElement(datos_2["value"]["song"])
        lugar1=(float(dato1["latitude"]),float(dato1["longitude"]))
        lugar2=(float(dato2["CapitalLatitude"]),float(dato2["CapitalLongitude"]))
        return float(hs.haversine(lugar1,lugar2))          


# Funciones de consulta

def mpsize(catalog):
    return m.size(catalog)

# COMPONENTES DE CONSULTA REQ 1:

    
def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['connections_scc'] = scc.KosarajuSCC(analyzer['connections'])
  
    return scc.connectedComponents(analyzer['connections_scc'])


def strongly_conected(catalog,v1,v2):

    if m.contains(catalog["connections_scc"]["idscc"],v1)==False or m.contains(catalog["connections_scc"]["idscc"],v2)==False:
        return False
    elif  scc.stronglyConnected(catalog["connections_scc"],v1,v2)==False:
        return 0
    elif  scc.stronglyConnected(catalog["connections_scc"],v1,v2)==True:
        return True
def vertices_buscables(catalog,v):
    elemento=m.get(catalog["ciudad_id"],v)
    if elemento==None:
        return v
    else:
       
        info=lt.firstElement(elemento["value"]["song"])
        return v+"-"+str(info["landing_point_id"])
    
#COMPONENTES DE CONSULTA REQ 2:
#


def consulta_conexion_criticos(catalog):
    critic_list=lt.newList(datastructure="ARRAY_LIST")
    landing_point_id=m.keySet(catalog["stos_cable_name"])
    for ids in lt.iterator(landing_point_id):
        temporary_list=[]
        info =m.get(catalog["stos_cable_name"],ids)

        for cables in lt.iterator(info["value"]):
            if cables not in temporary_list:
                temporary_list.append(cables)

        
        if len(temporary_list)>1:
            datos=m.get(catalog["landing_point_id"],info["key"])
            if datos !=None:
                first= datos["value"]["song"]
          
                name=first["elements"][0]["id"]
        
                pais=ciudad(catalog,info["key"])
                dato={"identificador":info["key"],"Pais":pais,"name":name,"conectados":str(len(temporary_list)) }
                lt.addLast(critic_list,dato)
    
    critic_list=merge_sort(critic_list,10,cmpfunction_merge_req2)
    return critic_list

# REQ3 -------------------------------------------------------------

def getcity(catalog,pais):
    info_pais=m.get(catalog["info_countries"],pais)
    if info_pais==None:
        return None
    else:
        elemento=lt.firstElement(info_pais["value"]["song"])
        return elemento["CapitalName"]

def dijkstra_path(catalog,ciudad1): 
    
     
        catalog['paths'] = djk.Dijkstra(catalog['connections'], ciudad1)
        return catalog
        
def dijkstra_llegada(catalog,ciudad2):
    path = djk.pathTo(catalog['paths'], ciudad2)
    return path
# REQ4

def prim_search(catalog):
     catalog["prim"] = prim.PrimMST(catalog)

     return catalog["prim"]

def nodos_totales(mst):
    return m.size(mst["marked"])

def ruta_min(mst):
    mst=mst["distTo"]
    keys=m.keySet(mst)
    suma=0.0
    for elementos in lt.iterator(keys):
        info = m.get(mst,elementos)
        
        suma+=info["value"]
    return suma
def conexion_larga(catalog,mst):
  
    componentes_analisar=lista_normal(mst["distTo"])
    catalog["mst_distTo_organizado"]=merge_sort(componentes_analisar,lt.size(componentes_analisar),cmpfunction_merge)
    return lt.firstElement(catalog["mst_distTo_organizado"])

def conexion_corta(catalog):
    return lt.getElement(catalog["mst_distTo_organizado"],lt.size(catalog["mst_distTo_organizado"]))


def lista_normal(mst):
    normal_list=lt.newList(datastructure="ARRAY_LIST")
    keys_ss=m.keySet(mst)
    for element in lt.iterator(keys_ss):
        lt.addLast(normal_list,m.get(mst,element))
    return normal_list

        
def cmpfunction_merge(vertex1, vertex2):

    return (float(vertex1["value"]) > float(vertex2["value"]))

def cmpfunction_merge_req5(vertex1, vertex2):

    return (float(vertex1["Distancia"]) > float(vertex2["Distancia"]))
def cmpfunction_merge_req2(vertex1, vertex2):

    return (float(vertex1["conectados"]) > float(vertex2["conectados"]))

def merge_sort(lista,size,compare_funct):
    sub_list = lt.subList(lista,0, size)
    sub_list = lista.copy()
    sorted_list=merg.sort(sub_list, compare_funct)
    return  sorted_list


#REQ5
def exsitencia(catalog,vertice):
    return m.contains(catalog["destinos"],vertice)

    
def landing_paises(catalog,lista,vertice):
    newlist=lt.newList(datastructure="ARRAY_LIST")

    lst_element=[]
    for element in lt.iterator(lista):
        distancia=gr.getEdge(catalog["connections"],element,vertice)
        ciudad=des_vertice(element)
        lista_grande=m.get(catalog["ciudad_id"],ciudad)
        if lista_grande!=None:
            dato=lt.firstElement(lista_grande["value"]["song"])
            pais=dato["name"].split(",")
            if len(pais)>2:
                if  pais[2] not in lst_element:
                    info={"Pais":str(pais[2]),"Distancia": str(round(float(distancia["weight"]),2))}
                    lt.addLast(newlist,info)
                    lst_element.append(pais[2])
            elif len(pais)==2:
                if pais[1] not in lst_element:
                    info={"Pais":str(pais[1]),"Distancia": str(round(float(distancia["weight"]),2))}
                    lt.addLast(newlist,info)
                    lst_element.append(pais[1])
            else:
                if pais[0] not in lst_element:
                    info={"Pais":str(pais[0]),"Distancia": str(round(float(distancia["weight"]),2))}
                    lt.addLast(newlist,info)
                    lst_element.append(pais[0])
  
    return newlist


def lista_paises_afectados(vertice,catalog):
    conexiones_directas= gr.adjacents(catalog["connections"],vertice)
    transform_landing_to_paises=landing_paises(catalog,conexiones_directas,vertice)
    return lt.size(transform_landing_to_paises),transform_landing_to_paises
    




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