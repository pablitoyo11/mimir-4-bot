import pickle
import os
from ClickAtMir import get_window_click_map_randomizer

def agregar_accion(x, y, accion, archivo):
    # Crear la carpeta si no existe
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    # Cargar las acciones existentes
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
    except FileNotFoundError:
        acciones = []
    # Agregar la nueva acción
    acciones.append((x, y, accion))  
    # Guardar las acciones actualizadas
    with open(archivo, 'wb') as file:
        pickle.dump(acciones, file)  
    print(f"Acción {accion} en ({x}, {y}) agregada y guardada en {archivo}.")

def mostrar_acciones(archivo):
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
            for accion in acciones:
                print(accion)
    except FileNotFoundError:
        print("No se encontraron acciones guardadas en el archivo.")

def eliminar_acciones(archivo):
    try:
        os.remove(archivo)
        print(f"Contenido del archivo {archivo} eliminado.")
    except FileNotFoundError:
        print("El archivo no existe.")

def leer_acciones(archivo):
    try:
        archivo = f"secuencias/{archivo}.pkl"
        print(f"Ruta del archivo: {archivo}") # Imprimir la ruta del archivo para verificar

        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
            return acciones
    except FileNotFoundError:
        print("El archivo no existe.")
        return []

def interpretar_acciones(archivo, window_title):
    try:
        archivo = f"secuencias/{archivo}.pkl"
##        print(f"Ruta del archivo: {archivo}") # Imprimir la ruta del archivo para verificar
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
    except FileNotFoundError:
        print("EXCEPT interpretar_acciones El archivo no existe.")
        return []
    for accion in acciones:
        print(f"FOR {accion}:")
        x, y, tipo_accion = accion
        if tipo_accion == 'AutomoveHandler':
            print("tipo_accion == 'AutomoveHandler'")
            get_window_click_map_randomizer(x, y, window_title,5)
        elif tipo_accion == 'OpeningChestHandler':
            print("tipo_accion == 'OpeningChestHandler'")
            get_window_click_map_randomizer(x, y, window_title,5)
        else:
            print(f"Acción desconocida {tipo_accion} en coordenadas ({x*640}, {y*375})")


if __name__ == "__main__":
##    get_window_click_map_randomizer(0, 0, "Mir4G[1]", 0)  # Inicialización

    while True:
        mapa = input("Ingrese el nombre del mapa: ")
        carpeta = 'secuencias'
        archivo = os.path.join(carpeta, f"{mapa}.pkl")

        # Crear la carpeta si no existe
        os.makedirs(carpeta, exist_ok=True)

        if os.path.exists(archivo):
            print("Ese mapa ya existe.")
            ver_mapa = input("¿Desea verlo? (s/n): ").strip().lower()
            while ver_mapa not in ['s', 'n']:
                ver_mapa = input("Respuesta inválida. ¿Desea verlo? (s/n): ").strip().lower()
            if ver_mapa == 's':
                mostrar_acciones(archivo)
            
            accion_mapa = input("¿Desea eliminar el contenido, continuar editando, crear un nuevo archivo o salir? (eliminar/continuar/nuevo/salir): ").strip().lower()
            while accion_mapa not in ['eliminar', 'continuar', 'nuevo', 'salir']:
                accion_mapa = input("Respuesta inválida. ¿Desea eliminar el contenido, continuar editando, crear un nuevo archivo o salir? (eliminar/continuar/nuevo/salir): ").strip().lower()
            if accion_mapa == 'eliminar':
                eliminar_acciones(archivo)
            elif accion_mapa == 'nuevo':
                continue  # Reinicia el bucle para preguntar el nombre del mapa nuevamente
            elif accion_mapa == 'salir':
                break
            else:
                print("Continuando con el mapa existente.")
        else:
            print("Creando mapa nuevo.")

        while True:
            try:
                x = int(input("Ingrese la coordenada X: "))
                y = int(input("Ingrese la coordenada Y: "))
            except ValueError:
                print("Coordenadas inválidas. Por favor, ingrese números enteros.")
                continue

            print("Seleccione la acción:")
            print("1. AutomoveHandler")
            print("2. OpeningChestHandler")
            accion_opcion = input("Ingrese el número de la acción: ").strip()
            while accion_opcion not in ['1', '2']:
                accion_opcion = input("Respuesta inválida. Ingrese el número de la acción (1 o 2): ").strip()

            if accion_opcion == '1':
                accion = 'AutomoveHandler'
            elif accion_opcion == '2':
                accion = 'OpeningChestHandler'
            
            # Acomodar a porcentajes resolución para ingresos 640x375
            x = round(x / 640, 3)
            y = round(y / 375, 3)
            
            agregar_accion(x, y, accion, archivo)

            continuar = input("¿Desea agregar otra acción? (s/n): ").strip().lower()
            while continuar not in ['s', 'n']:
                continuar = input("Respuesta inválida. ¿Desea agregar otra acción? (s/n): ").strip().lower()
            if continuar != 's':
                break

        print(f"Acciones guardadas en {archivo}:")
        mostrar_acciones(archivo)

        continuar_mapa = input("¿Desea agregar tareas en el mapa, ingresar nombre de otro mapa o salir? (agregar/otro/salir): ").strip().lower()
        while continuar_mapa not in ['agregar', 'otro', 'salir']:
            continuar_mapa = input("Respuesta inválida. ¿Desea agregar tareas en el mapa, ingresar nombre de otro mapa o salir? (agregar/otro/salir): ").strip().lower()
        if continuar_mapa == 'otro':
            continue
        elif continuar_mapa == 'salir':
            break
        else:
            print("Continuando con el mismo mapa.")

    # Parte del segundo módulo
    mapa = input("Ingrese el nombre del mapa a leer: ")
    archivo = mapa
    window_title = "Mir4G[1]"
    print(f"interpretar_acciones interpretar_acciones en {archivo}:")
    interpretar_acciones(archivo, window_title)
    print(f"interpretar_acciones interpretar_acciones en {archivo}:")

