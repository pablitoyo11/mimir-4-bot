import logging
import os
import tkinter as tk
from tkinter import ttk, messagebox

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class PKLEntryCreator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PKL Entry Creator")
        
        # Center the window on screen
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Create main frame with padding and scrollbar
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.main_frame = ttk.Frame(self.canvas, padding="20")
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas for main frame
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configure canvas scrolling
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Add title label
        title_label = ttk.Label(self.main_frame, text="PKL Entry Creator", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create working space frame
        self.input_type_frame = ttk.LabelFrame(self.main_frame, text="Select Working Space", padding="10")
        self.input_type_frame.pack(fill='x', pady=(0, 10))
        
        # Add UI and MAP buttons
        self.input_type = tk.StringVar()
        ui_radio = ttk.Radiobutton(self.input_type_frame, text="UI", variable=self.input_type, value="UI", command=self.input_type_changed)
        ui_radio.pack(side=tk.LEFT, padx=10)
        map_radio = ttk.Radiobutton(self.input_type_frame, text="MAP", variable=self.input_type, value="MAP", command=self.input_type_changed)
        map_radio.pack(side=tk.LEFT, padx=10)
        
        # Create map details frame
        self.map_details_frame = ttk.LabelFrame(self.main_frame, text="Map Details", padding="10")
        
        # Map name entry
        map_name_frame = ttk.Frame(self.map_details_frame)
        map_name_frame.pack(fill='x', pady=2)
        map_name_label = ttk.Label(map_name_frame, text="Map Name:", width=15)
        map_name_label.pack(side=tk.LEFT, padx=5)
        self.map_name_entry = ttk.Entry(map_name_frame)
        self.map_name_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        # Action entry
        action_frame = ttk.Frame(self.map_details_frame)
        action_frame.pack(fill='x', pady=2)
        action_label = ttk.Label(action_frame, text="Action:", width=15)
        action_label.pack(side=tk.LEFT, padx=5)
        self.action_entry = ttk.Entry(action_frame)
        self.action_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        
        # Create input type frame
        self.geometry_frame = ttk.LabelFrame(self.main_frame, text="Select Input Type", padding="10")
        self.geometry_frame.pack(fill='x', pady=(0, 10))
        
        # Add AREA, POINT, and KEY buttons
        self.geometry_type = tk.StringVar()
        area_radio = ttk.Radiobutton(self.geometry_frame, text="AREA", variable=self.geometry_type, value="AREA", command=self.geometry_type_changed)
        area_radio.pack(side=tk.LEFT, padx=10)
        point_radio = ttk.Radiobutton(self.geometry_frame, text="POINT", variable=self.geometry_type, value="POINT", command=self.geometry_type_changed)
        point_radio.pack(side=tk.LEFT, padx=10)
        self.key_radio = ttk.Radiobutton(self.geometry_frame, text="KEY", variable=self.geometry_type, value="KEY", command=self.geometry_type_changed)
        
        # Create coordinates frame
        self.coordinates_frame = ttk.LabelFrame(self.main_frame, text="Enter Coordinates", padding="10")
        self.coordinates_frame.pack(fill='x', pady=(0, 10))
        
        # Create list to store coordinate entries
        self.coord_entries = []
        
        # Create lines frame
        self.lines_frame = ttk.LabelFrame(self.main_frame, text="Lines", padding="10")
        self.lines_frame.pack(fill='x', pady=(0, 10))
        
        # List to store lines
        self.lines = []
        
        # Create buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill='x', pady=(10, 0))
        
        # Add Line button
        add_line_button = ttk.Button(buttons_frame, text="Add Line", command=self.add_line)
        add_line_button.pack(side=tk.LEFT, padx=5)
        
        # Add Generate and Clear buttons
        save_button = ttk.Button(buttons_frame, text="Save PKL", command=self.save_pkl)
        save_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(buttons_frame, text="Clear All", command=self.clear_form)
        clear_button.pack(side=tk.LEFT, padx=5)
    
    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        # Update the width of the canvas window to fit the frame
        self.canvas.itemconfig(self.canvas_frame, width=event.width)
    
    def input_type_changed(self):
        input_type = self.input_type.get()
        logger.info(f"Input type changed to: {input_type}")
        
        # Show/hide map details based on input type
        if input_type == "MAP":
            self.map_details_frame.pack(after=self.input_type_frame, fill='x', pady=(0, 10))
            self.geometry_frame.pack(after=self.map_details_frame, fill='x', pady=(0, 10))
            self.key_radio.pack_forget()  # Hide KEY option for MAP
        elif input_type == "UI":
            self.map_details_frame.pack_forget()
            self.geometry_frame.pack(after=self.input_type_frame, fill='x', pady=(0, 10))
            self.key_radio.pack(side=tk.LEFT, padx=10)  # Show KEY option for UI
            # Clear map details when switching to UI
            self.map_name_entry.delete(0, tk.END)
            self.action_entry.delete(0, tk.END)
        
        self.update_coordinate_fields()
    
    def geometry_type_changed(self):
        logger.info(f"Geometry type changed to: {self.geometry_type.get()}")
        self.update_coordinate_fields()
    
    def update_coordinate_fields(self):
        # Clear existing coordinate entries
        for widget in self.coordinates_frame.winfo_children():
            widget.destroy()
        self.coord_entries.clear()
        
        if not self.input_type.get() or not self.geometry_type.get():
            return
        
        # Add appropriate coordinate entry fields based on selection
        if self.geometry_type.get() == "KEY":
            # Add key input field
            key_frame = ttk.Frame(self.coordinates_frame)
            key_frame.pack(fill='x', pady=2)
            key_label = ttk.Label(key_frame, text="Keyboard Key:", width=15)
            key_label.pack(side=tk.LEFT, padx=5)
            key_entry = ttk.Entry(key_frame)
            key_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
            self.coord_entries.append(key_entry)
        elif self.geometry_type.get() == "POINT":
            self.add_coordinate_entry("X")
            self.add_coordinate_entry("Y")
        else:  # AREA
            self.add_coordinate_entry("Top Left X")
            self.add_coordinate_entry("Top Left Y")
            self.add_coordinate_entry("Bottom Right X")
            self.add_coordinate_entry("Bottom Right Y")
    
    def add_coordinate_entry(self, label):
        frame = ttk.Frame(self.coordinates_frame)
        frame.pack(fill='x', pady=2)
        
        label = ttk.Label(frame, text=f"{label}:", width=15)
        label.pack(side=tk.LEFT, padx=5)
        
        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, fill='x', expand=True, padx=5)
        self.coord_entries.append(entry)
    
    def add_line(self):
        if not self.input_type.get() or not self.geometry_type.get():
            messagebox.showerror("Error", "Please select both Input Type and Geometry Type")
            return
        
        # Get values based on geometry type
        values = []
        if self.geometry_type.get() == "KEY":
            values = [entry.get().strip() for entry in self.coord_entries]
            if not values[0]:
                messagebox.showerror("Error", "Please enter a keyboard key")
                return
        else:
            # Validate coordinates for AREA and POINT
            for entry in self.coord_entries:
                try:
                    value = float(entry.get())
                    values.append(value)
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numeric coordinates")
                    return
        
        # Format values based on geometry type
        if self.geometry_type.get() == "KEY":
            coord_str = values[0]
        elif self.geometry_type.get() == "POINT":
            coord_str = f"{int(values[0]) if values[0].is_integer() else values[0]} {int(values[1]) if values[1].is_integer() else values[1]}"
        else:  # AREA
            coord_str = f"{int(values[0]) if values[0].is_integer() else values[0]} {int(values[2]) if values[2].is_integer() else values[2]} {int(values[1]) if values[1].is_integer() else values[1]} {int(values[3]) if values[3].is_integer() else values[3]}"
        
        # Create line entry
        if self.input_type.get() == "UI":
            line_text = f"UI {self.geometry_type.get().lower()} {coord_str}"
        else:  # MAP
            map_name = self.map_name_entry.get().strip()
            action = self.action_entry.get().strip()
            if not map_name or not action:
                messagebox.showerror("Error", "Please enter both Map Name and Action")
                return
            line_text = f"MAP {map_name} {action} {self.geometry_type.get().lower()} {coord_str}"
        
        self.lines.append(line_text)
        
        # Add line to display
        line_frame = ttk.Frame(self.lines_frame)
        line_frame.pack(fill='x', pady=2)
        
        line_label = ttk.Label(line_frame, text=line_text)
        line_label.pack(side=tk.LEFT, padx=5)
        
        # Add delete button for this line
        delete_button = ttk.Button(line_frame, text="Delete", 
                                  command=lambda f=line_frame, i=len(self.lines)-1: self.delete_line(f, i))
        delete_button.pack(side=tk.RIGHT, padx=5)
        
        # Clear coordinate entries only
        for entry in self.coord_entries:
            entry.delete(0, tk.END)
        
        logger.info(f"Added line: {line_text}")
    
    def delete_line(self, frame, index):
        frame.destroy()
        del self.lines[index]
        logger.info(f"Deleted line at index {index}")
    
    def save_pkl(self):
        if not self.lines:
            messagebox.showerror("Error", "No lines to save")
            return
        
        # TODO: Implement PKL file saving logic
        logger.info(f"Saving PKL file with {len(self.lines)} lines")
        messagebox.showinfo("Success", "PKL file saving not yet implemented")
    
    def clear_form(self):
        self.input_type.set("")
        self.geometry_type.set("")
        self.map_name_entry.delete(0, tk.END)
        self.action_entry.delete(0, tk.END)
        self.update_coordinate_fields()
        
        # Clear lines
        for widget in self.lines_frame.winfo_children():
            widget.destroy()
        self.lines.clear()
        
        logger.info("Form cleared")
    
    def run(self):
        self.root.mainloop()

def main():
    app = PKLEntryCreator()
    app.run()

if __name__ == "__main__":
    main()
