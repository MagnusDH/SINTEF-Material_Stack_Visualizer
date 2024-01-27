import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL, Frame, Entry, StringVar, Label, Button, messagebox, font
from PIL import ImageGrab, Image
import pandas as pd
import pygetwindow
import pyautogui
import os

#Todo:
    #First: Draw material stack so that it has steps on the side
    #Second: finish the draw_text_on_rectangles method

class App:
    def __init__(self, window):
        self.program_title = "Layer stack visualizer"
        self.program_window_width = 800                 #Initial width of program window
        self.program_window_height = 850                #Initial height of program window
        self.excel_file = "Materials.xlsx"              #Excel-file to load materials from
        self.text_size = 10
        self.text_font = "Arial"
        self.switch_layout_counter = 0                  #Used to switch between "draw_material_stack_filled" and "draw_material_stack_realistic"
        
        #Dictionary containing all materials.
        self.materials = {}                             #KEY["material_name"] -VALUE: list[thickness, color, rectangle_id, slider_id, entry_id]

        #Set program_window title and dimensions
        window.title(self.program_title)
        window.geometry(f"{self.program_window_width}x{self.program_window_height}")

        #Read the given excel-file and populate self.materials dictionary
        self.load_materials_from_excel(self.excel_file)

        #Create a user interface
        self.user_interface_frame = self.create_user_interface(window)

        #Create a canvas supporting zoom and moving
        self.canvas = self.create_canvas(window)

        #Draw rectangle stack
        self.draw_material_stack()

    """Creates a Frame with sliders, entries and buttons"""
    def create_user_interface(self, window):
        #Create Frame and place it
        user_interface_frame = Frame(window)
        user_interface_frame.grid(row=0, column=0, sticky="n")

        row_counter = 0
        for material in self.materials:
            # Create label and place it
            label = Label(user_interface_frame, text=material)
            label.grid(row=row_counter, column=0, sticky="nw", padx=(0,0))
            label_height = label.winfo_reqheight()
           
            #Create entry and place it
            entry = Entry(user_interface_frame, 
                textvariable=StringVar(value=str(self.materials[material][0])), 
                bg="lightgrey"
            )
            entry.grid(row=row_counter, column=0, sticky="ne", pady=(2,0), padx=(0, 5))
            entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(event, e))

            #Create slider and place it
            slider = Scale(user_interface_frame,
                from_=1,
                to=1000,
                orient=HORIZONTAL, 
                width=10, 
                length=300, 
                troughcolor=self.materials[material][1],
                command=lambda value, identifier=material: self.material_slider_updated(value, identifier)
            )
            slider.grid(row=row_counter, column=0, sticky="s", pady=(label_height, 10))
            slider.set(self.materials[material][0])

            #Add slider and entry to self.materials to current material
            self.materials[material][3] = slider 
            self.materials[material][4] = entry 
                        
            #Increment row_counter
            row_counter+=1
                
        return user_interface_frame

    """Updates the thickness value in self.materials with the slider value and updates corresponding entry-widget"""
    def material_slider_updated(self, value, identifier):       
        #Update the thickness value in self.materials
        self.materials[identifier][0] = value

        #Update the entry corresponding to key
        self.materials[identifier][4].delete(0, tk.END)
        self.materials[identifier][4].insert(0, value)

        #Draw rectangle stack
        self.draw_material_stack()

    """Updates the thickness value in self.materials with the entered value and updates corresponding slider-widget"""
    def material_entry_updated(self, event, entry):
        #Find key that corresponds to "entry"
        for _key, value in self.materials.items():
            if entry in value:
                key = _key                          #This is not necessary but it makes it more readable
                break
        
        #Find entered value
        entered_value = int(entry.get())

        #Update the thickness value in self.materials
        self.materials[key][0] = entered_value

        #Update the slider corresponding to the key
        self.materials[key][3].set(entered_value)

        #Draw rectangle stack
        self.draw_material_stack()

    """Returns a canvas created in the given program window"""
    def create_canvas(self, window):
        #Update window to get updated values
        window.update_idletasks()

        #Create canvas and place it
        canvas = Canvas(window, height=self.user_interface_frame.winfo_reqheight(), width=self.program_window_width-5-self.user_interface_frame.winfo_width())
        canvas.grid(row=0, column=1, sticky="n")

        #Set bbox coordinates for later use
        self.visible_canvas_bbox_x0 = 2
        self.visible_canvas_bbox_y0 = 2
        self.visible_canvas_bbox_x1 = canvas.winfo_reqwidth() - 3
        self.visible_canvas_bbox_y1 = canvas.winfo_reqheight() - 3

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black")

        #Listen to mouse buttonpress, motion and zoom events
        canvas.bind("<ButtonPress-1>", lambda event, canvas=canvas: self.click_on_canvas(event, canvas))
        canvas.bind("<B1-Motion>", lambda event, canvas=canvas: self.canvas_drag(event, canvas))
        canvas.bind("<MouseWheel>", lambda event, canvas=canvas: self.canvas_zoom(event, canvas))

        #Create reset-button under canvas
        reset_canvas_button = Button(window, text="Reset canvas", command=self.reset_canvas)
        reset_canvas_button.grid(row=1, column=1, sticky="nw", padx=(0, 5))

        #Create reset-values-button under canvas
        reset_values_button = Button(window, text="Reset values", command=self.reset_values)
        reset_values_button.grid(row=1, column=1, sticky="n", padx=(0, 0))

        #Create switch-layout button under canvas
        switch_layout_button = Button(window, text="Switch layout", command=self.switch_layout)
        switch_layout_button.grid(row=1, column=1, sticky="ne", padx=(5, 0))

        #Create export_stack button under canvas
        export_stack_button = Button(window, text="Export stack", command=self.export_stack_as_svg)
        export_stack_button.grid(row=2, column=1, sticky="nw", padx=(5, 0))

        #Create export_layers button under canvas
        export_layers_button = Button(window, text="Export layers", command=self.export_layers_as_svg)
        export_layers_button.grid(row=2, column=1, sticky="n", padx=(0, 0))

        #Return canvas
        return canvas

    """Deletes the given canvas and creates a new one in its original place"""
    def reset_canvas(self):
        #Delete canvas from program window
        self.canvas.destroy()

        #Create a new canvas
        self.canvas = self.create_canvas(window)

        #Draw rectangle stack
        self.draw_material_stack()

    """Reads the excel file again and repopulated the "thickness" in self.materials. Updates sliders and entries with new values"""
    def reset_values(self):
        #Reload initial values from given excel file
        try:
            #Read given excel file into Pandas dataframe
            excel_data = pd.read_excel(self.excel_file)

            #Loop through the rows in excel_file and populate "self.materials"
            for index, row in excel_data.iterrows():
                material_name = row["Material"]
                material_thickness = row["Thickness"]
                
                #Populate material dictionary
                self.materials[material_name][0] = material_thickness
                
                #Update sliders and Entries
                self.materials[material_name][3].set(material_thickness)

                self.materials[material_name][4].delete(0, tk.END)
                self.materials[material_name][4].insert(0, material_thickness)
            
            #Draw rectangle stack with original values
            self.draw_material_stack()
        
        #Handle errors
        except Exception as error:
            messagebox.showerror("Error", "Could not reset values\nMay be a issue with reading from excel-file")
        
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
    
    """Draws the material_stack either filled or realistic based on "self.switch_layout_counter"""
    def switch_layout(self):
        self.switch_layout_counter += 1

        self.draw_material_stack()

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
                rectangle_id = None
                slider_id = None
                entry_id = None
                
                #Populate material dictionary
                self.materials[material_name] = [material_thickness, material_color, rectangle_id, slider_id, entry_id]
            
            #Reverse dictionary so that the materials is drawn in correct order
            self.materials = dict(reversed(self.materials.items()))
            
        #Handle errors
        except Exception as error:
            messagebox.showerror("Error", "Could not load materials from Excel-file")

    """Draws the rectangle stack either filled or realistic based on the "switch_layout_counter"""
    def draw_material_stack(self):
        if(self.switch_layout_counter % 2 == 0):
            self.draw_material_stack_filled(self.canvas)
        else:
            self.draw_material_stack_realistic(self.canvas)
        
        self.write_text_on_materials()

    """Draws the rectangle stack with "substrate" as 1/10 of the canvas"""
    def draw_material_stack_filled(self, canvas):
        #Clear all existing elements on canvas
        canvas.delete("all")

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black", tags="canvas_bounding_box_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in self.materials:
            if(material=="substrate"):
                continue    #Skip substrate
            rectangle_height = int(self.materials[material][0])
            sum_of_all_materials += rectangle_height
        
        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y0
        rectangle_x1 = self.visible_canvas_bbox_x1 - 150
        rectangle_y1 = self.visible_canvas_bbox_y1

        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = (self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0) * 0.9
        
        #Draw rectangles on canvas
        for material in self.materials:
            #"substrate" will be drawn on the bottom 1/10 of the canvas
            if(material == "substrate"):
                continue    #Skip "substrate"

            #find how many percent the current rectangle's height is of the total sum of materials
            rectangle_height = int(self.materials[material][0])
            rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
            #Convert rectangle percentage to pixels
            rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

            #draw rectangle from top of canvas to its number of pixles in height
            rectangle_y1 = rectangle_y0 + rectangle_height_pixels
            created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material][1], tags="material_rectangle")

            #Add rectangle_id to its place in self.materials
            self.materials[material][2] = created_rectangle

            #Add rectangle height to prevent overlaping
            rectangle_y0 += rectangle_height_pixels
        
        #Draw "substrate" on 1/10 of the canvas
        created_rectangle = canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y1, rectangle_x1, canvas_height, fill=self.materials["substrate"][1], tags="material_rectangle")
        #Add rectangle_id to its place in self.materials
        self.materials["substrate"][2] = created_rectangle

    """Draws the rectangle stack in a realistic way"""
    def draw_material_stack_realistic(self, canvas):
        #Clear all existing elements on canvas
        canvas.delete("all")

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black", tags="canvas_bounding_box_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in self.materials:
            rectangle_height = int(self.materials[material][0])
            sum_of_all_materials += rectangle_height
        
        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y0
        rectangle_x1 = self.visible_canvas_bbox_x1 - 150
        rectangle_y1 = self.visible_canvas_bbox_y1

        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = (self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0)
        
        #Draw rectangles on canvas
        for material in self.materials:
            #find how many percent the current rectangle's height is of the total sum of materials
            rectangle_height = int(self.materials[material][0])
            rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
            #Convert rectangle percentage to pixels
            rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

            #draw rectangle from top of canvas to its number of pixles in height
            rectangle_y1 = rectangle_y0 + rectangle_height_pixels
            created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material][1], tags="material_rectangle")

            #Add rectangle_id to its place in self.materials
            self.materials[material][2] = created_rectangle

            #Add rectangle height to prevent overlaping
            rectangle_y0 += rectangle_height_pixels
    
    """Writes text on rectangles in the material stack"""
    def write_text_on_materials(self):
        #Find out the height of a text's bounding box
        text_font = font.Font(family=self.text_font, size=self.text_size)
        text_height = text_font.metrics()['linespace']
        
        for material in self.materials:
            #Find coordinates and height of current material_rectangle
            rectangle_x0 = self.canvas.bbox(self.materials[material][2])[0]
            rectangle_y0 = self.canvas.bbox(self.materials[material][2])[1]
            rectangle_x1 = self.canvas.bbox(self.materials[material][2])[2]
            rectangle_y1 = self.canvas.bbox(self.materials[material][2])[3]
            rectangle_height = rectangle_y1-rectangle_y0

            #Text is drawn inside rectangle if it fits
            if(rectangle_height > text_height):
                self.canvas.create_text((rectangle_x1-rectangle_x0)/2, rectangle_y1-(rectangle_height/2), text=material, fill="black", font=(self.text_font, self.text_size), anchor="center", tags="Material_label")
            
            #Text is drawn outside rectangle
            else:
                pass
            
            # self.materials[material_name] = [material_thickness, material_color, rectangle_id, slider_id, entry_id]
    
    """Exports the stack without material names as SVG file"""
    def export_stack_as_svg(self):
        #Define the name of the svg file to be created
        filename = "stack.svg"

        #Specify a folder where the SVG-file should be saved
        folder_path = "svg_exports"

        #Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #Create the file path by joining the folder path and the filename
        file_path = os.path.join(folder_path, filename)

        #Find all elements created on canvas
        material_rectangles = self.canvas.find_withtag("material_rectangle")

        #Open the file for writing
        with open(file_path, 'w') as f:
            #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

            #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
            f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()))

            #Go through every rectangle found on canvas
            for rectangle in material_rectangles:
                #Find the coordinates of the rectangle
                rect_x0, rect_y0, rect_x1, rect_y1 = self.canvas.coords(rectangle)
                #Construct an SVG <rect> element for the rectangle
                svg_rect_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, self.canvas.itemcget(rectangle, 'fill'))
                #Write the SVG representation of the rectangle to the file
                f.write(svg_rect_element)
                #Construct an SVG <rect> element for the bounding box
                svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0)
                # Write the SVG representation of the bounding box to the file
                f.write(svg_bbox_element)

            #Write the closing SVG tag to the file, completing the SVG file.
            f.write('</svg>\n')

        #Close the SVG file
        f.close()

    """Exports each layer of the stack with names and arrows as SVG-file"""
    def export_layers_as_svg(self):
        print("EXPORT LAYERS")

#Main start point of program
if __name__ == "__main__":
    window = tk.Tk()
    
    #Create instance of class and run application
    app = App(window)

    #Closes the program if "esc" key is pressed
    window.bind("<Escape>", lambda event: window.destroy())

    window.mainloop()