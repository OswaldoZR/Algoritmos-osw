#-*- coding: utf-8 -*-"""
"""
Programador: Oswaldo Zamora.

Este programa está hecho para poder manejar grafos

                        #
                                #
                                            #
                                                        #
                                                                            #
"""

"""                                     BIBLIOTECAS                                 """
from ast import Return
from ctypes import Array
from itertools import count
from math import sqrt
import random
import string
from collections import UserDict
from tkinter import SE
from unittest import skip
import copy

"""                                       CLASES                                    """

# Clase para manejar las aristas.
class Arista(dict):
    pass;

# Clase para el manejo de nodos, cada nodo gestiona sus aristas.
class Nodo:
    def __init__(self,id,dirigido:bool = False, ponderado:bool = False, valor=None) -> None:
        self.id = id            # Identificador del nodo.
        self.dir = dirigido     # Determina si pertenece a un grafo dirigido o no dirigido
        self.pond = ponderado   # ¿Sus aristas están ponderadas?
        self.padre = None;      # Guarda un registro de su antesesor en el caso de los árboles.
        self.val = valor        # Valor que se le desee darle a los nodos
        self.A = Arista()       # Diccionario Nodo: ponderación, si es grafo simple => ponderación = 0.
        pass;

    def copy(self):
        return copy.copy(self);

    def deepCopy(self):
        return copy.deepcopy(self);

    def __str__(self) -> str:
        if self.pond:           # para mostrar información más detallada
            des = ''
            for v in self.A:
                des += f"\n\t{self.id.__str__()}"+(f"({self.val.__str__()})" if self.val != None else '')# ID del saliente.
                des += f" -{'>' if self.dir else '-'} " # Flecha o linea.
                des += f"{v.id.__str__()}"+(f"({self.val.__str__()})" if self.val != None else '')+';'   # ID del entrante.
                des += f" [label=\"{self.A[v].__str__()}\"]"
            return des;
        des = f"\n\t{self.id} -{'>' if self.dir else '-'} "             # Imprime según es o no dirigido.
        des += '{'
        for v in self.A:                                # Para cada clave del diccionario.
            des += v.id.__str__() + ' '                 # El objeto id debe tener funcion __str__
        des += '};'
        return des;                                     # Debuelve toda la cadena.


    # Añade una arista ó actualiza el valor de una ya existente.
    def add(self,nodo,valor = 1) -> None:
        peso = random.randrange(1,10) if self.pond else valor;
        self.A[nodo] = peso     # Añade la clave o la rescribe.
        if not self.dir : nodo.A[self] = peso          # Solo si es no dirigido (doble sentido).
    pass;

    # Elimina un nodo de sus conecciones (elimina arista)
    def elim(self,nodo) -> None:
        self.A.pop(nodo)
        if not self.dir : nodo.A.pop(self);
    
    # Elmina la arista que se relaciona con un nodo.
    def cut(self,nodo) -> None:
        self.A.pop(nodo,None)                           # None es para que no devuelva error si no existe.
        if not self.dir: nodo.A.pop(self,None)          # Solo para no dirigidos.
        pass;

    # Indica si el nodo 'a' está conectado a 'b'
    def isConected(self,b) -> bool:
        return b in self.A;

    # Devuelve una lista de aristas que maneja en forma de tupla.
    def getAristas(self):
        E = []
        for nodo in self.A.keys():
            E.append( (self,nodo,self.A[nodo]) )        # (a,b,peso)
        return E;

    # Devuelve una lista de aristas que maneja en forma de tupla usando el id de los objetos.
    def getDebugAristas(self):
        E = []
        for nodo in self.A.keys():
            E.append( (self.id,nodo.id) )
        return E;
    pass;


