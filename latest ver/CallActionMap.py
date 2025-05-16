import pickle
import os

def ejecutar_acciones(archivo):
    try:
        with open(archivo, 'rb') as file:
            acciones = pickle.load(file)
            for accion in acciones:
                x, y, accion = accion
                if accion == 'click':
                    click(x, y)
                elif accion == 'recolectar':
                    recolectar(x, y)
                else:
                    print(f"Acción desconocida: {accion}")
    except FileNotFoundError:
        print("No se encontraron acciones guardadas en el archivo.")

def click(x, y):
    print(f"Click en ({x}, {y})")
    # Aquí puedes agregar el código para realizar el click, por ejemplo:
    # pyautogui.moveTo(x, y)
    # pyautogui.click()

def recolectar(x, y):
    print(f"Recolectar en ({x}, {y})")
    # Aquí puedes agregar el código para realizar la acción de recolectar

if __name__ == "__main__":
    mapa = input("Ingrese el nombre del mapa: ")
    carpeta = 'secuencias'
    archivo = os.path.join(carpeta, f"{mapa}.pkl")

    # Verificar si el archivo existe
    if not os.path.exists(archivo):
        print(f"No se encontró el archivo {archivo}. Asegúrate de que el nombre del mapa es correcto y que el archivo existe.")
    else:
        ejecutar_acciones(archivo)
