""" 
*Nombre de clase: jugador.py 
* Autora: Yolanda Galván Redondo 
* Release/Creation date:6 noviembre 2024 
* Version de esta clase: 2.0 
* Descripcion: esta es la clase de la posición del jugador que se mueve  
""" 
class Jugador:
    
    def __init__(self, posicion):
        self.posicion = posicion #la posicion del jugador 
       
    def mover(self, direccion, grid):
        movimientos = {
            'u': (-1, 0),  #arriba
            'd': (1, 0),   #abajo
            'l': (0, -1),  #izquierda
            'r': (0, 1)    #derecha
        }

        if direccion not in movimientos:
            raise ValueError(f"Dirección inválida: {direccion}")
        dx, dy = movimientos[direccion]
        nueva_posicion = (self.posicion[0] + dx, self.posicion[1] + dy)
        if 0 <= nueva_posicion[0] < len(grid) and 0 <= nueva_posicion[1] < len(grid[0]):
            
            if grid[nueva_posicion[0]][nueva_posicion[1]] != '#':
                self.posicion = nueva_posicion  
                return nueva_posicion
            else:
                print("Movimiento bloqueado: Muro en la dirección.")
        else:
            print("Movimiento fuera de límites.")

        return self.posicion  


