import keyboard
from AutomoveHandler import automove_check
from MirWindowHandler import capture_window_screenshot
from RespawnHandler import respawn_check
from OpeningChestHandler import openingchest_check 
from time import sleep

"""
from typing import Protocol
class BotState(Protocol):
    def switch(self,bot) -> None:
        ...
"""

class AfkState:
    def __init__(self):
        print("AfkState Active - For AutoMoveState press 'F7'")
        print("For EXIT 'F8' key press...")

class AutoMoveState:
    def __init__(self):
        print("AutoMoveState Active - For AfkState press 'F7' - For EXIT 'F8'")
    
    def switch(self, bot):
        bot.state = AfkState()
        print("Switching to AfkState")


class OpeningChestState:
    def __init__(self):
        print(f"OpeningChestState State: is active")
    def switch(self, bot):
        bot.state = OpeningChestState()
        print("Switching to OpeningChestState")

class Bot:
    def __init__(self):
        self.state = AfkState()
    def switch(self):
##        if hasattr(self.state, 'switch'):
         self.state.switch(self)


def main():
    bot = Bot()

    while True:
        if keyboard.is_pressed('F7'):
            if isinstance(bot.state , AfkState):
                print("Switching to AutoMoveState")
                bot.state = AutoMoveState()            
                sleep(1)
            else:
                print("Switching to AfkState")
                bot.state = AfkState()
                sleep(1)
##        bot.switch()  # DEV call the switch method of the Bot class again only to exit loop
        if keyboard.is_pressed('F2'):
            bot.state = OpeningChestState()            
        if keyboard.is_pressed('F8'):
            print("bye")
            break  # Exit the loop after printing

if __name__ == "__main__":
    main()

