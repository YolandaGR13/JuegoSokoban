""" 
*Nombre de clase: nodo.py 
* Autora: Yolanda Galván Redondo 
* Release/Creation date:14 noviembre 2024 
* Version de esta clase: 5.2 
* Descripcion: esta clase contiene los elementos que componen un nodo ademas del calculo de su valor, comparacion e impresion
""" 
import hashlib
class Nodo:
    def __init__(self,
                 id_counter,#el contador de id de los nodos
                 estado,#el estado del nodo en el que se encuentra
                 padre=None,#el estado del nodo padre
                 accion='NOTHING', #la accion que se va a realizar, que al mepezar es nada 
                 profundidad=0, #la profundida a la que se encuentra el nodo
                 costo=0.0, #el coste del nodo
                 heuristica=0.0,#la heurtistica del nodo, que es la distancia al objetivo
                 estrategia=''):#la estrategia a seguir
        self.id_nodo    = id_counter
        self.estado     = estado
        self.padre      = padre
        self.accion     = accion
        self.profundidad= profundidad
        self.costo      = costo
        self.heuristica = heuristica
        self.estrategia = estrategia
        self.valor      = self.calcularValor()

    @classmethod
    def crear_hijo(cls, id_counter, padre, accion, nuevo_estado,
                   profundidad, costo, heuristica, estrategia):
        return cls(
            id_counter  = id_counter,
            estado      = nuevo_estado,
            padre       = padre,
            accion      = accion,
            profundidad = profundidad,
            costo       = costo,
            heuristica  = heuristica,
            estrategia  = estrategia
        )

    def calcularValor(self) -> float:
        if   self.estrategia == 'BFS':
            raw = float(self.profundidad)
        elif self.estrategia == 'DFS':
            raw = (1.0/(self.profundidad + 1) )+ 1e-9
        elif self.estrategia == 'UC':
            raw = float(self.costo)
        elif self.estrategia == 'GREEDY':
            raw = self.heuristica
        elif self.estrategia == 'A*':
            raw = self.costo + self.heuristica
        else:
            raw = 0.0
        self.raw = raw
        return raw

    def __lt__(self, otro):
        if self.raw != otro.raw:
            return self.raw < otro.raw
        return self.id_nodo < otro.id_nodo

    def camino(self):
        seq, nodo = [], self
        while nodo:
            seq.append(nodo)
            nodo = nodo.padre
        return list(reversed(seq))

    def __str__(self):
        parent_id   = self.padre.id_nodo if self.padre else 'None'
        estado_hash = hashlib.md5(self.estado.encode()).hexdigest().upper()
     
        return (
            f"{self.id_nodo},"
            f"{estado_hash},"
            f"{parent_id},"
            f"{self.accion},"
            f"{self.profundidad},"
            f"{self.costo:.2f},"
            f"{self.heuristica:.2f},"
            f"{self.valor:.2f}\n"
        )
