import pyautogui
from MirWindowHandler import bring_window_to_front

def press_key_in_game(window_title, key):
    bring_window_to_front(window_title)
    pyautogui.press(key)
    print(f"Pressed {key} in {window_title}")

if __name__ == "__main__":
    game_window_title = "Mir4G[1]"
    key_to_press = "b"  # key you want to press
    press_key_in_game(game_window_title, key_to_press)
    key_to_press = "n"  # Change this to the key you want to press
    press_key_in_game(game_window_title, key_to_press)

