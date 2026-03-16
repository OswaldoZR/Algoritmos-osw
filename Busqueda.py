# -*- coding: utf-8 -*-
"""
Programador: Oswaldo Zamora.

Este programa está hecho para poder calcular los arboles generados por la busqueda por
anchura y altura.
"""

import os
from vaporGraph import *


class Arbol(Grafo):
    def __init__(self,
                 algoritm,
                 grafo:Grafo,
                 nodo_s,
                 g_copy:bool=False,
                 id='A',
                 dirigido:bool=False) -> None:

        super().__init__(id,0,grafo.dir,grafo.pond,None)

        if g_copy:
            grafo = grafo.deepCopy()

        if algoritm == 0 or algoritm == "BFS":
            T = grafo.BFS(nodo_s)
        elif algoritm == 1 or algoritm == "DFS_R":
            T = grafo.DFS_R(nodo_s)
        else:
            T = grafo.DFS_I(nodo_s)

        self.id = id
        self.dir = T.dir
        self.pond = T.pond
        self.nodos = T.nodos
        self.card = T.card


def testBusqueda(func,*args,prefijo:str='',sufijo:str='',s=0):
    G = func(*args)
    G.save(prefijo+sufijo)
    Arbol("BFS",G,s,True,"BFS").save(prefijo+"_BFS_"+sufijo)
    Arbol("DFS_R",G,s,True,"DFS_R").save(prefijo+"_DFSR_"+sufijo)
    Arbol("DFS_I",G,s,True,"DFS_I").save(prefijo+"_DFSI_"+sufijo)


if __name__ == "__main__":
    if os.path.isdir("Proyecto2-resultados"):
        os.chdir("Proyecto2-resultados")

    testBusqueda(grafoMalla,5,6,prefijo="1_gnmMalla_30")
    testBusqueda(grafoMalla,10,10,prefijo="1_gnmMalla_100")
    testBusqueda(grafoMalla,20,25,prefijo="1_gnmMalla_500")

    testBusqueda(grafoErdosRenyi,30,100,prefijo="2_Erdos_30")
    testBusqueda(grafoErdosRenyi,100,400,prefijo="2_Erdos_100")
    testBusqueda(grafoErdosRenyi,500,2000,prefijo="2_Erdos_500")

    testBusqueda(grafoGilbert,30,0.3,prefijo="3_Gilbert_30")
    testBusqueda(grafoGilbert,100,0.3,prefijo="3_Gilbert_100")
    testBusqueda(grafoGilbert,500,0.3,prefijo="3_Gilbert_500")

    testBusqueda(grafoGeografico,30,0.3,prefijo="4_GeoSimple_30")
    testBusqueda(grafoGeografico,100,0.2,prefijo="4_GeoSimple_100")
    testBusqueda(grafoGeografico,500,0.12,prefijo="4_GeoSimple_500")

    testBusqueda(grafoBarabasiAlbert,30,4,prefijo="5_Albert_30")
    testBusqueda(grafoBarabasiAlbert,100,4,prefijo="5_Albert_100")
    testBusqueda(grafoBarabasiAlbert,500,4,prefijo="5_Albert_500")

    testBusqueda(grafoDorogovtsevMendes,30,prefijo="6_Dorogovtsev_30")
    testBusqueda(grafoDorogovtsevMendes,100,prefijo="6_Dorogovtsev_100")
    testBusqueda(grafoDorogovtsevMendes,500,prefijo="6_Dorogovtsev_500")