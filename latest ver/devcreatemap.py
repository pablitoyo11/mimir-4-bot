import pickle
import os

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

if __name__ == "__main__":
    mapa = input("Ingrese el nombre del mapa: ")
    carpeta = 'secuencias'
    archivo = os.path.join(carpeta, f"{mapa}.pkl")

    # Crear la carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)

    while True:
        x = int(input("Ingrese la coordenada X: "))
        y = int(input("Ingrese la coordenada Y: "))
        accion = input("Ingrese la acción: ")
        #acomodar a porcentajes resolucion para ingresos 640x375
        x = round(x / 640, 3)
        y = round(y / 375, 3)
        agregar_accion(x, y, accion, archivo)

        continuar = input("¿Desea agregar otra acción? (s/n): ")
        if continuar.lower() != 's':
            break

    print(f"Acciones guardadas en {archivo}:")
    mostrar_acciones(archivo)
