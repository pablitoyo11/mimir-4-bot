import pickle
import os
from ClickAtMir import get_window_click_map_randomizer
"""
def get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration):
def get_window_click_map_randomizer(x_percent,y_percent,window_title,duration):
"""

if __name__ == "__main__":
    get_window_click_map_randomizer(0, 0, "Mir4G[1]", 0)
    mapa = input("Ingrese el nombre del mapa a leer: ")
    archivo = f"secuencias/{mapa}.pkl"
    window_title = "Mir4G[1]"
    # window_title = input("Ingrese el título de la ventana: ")

    # Leer las acciones del archivo
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
    except FileNotFoundError:
        print("El archivo no existe.")
        acciones = []

    if acciones:
        print(f"Acciones guardadas en {archivo}:")
        for accion in acciones:
            x, y, tipo_accion = accion
            if 0 <= x <= 1 and 0 <= y <= 1:
                if tipo_accion == 'AutomoveHandler':
                    print(f"AutomoveHandler en coordenadas ({x}, {y})")
                    get_window_click_map_randomizer(0.5, 0.9, "Mir4G[1]", 5)
                    get_window_click_map_randomizer(x, y, window_title, 0)
                elif tipo_accion == 'OpeningChestHandler':
                    print(f"OpeningChestHandler en coordenadas ({x}, {y})")
                    get_window_click_map_randomizer(0.5, 0.9, "Mir4G[1]", 5)
                    get_window_click_map_randomizer(x, y, window_title, 0)
                else:
                    print(f"Acción desconocida {tipo_accion} en coordenadas ({x}, {y})")
            else:
                print(f"Coordenadas inválidas: ({x}, {y})")
    else:
        print("No se encontraron acciones guardadas en el archivo.")
