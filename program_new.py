import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL, Frame, Entry, StringVar, Label, Button, messagebox, font
from PIL import ImageGrab, Image
import pandas as pd
import pygetwindow
import pyautogui
import os

"""
Ide:
    -legg til alt som tilhører et materiale i self.materials slik:
        self.materials["name"] = [thickness, color, rectangle_id, slider, entry]
        NB: husk da å initialiser den med "None" variabler i "load_materials_from_excel"
            self.materials["name"] = [thickness, color, None, None, None] 
    
    -Når all informasjon ligger i self.materials kan det bli lettere å tegne stack, eksportere svg, oppdatere sliders/entries etc...

    -Kanskje du kan bruke "entry.bind" og kalle på en generell update som vil oppdatere stack, sliders, entries basert på det som ligger i self.materials?
"""

class App:
    def __init__(self, window):
        self.program_title = "Layer stack visualizer"
        self.program_window_width = 600                 #Initial width of program window
        self.program_window_height = 800                #Initial height of program window
        self.excel_file = "Materials.xlsx"              #Excel-file to load materials from

        #Dictionary containing all materials.
        self.materials = {}                             #KEY["material_name"] -VALUE: list[thickness, color]

        #Set program_window title and dimensions
        window.title(self.program_title)
        window.geometry(f"{self.program_window_width}x{self.program_window_height}")

        #Read the given excel-file and populate self.materials dictionary
        self.load_materials_from_excel(self.excel_file)

        #Create a user interface
        self.user_interface_frame = self.create_user_interface(window)

        #Create a canvas supporting zoom and moving
        self.canvas = self.create_canvas(window)

    def create_user_interface(self, window):
        #Create Frame and place it
        user_interface_frame = Frame(window)
        user_interface_frame.grid(row=0, column=0, sticky="n")

        row_counter = 0
        for material in self.materials:
            # Create label and place it
            label = Label(user_interface_frame, text=material)
            label.grid(row=row_counter, column=0, sticky="nw", padx=(50,0))
            label_height = label.winfo_reqheight()-7
           
            #Create slider and place it
            slider = Scale(user_interface_frame,
                from_=1,
                to=1000,
                orient=HORIZONTAL, 
                width=10, 
                length=300, 
                troughcolor=self.materials[material][1],
            )
            slider.grid(row=row_counter, column=0, sticky="s", pady=(label_height, 0))
            slider.set(self.materials[material][0])

            #Create entry and place it
            entry = Entry(user_interface_frame, 
                textvariable=StringVar(value=str(self.materials[material][0])), 
                bg="lightgrey"
            )
            entry.grid(row=row_counter, column=0, sticky="ne", pady=(2,0), padx=(0, 5))

            #Increment row_counter
            row_counter+=1

        return user_interface_frame

    """Returns a canvas created in the given program window"""
    def create_canvas(self, window):
        #Update window to get updated values
        window.update()

        #Create canvas and place it
        canvas = Canvas(window, height=self.program_window_height-5, width=self.program_window_width-5-self.user_interface_frame.winfo_width(), bg="lightblue")
        canvas.grid(row=0, column=1, sticky="n")

        #Set bbox coordinates for later use
        self.visible_canvas_bbox_x0 = 2
        self.visible_canvas_bbox_y0 = 2
        self.visible_canvas_bbox_x1 = canvas.winfo_reqwidth() - 3
        self.visible_canvas_bbox_y1 = canvas.winfo_reqheight() - 3

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black")

        #Listen to mouse buttonpress, motion and zoom events
        canvas.bind("<ButtonPress-1>", lambda event, canvas=canvas: self.click_on_canvas(event, self.canvas))
        canvas.bind("<B1-Motion>", lambda event, canvas=canvas: self.canvas_drag(event, self.canvas))
        canvas.bind("<MouseWheel>", lambda event, canvas=canvas: self.canvas_zoom(event, self.canvas))

        #Return canvas
        return canvas

    """Remembers the initial mouse click-position on the canvas"""
    def click_on_canvas(self, event, canvas):
        canvas.scan_mark(event.x, event.y)
    
    """Moves the position of the canvas"""
    def canvas_drag(self, event, canvas):
        canvas.scan_dragto(event.x, event.y, gain=1)

    """Scales all the elements on the canvas up or down"""
    def canvas_zoom(self, event, canvas):
        zoom_factor = 1.05
        #Zoom in: Scale all items on the canvas around the mouse cursor
        if event.delta > 0:
            canvas.scale("all", event.x, event.y, zoom_factor, zoom_factor)
        #Zoom out: Scale all items on the canvas around the mouse cursor
        elif event.delta < 0:
            canvas.scale("all", event.x, event.y, 1.0/zoom_factor, 1.0/zoom_factor)
        

    """Reads the given excel-file and populates the self.materials dictionary with materials and thickness"""
    def load_materials_from_excel(self, excel_file):
        try:
            #Read given excel file into Pandas dataframe
            excel_data = pd.read_excel(excel_file)

            #Loop through the rows in excel_file and populate "self.materials"
            for index, row in excel_data.iterrows():
                material_name = row["Material"]
                material_thickness = row["Thickness"]
                material_color = row["Color"]
                
                #Populate material dictionary
                self.materials[material_name] = [material_thickness, material_color]
            
            #Reverse dictionary so that the materials is drawn in correct order
            self.materials = dict(reversed(self.materials.items()))
            
        #Handle errors
        except Exception as error:
            messagebox.showerror("Error", "Could not load materials from Excel-file")


#Main start point of program
if __name__ == "__main__":
    window = tk.Tk()
    
    #Create instance of class and run application
    app = App(window)

    #Closes the program if "esc" key is pressed
    window.bind("<Escape>", lambda event: window.destroy())

    window.mainloop()