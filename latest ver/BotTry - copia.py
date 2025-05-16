from AutomoveHandler import automove_check
from MirWindowHandler import capture_window_screenshot
from RespawnHandler import respawn_check
from OpeningChestHandler import openingchest_check 
from CreateNLoadSecuencias import interpretar_acciones
from ClickAtMir import get_window_click_map_randomizer

def try_forever(window_title):
    get_window_click_map_randomizer(0,0,window_title,0) #initialization ??? it doesn't work without this
    try:
        archivo = input("archivo de acciones?")
##    acciones = leer_acciones(archivo)
        interpretar_acciones(archivo,window_title)
        while True:
            window_title = "Mir4G[1]"
            capture_window_screenshot(window_title)
            status = automove_check()
            print(f"This will run forever: {status}")
            status = respawn_check()
            print(f"This will run forever: {status}")
            status = openingchest_check()
            print(f"This will run forever: {status}")
    except KeyboardInterrupt:
        print("Stopped by user")

window_title = "Mir4G[1]"

try_forever(window_title)
