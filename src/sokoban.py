
""" 
*Nombre de clase: sokoban.py 
* Autora: Yolanda Galván Redondo 
* Release/Creation date:26 septiembre 2024 
* Version de esta clase: 4.0 
* Descripcion: este es el main, es decir, la clase principal que ejecuta el programa 
""" 
import hashlib
import sys
from nivel import Nivel

def main():
    
    if len(sys.argv) > 1:
        opcion = sys.argv[1]  

        
        if opcion not in ['T1', 'T2S','T2T', 'T3', 'T4']:
            print(f"Opción no reconocida: {opcion}")
            return

        if '-l' in sys.argv:
           
            grid = sys.argv[sys.argv.index('-l') + 1]
            niveles = [grid] 
        elif '-i' in sys.argv:
            
            archivo_entrada = sys.argv[sys.argv.index('-i') + 1]
            niveles = Nivel.cargar_niveles(archivo_entrada)

        else:
            print("Error: Debes proporcionar un nivel con -l o un archivo de niveles con -i.")
            return
        
        if '-o' in sys.argv:
            archivo_salida = sys.argv[sys.argv.index('-o') + 1]
        else:
            archivo_salida = 'salida.txt'  
      
        with open(archivo_salida, 'w') as salida:
            for i, nivel_text in enumerate(niveles, start=1):
                if opcion == 'T1':
                    info = tarea1(nivel_text,i)
                elif opcion == 'T2S':
                    info = tareaT2S(nivel_text, i)
                elif opcion == 'T2T':
                    info = tareaT2T(nivel_text, i)
                elif opcion == 'T3' or opcion == 'T4':
                    info = tareaT3(nivel_text, i)
                
                salida.write(info + '\n')
                print(info)

    else:
        print("Error: No se han proporcionado suficientes argumentos.")
        


def tarea1(grid, id_nivel):

    nivel = Nivel(grid, id_nivel)
    info = nivel.mostrar_nivel()
    return info

def tareaT2S(nivel_texto, id_nivel):
    """Genera y muestra los sucesores del nivel."""
    nivel = Nivel(nivel_texto, id_nivel)
    sucesores = nivel.generar_sucesores()
    id_nivel = hashlib.md5(nivel.crear_estado(nivel.jugador, nivel.cajas).encode()).hexdigest().upper()
    resultado = [f"ID:{id_nivel}"]


    for accion, nuevo_estado, costo in sucesores:
        estado_md5 = hashlib.md5(nuevo_estado.encode()).hexdigest().upper()
        resultado.append(f"[{accion},{estado_md5},{costo}]")

    return "\n".join(resultado)


def tareaT2T(nivel_texto, id_nivel):
    """Evalúa si el nivel está en estado objetivo."""
    nivel = Nivel(nivel_texto, id_nivel)
    return "TRUE" if nivel.es_estado_objetivo() else "FALSE"

def tareaT3(nivel_texto, id_nivel):

    if '-s' not in sys.argv or '-d' not in sys.argv:
        raise ValueError("Debes proporcionar los parámetros -s (estrategia) y -d (profundidad máxima).")

    estrategia = sys.argv[sys.argv.index('-s') + 1].upper()
    try:
        max_profundidad = int(sys.argv[sys.argv.index('-d') + 1])
    except ValueError:
        raise ValueError("El parámetro -d debe ser un número entero.")
    
    if estrategia not in ['BFS', 'DFS', 'UC', 'GREEDY', 'A*']:
        raise ValueError(f"Estrategia no válida: {estrategia}. Debe ser BFS, DFS,UC, GREEDY o A*.")


    nivel = Nivel(nivel_texto, id_nivel)

   
    solucion= nivel.todosAlgoritmos(estrategia, max_profundidad)
 
    resultado = nivel_texto + "\n" 

    if solucion:
        
        resultado += "\n".join(map(str, solucion))
    else:
        resultado += "No se encontro solucióm"

    return resultado

if __name__ == "__main__":
    main()
