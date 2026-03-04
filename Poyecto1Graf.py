#-*- coding: utf-8 -*-"""
"""
Programador: Oswaldo Zamora



                        #
                                #
                                            #
                                                        #
                                                                            #
"""

"""                                     BIBLIOTECAS                                 """

import os
import random
import math

import matplotlib.pyplot as plt


"""                                       CLASES                                    """


class Arista:
    def __init__(self, origen, destino, peso=None):
        self.origen = origen
        self.destino = destino
        self.peso = peso


class Nodo:

    def __init__(self, id, x=None, y=None):
        self.id = id
        self.x = x
        self.y = y
        self.vecinos = {}


class Grafo:

    def __init__(self, dirigido=False, nombre="G"):

        self.dirigido = bool(dirigido)
        self.nombre = str(nombre)
        self.nodos = {}

    def agregarNodo(self, nodo):

        self.nodos[nodo.id] = nodo

    def agregarArista(self, a, b, peso=None):

        if a == b:
            return

        if a not in self.nodos or b not in self.nodos:
            return

        nodoA = self.nodos[a]
        nodoB = self.nodos[b]

        if b in nodoA.vecinos:
            return

        nodoA.vecinos[b] = Arista(nodoA, nodoB, peso)

        if not self.dirigido:
            nodoB.vecinos[a] = Arista(nodoB, nodoA, peso)

    def obtenerAristas(self):

        lista = []
        vistos = set()

        for nodo in self.nodos.values():

            for v in nodo.vecinos:

                if self.dirigido:
                    lista.append(nodo.vecinos[v])

                else:
                    par = tuple(sorted((nodo.id, v)))

                    if par not in vistos:
                        vistos.add(par)
                        lista.append(nodo.vecinos[v])

        return lista

    def guardarGraphViz(self, archivo):

        operador = "->" if self.dirigido else "--"
        tipo = "digraph" if self.dirigido else "graph"

        texto = [f"{tipo} {self.nombre} {{"]

        for nid in sorted(self.nodos.keys()):
            nodo = self.nodos[nid]

            if nodo.x != None and nodo.y != None:
                texto.append(f'  {nodo.id} [pos="{nodo.x:.6f},{nodo.y:.6f}!"];')
            else:
                texto.append(f"  {nodo.id};")

        for arista in self.obtenerAristas():
            texto.append(f"  {arista.origen.id} {operador} {arista.destino.id};")

        texto.append("}")

        with open(archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(texto))

    def guardarPNG(self, archivo, posiciones=None, semilla=7):

        if posiciones == None:
            posiciones = {}

        # Si no hay posiciones (Erdos/Gilbert/Albert/Dorogovtsev), uso un layout force simple
        if not posiciones:
            posiciones = layoutForce(self, pasos=220, semilla=semilla)

        deg = grados(self)

        ids = sorted(self.nodos.keys())

        # resaltar los 6 con mayor grado (se ve bien y tiene sentido)
        top = sorted(ids, key=lambda i: deg.get(i, 0), reverse=True)[:6]
        top_set = set(top)

        aristas = self.obtenerAristas()

        # para grafos grandes, limitamos líneas para que no sea una mancha
        max_lineas = 6000 if len(ids) <= 500 else 15000
        if len(aristas) > max_lineas:
            aristas = aristas[:max_lineas]

        fig = plt.figure(figsize=(8, 7))
        ax = plt.gca()

        ax.set_facecolor("#2b2b2b")
        fig.patch.set_facecolor("#2b2b2b")

        # aristas verde menta translúcidas
        for e in aristas:
            x1, y1 = posiciones[e.origen.id]
            x2, y2 = posiciones[e.destino.id]
            ax.plot([x1, x2], [y1, y2], linewidth=0.6, alpha=0.20)

        # nodos con tamaño por grado
        xs = []
        ys = []
        sizes = []
        colors = []

        max_deg = max(deg.values()) if deg else 1

        for nid in ids:
            x, y = posiciones[nid]
            xs.append(x)
            ys.append(y)

            d = deg.get(nid, 0)

            base = 120
            extra = (d / max_deg) * 260 if max_deg > 0 else 0

            s = base + extra

            if nid in top_set:
                s *= 1.35
                colors.append("#0c6b3c")
            else:
                colors.append("#66c2a4")

            sizes.append(s)

        ax.scatter(xs, ys, s=sizes, c=colors, edgecolors="#1b1b1b", linewidths=1.2, alpha=0.95)

        # etiquetas (números) centradas
        for nid in ids:
            x, y = posiciones[nid]
            txt_color = "#e8fff4" if nid in top_set else "#d7fff0"
            ax.text(x, y, str(nid), fontsize=8, ha="center", va="center", color=txt_color)

        ax.set_axis_off()
        plt.tight_layout()
        plt.savefig(archivo, dpi=220, facecolor=fig.get_facecolor())
        plt.close()


