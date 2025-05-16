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

def agregar_area(xs, ys, xe, ye, accion, archivo):
    # Crear la carpeta si no existe
    os.makedirs(os.path.dirname(archivo), exist_ok=True)
    # Cargar las acciones existentes
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
    except FileNotFoundError:
        acciones = []
    # Agregar la nueva acción de área
    acciones.append((xs, ys, xe, ye, accion))  
    # Guardar las acciones actualizadas
    with open(archivo, 'wb') as file:
        pickle.dump(acciones, file)  
    print(f"Acción {accion} en área ({xs}, {ys}, {xe}, {ye}) agregada y guardada en {archivo}.")

def mostrar_acciones(archivo):
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
            for i, accion in enumerate(acciones):
                if len(accion) == 3:
                    x, y, tipo_accion = accion
                    x = round(x * 640)
                    y = round(y * 375)
                    print(f"Línea {i+1}: ({x}, {y}, {tipo_accion})")
                elif len(accion) == 5:
                    xs, ys, xe, ye, tipo_accion = accion
                    xs = round(xs * 640)
                    ys = round(ys * 375)
                    xe = round(xe * 640)
                    ye = round(ye * 375)
                    print(f"Línea {i+1}: ({xs}, {ys}, {xe}, {ye}, {tipo_accion})")
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
        if len(acciones[linea - 1]) == 3:
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
            x = int(input("Ingrese la coordenada X: "))
            y = int(input("Ingrese la coordenada Y: "))
            x = round(x / 640, 3)
            y = round(y / 375, 3)
            acciones[linea - 1] = (x, y, accion)
        elif len(acciones[linea - 1]) == 5:
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
            xs = int(input("Ingrese la coordenada X inicial: "))
            ys = int(input("Ingrese la coordenada Y inicial: "))
            xe = int(input("Ingrese la coordenada X final: "))
            ye = int(input("Ingrese la coordenada Y final: "))
            xs = round(xs / 640, 3)
            ys = round(ys / 375, 3)
            xe = round(xe / 640, 3)
            ye = round(ye / 375, 3)
            acciones[linea - 1] = (xs, ys, xe, ye, accion)
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

def insertar_area(archivo, xs, ys, xe, ye, accion):
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
        acciones.append((xs, ys, xe, ye, accion))
        with open(archivo, 'wb') as file:
            pickle.dump(acciones, file)
        print("Nueva área insertada con éxito.")
    except FileNotFoundError:
        print("Error: El archivo no existe.")

def manejar_click_mapa(archivo):
    try:
        x = int(input("Ingrese la coordenada X: "))
        y = int(input("Ingrese la coordenada Y: "))
        print("Seleccione la acción:")
        print("1. AutomoveHandler")
        print("2. OpeningChestHandler")
        print("3. MiningHandler")
        print("4. AtackHandler")
        print("5. MovingWaitHandler")
        accion_opcion = input("Ingrese el número de la acción: ").strip()
        while accion_opcion not in ['1', '2', '3', '4', '5']:
            accion_opcion = input("Respuesta inválida. Ingrese el número de la acción (1, 2, 3, 4 o 5): ").strip()
        if accion_opcion == '1':
            accion = 'AutomoveHandler'
        elif accion_opcion == '2':
            accion = 'OpeningChestHandler'
        elif accion_opcion == '3':
            accion = 'MiningHandler'
        elif accion_opcion == '4':
            accion = 'AtackHandler'
        elif accion_opcion == '5':
            accion = 'MovingWaitHandler'
        x = round(x / 640, 3)
        y = round(y / 375, 3)
        agregar_accion(x, y, accion, archivo)
    except ValueError:
        print("Entrada inválida. Por favor, ingrese números enteros.")

