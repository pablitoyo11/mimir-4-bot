import pickle
import os
import time
import random
import numpy as np
from ClickAtMir2 import get_window_click_area_randomizer, press_key_in_game
from MouseFunctions import double_click_current_position

def pointarea_resizer(x_start, y_start, x_end, y_end):
    """
    Converts the input coordinates to percentages based on a 640x375 window size and returns them.
    Returns:
        tuple: A tuple containing (x_start, y_start, x_end, y_end) as floats
               representing the percentage coordinates.
    """
    x_start = round(x_start / 640, 3)
    y_start = round(y_start / 375, 3)
    x_end = round(x_end / 640, 3)
    y_end = round(y_end / 375, 3)
    return x_start, y_start, x_end, y_end

def interprete_de_accion(linea, window_title):
    linea_lowercase = [element.lower() if isinstance(element, str) else element for element in linea]
    print(linea)
    try:
        duration = random.randint(1, 2)
        if "map" in linea_lowercase:
            OpenMap_x_start,OpenMap_y_start,OpenMap_x_end,OpenMap_y_end = 520,70,590,80
            OpenMap_x_start = round(OpenMap_x_start / 640, 3)
            OpenMap_y_start = round(OpenMap_y_start / 375, 3)
            OpenMap_x_end = round(OpenMap_x_end / 640, 3)
            OpenMap_y_end = round(OpenMap_y_end / 375, 3)
            get_window_click_area_randomizer(OpenMap_x_start,OpenMap_y_start,OpenMap_x_end,OpenMap_y_end,window_title,duration)
##        if np.isin("pointarea", linea):
            if "pointarea" in linea_lowercase:
                linea_subindex = np.where(linea == "pointarea")[0]
##            print(linea_subindex)
                x_start = int(linea[linea_subindex+1])
                y_start = int(linea[linea_subindex+2])
                x_end = int(linea[linea_subindex+3])
                y_end = int(linea[linea_subindex+4])
                #transform to percent according to window size 640*375
                x_start,y_start,x_end,y_end = pointarea_resizer(x_start,y_start,x_end,y_end)
                #changed all this to a function pointarea_resizer
##                x_start = round(x_start / 640, 3)
##                y_start = round(y_start / 375, 3)
##                x_end = round(x_end / 640, 3)
##                y_end = round(y_end / 375, 3)
                get_window_click_area_randomizer(x_start,y_start,x_end,y_end,window_title,duration)
                #since we are in map, do double click to press the move popup
                double_click_current_position()
            action_type=linea[2]
            print(action_type)
            return action_type
        
        elif "pointarea" in linea_lowercase:
            linea_subindex = np.where(linea == "pointarea")[0]
##            print(linea_subindex)
            x_start = int(linea[linea_subindex+1])
            y_start = int(linea[linea_subindex+2])
            x_end = int(linea[linea_subindex+3])
            y_end = int(linea[linea_subindex+4])
            #transform to percent according to window size 640*375
            #changed all this to a function pointarea_resizer
            x_start,y_start,x_end,y_end = pointarea_resizer(x_start,y_start,x_end,y_end)
##            x_start = round(x_start / 640, 3)
##            y_start = round(y_start / 375, 3)
##            x_end = round(x_end / 640, 3)
##            y_end = round(y_end / 375, 3)
            get_window_click_area_randomizer(x_start,y_start,x_end,y_end,window_title,duration)
        if "key" in linea_lowercase:
            linea_subindex = np.where(linea == "key")[0]
            key = linea[linea_subindex+1]
            press_key_in_game(key, window_title)
##        return action_type
    except Exception as e:
        print(f"interprete_de_accion Error during action execution: {e}")
        return None


def travel_to_map(intended_map, window_title):
##  last edit     archivo = f"secuencias/maptravel/{intended_map}" + TravelTo + .pkl
    print("intended map")
    print(intended_map)
    archivo = f"secuencias/maptravel/TravelTo{intended_map}.pkl"
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
            acciones = np.array(acciones)
            for accion in acciones:
                interprete_de_accion(accion, window_title)
                time.sleep(1)  # Esperar 1 segundo entre cada acción
        print(f"Viaje al mapa {intended_map} completado.")
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe.")
    except Exception as e:
        print(f"Error durante el viaje al mapa {intended_map}: {e}")