"""                                 FUNCIONES AUXILIARES                              """


def grados(grafo):

    deg = {}

    for nid, nodo in grafo.nodos.items():
        deg[nid] = len(nodo.vecinos)

    return deg


def layoutForce(grafo, pasos=250, k=None, semilla=7):

    random.seed(semilla)

    ids = sorted(grafo.nodos.keys())
    n = len(ids)

    if n == 0:
        return {}

    pos = {i: (random.random(), random.random()) for i in ids}

    if k == None:
        k = 1.0 / math.sqrt(max(n, 2))

    edges = []
    for e in grafo.obtenerAristas():
        edges.append((e.origen.id, e.destino.id))

    for _ in range(pasos):

        disp = {i: [0.0, 0.0] for i in ids}

        # repulsión (para 50/200/500 va bien; para 5000 no la usamos en automático)
        for a in range(n):
            v = ids[a]
            x_v, y_v = pos[v]

            for b in range(a + 1, n):
                u = ids[b]
                x_u, y_u = pos[u]

                dx = x_v - x_u
                dy = y_v - y_u

                dist = math.sqrt(dx * dx + dy * dy) + 1e-9
                force = (k * k) / dist

                fx = (dx / dist) * force
                fy = (dy / dist) * force

                disp[v][0] += fx
                disp[v][1] += fy

                disp[u][0] -= fx
                disp[u][1] -= fy

        # atracción en aristas
        for (v, u) in edges:

            x_v, y_v = pos[v]
            x_u, y_u = pos[u]

            dx = x_v - x_u
            dy = y_v - y_u

            dist = math.sqrt(dx * dx + dy * dy) + 1e-9
            force = (dist * dist) / k

            fx = (dx / dist) * force
            fy = (dy / dist) * force

            disp[v][0] -= fx
            disp[v][1] -= fy

            disp[u][0] += fx
            disp[u][1] += fy

        temp = 0.05

        for v in ids:

            x, y = pos[v]
            dx, dy = disp[v]

            dist = math.sqrt(dx * dx + dy * dy) + 1e-9

            x += (dx / dist) * min(dist, temp)
            y += (dy / dist) * min(dist, temp)

            x = max(0.0, min(1.0, x))
            y = max(0.0, min(1.0, y))

            pos[v] = (x, y)

    return pos


"""                                       FUNCIONES                                    """


def grafoMalla(m, n, dirigido=False):

    if m <= 1 or n <= 1:
        return Grafo(dirigido)

    g = Grafo(dirigido)

    for i in range(m):
        for j in range(n):

            g.agregarNodo(Nodo(i*n + j, x=float(i), y=float(j)))

    for i in range(m):
        for j in range(n):

            u = i*n + j

            if i < m-1:
                g.agregarArista(u, (i+1)*n + j)

            if j < n-1:
                g.agregarArista(u, i*n + (j+1))

    return g


def grafoErdosRenyi(n, m, dirigido=False):

    if n <= 0:
        return Grafo(dirigido)

    g = Grafo(dirigido)

    for i in range(n):
        g.agregarNodo(Nodo(i))

    posibles = []

    if dirigido:

        for a in range(n):
            for b in range(n):
                if a != b:
                    posibles.append((a,b))

    else:

        for a in range(n):
            for b in range(a+1, n):
                posibles.append((a,b))

    if m > len(posibles):
        m = len(posibles)

    for a,b in random.sample(posibles, m):

        g.agregarArista(a,b)

    return g


def grafoGilbert(n, p, dirigido=False):

    if n <= 0:
        return Grafo(dirigido)

    g = Grafo(dirigido)

    for i in range(n):
        g.agregarNodo(Nodo(i))

    if dirigido:

        for i in range(n):
            for j in range(n):

                if i == j:
                    continue

                if random.random() <= p:
                    g.agregarArista(i,j)

    else:

        for i in range(n):
            for j in range(i+1, n):

                if random.random() <= p:
                    g.agregarArista(i,j)

    return g


