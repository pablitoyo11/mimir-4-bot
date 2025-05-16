import pickle
import random
from ClickAtMir import press_key_in_game
from ClickAtMir2 import get_window_click_map_randomizer, get_window_click_space_randomizer, get_window_click_area_randomizer, get_window_click_point_randomizer
from SSCompare_tmp_ref import map_check

def cargar_archivo(archivo_pkl):
    # Cargar el archivo pkl
    with open(archivo_pkl, 'rb') as file:
        data = pickle.load(file)
    return data

def procesar_lineas(archivo_pkl, window_title):
    data = cargar_archivo(archivo_pkl)
    for linea in data:
        interprete_de_acciones(linea, window_title)

def interprete_de_acciones(lineaArchivo, window_title):
    main_command = lineaArchivo[0]
    if main_command == "UI":
        UI_mcmd, UI_scmd, Para1, Para2, Para3, Para4 = lineaArchivo
        if UI_scmd == "area":
            xs_percent, xe_percent, ys_percent, ye_percent = Para1, Para2, Para3, Para4
            get_window_click_area_randomizer(xs_percent, ys_percent, xe_percent, ye_percent, window_title, duration=1)
        elif UI_scmd == "point":
            x_percent, y_percent = Para1, Para2
            get_window_click_point_randomizer(x_percent, y_percent, window_title, duration=1)
        elif UI_scmd == "key":
            key = Para1
            press_key_in_game(key, window_title)
    elif main_command == "MAP":
        MAP_mcmd, mapname, accion, MAP_scmd, Para1, Para2, Para3, Para4 = lineaArchivo
        try:
            if map_check(mapname, window_title):
                if MAP_scmd == "area":
                    xs_percent, xe_percent, ys_percent, ye_percent = Para1, Para2, Para3, Para4
                    get_window_click_area_randomizer(xs_percent, ys_percent, xe_percent, ye_percent, window_title, duration=1)
                elif MAP_scmd == "point":
                    x_percent, y_percent = Para1, Para2
                    get_window_click_point_randomizer(x_percent, y_percent, window_title, duration=1)
                ejecutar_accion(accion)
            else:
                travel_to_map(mapname, window_title)
        except Exception as e:
            print(f"Error al verificar el mapa: {e}")

def travel_to_map(intended_map, window_title):
    print(f"Viajando al mapa {intended_map} en la ventana {window_title}")

def ejecutar_accion(accion):
    print(f"Acción {accion} activada")

if __name__ == "__main__":
    archivo_pkl = 'archivo.pkl'
    procesar_lineas(archivo_pkl, "window_title")
