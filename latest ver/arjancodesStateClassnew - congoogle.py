import keyboard
import pickle
import time
import random
import numpy as np
from SSCompare_tmp_ref import respawn_check, automove_check, autocollecting_check, map_check, collectingvoidorb_check, autocollecting_check
from time import sleep
from MirWindowHandler import capture_window_screenshot
from ClickAtMir2 import press_key_in_game
##from CreateNLoadSecuencias import interprete_de_accion, travel_to_map
#creando nuevo interprete y travel (travel es el mismo nuevo archivo)
from CreateMapGGleInportModulesComas import interprete_de_accion, travel_to_map

class AfkState:
    def __init__(self):
        print("AfkState Active - For AutoMoveState press 'F7'")
        print("For EXIT 'F8' key press...")
        
    def execute(self):
        print("AFK")


class ReturningToMapState:
    def __init__(self, bot, actions_loaded, window_title, current_action_index=0):
        self.bot = bot
        self.actions_loaded = actions_loaded
        self.window_title = window_title
        self.current_action_index = current_action_index
        #añadir current action para leer nombre de mapa dentro del archivo en la accion que debe
        press_key_in_game(self.window_title, "escape") #prevent open ui
        press_key_in_game(self.window_title, "esc")
        sleep(1)
        print("ReturningToMapState initialized...")

    def execute(self):
        print("Checking map status...")
##        mapcheck = map_check(self.actions_file[:-4],self.window_title)
#cambio1#hecho        # hacer map check despues cuando se itenera entre acciones y [0] = MAP y [1] = nombre mapa
        mapcheck = map_check(self.actions_loaded[self.current_action_index][1],self.window_title)
        print (self.actions_loaded[self.current_action_index][1])
        print(mapcheck)
        if mapcheck == "map_on":
            print("Map is on, Switched to AutoMoveState")
            self.bot.state = AutoMoveState(self.bot, self.actions_loaded, self.window_title)  # Volver al automove
        elif mapcheck == "map_off":
            print("Map is off, executing travel_to_map")
            print(self.actions_loaded[self.current_action_index][1])
##            travel_to_map(self.actions_file, self.bot.window_title)  # Llamar a travel_to_map
#cambio2#hecho            #hacer travel to map con [1](nombre de mapa), y self.actions_file puede tener cualquier nombre ahora
            travel_to_map(self.actions_loaded[self.current_action_index][1], self.bot.window_title)
            sleep(random.randint(8, 11))  # Tiempo para cargar el mapa de viaje
            press_key_in_game(self.window_title, "escape") #prevent open ui
            press_key_in_game(self.window_title, "esc")
            self.bot.state = AutoMoveState(self.bot, self.actions_loaded, self.window_title)
            print("Switched to AutoMoveState")

class RespawningState:
    def __init__(self, bot, actions_loaded, window_title):
        self.bot = bot
        self.window_title = window_title
        self.previous_state = bot.previous_state
        self.actions_loaded = actions_loaded  # Agregar self.actions_loaded
        print("Just started respawning...")
        
    def execute(self):
        print("Respawning... Waiting for a random duration")
        sleep(random.randint(8, 11))  # Tiempo para respawning y cargar el mapa de la ciudad
        print("Switched to ReturningToMapState")
        self.bot.state = ReturningToMapState(self.bot, self.actions_loaded, self.window_title)


class AutoMoveState:
    def __init__(self, bot, actions_loaded, window_title):
        self.bot = bot
 #acaa actions
##        self.actions_file = f"secuencias/{actions_file}"  # Asignar ubicacion de self.actions_file correctamente
        self.window_title = window_title
#acaa nomas
##        self.actions = self.load_actions()
        self.actions_loaded = actions_loaded
        line_count = len(self.actions_loaded)#contar lineas
##        
        self.random_action_pos_start = random.randint(0, line_count -2)# random cantidad de lineas 
        self.current_action_index = self.random_action_pos_start #asignar a current action el pos random
##        self.current_action_index = 0
        self.start_time = time.time()
        self.max_check_time = random.randint(4, 5)  # Random duration between 2 and 3 seconds
        self.previous_action = None  # Initialize previous_action
        sleep(2)  # wait 3 seconds to start
        press_key_in_game(self.window_title, "escape")
        press_key_in_game(self.window_title, "esc")
        sleep(1)  # wait 3 seconds to start
        press_key_in_game(self.window_title, "b")  # Press autoattack button
        press_key_in_game(self.window_title, "n")  # Fast switch to automine
        press_key_in_game(self.window_title, "n")  # Fast switch to turn off automine        
        print("AutoMoveState Active - For AfkState press 'F7' - For EXIT 'F8'")

