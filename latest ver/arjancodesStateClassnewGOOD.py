import keyboard
import pickle
import time
import random
from SSCompare_tmp_ref import respawn_check, automove_check, openingchest_check
from time import sleep
from MirWindowHandler import capture_window_screenshot
from ClickAtMir import get_window_click_space_randomizer, get_window_click_map_randomizer

class AfkState:
    def __init__(self):
        print("AfkState Active - For AutoMoveState press 'F7'")
        print("For EXIT 'F8' key press...")
        
    def execute(self):
        print("AFK")

class RespawningState:
    def __init__(self, bot):
        self.bot = bot
        self.previous_state = bot.previous_state
        print("Just started respawning...")
        
    def execute(self):
        print("Respawning... Waiting for a random duration")
        sleep(random.randint(8, 12))
        self.bot.state = self.previous_state

class AutoMoveState:
    def __init__(self, bot, actions_file, window_title):
        self.bot = bot
        self.actions_file = actions_file
        self.window_title = window_title
        self.actions = self.load_actions()
        self.current_action_index = 0
        self.start_time = time.time()
        self.max_check_time = 3  # Maximum duration to check automove status
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
            automoveCheck = automove_check()
            print(automoveCheck)
            if automoveCheck == "automove_on":
                self.start_time = current_time  # Reset the timer if automove is on
            elif automoveCheck == "automove_off" and elapsed_time >= self.max_check_time:
                if self.current_action_index < len(self.actions):
                    x, y, action_type = self.actions[self.current_action_index]
                    get_window_click_map_randomizer(x, y, self.window_title, 5)
                    self.bot.previous_state = self.bot.state
                    self.start_time = current_time  # Reset the timer before checking automove status again
                    if action_type == "OpeningChestHandler":
                        self.bot.state = OpeningChestState(self.bot)
                    self.current_action_index += 1
        except Exception as e:
            print(f"Error during automove_check: {e}")

class OpeningChestState:
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.search_duration = random.randint(15, 18)  # Random time to search for chests between 15 and 18 seconds
        print(f"OpeningChestState State: is active")

    def switch(self, bot):
        bot.state = OpeningChestState(bot)
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
            print(f"chest_status{chest_status}")
            if chest_status == "openingchest_on":
                self.start_time = current_time  # Reset the timer for additional search
        except Exception as e:
            print(f"Error during openingchest_check: {e}")

class Bot:
    def __init__(self, window_title):
        self.state = AfkState()
        self.previous_state = None
        self.window_title = window_title

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
                self.state = RespawningState(self)
                return  # Exit the method to cancel subsequent execution
        except Exception as e:
            print(f"Error during respawn_check: {e}")
        
        self.state.execute()

def main():
    window_title = "Mir4G[1]"
    actions_file = "secuencias/1.pkl"
    bot = Bot(window_title)

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
