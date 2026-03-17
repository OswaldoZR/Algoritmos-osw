Posible causa técnica

Gephi, al importar DOT, no siempre maneja bien la sintaxis de listas {...}.

En un árbol BFS, como cada nodo tiene un único padre, Gephi puede estar leyendo dos veces la misma arista:

Una vez desde la definición del nodo padre.

Otra vez desde la definición del hijo.

Eso genera la advertencia de “aristas paralelas” y, en el layout, parece que “se inventa” conexiones.

Por qué solo en BFS

En un árbol BFS, la estructura es muy regular: cada nodo aparece exactamente una vez como hijo.

Esto hace más evidente la duplicación, porque Gephi interpreta que (0,4) y (4,0) son dos aristas distintas aunque deberían ser la misma.

En otros grafos más densos, esa duplicación queda “oculta” entre muchas aristas y no dispara la advertencia.