# Pila ponderada de vertices.
class PilaPond(list):
    # Inicializador.
    def __init__(init_list:list = []):
        super().__init__(init_list);
    # Meter un elemento.
    def append(self, v:Nodo):
        if len(self) == 0:
            self.insert(0,v)
            return 0;
        izq:int = 0                                     # Limite izquierdo de la búsqueda.
        der:int = len(self) - 1                         # Limite derecho de la búsqueda.
        while izq <= der:                               # Mientras no explore todo el array.
            i = izq + (der - izq)//2                    # i toma el valor de la mitad.
            if v.val >= self[i].val:                    # Si es el nodo buscado.
                self.insert(i+1,v)                      # Lo agrega después del nodo i.
                return 0;
            elif self[i].val < v.val:                   # Si el pibote está a ala izquierda del nodo.
                izq = i + 1                             # El limite izq ahora está a la der de i.
            else:
                der = i - 1                             # El limite der está a la izq de i.
        self.insert(i,v)
        return -1;                                      # Si no lo encuentra retorna -1.

    # Para trabajar aristas tipo tupla (a,b,peso)
    def appendAri(self,a):
        if len(self) == 0:
            self.insert(0,a)
            return 0;
        izq:int = 0                                     # Limite izquierdo de la búsqueda.
        der:int = len(self) - 1                         # Limite derecho de la búsqueda.
        while izq <= der:                               # Mientras no explore todo el array.
            i = izq + (der - izq)//2                    # i toma el valor de la mitad.
            if a[2] >= self[i][2]:                      # Si es el nodo buscado.
                self.insert(i+1,a)                      # Lo agrega después del nodo i.
                return 0;
            elif self[i][2] < a[2]:                     # Si el pibote está a ala izquierda del nodo.
                izq = i + 1                             # El limite izq ahora está a la der de i.
            else:
                der = i - 1                             # El limite der está a la izq de i.
        self.insert(i,a)
        return -1;                                      # Si no lo encuentra retorna -1.


