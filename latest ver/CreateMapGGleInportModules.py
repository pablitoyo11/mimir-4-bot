import pickle
import os
import random
from ClickAtMir2 import get_window_click_area_randomizer

def interprete_de_accion(linea, window_title):
    try:
        duration = random.randint(0.3, 1)
        if "pointarea" in linea:
            linea_subindex = linea.index("pointarea")
            x_center = linea[linea_subindex+1]
            y_center = linea[linea_subindex+2]
            x_size = linea[linea_subindex+3]
            y_size = linea[linea_subindex+4]
            #transform to percent according to window size 640*375
            x_center = round(x_center / 640, 3)
            y_center = round(y_center / 375, 3)
            x_size = round(x_size / 640, 3)
            y_size = round(y_size / 375, 3)
            get_window_click_area_randomizer(x_center,y_center,x_size,y_size,window_title,duration)
        if "key" in linea:
            linea_subindex = linea.index("key")
            key = linea[linea_subindex+1]
            press_key_in_game(key, window_title)
##        return action_type
    except Exception as e:
        print(f"interprete_de_accion Error during action execution: {e}")
        return None


def travel_to_map(intended_map, window_title):
##  last edit     archivo = f"secuencias/maptravel/{intended_map}" + TravelTo + .pkl
    archivo = f"secuencias/maptravel/TravelTo{intended_map}.pkl"
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
            for accion in acciones:
                interprete_de_accion(accion, window_title)
                time.sleep(1)  # Esperar 1 segundo entre cada acción
        print(f"Viaje al mapa {intended_map} completado.")
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe.")
    except Exception as e:
        print(f"Error durante el viaje al mapa {intended_map}: {e}")
