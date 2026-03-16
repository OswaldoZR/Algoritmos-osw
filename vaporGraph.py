# -*- coding: utf-8 -*-
"""
Programador: Oswaldo Zamora Rodríguez.
Biblioteca para manejo y generación de grafos.
"""

import random
import copy
from math import sqrt


class Arista(dict):
    pass


class Nodo:
    def __init__(self,id,dirigido=False,ponderado=False,valor=None):
        self.id = id
        self.dir = dirigido
        self.pond = ponderado
        self.padre = None
        self.val = valor
        self.A = Arista()

    def copy(self):
        return copy.copy(self)

    def deepCopy(self):
        return copy.deepcopy(self)

    def __str__(self):
        des = ""
        con = "->" if self.dir else "--"
        for v in self.A:
            if self.pond:
                des += f'\n\t{self.id} {con} {v.id} [label="{self.A[v]}"];'
            else:
                des += f"\n\t{self.id} {con} {v.id};"
        return des

    def add(self,nodo,valor=1):
        peso = random.randrange(1,10) if self.pond else valor
        self.A[nodo] = peso
        if not self.dir:
            nodo.A[self] = peso

    def elim(self,nodo):
        self.A.pop(nodo,None)
        if not self.dir:
            nodo.A.pop(self,None)

    def getAristas(self):
        E=[]
        for nodo in self.A.keys():
            E.append((self,nodo,self.A[nodo]))
        return E


class Grafo:

    def __init__(self,id='G',num_nodos=10,dirigido=False,ponderado=False,init_valor=None):

        self.nodos=[Nodo(n,dirigido,ponderado,init_valor) for n in range(num_nodos)]
        self.card=len(self.nodos)
        self.id=id
        self.dir=dirigido
        self.pond=ponderado


    def __str__(self):

        descripcion=("digraph " if self.dir else "graph ") + str(self.id) + " {"
        usados=set()

        for nodo in self.nodos:
            for vecino in nodo.A:

                if not self.dir:
                    llave=tuple(sorted((nodo.id,vecino.id)))
                    if llave in usados:
                        continue
                    usados.add(llave)

                if self.pond:
                    descripcion+=f'\n\t{nodo.id} {"->" if self.dir else "--"} {vecino.id} [label="{nodo.A[vecino]}"];'
                else:
                    descripcion+=f'\n\t{nodo.id} {"->" if self.dir else "--"} {vecino.id};'

        descripcion+="\n}"
        return descripcion


    def addVert(self,v,by_id=False):

        if not by_id:
            self.nodos.append(v)
        else:
            i=0
            while i < self.card:
                if v.id <= self.nodos[i].id:
                    break
                i+=1
            self.nodos.insert(i,v)

        self.card=len(self.nodos)
        return v


    def addAri(self,a,b,dist=1):
        a.add(b,dist)


    def save(self,nombre="grafo",extension=".gv"):

        if not extension.startswith("."):
            extension="."+extension

        with open(nombre+extension,"w",encoding="utf-8") as archivo:
            archivo.write(str(self))

        return self


# =========================
# BFS
# =========================

    def BFS(self,s):

        getNodo=lambda t:self.nodos[t] if type(t)==int else t
        s=getNodo(s)

        T=Grafo("BFS",0,self.dir,self.pond)

        mapa={}
        visitados=set()
        cola=[s]

        mapa[s]=Nodo(s.id,self.dir,self.pond)
        T.addVert(mapa[s],True)

        visitados.add(s)

        while cola:

            actual=cola.pop(0)

            for vecino in actual.A:

                if vecino not in visitados:

                    visitados.add(vecino)
                    cola.append(vecino)

                    mapa[vecino]=Nodo(vecino.id,self.dir,self.pond)
                    T.addVert(mapa[vecino],True)

                    mapa[actual].add(mapa[vecino],actual.A[vecino])

        return T


