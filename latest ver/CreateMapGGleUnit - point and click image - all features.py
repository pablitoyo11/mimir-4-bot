import tkinter as tk
from tkinter import scrolledtext, Radiobutton, filedialog, messagebox
import platform
import time
import threading
import os
import pickle
from datetime import datetime
from PIL import Image, ImageTk
import json

if platform.system() == 'Windows':
    import win32gui
    import win32api
    import keyboard as kb
elif platform.system() == 'Darwin':
    from AppKit import NSWorkspace
    from Quartz import (
        CGWindowListCopyWindowInfo,
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID
    )
    from AppKit import NSEvent
    import keyboard as kb
elif platform.system() == 'Linux':
    import subprocess
    import keyboard as kb

is_running = True
saved_positions = []
ctrl_pressed = False
collecting_two_points = False
temp_points = []
collecting_key = False
key_string = None
edit_mode = False
edit_index = None
image_path = None
checkbox_states = {}
right_click_start_point = None
right_click_rect = None  # Store rectangle id


class WindowTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Window Info (Background)")
        self.root.geometry("1200x800")
        self.root.minsize(1200, 800)

        self.current_mode = tk.StringVar(value="UI")
        self.input_mode = tk.StringVar(value="otherWindow")
        self.image_tk = None

        self.label = tk.Label(self.root, text="Initializing...", font=("Arial", 12))
        self.label.pack(pady=20)

        # Main Frame to Hold Radio and Input Frames (Left Side)
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.X, padx=50)

        # Radio Buttons Frame (Left Top)
        radio_frame = tk.Frame(main_frame)
        radio_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        # Radio Buttons for Mode Selection
        self.radio_ui = Radiobutton(radio_frame, text="UI", variable=self.current_mode, value="UI",
                                    command=self.set_ui_mode)
        self.radio_ui.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

        self.radio_map = Radiobutton(radio_frame, text="MAP", variable=self.current_mode, value="MAP",
                                     command=self.set_map_mode)
        self.radio_map.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

        # Input Fields Frame (Left Top)
        input_frame = tk.Frame(main_frame)
        input_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        self.map_name_entry_label = tk.Label(input_frame, text="Map Name:")
        self.map_name_entry_label.pack(side=tk.TOP, anchor=tk.CENTER)
        self.map_name_entry = tk.Entry(input_frame, width=15, state=tk.DISABLED)
        self.map_name_entry.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

        self.map_action_entry_label = tk.Label(input_frame, text="Map Action:")
        self.map_action_entry_label.pack(side=tk.TOP, anchor=tk.CENTER)
        self.map_action_entry = tk.Entry(input_frame, width=15, state=tk.DISABLED)
        self.map_action_entry.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

        # Buttons Frame (Left Top)
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.TOP, pady=10)
        self.area_button = tk.Button(button_frame, text="AREA", command=self.area_button_click)
        self.area_button.pack(side=tk.LEFT, padx=5)
        self.point_button = tk.Button(button_frame, text="POINT", command=self.point_button_click)
        self.point_button.pack(side=tk.LEFT, padx=5)
        self.key_button = tk.Button(button_frame, text="KEY", command=self.key_button_click)
        self.key_button.pack(side=tk.LEFT, padx=5)

        # Save and Load Buttons (Left Top)
        save_load_frame = tk.Frame(main_frame)
        save_load_frame.pack(side=tk.TOP, pady=10)
        self.save_button = tk.Button(save_load_frame, text="Save", command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.load_button = tk.Button(save_load_frame, text="Load", command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Data Area (Right Top)
        self.data_area = tk.Frame(self.root)
        self.data_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=10)

        # Checkbox All Button (Right Top)
        self.checkbox_all_button = tk.Button(self.data_area, text="Select All / None", command=self.toggle_all_checkboxes)
        self.checkbox_all_button.pack(side=tk.TOP, pady=5, anchor=tk.CENTER)

        # Chat Frame with Scrollbar (Right Top)
        self.chat_frame_container = tk.Frame(self.data_area)
        self.chat_frame_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.chat_canvas = tk.Canvas(self.chat_frame_container, bg="white")
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.chat_scrollbar = tk.Scrollbar(self.chat_frame_container, orient=tk.VERTICAL,
                                            command=self.chat_canvas.yview)
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        self.chat_canvas.bind('<Configure>',
                             lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))

        self.chat_frame = tk.Frame(self.chat_canvas, bg="white")
        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

         # Information Labels (Left Bottom)
        self.info_label_frame = tk.Frame(self.root)
        self.info_label_frame.pack(side=tk.TOP, pady=5)
        self.info_label_1 = tk.Label(self.info_label_frame, text="At mouse location")
        self.info_label_1.pack(side=tk.LEFT, padx=5)
        self.info_label_2 = tk.Label(self.info_label_frame, text="press control+a to initiate area input")
        self.info_label_2.pack(side=tk.LEFT, padx=5)
        self.info_label_3 = tk.Label(self.info_label_frame, text="press again to close area and save")
        self.info_label_3.pack(side=tk.LEFT, padx=5)
        self.info_label_4 = tk.Label(self.info_label_frame, text="press control+p to insert point")
        self.info_label_4.pack(side=tk.LEFT, padx=5)

        # Load Image Button (Above Image)
        self.load_image_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_image_button.pack(side=tk.TOP, pady=10, anchor=tk.CENTER)

         # Input Mode Frame (Right of Image)
        self.input_mode_frame = tk.Frame(self.root)
        self.input_mode_frame.pack(side=tk.TOP, pady=10, anchor = tk.CENTER)

        # Image Canvas with Border (Bottom)
        self.image_canvas_container = tk.Frame(self.root, bg = "gray")
        self.image_canvas_container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True, pady = 10, padx = 5)

        self.image_canvas = tk.Canvas(self.image_canvas_container, bg="white", highlightthickness=0)
        self.image_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx= 1, pady = 1)

        # Radio Buttons for Input Selection
        self.radio_button_input = Radiobutton(self.input_mode_frame, text="other window input", variable=self.input_mode,
                                            value="otherWindow", command=self.set_radio_button_input_mode)
        self.radio_button_input.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

        self.radio_image = Radiobutton(self.input_mode_frame, text="image input", variable=self.input_mode, value="IMAGE",
                                    command=self.set_image_input_mode)
        self.radio_image.pack(side=tk.LEFT, padx=10, anchor=tk.CENTER)

        # Remove zoom on mousewheel, keep only the pan
        self.image_canvas.bind("<ButtonPress-1>", self.start_pan)
        self.image_canvas.bind("<B1-Motion>", self.pan_image)
        self.image_canvas.bind("<ButtonRelease-1>", self.stop_pan)

        self.image_canvas.bind("<KeyPress-plus>", self.zoom_in_key)
        self.image_canvas.bind("<KeyPress-minus>", self.zoom_out_key)
        self.image_canvas.bind("<Button-1>", self.on_image_click)
        self.image_canvas.bind("<Button-3>", self.on_right_click_press)
        self.image_canvas.bind("<B3-Motion>", self.on_right_click_drag)
        self.image_canvas.bind("<ButtonRelease-3>", self.on_right_click_release)

        self.pan_start_x = 0
        self.pan_start_y = 0
        self.pan_canvas_start_x = 0
        self.pan_canvas_start_y = 0

        self.zoom_scale = 1.0

        threading.Thread(target=self.tracking_loop, daemon=True).start()
        self.start_key_listener()

        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)

    def get_active_window_info(self):
        if platform.system() == 'Windows':
            try:
                hwnd = win32gui.GetForegroundWindow()
                if hwnd:
                    title = win32gui.GetWindowText(hwnd)
                    return hwnd, title
                else:
                    return None, None
            except Exception as e:
                print(f"Error getting active window info (Windows): {e}")
                return None, None
        elif platform.system() == 'Darwin':
            try:
                window_info = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
                if window_info:
                    for info in window_info:
                        if info.get('kCGWindowLayer', 0) == 0 and info.get('kCGWindowOwnerPID') == os.getpid():
                            return info.get('kCGWindowNumber'), info.get('kCGWindowName')
                return None, None
            except Exception as e:
                print(f"Error getting active window info (macOS): {e}")
                return None, None
        elif platform.system() == 'Linux':
            try:
                result = subprocess.run(['xdotool', 'getactivewindow'], capture_output=True, text=True, check=True)
                window_id = result.stdout.strip()
                if window_id:
                    result = subprocess.run(['xdotool', 'getwindowname', window_id], capture_output=True, text=True, check=True)
                    window_title = result.stdout.strip()
                    return window_id, window_title
                else:
                    return None, None
            except (FileNotFoundError, subprocess.CalledProcessError) as e:
                print(f"Error getting active window info (Linux): {e}")
                return None, None
            except Exception as e:
                print(f"Error getting active window info (Linux): {e}")
                return None, None
        else:
            return None, None
        return None, None

    def get_mouse_position(self):
        if platform.system() == 'Windows':
            try:
                x, y = win32api.GetCursorPos()
                return x, y
            except Exception as e:
                print(f"Error getting mouse position (Windows): {e}")
                return None, None
        elif platform.system() == 'Darwin':
            try:
                point = NSEvent.mouseLocation()
                return point.x, point.y
            except Exception as e:
                print(f"Error getting mouse position (macOS): {e}")
                return None, None
        elif platform.system() == 'Linux':
            try:
                output = subprocess.check_output(['xdotool', 'getmouselocation'], text=True)
                parts = output.split()
                x = int(parts[0].split(':')[1])
                y = int(parts[1].split(':')[1])
                return x, y
            except (FileNotFoundError, subprocess.CalledProcessError) as e:
                print(f"Error getting mouse position (Linux): {e}")
                return None, None
            except Exception as e:
                print(f"Error getting mouse position (Linux): {e}")
                return None, None
        else:
            return None, None
        return None, None

    def get_relative_mouse_position(self, hwnd, mouse_x, mouse_y):
        if hwnd is not None and mouse_x is not None and mouse_y is not None:
            if platform.system() == 'Windows':
                x = mouse_x - win32gui.GetWindowRect(hwnd)[0]
                y = mouse_y - win32gui.GetWindowRect(hwnd)[1]
            elif platform.system() == 'Darwin':
                bounds = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)[0].get('kCGWindowBounds', {})
                x = mouse_x - bounds.get('x', 0)
                y = mouse_y - bounds.get('y', 0)
            elif platform.system() == 'Linux':
                try:
                    x = mouse_x - int(subprocess.run(['xwininfo', '-id', hwnd], capture_output=True, text=True,
                                                    check=True).stdout.split("Absolute upper-left X: ")[1].split("\n")[
                                        0])
                    y = mouse_y - int(subprocess.run(['xwininfo', '-id', hwnd], capture_output=True, text=True,
                                                    check=True).stdout.split("Absolute upper-left Y: ")[1].split("\n")[
                                        0])
                except (FileNotFoundError, subprocess.CalledProcessError):
                    print(f"Error getting relative position")
                    return None, None
            return x, y
        return None, None

    def tracking_loop(self):
        global is_running
        while is_running:
            hwnd, window_title = self.get_active_window_info()
            mouse_x, mouse_y = self.get_mouse_position()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            if hwnd is not None and mouse_x is not None and mouse_y is not None:
                try:
                    x, y = self.get_relative_mouse_position(hwnd, mouse_x, mouse_y)
                    self.label.config(text=f"{timestamp}: Window: {window_title}\nMouse: x={int(x)}, y={int(y)}")
                except Exception as e:
                    print(f"Error Getting window Rect or Position {e}")
                    self.label.config(text=f"{timestamp}: Window: (Error Getting window Rect or Position)\nMouse: x=n/a, y=n/a")
            else:
                self.label.config(text=f"{timestamp}: Window: (No Window Under Mouse)\nMouse: x=n/a, y=n/a")
            time.sleep(0.1)

    def stop_tracking(self):
        global is_running
        is_running = False

    def exit_program(self):
         # Unregister the hotkeys to avoid keys from being locked
        try:
          kb.unhook_all()
        except:
           pass

        self.stop_tracking()
        self.root.destroy()

    def save_position(self):
        global saved_positions, temp_points, collecting_two_points, edit_mode, edit_index

        x, y = None, None
        map_name = self.map_name_entry.get()
        map_action = self.map_action_entry.get()
        new_data = None
        if collecting_two_points:
             if len(temp_points) == 2:
                 x1, y1 = temp_points[0]
                 x2, y2 = temp_points[1]
                 if self.current_mode.get() == 'MAP':
                     new_data = f'MAP {map_name} {map_action} pointarea {int(x1)} {int(y1)} {int(x2)} {int(y2)}'
                 elif self.current_mode.get() == 'UI':
                      new_data = f'UI pointarea {int(x1)} {int(y1)} {int(x2)} {int(y2)}'
                 elif self.input_mode.get() == 'IMAGE':
                      new_data = f'pointarea {int(x1)} {int(y1)} {int(x2)} {int(y2)}'
                 else:
                      new_data = f'pointarea {int(x1)} {int(y1)} {int(x2)} {int(y2)}'
                 temp_points = []
                 collecting_two_points = False
        elif self.input_mode.get() == "otherWindow":
                hwnd, window_title = self.get_active_window_info()
                mouse_x, mouse_y = self.get_mouse_position()
                
                x, y = self.get_relative_mouse_position(hwnd, mouse_x, mouse_y)
                if x is not None and y is not None:
                    if self.current_mode.get() == 'MAP':
                        new_data = f'MAP {map_name} {map_action} pointarea {int(x)} {int(y)} {int(x)} {int(y)}'
                    elif self.current_mode.get() == 'UI':
                        new_data = f'UI pointarea {int(x)} {int(y)} {int(x)} {int(y)}'
                    else:
                        new_data = f'pointarea {int(x)} {int(y)} {int(x)} {int(y)}'

        elif self.input_mode.get() == "IMAGE" and self.image_tk:
            x, y = self.get_mouse_position_on_image()
            if self.current_mode.get() == 'MAP':
                 new_data = f'MAP {map_name} {map_action} pointarea {int(x)} {int(y)} {int(x)} {int(y)}'
            elif self.current_mode.get() == 'UI':
                 new_data = f'UI pointarea {int(x)} {int(y)} {int(x)} {int(y)}'
            elif self.input_mode.get() == 'IMAGE':
                 new_data = f'pointarea {int(x)} {int(y)} {int(x)} {int(y)}'
            else:
                 new_data = f'pointarea {int(x)} {int(y)} {int(x)} {int(y)}'

        # Modify data or append based on edit_mode
        if new_data:
            if edit_mode:
                saved_positions[edit_index] = new_data
                edit_mode = False
                edit_index = None
            else:
                saved_positions.append(new_data)

            self.update_chatbox()
    
    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl")
        if file_path:
            try:
                with open(file_path, 'wb') as f:
                    pickle.dump(saved_positions, f)
                messagebox.showinfo("Save", "Data saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving data: {e}")

    def load_data(self):
        global saved_positions, checkbox_states, image_path
        file_path = filedialog.askopenfilename(defaultextension=".pkl")
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    saved_positions = pickle.load(f)
                    checkbox_states = {i: True for i in range(len(saved_positions))}
                self.update_chatbox()
                if image_path:
                    self.load_image_on_canvas(image_path)
                messagebox.showinfo("Load", "Data loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error loading data: {e}")

    def load_image(self):
        global image_path, saved_positions
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            image_path = file_path
            self.load_image_on_canvas(file_path)
            self.update_chatbox()

    def load_image_on_canvas(self, image_path):
        try:
            image = Image.open(image_path)
            self.image_tk = ImageTk.PhotoImage(image)

            self.image_canvas.delete("all")
            self.image_canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW, tags="image_on_canvas")
            self.image_canvas.image = self.image_tk

            # Calculate scaling to fit the image
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            image_width = image.width
            image_height = image.height

            width_scale = canvas_width / image_width
            height_scale = canvas_height / image_height
            scale_factor = min(width_scale, height_scale)

            self.zoom_scale = scale_factor
            self.image_canvas.scale("all", 0, 0, scale_factor, scale_factor)

            # Update the scroll region and remove space around the image
            self.image_canvas.config(scrollregion=self.image_canvas.bbox("all"))

            # Adjust container to fit exactly the image
            self.image_canvas_container.config(width = int(image_width * scale_factor) + 2, height = int(image_height * scale_factor) + 2)

            #Update window size
            self.update_window_size(image.width, image.height)

        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")
            image_path = None
            return

    def update_window_size(self, image_width, image_height):
        min_width = 1200  # set initial min width
        min_height = 800  # set initial min height

        chat_width = 400 # Set the chat width
        padding_x = 50
        padding_y = 300
        new_width = max(min_width, image_width + padding_x + 150)  # Minimum width to fit image and some padding
        new_height = max(min_height, image_height + padding_y) # Min height to fit the image and some padding
        self.root.geometry(f"{new_width}x{new_height}")

    def update_chatbox(self):
        # Destroy existing widgets in the chat_frame
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        # Clear the image canvas and load the image
        self.image_canvas.delete("all")
        if image_path:
            self.load_image_on_canvas(image_path)
        else:
            self.zoom_scale = 1

        for index, item in enumerate(saved_positions):
            line_frame = tk.Frame(self.chat_frame, bg="white")
            line_frame.pack(fill=tk.X, padx=5, pady=1)

            line_frame.grid_columnconfigure(2, weight=1)
            bg_color = "lightgray" if edit_mode and edit_index == index else "white"
            line_frame.config(bg=bg_color)

            checkbox_var = tk.BooleanVar(value=checkbox_states.get(index, True))
            checkbox = tk.Checkbutton(line_frame, variable=checkbox_var,
                                      command=lambda i=index, var=checkbox_var: self.toggle_checkbox(i, var))
            checkbox.grid(row=0, column=0, sticky="w")

            line_num_label = tk.Label(line_frame, text=f"{index}.", width=3, bg=bg_color)
            line_num_label.grid(row=0, column=1, sticky="w")

            data_label = tk.Label(line_frame, text=item, anchor="w", wraplength=350, bg=bg_color)
            data_label.grid(row=0, column=2, sticky="ew", padx=5)

            edit_button = tk.Button(line_frame, text="Edit", command=lambda i=index: self.edit_line(i))
            edit_button.grid(row=0, column=3, sticky="e", padx=2)

            delete_button = tk.Button(line_frame, text="Delete", command=lambda i=index: self.delete_line(i))
            delete_button.grid(row=0, column=4, sticky="e", padx=2)
            # Draw point on image canvas
            if image_path and item.startswith(("UI pointarea", "MAP", "IMAGE")):
                try:
                    point_parts = item.split()
                    x1 = int(point_parts[-4])
                    y1 = int(point_parts[-3])
                    x2 = int(point_parts[-2])
                    y2 = int(point_parts[-1])
                    self.draw_pointarea(x1, y1, x2, y2, index, checkbox_var.get())
                except Exception as e:
                    print(f"error reading item pointarea in chatbox{e}")

        self.chat_frame.update_idletasks()
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1)

    def draw_pointarea(self, x1, y1, x2, y2, line_number, is_checked):
       self.image_canvas.delete(f"pointarea{line_number}")
       if is_checked:
           # Ensure x1, y1 is top-left corner and x2, y2 is bottom-right
            canvas_x1 = min(x1,x2)
            canvas_y1 = min(y1, y2)
            canvas_x2 = max(x1,x2)
            canvas_y2 = max(y1, y2)

            # Draw rectangle
            self.image_canvas.create_rectangle(canvas_x1, canvas_y1, canvas_x2, canvas_y2, outline="green", tags=f"pointarea{line_number}")
            # Draw Point
            radius = 3
            point_x = canvas_x1
            point_y = canvas_y1
            self.image_canvas.create_oval(point_x - radius, point_y - radius, point_x + radius, point_y + radius, fill="red",
                                        tags=f"pointarea{line_number}")
             # Draw Text
            self.image_canvas.create_text(point_x + 8, point_y, text=f"{line_number}", fill="blue", anchor=tk.W,
                                      tags=f"pointarea{line_number}")


    def delete_line(self, index):
        global saved_positions
        if image_path:
            self.image_canvas.delete(f"pointarea{index}")
        del saved_positions[index]
        del checkbox_states[index]
        self.update_chatbox()

    def edit_line(self, index):
        global edit_mode, edit_index
        edit_mode = True
        edit_index = index
        self.update_chatbox()
        # Now the next save_position() call will replace the line
        # No need for a dialog anymore, just initiate the normal capturing behavior.

    def toggle_checkbox(self, index, checkbox_var):
        checkbox_states[index] = checkbox_var.get()
        self.update_chatbox()

    def toggle_all_checkboxes(self):
        all_checked = all(checkbox_states.values())
        new_state = not all_checked

        for index in range(len(saved_positions)):
            checkbox_states[index] = new_state

        self.update_chatbox()

    def start_key_listener(self):
        global ctrl_pressed, collecting_two_points, collecting_key, key_string

        def on_ctrl_press(event):
            global ctrl_pressed
            ctrl_pressed = True

        def on_ctrl_release(event):
            global ctrl_pressed
            ctrl_pressed = False

        kb.on_press_key('ctrl', on_ctrl_press)
        kb.on_release_key('ctrl', on_ctrl_release)

        self.update_keybindings_based_on_mode()

    def set_radio_button_input_mode(self):
        global collecting_two_points, temp_points
        self.input_mode.set("otherWindow")
        self.reset_state()
        self.update_keybindings_based_on_mode()

    def set_image_input_mode(self):
        global collecting_two_points, temp_points
        self.input_mode.set("IMAGE")
        self.reset_state()
        self.update_keybindings_based_on_mode()
    
    def reset_state(self):
         global collecting_two_points, temp_points
         collecting_two_points = False
         temp_points = []


    def update_keybindings_based_on_mode(self):
          # Remove previous hotkeys so they don't get called anymore
        try:
           kb.remove_hotkey('ctrl+p')
           kb.remove_hotkey('ctrl+a')
        except:
           pass
        if self.input_mode.get() == "otherWindow":
             def on_key_combination_p():
                 if self.input_mode.get() == "otherWindow":
                     self.save_position()
             def on_key_combination_a():
                global collecting_two_points, temp_points
                if self.input_mode.get() == "otherWindow":
                    if not collecting_two_points:
                        collecting_two_points = True
                        hwnd, window_title = self.get_active_window_info()
                        mouse_x, mouse_y = self.get_mouse_position()
                        x, y = self.get_relative_mouse_position(hwnd, mouse_x, mouse_y)
                        if x is not None and y is not None:
                            temp_points.append((int(x),int(y)))
                    
                    else:
                        hwnd, window_title = self.get_active_window_info()
                        mouse_x, mouse_y = self.get_mouse_position()
                        x, y = self.get_relative_mouse_position(hwnd, mouse_x, mouse_y)
                        if x is not None and y is not None:
                            temp_points.append((int(x),int(y)))
                        self.save_position()
             kb.add_hotkey('ctrl+p', on_key_combination_p, suppress=True)
             kb.add_hotkey('ctrl+a', on_key_combination_a, suppress=True)
        elif self.input_mode.get() == "IMAGE":
            pass

    def set_ui_mode(self):
        self.current_mode.set("UI")
        self.area_button.config(state=tk.NORMAL)
        self.point_button.config(state=tk.NORMAL)
        self.key_button.config(state=tk.NORMAL)
        self.map_name_entry.config(state=tk.DISABLED)
        self.map_action_entry.config(state=tk.DISABLED)

    def set_map_mode(self):
        self.current_mode.set("MAP")
        self.area_button.config(state=tk.NORMAL)
        self.point_button.config(state=tk.NORMAL)
        self.key_button.config(state=tk.DISABLED)
        self.map_name_entry.config(state=tk.NORMAL)
        self.map_action_entry.config(state=tk.NORMAL)

    def area_button_click(self):
        global collecting_two_points
        if not collecting_two_points:
            collecting_two_points = True
        else:
            collecting_two_points = False

    def point_button_click(self):
        pass

    def key_button_click(self):
        global key_string
        if self.current_mode.get() == "UI":
            def save_key(key):
                global saved_positions, edit_mode, edit_index
                if edit_mode:
                    saved_positions[edit_index] = f'key {key}'
                    edit_mode = False
                    edit_index = None
                else:
                    saved_positions.append(f'key {key}')
                self.update_chatbox()

            prompt = self.KeyInputPrompt(self.root, save_key)
            self.root.wait_window(prompt)
        else:
            return

    class KeyInputPrompt(tk.Toplevel):
        def __init__(self, master, callback):
            super().__init__(master)
            self.title("Key Input")
            self.geometry("200x100")
            self.label = tk.Label(self, text="Waiting for key input", font=("Arial", 12))
            self.label.pack(pady=20)
            self.callback = callback
            self.bind("<Key>", self.on_key_press)
            self.grab_set()
            self.focus_force()

        def on_key_press(self, event):
            self.destroy()
            self.callback(event.keysym)

    # Image Zoom Function
    def on_mousewheel(self, event):
        pass

    def zoom_in(self):
        self.zoom_scale *= 1.1
        self.image_canvas.scale("all", 0, 0, 1.1, 1.1)
        self.image_canvas.config(scrollregion=self.image_canvas.bbox("all"))

    def zoom_out(self):
        self.zoom_scale *= 0.9
        self.image_canvas.scale("all", 0, 0, 0.9, 0.9)
        self.image_canvas.config(scrollregion=self.image_canvas.bbox("all"))

    def zoom_in_key(self, event):
        self.zoom_in()

    def zoom_out_key(self, event):
        self.zoom_out()

    # Image Pan Functions
    def start_pan(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y
        self.pan_canvas_start_x = self.image_canvas.canvasx(event.x)
        self.pan_canvas_start_y = self.image_canvas.canvasy(event.y)

    def pan_image(self, event):
        dx = event.x - self.pan_start_x
        dy = event.y - self.pan_start_y
        self.image_canvas.scan_dragto(self.pan_canvas_start_x - dx, self.pan_canvas_start_y - dy, gain=1)

        self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))

    def stop_pan(self, event):
        pass

    def get_mouse_position_on_image(self):
        x = self.image_canvas.canvasx(self.root.winfo_pointerx() - self.image_canvas.winfo_rootx())
        y = self.image_canvas.canvasy(self.root.winfo_pointery() - self.image_canvas.winfo_rooty())
        return x, y

    def on_image_click(self, event):
        if self.input_mode.get() == "IMAGE":
            if not ctrl_pressed:
                self.save_position()

    def on_right_click_press(self, event):
        global right_click_start_point, collecting_two_points, right_click_rect, temp_points
        if self.input_mode.get() == "IMAGE":
            collecting_two_points = True
            x, y = self.get_mouse_position_on_image()
            right_click_start_point = (int(x), int(y))
            temp_points = [right_click_start_point]
            # Clear any existing rectangle
            if right_click_rect:
                self.image_canvas.delete(right_click_rect)
                right_click_rect = None

    def on_right_click_drag(self, event):
        global right_click_start_point, collecting_two_points, right_click_rect
        if self.input_mode.get() == "IMAGE" and collecting_two_points and right_click_start_point:
            x, y = self.get_mouse_position_on_image()
            current_x = int(x)
            current_y = int(y)
            start_x, start_y = right_click_start_point

            # Clear any existing rectangle
            if right_click_rect:
                self.image_canvas.delete(right_click_rect)

            # Create a new rectangle to show the selection
            right_click_rect = self.image_canvas.create_rectangle(
            start_x, start_y, current_x, current_y, outline="blue")

    def on_right_click_release(self, event):
        global right_click_start_point, collecting_two_points, temp_points, right_click_rect
        if self.input_mode.get() == "IMAGE":
            if collecting_two_points and right_click_start_point:
                x, y = self.get_mouse_position_on_image()
                temp_points.append((int(x), int(y)))
                self.save_position()
                right_click_start_point = None
                
                # Clear the rectangle
                if right_click_rect:
                    self.image_canvas.delete(right_click_rect)
                    right_click_rect = None
                collecting_two_points = False
                temp_points = []

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowTrackerApp(root)
    root.mainloop()