# Clase grafo encargado de crear los nodos que se neciesiten y tenerlos en una lista acorde al ID.
class Grafo:
    def __init__(self,id='G', num_nodos:int = 10,dirigido:bool = False, ponderado:bool = False, init_valor=None) -> None:
        self.nodos = [Nodo(n,dirigido,ponderado,init_valor) for n in range(num_nodos)]  # Creo los nodos.
        self.card = len(self.nodos)                     # Cardinalidad o numero de nodos.
        self.id = id                                    # Identificador del grafo.
        self.dir = dirigido                             # Si es o no un grafo dirigido.
        self.pond = ponderado                           # Tiene ponderaciones?
        self.posibles = self.card**2 if self.dir else ((self.card-1)**2+(self.card-1))/2# La cantidad de aristas que pueden existir.
        pass;

    def __str__(self) -> str:
        descripcion = ("digraph " if self.dir else "graph ") + self.id.__str__() + " {"
        if self.pond:
            for nodo in self.nodos:
                descripcion += f"\n\t{nodo.id.__str__()}"+(f"({nodo.val.__str__()})" if nodo.val != None else '')
                #descripcion += f" [valor = {nodo.val.__str__()}];"
        for nodo in self.nodos:                         # Manda a expresar las aristas de cada nodo.
            descripcion += f"{nodo.__str__()}";
        descripcion += "\n}"                            # Cierra la descripción del grafo.
        return descripcion;                             # Retorna el string

    def copy(self):
        return copy.copy(self);

    def deepCopy(self):
        return copy.deepcopy(self);

    # Busca un nodo por su id, mediante busqueda binaria
    def searchNodo(self,v):
        izq:int = 0                                     # Limite izquierdo de la búsqueda.
        der:int = self.card - 1                         # Limite derecho de la búsqueda.
        while izq <= der:                               # Mientras no explore todo el array.
            i = izq + (der - izq)//2                    # i toma el valor de la mitad.
            if self.nodos[i].id == v.id:                # Si es el nodo buscado.
                return i;
            elif self.nodos[i].id < v.id:               # Si el pibote está a ala izquierda del nodo.
                izq = i + 1                             # El limite izq ahora está a la der de i.
            else:
                der = i - 1                             # El limite der está a la izq de i.
        return -1;                                      # Si no lo encuentra retorna -1.

    # Indica si la arista (a,b) existe, o si el nodo 'a' pertenece al grafo.
    def exist(self,a,b=None) -> bool:
        return b in a.A if b!=None else self.searchNodo(a) >= 0;   # La clave 'b' está en el diccinario de 'a'?

    # Sobrescribo el operador 'in' para usar con Aristas (tuplas) o nodos (clase Nodo), para saber si pertenece al grafo.
    def __contains__(self,item):
        return item[1] in item[0].A if type(item) != Nodo else self.searchNodo(item) >= 0;

    # Agrega un nodo al grafo.
    def addVert(self,v,by_id:bool=False):
        if (not by_id) or self.nodos == []:
            self.nodos.append(v)
        else:
            i=0
            while(i<self.card):
                if v.id <= self.nodos[i].id: break
                i += 1;
            self.nodos.insert(i,v)
        self.card = len(self.nodos)
        self.posibles = self.card**2 if self.dir else ((self.card-1)**2+(self.card-1))/2# La cantidad de aristas que pueden existir.
        return v;

    # Añade una arista al grafo.
    def addAri(self,a,b,dist):
        a.add(b,dist);

    # Para trabajar tuplas (a,b,peso) vease getAristas()
    def delAri(self,arista):
        arista[0].elim(arista[1])

    # Ingresa un valor a todos los nodos del grafo.
    def setAll(self,valor,fun = None):
        if fun == None:
            for i in range(self.card):
                try:
                    self.nodos[i].val = valor.copy();   # Para que sus modif. sean indep.
                except AttributeError:
                    self.nodos[i].val = valor;          # Si no tiene función copy
        else:
            for i in range(self.card):
                self.nodos[i].val = fun(i,valor);
        return self;

    def getAristas(self,ordenadas = True):
        lista = []
        for nodo in self.nodos:
            if self.dir:
                lista += nodo.getAristas()              # A cada nodo le pregunta y agrega sus aristas.
            else:
                aristas = nodo.getAristas()
                for arista in aristas:                  # Verifica que las aristas no se repitan pero al revés.
                    if not (arista[1],arista[0],arista[2]) in lista:
                        lista.append(arista)            # Agrega arista por arista.

        if ordenadas:
            switch = True
            while switch:
                switch = False
                for i in range(1,len(lista)):
                    if lista[i-1][2] > lista[i][2]:
                        lista[i-1] , lista[i] = lista[i] , lista[i-1]
                        switch = True
        return lista;

    # Guarda el contenido del grafo.
    def save(self,nombre:str = "vapor", extension:str = ".gv"):
        # Validar que la extensión comience con punto.
        if not extension.startswith('.'):
            extension = '.' + extension
        # Construir el nombre completo del archivo
        nombre_archivo = nombre + extension
        # Escribir contenido en el archivo
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(self.__str__())
            print(f"Archivo guardado como: {nombre_archivo}")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
        return self;






    # Conecta un grafo gnm malla.
    def gnmalla(self, n:int = 10,m:int = 10):
        for i in range(self.card):
            #print(i,end = ' ')
            if i%n<n-1:         # Columnas.
                self.nodos[i].add(self.nodos[n*(i//n) + (i+1)%n])
                #                                j       i+1
            #else:
                #print('\n',end='')
            if i//n < m-1:      # Filas (j<m-1).
                self.nodos[i].add(self.nodos[n*((i+n)//n) + (i%n)])
                #                                j+1          i
            #print(f"{i} -> {i//n < m-1}")
            #print(f"\t + {n*( (i+n)//n ) + (i%n)}")
        return self;

    # Conecta un grafo a partir del modelo Erdős–Rényi.
    def gnm(self,m:int = 10):
        # Por si piden cosas raras xd...
        if( m > self.posibles ):
            print("No pueden existir tantas aristas diferentes!")
            return self;
        # Preparaciones para trabajar O(n^2)...
        V = self.nodos.copy()   # Nodos que tienen posiblidad de crear aristas.
        self.setAll(V,lambda i,valor:valor[:i] +valor[i+1:])                # Ingreso la posibilidad de conectar todos los nodos entre si.
        # Crea las m aristas O(m)...
        i:int = 0               # ninguna arista creada.
        while(i < m):
            # Eligo mis elmentos...
            a = random.choice(V)            # Elijo uno de los que tienen posibilidad.
            #print(f" {i}... {a.id}")
            #print(f"\t{a.id} -> {[n.id for n in a.val]}")
            b = random.choice(a.val)        # Elijo cualquier nodo posible a emparejar.
            #print("\t(",a,',',b,")")
            #print(f"\t{a.id} -> {[n.id for n in a.val]}")
            #print(f"\t{b.id} -> {[n.id for n in b.val]}")
            # Creo la arista...
            a.add(b)                        # Creo la arista.
            # Elmino la posibilidad de crear nuevamente esa arista...
            a.val.remove(b)                 # Elimino la posiblidad de (a,b)
            if not self.dir:    # Si es no dirigido,
                b.val.remove(a) # Elimino la posiblidad (b,a).
                if b.val == []: # Si ya no puede conectarse,
                    V.remove(b) # Elimina la posiblididad de ser elegido.
                    print([x.id for x in V])
            # Si ya no es posible crear más aristas con 'a'.
            if a.val == []:     # Si ya no es posible conectar con ningun nodo a 'a',
                V.remove(a)     # Elimino a 'a' de la lista de nodos con posibilidad.
                print([x.id for x in V])
            i += 1              # Indico que ya creé una arista.
        return self; # O(n^2+m) para tiempo, O(n^2) para espacio.

    # crea un grafo con el modelo Gn,p de Gilbert
    def gnp(self,p:float = 0.5):
        if (p > 1 or p <= 0):
            if p != 0:
                print("ERROR!! La probabilidad debe variar entre 0 y 1")
            return self;
        # Preparaciones para trabajar O(n^2)...
        V = self.nodos.copy()   # Nodos que tienen posiblidad de crear aristas.
        self.setAll(V,lambda i,valor:valor[:i] +valor[i+1:])                # Ingreso la posibilidad de conectar todos los nodos entre si.
        del V
        # Crea las m aristas O(m)...
        for v in self.nodos:
            for u in v.val:
                if random.random() <= p:
                    # Creo la arista...
                    v.add(u)                        # Creo la arista.
                    # Elmino la posibilidad de crear nuevamente esa arista...
                    v.val.remove(u)                 # Elimino la posiblidad de (v,u)
                    if not self.dir:    # Si es no dirigido,
                        u.val.remove(v) # Elimino la posiblidad (u,v).
        return self; # O(n^2)

    # Crea un grafo geografico simple.
    def gnr(self,r = 1,col:int = 2):
        fil = self.card//col -1             # Obtengo el numero de filas posibles.
        for vi in range(self.card):         # Para cada nodo.
            xi = vi%col         # Obtengo su posición en x.
            yi = vi//col        # Obtengo su posición en y.
            for vj in range(self.card):     # Reviso cada nodo si puede conectarse.
                xj = vj%col     # Obtengo su posición en x.
                yj = vj//col    # Obtengo su posición en x.
                if( r**2 < (xi-xj)**2 + (yi-yj)**2 ): continue              # Fuera del radio.
                if( (xi,yi) == (xj,yj) ): continue      # Es el mismo nodo.
                self.nodos[vi].add(self.nodos[vj])      # Lo conecto si cumple.
        return self;            # O(n^2)

    # Crea un grafo con el modelo Gnd Barabási-Albert
    def gnd(self,d:int = 1):
        # Verificaciones...
        if d == 1 or d > len(self.nodos):
            print("¡Valor no valido para d!")
            return self;
        # Conectamos los d nodos...
        for vi in self.nodos[:d]:
            for vj in self.nodos[:d]:
                if vi == vj: continue
                vi.add(vj)
                vi.val = len(vi.A)
                #print(vi.id,".",vi.val)
        # Calculo el numero de aristas...
        sk = d*(d-1) if self.dir else ((d-1)**2+(d-1))/2
        # Conectamos los nodos restantes...
        for vi in self.nodos[d:]:
            for vj in self.nodos[:vi.id]:
                pj = vj.val/sk
                if random.random() <= pj:
                    vi.add(vj)
                    sk += 1
                    vi.val += 1
        return self;

    # Crea un grafo con el modelo Gn Dorogovtsev-Mendes.
    def gn(self):
        n = self.card
        if n<3:
            print("Se requieren minimo 3 nodos para este algoritmo!!!")
            return self;
        for i in range(3):
            self.nodos[i].add(self.nodos[(i+1)%3])
        conteo = 3;
        triangulo = [ x.getAristas() for x in self.nodos[:3]]
        aristas = []
        for ar in triangulo:
            aristas += ar
        while(conteo<n):
            ari = random.choice(triangulo)[0]
            a = ari[0]
            b = ari[1]
            self.nodos[conteo].add(a)
            self.nodos[conteo].add(b)
            conteo += 1
        return self


    # Algoritmos de Dijkstra...
    def dijkstra(self,s):
        """
        Requiere que los nodos se inicialicen con None.
        """
        S = Grafo('S',0,self.dir,self.pond) # Grafo nuevo a generar.
        # Obtener el primer nodo de búsqueda
        getNodo = lambda t: self.nodos[t] if type(t) == int else t;
        pila = PilaPond()       # Pila ponderada (el de menor valor hasta arriba).
        actual = getNodo(s)     # Obtengo el nodo s.
        actual.val = 0          # Le pongo el valor 0 porque es el inicial.
        actual.padre = None     # Indico que no tiene padre.
        pila.append(actual)     # Lo agrego a la pila.
        actual = None           # Nungun seleccionado por el momento.
        # Ir recorriendo el grafo, según la pila...
        while pila:             # Mientras la pila no se vacie.
            # Selecciono el siguiente nodo...
            aux = pila.pop()    # Selecciono el sig en la pila.
            # Creo una copia con el valor original e indico al original que será explorado...
            aux2 = aux      # Uso aux2 como duplicado.
            aux = aux.copy()# Solo creo la copia.
            # Tratro los valores del elegido nodo para trabajar como el actual...
            aux.A = Arista()    # La copia ahora está desconectada.
            aux2.val = True # Altero el valor de visitado del original.
            # Trabajo con el nodo actual...
            if actual != None:  # Porque en el primer recorrido no hay actual.
                S.addVert(actual)           # Añado al nuevo grafo el nodo actual.
                aux.padre.add(aux) # Conecto el actual con el nodo elegido.
            actual = aux        # El nodo elegido ahora es el actual.
            for t in aux2.A:
                if t.val != True:           # Así sé que ya fue explorado y no lo tengo que buscar.
                    du = actual.val + aux2.A[t]      # d(u) + l_e (distancia entre el actual y la arista del nodo t)
                    if t.val == None:       # None == infinito
                        t.val = du          # Le pongo si o sí ese valor y quien se lo hereda.
                        t.padre = actual    # Le indico que su padre es el actual (su copia).
                        pila.append(t)      # Agrego ese nodo a la pila.
                    else:
                        if du < t.val:
                            t.padre = actual# asigno el padre que le herdará la minima.
                            t.val = du      # La minima dist. es la actual con la arista.
                        pila.append( pila.pop( pila.index(t) ) )            # Reordena el elemento en la pila.
        S.addVert(actual)           # Añado al nuevo grafo el nodo actual.
        return S;




    # TSM Algoritmo de Kruskal.
    def kruskalD(self):
        T = Grafo('T',0,self.dir,self.pond) # Grafo nuevo a generar.
        # Los nodos del grafo original tienen que estár ordenados.
        # Hacer una copia del conjunto de nodos...
        v_t = []
        for n in self.nodos:
            n.val = True
            n = n.copy()
            n.A = Arista()
            v_t.append(n)
        # Obtengo las arisats ordenadas...
        aristas = self.getAristas()
        count_a = 0                 # Para saber cuantas aristas tiene T
        # Exploro las aristas...
        for a in aristas:
            # Agrego las aristas si no están en T...
            if a[0].val:            # El primer nodo no está añadido?
                T.addVert(v_t[a[0].id],True)
                a[0].val = None     # Modifico el original para no volve a añadirlo.
                v_t[a[0].id].val = None;    # Añado la copia para que no quede con valor basura.
            if a[1].val:            # El segundo nodo no está?
                T.addVert(v_t[a[1].id],True)
                a[1].val = None     # Modifico el original para no volve a añadirlo.
                v_t[a[1].id].val = None;    # Añado la copia para que no quede con valor basura.
            # Agrego la arista...
            if count_a < T.card - 1:# Por propiedad de ser un árbol |V| = |E| + 1
                T.addAri(v_t[a[0].id],v_t[a[1].id],a[2])
                count_a += 1
        return T;

    # TSM Kruskal Inverso.
    def kruskalI(self):
        """
        Waring!! esta función modifica el grafo original.
        """
        # Obtengo las arisats ordenadas...
        aristas = self.getAristas()
        count_a = len(aristas)              # Para saber cuantas aristas tiene T
        # Empiezo a desconectar aristas...
        while count_a > self.card - 1:
            if aristas: a = aristas.pop()
            self.delAri(a)                  # Primero el chanclazo y luego pregunto xD
            self.setAll(None)
            if self.dijkstra(a[0]).card < self.card:    # Verifico con dijstra si lo desconecté.
                self.addAri(a[0],a[1],a[2]) # Justifico el chanclazo y le sobo xD
            else: count_a -= 1      # Ahora hay una arista menos.
        return self;

    # TSM con prim.
    def prim(self):
        T = Grafo('T',0,self.dir,self.pond) # Grafo nuevo a generar.
        # Los nodos del grafo original tienen que estár ordenados.
        # Hacer una copia del conjunto de nodos...
        v_t = []
        for n in self.nodos:
            n.val = True
            n = n.copy()
            n.A = Arista()
            v_t.append(n)
        # Creo una pila ponderada...
        pila = PilaPond()       # Pila ponderada (el de menor valor hasta arriba).
        vecino = self.nodos[0]  # Comienzo con el nodo 0 pero no importa con cual.
        # Do While la pila no esté vacia...
        while True:
            # Para cada arista en el nodo vecino...
            if vecino.val:
                for a in vecino.getAristas():
                    if (not a in pila) and ( True if self.dir else (not (a[1],a[0],a[2]) in pila) ):
                        pila.appendAri(a)   # La incerto.
                vecino.val = None
                v_t[vecino.id].val = None
                T.addVert(v_t[vecino.id])
            # Si ya tengo todos los nodos...
            if T.card == self.card: break;
            # Por seguridad...
            if len(pila) == 0: break;
            # Elijo la arista con menor peso...
            a = pila.pop(0)
            if a[1]:            # Si el sig. nodo no ha sido explorado...
                v_t[a[0].id].add(v_t[a[1].id],a[2])           # Añado la arista con las copias.
                vecino = a[1]   # Ahora el vecino es el sig.
        return T;
    pass;










"""                                       FUNCIONES                                    """
# 1. Crea un grafo en forma de malla. Crea m*n nodos. Para el nodo ni,j crear una arista con el nodo ni+1,j y otra 
def gnmMalla(n:int = 2,m:int = 5,dirigido:bool=False,grafo_name="G",pon = True):
    """
    Genera grafo de malla
    :param m: número de columnas (> 1)
    :param n: número de filas (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n*m,dirigido,pon).gnmalla(n,m);

# 2. Crea un grafo a partir del modelo Erdős–Rényi. Crea n nodos y elegir uniformemente al azar m distintos pares de distintos vértices.
def gErdosRenyi(n_nodos:int = 10,m_aristas:int =10,dirigido:bool = False,grafo_name = "G",pon=True):
    """
    Genera grafo aleatorio con el modelo Erdos-Renyi
    :param n: número de nodos (> 0)
    :param m: número de aristas (>= n-1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n_nodos,dirigido,pon).gnm(m_aristas);

# 3. Modelo Gn,p de Gilbert. Crear n nodos y poner una arista entre cada par independiente y uniformemente con probabilidad p.
def gGilbert(n:int = 10, p:float = 0.5, dirigido=False,grafo_name="G",pon=True):
    """
    Genera grafo aleatorio con el modelo Gilbert
    :param n: número de nodos (> 0)
    :param p: probabilidad de crear una arista (0, 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n,dirigido,pon).gnp(p);

# 4. Modelo Gn,r geográfico simple. Colocar n nodos en un rectángulo unitario con coordenadas uniformes (o normales)
# y colocar una arista entre cada par que queda en distancia r o menor.
def gGeografico(n:int=10, r:int=3, dirigido=False,grafo_name="G",columnas:int = 2,pon = True):
    """
    Genera grafo aleatorio con el modelo geográfico simple
    :param n: número de nodos (> 0)
    :param r: distancia máxima para crear un nodo (0, 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n,dirigido,pon).gnr(r,columnas);

# 5. Variante del modelo Gn,d Barabási-Albert. Colocar n nodos uno por uno, asignando a cada uno d aristas a vértices distintos
# de tal manera que la probabilidad de que el vértice nuevo se conecte a un vértice existente v es proporcional a la cantidad de aristas que v tiene actualmente los primeros d vértices se conecta todos a todos.
def gBarabasiAlbert(n, d, dirigido=False, grafo_name = 'G',pon=True):
    """
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (> 0)
    :param d: grado máximo esperado por cada nodo (> 1)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n,init_valor=0,dirigido=dirigido,ponderado=pon).gnd(d);

# 6. Crea un grafo con Dorogovtsev-Mendes. Crear 3 nodos y 3 aristas formando un triángulo.
# Después, para cada nodo adicional, se selecciona una arista al azar y se crean aristas entre
# el nodo nuevo y los extremos de la arista seleccionada.
def gDorogovtsevMendes(n, dirigido=False,grafo_name = "G",pon = True):
    """
    Genera grafo aleatorio con el modelo Barabasi-Albert
    :param n: número de nodos (≥ 3)
    :param dirigido: el grafo es dirigido?
    :return: grafo generado
    """
    return Grafo(grafo_name,n,dirigido,ponderado=pon).gn()

# Código que solo se ejecuta si este archivo se corre directamente.
if __name__ == "__main__":
    #G = Grafo('G',9,ponderado=True).gnmalla(3,3)
    #print(G)
    #print(G.prim().save("TestPrim"))
    # Resultados de malla...
    """G = gnmMalla(3,3)
    G.kruskalD().save("1_gnmMalla_kD_9")
    G.kruskalI().save("1_gnmMalla_kI_9")
    G.prim().save("1_gnmMalla_prim_9")
    G = gnmMalla(20,10).save("1_gnmMalla_200")
    G.kruskalD().save("1_gnmMalla_kD_200")
    G.prim().save("1_gnmMalla_prim_200")
    G.kruskalI().save("1_gnmMalla_kI_200")"""
    # Resultados de Erdős–Rényi...
    """G = gErdosRenyi(10,20).setAll(None).save("2_Erdos_Djk_10")
    G.kruskalD().save("2_Erdos_kD_10")
    G.prim().save("2_Erdos_prim_10")
    G.kruskalI().save("2_Erdos_kI_10")
    G = gErdosRenyi(200,20).setAll(None).save("2_Erdos_Djk_200")
    G.kruskalD().save("2_Erdos_kD_200")
    G.prim().save("2_Erdos_prim_200")
    G.kruskalI().save("2_Erdos_kI_200")"""
    # Resultados de Gilbert...
    """G = gGilbert(10,0.3).setAll(None).save("3_Gilbert_10")
    G.kruskalD().save("3_Gilbert_kD_10")
    G.prim().save("3_Gilbert_prim_10")
    G.kruskalI().setAll(None).save("3_Gilbert_kI_10")
    G = gGilbert(200,0.3).setAll(None).save("3_Gilbert_200")
    G.kruskalD().save("3_Gilbert_kD_200")
    G.prim().save("3_Gilbert_prim_200")
    G.kruskalI().setAll(None).save("3_Gilbert_kI_200")"""
    # Resultados de geográfico simple...
    """G = gGeografico(10,5,False,'GS',5).setAll(None).save("4_GeoSimple_10")
    G.kruskalD().save("4_GeoSimple_kD_10")
    G.prim().save("4_GeoSimple_prim_10")
    G.kruskalI().setAll(None).save("4_GeoSimple_kI_10")
    G = gGeografico(200,5,False,'GS',5).setAll(None).save("4_GeoSimple_200")
    G.kruskalD().save("4_GeoSimple_kD_200")
    G.prim().save("4_GeoSimple_prim_200")
    G.kruskalI().setAll(None).save("4_GeoSimple_kI_200")"""
    # Resultados de Barabási-Albert..."""
    """G = gBarabasiAlbert(10,4).setAll(None).save("5_Albert_10")
    G.kruskalD().save("5_Albert_kD_10")
    G.prim().save("5_Albert_prim_10")
    G.kruskalI().setAll(None).save("5_Albert_kI_10")
    G = gBarabasiAlbert(200,4).setAll(None).save("5_Albert_200")
    G.kruskalD().save("5_Albert_kD_200")
    G.prim().save("5_Albert_prim_200")
    G.kruskalI().setAll(None).save("5_Albert_kI_200") # No jala"""
    # Resultados de Dorogovtsev-Mendes...
    G = gDorogovtsevMendes(10).setAll(None).save("6_Dorogovtsev_10")
    G.kruskalD().save("6_Dorogovtsev_kD_10")
    G.prim().save("6_Dorogovtsev_prim_10")
    G.kruskalI().setAll(None).save("6_Dorogovtsev_kI_10")
    G = gDorogovtsevMendes(200).setAll(None).save("6_Dorogovtsev_200")
    G.kruskalD().save("6_Dorogovtsev_kD_200")
    G.prim().save("6_Dorogovtsev_prim_200")
    G.kruskalI().setAll(None).save("6_Dorogovtsev_kI_200")
    pass;