# =========================
# DFS RECURSIVO
# =========================

    def DFS_R(self,s):

        getNodo=lambda t:self.nodos[t] if type(t)==int else t
        s=getNodo(s)

        T=Grafo("DFS_R",0,self.dir,self.pond)

        visitados=set()
        mapa={}

        def dfs(v):

            visitados.add(v)

            if v not in mapa:
                mapa[v]=Nodo(v.id,self.dir,self.pond)
                T.addVert(mapa[v],True)

            for u in v.A:

                if u not in visitados:

                    mapa[u]=Nodo(u.id,self.dir,self.pond)
                    T.addVert(mapa[u],True)

                    mapa[v].add(mapa[u],v.A[u])

                    dfs(u)

        dfs(s)

        return T


# =========================
# DFS ITERATIVO
# =========================

    def DFS_I(self,s):

        getNodo=lambda t:self.nodos[t] if type(t)==int else t
        s=getNodo(s)

        T=Grafo("DFS_I",0,self.dir,self.pond)

        visitados=set()
        pila=[s]
        mapa={}

        mapa[s]=Nodo(s.id,self.dir,self.pond)
        T.addVert(mapa[s],True)

        while pila:

            v=pila.pop()

            if v in visitados:
                continue

            visitados.add(v)

            vecinos=list(v.A.keys())
            vecinos.reverse()

            for u in vecinos:

                if u not in visitados:

                    mapa[u]=Nodo(u.id,self.dir,self.pond)
                    T.addVert(mapa[u],True)

                    mapa[v].add(mapa[u],v.A[u])

                    pila.append(u)

        return T


# =========================
# MODELOS DE GRAFOS
# =========================

def grafoMalla(m,n,dirigido=False):

    G=Grafo("Malla",m*n,dirigido)

    for i in range(m):
        for j in range(n):

            idx=i*n+j

            if j<n-1:
                G.nodos[idx].add(G.nodos[idx+1])

            if i<m-1:
                G.nodos[idx].add(G.nodos[idx+n])

    return G


def grafoErdosRenyi(n,m,dirigido=False):

    G=Grafo("Erdos",n,dirigido)

    posibles=[]

    for i in range(n):
        for j in range(i+1,n):
            posibles.append((i,j))

    elegidas=random.sample(posibles,min(m,len(posibles)))

    for a,b in elegidas:
        G.nodos[a].add(G.nodos[b])

    return G


def grafoGilbert(n,p,dirigido=False):

    G=Grafo("Gilbert",n,dirigido)

    for i in range(n):
        for j in range(i+1,n):

            if random.random()<=p:
                G.nodos[i].add(G.nodos[j])

    return G


def grafoGeografico(n,r,dirigido=False):

    G=Grafo("Geo",n,dirigido)

    coords=[(random.random(),random.random()) for _ in range(n)]

    for i in range(n):
        for j in range(i+1,n):

            x1,y1=coords[i]
            x2,y2=coords[j]

            if sqrt((x1-x2)**2+(y1-y2)**2)<=r:
                G.nodos[i].add(G.nodos[j])

    return G


def grafoBarabasiAlbert(n,d,dirigido=False):

    G=Grafo("Albert",n,dirigido)

    for i in range(d):
        for j in range(i+1,d):
            G.nodos[i].add(G.nodos[j])

    for i in range(d,n):

        existentes=G.nodos[:i]
        grados=[len(v.A)+1 for v in existentes]

        for _ in range(d):
            v=random.choices(existentes,weights=grados)[0]
            G.nodos[i].add(v)

    return G


def grafoDorogovtsevMendes(n,dirigido=False):

    G=Grafo("DM",n,dirigido)

    G.nodos[0].add(G.nodos[1])
    G.nodos[1].add(G.nodos[2])
    G.nodos[2].add(G.nodos[0])

    for i in range(3,n):

        aristas=G.nodos[random.randint(0,i-1)].getAristas()

        if aristas:
            a,b,_=random.choice(aristas)
            G.nodos[i].add(a)
            G.nodos[i].add(b)

    return G