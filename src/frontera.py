
import heapq
from collections import deque

class Frontera:
    def __init__(self, estrategia):
        self.estrategia = estrategia
        if estrategia == 'BFS':
            self.cola = deque()
        else:
            self.heap = [] 

    def insertar(self, nodo):
        if self.estrategia == 'BFS':
            self.cola.append(nodo)
        else:
            heapq.heappush(self.heap, nodo)

    def extraer(self):
        if self.estrategia == 'BFS':
            return self.cola.popleft()
        else:
            return heapq.heappop(self.heap) if self.heap else None

    def esta_vacia(self):
        if self.estrategia == 'BFS':
            return not self.cola
        else:
            return not self.heap
