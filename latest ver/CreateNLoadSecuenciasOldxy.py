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
            for i, accion in enumerate(acciones):
                x, y, tipo_accion = accion
                x = round(x * 640)
                y = round(y * 375)
                print(f"Línea {i+1}: ({x}, {y}, {tipo_accion})")
    except FileNotFoundError:
        print("No se encontraron acciones guardadas en el archivo.")

def eliminar_acciones(archivo):
    try:
        os.remove(archivo)
        print(f"Archivo {archivo} eliminado.")
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

def editar_accion(archivo):
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
        linea = int(input("Ingrese el número de la línea: "))
        x = int(input("Ingrese la coordenada X: "))
        y = int(input("Ingrese la coordenada Y: "))
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
        x = round(x / 640, 3)
        y = round(y / 375, 3)
        acciones[linea - 1] = (x, y, accion)
        with open(archivo, 'wb') as file:
            pickle.dump(acciones, file)
        print(f"Línea {linea} editada con éxito.")
    except (FileNotFoundError, IndexError, ValueError):
        print("Error: El archivo no existe, la línea es inválida o la entrada es incorrecta.")

def insertar_accion(archivo, x, y, accion):
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
        acciones.append((x, y, accion))
        with open(archivo, 'wb') as file:
            pickle.dump(acciones, file)
        print("Nueva línea insertada con éxito.")
    except FileNotFoundError:
        print("Error: El archivo no existe.")

if __name__ == "__main__":
    while True:
        opcion = input("¿Desea ingresar un nuevo mapa o salir? (ingresar/salir): ").strip().lower()
        while opcion not in ['ingresar', 'salir']:
            opcion = input("Respuesta inválida. ¿Desea ingresar un nuevo mapa o salir? (ingresar/salir): ").strip().lower()

        if opcion == 'ingresar':
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
                    
                    accion_mapa = input("¿Desea eliminar el contenido, continuar editando, crear un nuevo archivo o salir? (eliminar/editar/nuevo/salir): ").strip().lower()
                    while accion_mapa not in ['eliminar', 'editar', 'nuevo', 'salir']:
                        accion_mapa = input("Respuesta inválida. ¿Desea eliminar el contenido, continuar editando, crear un nuevo archivo o salir? (eliminar/editar/nuevo/salir): ").strip().lower()
                    if accion_mapa == 'eliminar':
                        eliminar_acciones(archivo)
                        break
                    elif accion_mapa == 'nuevo':
                        continue  # Reinicia el bucle para preguntar el nombre del mapa nuevamente
                    elif accion_mapa == 'salir':
                        break
                    elif accion_mapa == 'editar':
                        mostrar_acciones(archivo)
                        editar_opcion = input("¿Desea editar una línea existente o insertar una nueva línea? (editar/insertar): ").strip().lower()
                        while editar_opcion not in ['editar', 'insertar']:
                            editar_opcion = input("Respuesta inválida. ¿Desea editar una línea existente o insertar una nueva línea? (editar/insertar): ").strip().lower()
                        if editar_opcion == 'editar':
                            editar_accion(archivo)
                        elif editar_opcion == 'insertar':
                            try:
                                x = int(input("Ingrese la coordenada X: "))
                                y = int(input("Ingrese la coordenada Y: "))
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
                                x = round(x / 640, 3)
                                y = round(y / 375, 3)
                                insertar_accion(archivo, x, y, accion)
                            except ValueError:
                                print("Entrada inválida. Por favor, ingrese números enteros.")
                            mostrar_acciones(archivo)
                            break
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
                    break
                elif continuar_mapa == 'salir':
                    break
                else:
                    print("Continuando con el mismo mapa.")

        elif opcion == 'salir':
            break