def grafoGeografico(n, r, dirigido=False):

    if n <= 0:
        return Grafo(dirigido)

    g = Grafo(dirigido)

    coords = []

    for i in range(n):

        x = random.random()
        y = random.random()

        coords.append((x,y))

        g.agregarNodo(Nodo(i, x, y))

    # hashing espacial para que n=5000 sea viable
    cell = r
    if cell <= 0:
        return g

    buckets = {}

    for i, (x, y) in enumerate(coords):

        cx = int(x // cell)
        cy = int(y // cell)

        buckets.setdefault((cx, cy), []).append(i)

    r2 = r * r
    vec_celdas = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]

    if dirigido:

        for (cx, cy), ids in buckets.items():

            for i in ids:

                xi, yi = coords[i]

                for dx, dy in vec_celdas:

                    cand = buckets.get((cx + dx, cy + dy), [])

                    for j in cand:

                        if i == j:
                            continue

                        xj, yj = coords[j]

                        ddx = xi - xj
                        ddy = yi - yj

                        if ddx*ddx + ddy*ddy <= r2:
                            g.agregarArista(i, j)

    else:

        for (cx, cy), ids in buckets.items():

            for i in ids:

                xi, yi = coords[i]

                for dx, dy in vec_celdas:

                    cand = buckets.get((cx + dx, cy + dy), [])

                    for j in cand:

                        if j <= i:
                            continue

                        xj, yj = coords[j]

                        ddx = xi - xj
                        ddy = yi - yj

                        if ddx*ddx + ddy*ddy <= r2:
                            g.agregarArista(i, j)

    return g


def grafoBarabasiAlbert(n, d, dirigido=False):

    if n <= 0 or d <= 1 or d >= n:
        return Grafo(dirigido)

    g = Grafo(dirigido)

    for i in range(n):
        g.agregarNodo(Nodo(i))

    # primeros d conectados todos con todos
    for i in range(d):
        for j in range(i+1, d):

            g.agregarArista(i,j)

    # preferencia por grado
    for nuevo in range(d, n):

        pool = []

        for v in range(nuevo):

            grado = len(g.nodos[v].vecinos)
            pool += [v] * max(grado, 1)

        destinos = set()

        while len(destinos) < d:
            destinos.add(random.choice(pool))

        for v in destinos:
            if v != nuevo:
                g.agregarArista(nuevo, v)

    return g


def grafoDorogovtsevMendes(n, dirigido=False):

    if n < 3:
        return Grafo(dirigido)

    g = Grafo(dirigido)

    for i in range(n):
        g.agregarNodo(Nodo(i))

    # triángulo inicial
    g.agregarArista(0,1)
    g.agregarArista(1,2)
    g.agregarArista(2,0)

    for nuevo in range(3, n):

        arista = random.choice(g.obtenerAristas())

        g.agregarArista(nuevo, arista.origen.id)
        g.agregarArista(nuevo, arista.destino.id)

    return g


"""                                       RESULTADOS                                  """


def generarResultados(carpeta="Proyecto1-resultados"):

    os.makedirs(carpeta, exist_ok=True)

    # semilla fija para que sea reproducible
    random.seed(7)

    # 1) MALLA
    mallas = {50:(5,10), 200:(10,20), 500:(20,25)}

    for size,(m,n) in mallas.items():

        g = grafoMalla(m,n)

        gv = os.path.join(carpeta, f"1_gnmMalla_{size}.gv")
        png = os.path.join(carpeta, f"1_gnmMalla_{size}.png")

        g.guardarGraphViz(gv)

        pos = {i:(g.nodos[i].x/float(m), g.nodos[i].y/float(n)) for i in g.nodos}
        g.guardarPNG(png, pos)

    # 2) ERDOS
    for size in (50,200,500):

        # m razonable (>= n-1)
        m = 2*size

        g = grafoErdosRenyi(size, m)

        gv = os.path.join(carpeta, f"2_Erdos_{size}.gv")
        png = os.path.join(carpeta, f"2_Erdos_{size}.png")

        g.guardarGraphViz(gv)
        g.guardarPNG(png)

    # 3) GILBERT
    for size in (50,200,500):

        p = 0.06 if size==50 else (0.03 if size==200 else 0.012)

        g = grafoGilbert(size, p)

        gv = os.path.join(carpeta, f"3_Gilbert_{size}.gv")
        png = os.path.join(carpeta, f"3_Gilbert_{size}.png")

        g.guardarGraphViz(gv)
        g.guardarPNG(png)

    # 4) GEO SIMPLE (incluye 5000)
    for size in (50,200,500,5000):

        r = 0.12 if size==50 else (0.08 if size==200 else (0.05 if size==500 else 0.02))

        g = grafoGeografico(size, r)

        gv = os.path.join(carpeta, f"4_GeoSimple_{size}.gv")
        png = os.path.join(carpeta, f"4_GeoSimple_{size}.png")

        g.guardarGraphViz(gv)

        pos = {i:(g.nodos[i].x, g.nodos[i].y) for i in g.nodos}
        g.guardarPNG(png, pos)

    # 5) ALBERT (Barabasi-Albert)
    for size in (50,200,500):

        g = grafoBarabasiAlbert(size, 3)

        gv = os.path.join(carpeta, f"5_Albert_{size}.gv")
        png = os.path.join(carpeta, f"5_Albert_{size}.png")

        g.guardarGraphViz(gv)
        g.guardarPNG(png)

    # 6) DOROGOVTSEV
    for size in (50,200,500):

        g = grafoDorogovtsevMendes(size)

        gv = os.path.join(carpeta, f"6_Dorogovtsev_{size}.gv")
        png = os.path.join(carpeta, f"6_Dorogovtsev_{size}.png")

        g.guardarGraphViz(gv)
        g.guardarPNG(png)


if __name__ == "__main__":

    generarResultados()