if __name__ == "__main__":
    while True:
        opcion = input("¿Desea ingresar un nuevo mapa o salir? (1. ingresar / 2. salir): ").strip().lower()
        while opcion not in ['1', '2']:
            opcion = input("Respuesta inválida. ¿Desea ingresar un nuevo mapa o salir? (1. ingresar / 2. salir): ").strip().lower()

        if opcion == '1':
            while True:
                mapa = input("Ingrese el nombre del mapa: ")
                carpeta = 'secuencias'
                archivo = os.path.join(carpeta, f"{mapa}.pkl")

                # Crear la carpeta si no existe
                os.makedirs(carpeta, exist_ok=True)

                if os.path.exists(archivo):
                    print("Ese mapa ya existe.")
                    ver_mapa = input("¿Desea verlo? (1. sí / 2. no): ").strip().lower()
                    while ver_mapa not in ['1', '2']:
                        ver_mapa = input("Respuesta inválida. ¿Desea verlo? (1. sí / 2. no): ").strip().lower()
                    if ver_mapa == '1':
                        mostrar_acciones(archivo)
                    
                    accion_mapa = input("¿Desea eliminar el contenido, continuar editando, crear un nuevo archivo o salir? (1. eliminar / 2. editar / 3. nuevo / 4. salir): ").strip().lower()
                    while accion_mapa not in ['1', '2', '3', '4']:
                        accion_mapa = input("Respuesta inválida. ¿Desea eliminar el contenido, continuar editando, crear un nuevo archivo o salir? (1. eliminar / 2. editar / 3. nuevo / 4. salir): ").strip().lower()
                    if accion_mapa == '1':
                        eliminar_acciones(archivo)
                        break
                    elif accion_mapa == '3':
                        continue  # Reinicia el bucle para preguntar el nombre del mapa nuevamente
                    elif accion_mapa == '4':
                        break
                    elif accion_mapa == '2':
                        mostrar_acciones(archivo)
                        editar_opcion = input("¿Desea editar una línea existente o insertar una nueva línea? (1. editar / 2. insertar): ").strip().lower()
                        while editar_opcion not in ['1', '2']:
                            editar_opcion = input("Respuesta inválida. ¿Desea editar una línea existente o insertar una nueva línea? (1. editar / 2. insertar): ").strip().lower()
                        if editar_opcion == '1':
                            editar_accion(archivo)
                        elif editar_opcion == '2':
                            try:
                                print("Seleccione la acción:")
                                print("1. AbrirMapa")
                                print("2. ClickMapa")
                                accion_opcion = input("Ingrese el número de la acción: ").strip()
                                while accion_opcion not in ['1', '2']:
                                    accion_opcion = input("Respuesta inválida. Ingrese el número de la acción (1 o 2): ").strip()
                                if accion_opcion == '1':
                                    accion = 'AbrirMapa'
                                    insertar_area(archivo, 520, 70, 600, 75, accion)
                                elif accion_opcion == '2':
                                    manejar_click_mapa(archivo)
                            except ValueError:
                                print("Entrada inválida. Por favor, ingrese números enteros.")
                            mostrar_acciones(archivo)
                            break
                else:
                    print("Creando mapa nuevo.")
                while True:
                    print("Seleccione la acción:")
                    print("1. AbrirMapa")
                    print("2. ClickMapa")
                    accion_opcion = input("Ingrese el número de la acción: ").strip()
                    while accion_opcion not in ['1', '2']:
                        accion_opcion = input("Respuesta inválida. Ingrese el número de la acción (1 o 2): ").strip()
                    if accion_opcion == '1':
                        accion = 'AbrirMapa'
                        agregar_area(520, 70, 600, 75, accion, archivo)
                    elif accion_opcion == '2':
                        manejar_click_mapa(archivo)

                    continuar = input("¿Desea agregar otra acción? (1. sí / 2. no): ").strip().lower()
                    while continuar not in ['1', '2']:
                        continuar = input("Respuesta inválida. ¿Desea agregar otra acción? (1. sí / 2. no): ").strip().lower()
                    if continuar != '1':
                        break

                print(f"Acciones guardadas en {archivo}:")
                mostrar_acciones(archivo)

                continuar_mapa = input("¿Desea agregar tareas en el mapa, ingresar nombre de otro mapa o salir? (1. agregar / 2. otro / 3. salir): ").strip().lower()
                while continuar_mapa not in ['1', '2', '3']:
                    continuar_mapa = input("Respuesta inválida. ¿Desea agregar tareas en el mapa, ingresar nombre de otro mapa o salir? (1. agregar / 2. otro / 3. salir): ").strip().lower()
                if continuar_mapa == '2':
                    break
                elif continuar_mapa == '3':
                    break
                else:
                    print("Continuando con el mismo mapa.")

        elif opcion == '2':
            break
