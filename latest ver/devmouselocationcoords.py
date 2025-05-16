import pyautogui
import win32gui
import pygetwindow as gw
import time

def get_mouse_location():
    # Get the screen coordinates of the mouse
    screen_x, screen_y = pyautogui.position()
    print(f"Screen coordinates: ({screen_x}, {screen_y})")
    return screen_x, screen_y

def get_mouse_window_info(screen_x, screen_y):
    # Get the window handle at the mouse position
    hwnd = win32gui.WindowFromPoint((screen_x, screen_y))
    if hwnd != 0:
        window_title = win32gui.GetWindowText(hwnd)
        if window_title:
            left, top = win32gui.ClientToScreen(hwnd, (0, 0))
            rel_x = screen_x - left
            rel_y = screen_y - top
            print(f"Mouse is over window '{window_title}' (HWND: {hwnd})")
            print(f"Window coordinates: ({rel_x}, {rel_y}) relative to window '{window_title}'")
            return hwnd, rel_x, rel_y
    print("Mouse is not over any window")
    return None, None, None

while True:
    screen_x, screen_y = get_mouse_location()
    hwnd, rel_x, rel_y = get_mouse_window_info(screen_x, screen_y)
    time.sleep(1)  # Update every second
