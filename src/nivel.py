""" 
*Nombre de clase: nivel.py 
* Autora: Yolanda Galván Redondo 
* Release/Creation date:14 noviembre 2024 
* Version de esta clase: 10.2 
* Descripcion: esta es la clase nivel que tiene todos los elementos y su forma de interactuar unos con otros 
""" 
import hashlib
import re
from nodo import Nodo
from frontera import Frontera

class Nivel:
    def __init__(self, nivelText, id_nivel):
        self.id_nivel = id_nivel
        self.grid, self.nfila, self.ncol = self.crear_grid(nivelText)
        self.jugador, self.cajas, self.objetivos, self.muros = self.encontrar_elementos()

    def crear_grid(self, nivelText):
        filas = nivelText.split('\\n')
        grid = [list(fila) for fila in filas]
        nfila = len(grid)
        ncol = max(len(fila) for fila in grid) if nfila > 0 else 0
        return grid, nfila, ncol

    def encontrar_elementos(self):
        jugador = None
        cajas = []
        objetivos = []
        muros = []

        for fila in range(self.nfila):
            for columna in range(len(self.grid[fila])):
                celda = self.grid[fila][columna]
                if celda == '@':
                    jugador = (fila, columna)
                elif celda == '#':
                    muros.append((fila, columna))
                elif celda == '$':
                    cajas.append((fila, columna))
                elif celda == '.':
                    objetivos.append((fila, columna))
                elif celda == '+':
                    jugador = (fila, columna)
                    objetivos.append((fila, columna))
                elif celda == '*':
                    cajas.append((fila, columna))
                    objetivos.append((fila, columna))

        return jugador, cajas, objetivos, muros

    """
    Nombre del método:generar_sucesores

    Descripción del método:
        Genera la lista de estados sucesores a partir del estado actual
        o de una cadena de estado dada. Para cada movimiento posible
        (arriba, derecha, abajo, izquierda) calcula la nueva posición
        del jugador y, si hay una caja en esa posición, intenta empujarla.
        Además filtra los movimientos inválidos por muros o límites, crea cada
        nuevo estado y lo devuelve con su coste (que siempre es 1), ordenados
        según un criterio fijo de prioridad de acciones.

    Argumentos de llamada:
        self: instancia de la clase que contiene los atributos:
              - jugador (Tuple[int, int]): posición actual del jugador.
              - cajas (List[Tuple[int, int]]): posiciones actuales de las cajas.
              - objetivos, es_posicion_valida, crear_estado, etc.
        estado_str (str | None, opcional): cadena con el formato
              "(fila,cola_jugador)[(f1,c1),(f2,c2),...]". Si se proporciona,
              parsea jugador y cajas desde esta cadena; si es None, usa
              los atributos self.jugador y self.cajas.

    Valor de retorno:
        List[Tuple[str, Estado, int]]: lista de sucesores, donde cada tupla
        contiene:
          - accion (str): letra del movimiento ('u','U','r','R','d','D','l','L')
                          indicando simple paso (minúscula) o empuje (mayúscula).
          - nuevo_estado (Estado): nuevo objeto de estado generado.
          - coste (int): coste del movimiento (siempre 1).

    Archivos requeridos:
        Ninguno. Solo hace uso de la librería estándar `re` (si parsea
        estado_str) y de los métodos de la clase:
        - es_posicion_valida
        - crear_estado

    Excepciones controladas:
        - Los movimientos inválidos (dirección no válida,
          fuera de límites o empuje bloqueado) se descartan internamente
          sin lanzar errores.
    """
    def generar_sucesores(self, estado_str=None):
        if estado_str is not None:
            match = re.match(r'\((\d+),(\d+)\)\[((?:\(\d+,\d+\),?)*)\]', estado_str)
            if not match:
                return []
            jugador = (int(match.group(1)), int(match.group(2)))
            cajas = [tuple(map(int, c)) for c in re.findall(r'\((\d+),(\d+)\)', match.group(3))]
        else:
            jugador = self.jugador
            cajas = list(self.cajas)

        sucesores = []
        for accion, dx, dy in [('u', -1, 0), ('r', 0, 1), ('d', 1, 0), ('l', 0, -1)]:
            nueva_j = (jugador[0] + dx, jugador[1] + dy)
            if not self.es_posicion_valida(nueva_j):
                continue

            if nueva_j in cajas:
                nueva_b = (nueva_j[0] + dx, nueva_j[1] + dy)
                if not self.es_posicion_valida(nueva_b) or nueva_b in cajas:
                    continue
                cajas2 = [nueva_b if c==nueva_j else c for c in cajas]
                accion_final = accion.upper()
            else:
                cajas2 = cajas.copy()
                accion_final = accion.lower()

  
            nuevo_estado = self.crear_estado(nueva_j, cajas2)
            sucesores.append((accion_final, nuevo_estado, 1))

        orden = ['u','U','r','R','d','D','l','L']
        sucesores.sort(key=lambda s: orden.index(s[0]))

        return sucesores

  

    def es_posicion_valida(self, posicion):
        
        fila, columna = posicion
        if 0 <= fila < self.nfila and 0 <= columna < self.ncol:
            return self.grid[fila][columna] != '#'
        
        return False

    def es_estado_objetivo(self):
        return all(caja in self.objetivos for caja in self.cajas)

    def crear_estado(self, jugador, cajas):
        id_cadena = f"({jugador[0]},{jugador[1]})[{','.join(f'({caja[0]},{caja[1]})' for caja in sorted(cajas))}]"
        return id_cadena

    def mostrar_nivel(self):
        id_cadena = self.crear_estado(self.jugador, self.cajas)
        filamd5 = hashlib.md5(id_cadena.encode()).hexdigest().upper()
        info = (
            f"ID:{filamd5}\n"
            f"Rows:{self.nfila}\n"
            f"Columns:{self.ncol}\n"
            f"Walls:{self.muros}\n"
            f"Targets:{self.objetivos}\n"
            f"Player:{self.jugador}\n"
            f"Boxes:{self.cajas}\n"
        )
        
        return info
    
    
    """
    Nombre del método:
        Hmanhattan

    Autor original:
        [Tu nombre o autor original]

    Descripción del método:
        Calcula la suma de las distancias de Manhattan mínimas desde cada
        caja hasta el objetivo más cercano definido en self.objetivos.
        Redondea el resultado a dos decimales. Si el formato de 'estado'
        no coincide con el patrón esperado, devuelve 0.0.

    Argumentos de llamada:
        self: instancia de la clase que contiene el atributo:
              - objetivos (List[Tuple[int, int]]): posiciones de los objetivos.
        estado (str): cadena con el formato
              "(fila,cola_jugador)[(f1,c1),(f2,c2),...]" que incluye
              la posición del jugador y de las cajas.

    Valor de retorno:
        float: heurística de Manhattan redondeada a dos decimales,
               o 0.0 si el formato de 'estado' es inválido.

    Archivos requeridos:
        Ninguno. Solo usa la librería estándar 're' y el atributo
        self.objetivos de la instancia.

    Excepciones controladas:
        No lanza excepciones comprobadas. Si 'estado' no encaja con
        la expresión regular, retorna 0.0 sin propagar error.
    """

    def Hmanhattan(self,estado):
            match = re.match(r'\((\d+),(\d+)\)\[((?:\(\d+,\d+\),?)*)\]', estado)
            if not match:
                return 0.0
            cajas_str = match.group(3)
            cajas = re.findall(r'\((\d+),(\d+)\)', cajas_str)
            cajas = [tuple(map(int, caja)) for caja in cajas]

            total = 0
            for caja in cajas:
                min_dist = min(abs(caja[0] - obj[0]) + abs(caja[1] - obj[1]) for obj in self.objetivos)
                total += min_dist
            total=round(total,2)
            return total

    def es_estado_objetivo_estado(self, estado):
            
            match = re.match(r'\((\d+),(\d+)\)\[((?:\(\d+,\d+\),?)*)\]', estado)
            if not match:
                return False
            cajas_str = match.group(3)
            cajas = re.findall(r'\((\d+),(\d+)\)', cajas_str)
            cajas = [tuple(map(int, caja)) for caja in cajas]
            return all(caja in self.objetivos for caja in cajas)
    
    """
    Nombre del método: todosAlgoritmos

    Autor original: No sabria muy bien que poner aqui, porque tuve problemas y fui a tutoria 
    que es donde me ayudaron a entenderlo y no se si poner el nombre del profesor o el mio.

    Descripción del método:
        Ejecuta la búsqueda de solución usando la estrategia indicada
        ('BFS', 'DFS', 'UC', 'GREEDY' o 'A*') hasta una profundidad máxima.
        Gestiona la frontera, expande nodos, aplica heurísticas cuando
        corresponda y devuelve el camino solución si se alcanza el objetivo.

    Argumentos de llamada:
        self: instancia de la clase que contiene:
              - jugador (Tuple[int,int])
              - cajas (List[Tuple[int,int]])
              - muros (Set[Tuple[int,int]])
              - métodos: crear_estado, es_estado_objetivo_estado,
                         generar_sucesores, Hmanhattan, _extraer_estado
        estrategia (str): criterio de ordenación de la frontera.
                          Puede ser 'BFS', 'DFS', 'UC', 'GREEDY' o 'A*'.
        max_profundidad (int): límite máximo de profundidad a explorar.

    Valor de retorno:
        List[Accion] | None:
            - Si encuentra un estado objetivo, devuelve la lista de
              acciones que llevan desde el estado inicial al objetivo
              (nodo.camino()).
            - Si no halla solución antes de vaciar la frontera o superar
              la profundidad, devuelve None.

    Archivos requeridos:
        Ninguno. Utiliza únicamente clases y métodos internos:
        - Frontera
        - Nodo
        - librería estándar re (si Hmanhattan se invoca)

    Excepciones controladas:
        - ValueError: capturada al extraer datos de estado con
          self._extraer_estado, en cuyo caso se omite ese sucesor.
    """
    
    def todosAlgoritmos(self, estrategia, max_profundidad):
        id_counter=0
        frontera = Frontera(estrategia)
        estado0 = self.crear_estado(self.jugador, self.cajas)
        if estrategia == 'BFS' or estrategia == 'UC' or estrategia=='DFS':
            hHijo = 0.0
        elif estrategia == 'GREEDY' or estrategia == 'A*':
            hHijo=self.Hmanhattan(estado0)
        nodo0=Nodo(
            id_counter  = id_counter,
            estado      = estado0,
            padre       = None,
            accion      = 'NOTHING',
            profundidad = 0,
            costo       = 0.0,
            heuristica  = hHijo,
            estrategia  = estrategia
        )
        visitados = set()
        frontera.insertar(nodo0)
        while not frontera.esta_vacia() :
            nodo= frontera.extraer()
            if  self.es_estado_objetivo_estado(nodo.estado):
                return nodo.camino()
            else:
                
                if nodo.estado not in visitados and nodo.profundidad < max_profundidad:
                    visitados.add(nodo.estado)
                    sucesores = list(self.generar_sucesores(nodo.estado))
                    for accion, estado_suc, costo_paso in sucesores:
                        id_counter += 1
                        if estado_suc not in visitados:    
                            try:
                                jugador, cajas = self._extraer_estado(estado_suc)
                                
                            except ValueError:
                                continue
                            if ( jugador is not None and self.es_posicion_valida(jugador) and all(c not in self.muros for c in cajas)
                            and len(set(cajas)) == len(cajas) ):
                                prof_hijo = nodo.profundidad + 1
                                cost_hijo = nodo.costo + costo_paso
                                if estrategia == 'BFS' or estrategia == 'UC' or estrategia=='DFS':
                                    hHijo = 0.0
                                elif estrategia == 'GREEDY' or estrategia == 'A*':
                                    hHijo=self.Hmanhattan(estado_suc)
                                
                                hijo = Nodo.crear_hijo(
                                    id_counter   = id_counter,
                                    padre        = nodo,
                                    accion       = accion,
                                    nuevo_estado = estado_suc,
                                    profundidad  = prof_hijo,
                                    costo        = cost_hijo,
                                    heuristica   = hHijo,
                                    estrategia   = estrategia
                                )
                                
                                frontera.insertar(hijo)
        return None
         
    def _extraer_estado(self, estado):
        match = re.match(r'\((\d+),(\d+)\)\[\((.*?)\)\]', estado)
        if not match:
            raise ValueError("Estado malformado")
        jugador = (int(match.group(1)), int(match.group(2)))
        cajas_str = match.group(3)
        cajas = re.findall(r'\((\d+),(\d+)\)', f'({cajas_str})')
        cajas = [tuple(map(int, caja)) for caja in cajas]

        return jugador, cajas


