import pickle
import os
from ClickAtMir import get_window_click_map_randomizer
##def get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration):
##def get_window_click_map_randomizer(x_percent,y_percent,window_title,duration):

##from MirWindowHandler import identify_mir,bring_window_to_front
##identify_mir("Mir4G[1]")
##bring_window_to_front("Mir4G[1]")


#get_window_click_map_randomizer(0.5,0.9,"Mir4G[1]",5)
"""
def leer_acciones(archivo):
    try:
        archivo = f"secuencias/{archivo}.pkl"
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
            return acciones
    except FileNotFoundError:
        print("El archivo no existe.")
        return []
"""
def interpretar_acciones(archivo, window_title):
    try:
        archivo = f"secuencias/{archivo}.pkl"
##        print(f"Ruta del archivo: {archivo}") # Imprimir la ruta del archivo para verificar
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
            return acciones
    except FileNotFoundError:
        print("El archivo no existe.")
        return []
    
    for accion in acciones:
        x, y, tipo_accion = accion
        if tipo_accion == 'AutomoveHandler':
            get_window_click_map_randomizer(x, y, window_title,5)
        elif tipo_accion == 'OpeningChestHandler':
            get_window_click_map_randomizer(x, y, window_title,5)
        else:
            print(f"Acción desconocida {tipo_accion} en coordenadas ({x*640}, {y*375})")


if __name__ == "__main__":
    get_window_click_map_randomizer(0,0,"Mir4G[1]",0) #initialization ??? it doesn't work without this  
    mapa = input("Ingrese el nombre del mapa a leer: ")
    archivo = mapa
##        carpeta = 'secuencias'
##    archivo = os.path.join(carpeta, f"{mapa}.pkl")
    window_title = "Mir4G[1]"
##    window_title = input("Ingrese el título de la ventana: ")

    # Leer las acciones del archivo
    interpretar_acciones(archivo, window_title)
##    acciones = leer_acciones(archivo)
"""
    if acciones:        
        print(f"Acciones guardadas en {archivo}:")
        interpretar_acciones(acciones, window_title)
    else:
        print("No se encontraron acciones guardadas en el archivo.")
"""
