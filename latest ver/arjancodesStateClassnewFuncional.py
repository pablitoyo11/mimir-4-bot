import keyboard
import pickle
import time
import random
from SSCompare_tmp_ref import respawn_check, automove_check, openingchest_check, map_check
from time import sleep
from MirWindowHandler import capture_window_screenshot
from ClickAtMir import press_key_in_game
from CreateNLoadSecuencias import interprete_de_accion, travel_to_map

class AfkState:
    def __init__(self):
        print("AfkState Active - For AutoMoveState press 'F7'")
        print("For EXIT 'F8' key press...")
        
    def execute(self):
        print("AFK")

class RespawningState:
    def __init__(self, bot, actions_file, window_title):
        self.bot = bot
        self.window_title = window_title
        self.previous_state = bot.previous_state
        self.actions_file = actions_file  # Agregar self.actions_file
        print("Just started respawning...")
        
    def execute(self):
        print("Respawning... Waiting for a random duration")
        sleep(random.randint(12, 17)) #time for respawning and loading city map
        print("Returning to map... Waiting for a random duration")
        travel_to_map(self.actions_file, self.bot.window_title)  # Llamar a travel_to_map
        sleep(random.randint(12, 17)) #time for loading travel map    
        self.bot.state = AutoMoveState(self.bot, self.actions_file, self.window_title)            



class AutoMoveState:
    def __init__(self, bot, actions_file, window_title):
        self.bot = bot
        self.actions_file = f"secuencias/{actions_file}"  # Asignar self.actions_file correctamente
        self.window_title = window_title
        self.actions = self.load_actions()
        self.current_action_index = 0
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

    def load_actions(self):
        with open(self.actions_file, 'rb') as file:
            return pickle.load(file)

    def switch(self, bot):
        bot.state = AfkState()
        print("Switching to AfkState")

    def execute(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        print("AutoMove: Checking automove...")
        try:
            automoveCheck = automove_check()  # No parameters needed
            print(f"automoveCheck: {automoveCheck}")
            if automoveCheck == "automove_on":
                self.start_time = current_time  # Reset the timer if automove is on
            elif automoveCheck == "automove_off" and elapsed_time >= self.max_check_time:
                if self.previous_action == "OpeningChestHandler":
                    self.previous_action = None  # Clear previous_action
                    self.bot.state = OpeningChestState(self.bot, self.window_title)
                elif self.current_action_index < len(self.actions):
                    action_type = interprete_de_accion(self.actions[self.current_action_index], self.window_title)
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
        self.search_duration = random.randint(15, 18)  # Random time to search for chests between 15 and 18 seconds
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

            chest_status = openingchest_check()
            print(f"chest_status: {chest_status}")
            if chest_status == "openingchest_on":
                self.start_time = current_time  # Reset the timer for additional search
        except Exception as e:
            print(f"Error during openingchest_check: {e}")

class Bot:
    def __init__(self, window_title, actions_file):
        self.state = AfkState()
        self.previous_state = None
        self.window_title = window_title
        self.actions_file = actions_file  # Asignar self.actions_file correctamente

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
            respawnCheck = respawn_check()
            print(respawnCheck)
            if respawnCheck == "respawn_on":
                self.previous_state = self.state
                self.state = RespawningState(self, self.actions_file, self.window_title)  # Pasar actions_file
                return  # Exit the method to cancel subsequent execution
        except Exception as e:
            print(f"Error during respawn_check: {e}")
        self.state.execute()


def main():
    window_title = "Mir4G[1]"
    actions_file = "EliteBicheonCastleBackstreet.pkl"
    bot = Bot(window_title, actions_file) # Pasar actions_file
    
    while True:
        if keyboard.is_pressed('F7'):
            if isinstance(bot.state, AfkState):
                print("Switching to AutoMoveState")
                bot.state = AutoMoveState(bot, actions_file, window_title)            
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
