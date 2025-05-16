from AutomoveHandler import automove_check
from MirWindowHandler import capture_window_screenshot
from RespawnHandler import respawn_check
from OpeningChestHandler import openingchest_check 

# import sys
#import pygame
#import states () import menu, gameplay, game over,
#


pygame.init()
screen = pygame.display.set_mode((1920,1080))
states = {
    "AfkState": AfkState(),
    "AutoMoveState": AutoMoveState(),
    "OpeningChestState": OpeningChestState(),
}

game = Game(screen,states, "AfkState")
game.run()

pygame.quit()
sys.exit()




class BotState(Protocol):
    def switch(self,bot) -> None:
        ...

class AfkState:
    def switch(self,bot) -> None:
        bot.state = AutoMoveState()
        print("Afkstate")

class AutoMoveState:
    def switch(self,bot) -> None:
        bot.state = AfkState()
        print("AutoMoveState")
"""
class OpeningChestState:
    def switch(self,bot) -> None:
        bot.state = OpeningChestState()
        print("OpeningChestState")
"""

"""
class Bot:
    def __init__(self) -> None:
        self.state = AfkState()
    def switch(self) -> None:
        self.state.switch(self)
"""
class Game(object):
    def __init__(self) -> None:
        self.state = AfkState()
    def switch(self) -> None:
        self.state.switch(self)

def main() -> None:
    bot = Bot()
    bot.switch()
    bot.switch()
    bot.switch()
    bot.switch()


if __name__ == "__main__":
    main()

        