##    def load_actions(self):
##        with open(self.actions_file, 'rb') as file:
##            return pickle.load(file)

    def switch(self, bot):
        bot.state = AfkState()
        print("Switching to AfkState")

    def execute(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        print("AutoMove: Checking automove...")
        try:
            automoveCheck = automove_check(self.window_title)  # No parameters needed
            print(f"automoveCheck: {automoveCheck}")
            if automoveCheck == "automove_on":
                self.start_time = current_time  # Reset the timer if automove is on
            elif automoveCheck == "automove_off" and elapsed_time >= self.max_check_time:
                if self.previous_action in ["Chest","OpenChest","OpeningChestHandler", "RecolectingVoidOrbHandler"]:
                    self.previous_action = None  # Clear previous_action
                    self.bot.state = OpeningChestState(self.bot, self.window_title)
                elif self.current_action_index < len(self.actions_loaded):       
#cambio3#hecho                    #cambiar el interprete porque funciona de otra manera ahora
##   acaa            #interprete de acciones, hara lo que diga la linea, y devuelve la accion en la posicion 3 para continuar     
                    action_type = interprete_de_accion(self.actions_loaded[self.current_action_index], self.window_title)                   
                    self.bot.previous_state = self.bot.state
                    self.previous_action = action_type  # Save the current action as previous_action
                    self.start_time = current_time  # Reset the timer before checking automove status again
                    self.current_action_index += 1
                    print(f"action_type: {action_type}")
                else:
                    self.current_action_index = 0 # Reset the counter to repeat the file from action 0
                    print("Resetting action index to 0")
        except Exception as e:
            print(f"Error during automove_check: {e}")



class OpeningChestState:
    def __init__(self, bot, window_title):
        self.bot = bot
        self.window_title = window_title
        self.start_time = time.time()
        self.search_duration = random.randint(16, 17)  # Random time to search for chests between 15 and 18 seconds
        press_key_in_game(self.window_title, "escape") #prevent open ui
        press_key_in_game(self.window_title, "esc")
        press_key_in_game(self.window_title, "b")  # Press autoattack button
        press_key_in_game(self.window_title, "n")  # Fast switch to automine
        print(f"OpeningChestState State: is active")

    def switch(self, bot):
        bot.state = OpeningChestState(bot, self.window_title)
        print("Switching to OpeningChestState")

    def execute(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        try:
            if elapsed_time >= self.search_duration:
                print("Search duration exceeded, switching back to previous state")
                self.bot.state = self.bot.previous_state
                return

            chest_status = autocollecting_check(self.window_title)
            print(f"chest_status: {chest_status}")
            if chest_status == "autocollecting_on":
                self.start_time = current_time  # Reset the timer for additional search
        except Exception as e:
            print(f"Error during autocollecting_check: {e}")


class Bot:
    def __init__(self, window_title, actions_loaded, current_action_index):
        self.state = AfkState()
        self.previous_state = None
        self.window_title = window_title
        self.actions_loaded = actions_loaded  # Asignar self.actions_file correctamente
        self.current_action_index = current_action_index
        self.map_check_start_time = None  # Inicializar el contador de tiempo
        print(self.actions_loaded[1][0])

    def switch(self):
        self.state.switch(self)

    def execute(self):
        if isinstance(self.state, AfkState):
            print("AFK: Skipping capture window, respawn check, and state execution")
            return

        try:
            capture_window_screenshot(self.window_title)
        except Exception as e:
            print(f"Error capturing screenshot: {e}")

        try:
            respawnCheck = respawn_check(self.window_title)
            print(respawnCheck)
            if respawnCheck == "respawn_on":
                self.previous_state = self.state
                self.state = RespawningState(self, self.actions_loaded, self.window_title)  # Pasar actions_file y window_title
                return  # Exit the method to cancel subsequent execution
        except Exception as e:
            print(f"Error during respawn_check: {e}")

        if not isinstance(self.state, ReturningToMapState):
            print (self.actions_loaded[self.current_action_index][1])
            try:
## cambiado de donde viene el nombre del mapa
##                mapcheck = map_check(self.actions_file[:-4],self.window_title)  # Cortar extensión ".pkl"
                mapcheck = map_check(self.actions_loaded[self.current_action_index][1],self.window_title)                
                print(mapcheck)
                if mapcheck == "map_off":
                    if self.map_check_start_time is None:
                        self.map_check_start_time = time.time()  # Inicializar el contador de tiempo
                    elapsed_time = time.time() - self.map_check_start_time
                    if elapsed_time >= 20:
                        print("Map is off for 20 seconds, switching to ReturningToMapState")
                        self.previous_state = self.state
                        self.state = ReturningToMapState(self, self.actions_loaded, self.window_title)  # Cambiar estado a ReturningToMapState
                        return  # Exit the method to cancel subsequent execution
                    else:
                        print(f"Map is off, elapsed time: {elapsed_time:.2f} seconds")
                else:
                    self.map_check_start_time = None  # Reiniciar el contador de tiempo si el mapa está bien
            except Exception as e:
                print(f"Error during map_check: {e}")

        self.state.execute()




def main():
    window_title = "Mir4G[1]"
##    actions_file = "EliteBicheonCastleBackstreet.pkl"
    actions_file_name = "combine2"
    current_action_index = 0 #initiate at random 0 raction

##    def load_actions_file(actions_file_name):
##        actions_file = f"secuencias/{actions_file_name}.pkl"
##        with open(actions_file, 'rb') as file:
##            return pickle.load(file)
    def load_actions_file(actions_file_name):
        actions_file = f"secuencias/{actions_file_name}.pkl"
        with open(actions_file, 'rb') as file:
            loaded_data = pickle.load(file)
        return np.array(loaded_data)

    
    actions_loaded = load_actions_file(actions_file_name)
    bot = Bot(window_title, actions_loaded, current_action_index) # Pasar actions_file
    
    while True:
        if keyboard.is_pressed('F7'):
            if isinstance(bot.state, AfkState):
                print("Switching to AutoMoveState")
                bot.state = AutoMoveState(bot, actions_loaded, window_title)            
                sleep(1)
            else:
                print("Switching to AfkState")
                bot.state = AfkState()
                sleep(1)
        if keyboard.is_pressed('F2'):
            bot.state = OpeningChestState(bot)            
        if keyboard.is_pressed('F8'):
            print("bye")
            break  # Exit the loop after printing

        try:
            bot.execute()
        except Exception as e:
            print(f"Error executing state: {e}")
        
        sleep(0.1)  # Small delay to prevent high CPU usage

if __name__ == "__main__":
    main()
