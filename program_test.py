import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL, Frame, Entry, StringVar, Label, Button, messagebox, font
from PIL import ImageGrab, Image
import pandas as pd
import pygetwindow
import pyautogui
import os
import math
import openpyxl

#Nye funksjoner: tekst blir større når du zoomer inn. Gule ruter i excel arket blir "disabled" i programmet

#Todo:
    #Ferdigstill draw_text_on_rectangles funksjonen

class App:
    def __init__(self, window):       
        self.program_title = "Layer stack visualizer"
        self.program_window_width = 800                 #Initial width of program window
        self.program_window_height = 850                #Initial height of program window
        self.excel_file = "Materials.xlsx"              #Excel-file to load materials from
        self.original_text_size = 10
        self.current_text_size = self.original_text_size
        self.text_font = "Arial"
        self.switch_layout_counter = 0                  #Used to switch between "draw_material_stack_filled" and "draw_material_stack_realistic"

        #Dictionary containing ALL info about materials. See README-file for info about the dictionary
        self.materials = {}

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

        biggest_material = 0
        for material in self.materials:
            if(int(self.materials[material]["thickness"]) > biggest_material):
                biggest_material = int(self.materials[material]["thickness"])

        row_counter = 0
        # for material in self.materials:
        for material in dict(reversed(self.materials.items())):

            # Create label and place it
            label = Label(user_interface_frame, text=material)
            label.grid(row=row_counter, column=0, sticky="nw", padx=(0,0))
            label_height = label.winfo_reqheight()
           
            #Create entry and place it
            entry = Entry(user_interface_frame, 
                textvariable=StringVar(value=str(self.materials[material]["thickness"])), 
                bg="lightgrey"
            )
            entry.grid(row=row_counter, column=0, sticky="ne", pady=(2,0), padx=(0, 5))
            entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(event, e))
            self.materials[material]["entry_id"] = entry 


            #Create slider and place it
            slider = Scale(user_interface_frame,
                from_=1,
                to=biggest_material,
                orient=HORIZONTAL, 
                width=10, 
                length=300, 
                troughcolor=self.materials[material]["color"],
                command=lambda value, identifier=material: self.material_slider_updated(value, identifier)
            )
            slider.grid(row=row_counter, column=0, sticky="s", pady=(label_height, 10))
            slider.set(self.materials[material]["thickness"])
            self.materials[material]["slider_id"] = slider 
            #Disable slider and Entry if specified by the excel-file
            if(self.materials[material]["status"] == "disabled"):
                self.materials[material]["slider_id"].config(state="disabled") #Disable slider
                self.materials[material]["entry_id"].delete(0, tk.END)        #Disable Entry
                self.materials[material]["entry_id"].insert(0, "Disabled")    #Disable Entry
                self.materials[material]["entry_id"].config(state= "disabled")#Disable Entry

            #Increment row_counter
            row_counter+=1
        
        #Create reset-button under canvas
        reset_canvas_button = Button(window, text="Reset canvas", command=self.reset_canvas)
        reset_canvas_button.grid(row=1, column=1, sticky="nw", padx=(0, 5))

        #Create reset-values-button under canvas
        reset_values_button = Button(window, text="Reset values", command=self.reset_values)
        reset_values_button.grid(row=1, column=1, sticky="n", padx=(0, 0))

        #Create switch-layout button under canvas
        switch_layout_button = Button(window, text="Switch layout", command=self.switch_layout)
        switch_layout_button.grid(row=1, column=1, sticky="ne", padx=(5, 0))
        self.switch_layout_label = Label(window, text="Filled", font="bold")
        self.switch_layout_label.grid(row=2, column=1, sticky="e")

        #Create export_stack button under canvas
        export_stack_button = Button(window, text="Export stack", command=self.export_stack_as_svg)
        export_stack_button.grid(row=2, column=1, sticky="nw", padx=(5, 0))

        #Create export_layers button under canvas
        export_layers_button = Button(window, text="Export layers", command=self.export_layers_as_svg)
        export_layers_button.grid(row=2, column=1, sticky="n", padx=(0, 0))
                
        return user_interface_frame

    """Updates the thickness value in self.materials with the slider value and updates corresponding entry-widget"""
    def material_slider_updated(self, value, identifier):       
        #Update the thickness value in self.materials
        self.materials[identifier]["thickness"] = value

        #Update the entry corresponding to key
        self.materials[identifier]["entry_id"].delete(0, tk.END)
        self.materials[identifier]["entry_id"].insert(0, value)

        #Draw rectangle stack
        self.draw_material_stack()

    """Updates the thickness value in self.materials with the entered value and updates corresponding slider-widget"""
    def material_entry_updated(self, event, entry):
        #Find material that corresponds to "entry"
        for material in self.materials:
            if(self.materials[material]["entry_id"] == entry):
                #Find entered value
                entered_value = int(entry.get())

                #Update the thickness value in self.materials
                self.materials[material]["thickness"] = entered_value

                #Update the slider corresponding to the key
                self.materials[material]["slider_id"].set(entered_value)

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

        #Return canvas
        return canvas

    """Deletes the given canvas and creates a new one in its original place"""
    def reset_canvas(self, *args):
        #Delete canvas from program window
        self.canvas.destroy()

        #Create a new canvas
        self.canvas = self.create_canvas(window)

        #Reset the text size back to original
        self.current_text_size = self.original_text_size

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
                self.materials[material_name]["thickness"] = material_thickness
                
                #Update sliders and Entries
                self.materials[material_name]["slider_id"].set(material_thickness)

                self.materials[material_name]["entry_id"].delete(0, tk.END)
                self.materials[material_name]["entry_id"].insert(0, material_thickness)
            
            #Reset text_size
            self.current_text_size = self.original_text_size
            
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
            self.current_text_size *= zoom_factor
            self.current_text_size = math.ceil(self.current_text_size)

        #Zoom out: Scale all items on the canvas around the mouse cursor
        elif event.delta < 0:
            canvas.scale("all", event.x, event.y, 1.0/zoom_factor, 1.0/zoom_factor)
            self.current_text_size /= zoom_factor
            self.current_text_size = math.floor(self.current_text_size)

        #Delete all texts on canvas and draw them again
        for text in self.canvas.find_withtag("Material_label"):
            self.canvas.delete(text)
        self.write_text_on_materials(self.current_text_size)

    """
    -Draws the material_stack either filled, realistic or stepped based on "self.switch_layout_counter
    -Disables or enables the "substrate" slider&entry"""
    def switch_layout(self):
        self.switch_layout_counter += 1

        #Draw different material_stacks
        self.draw_material_stack()

        #Update the text of the switch_layout_label and disable "substrate" slider and entry
        if(self.switch_layout_counter % 3 == 0):
            self.switch_layout_label.config(text="Filled")
            # self.materials["substrate"]["slider_id"].config(state="disabled") #Disable slider
            # self.materials["substrate"]["entry_id"].delete(0, tk.END)        #Disable Entry
            # self.materials["substrate"]["entry_id"].insert(0, "Disabled")    #Disable Entry
            # self.materials["substrate"]["entry_id"].config(state= "disabled")#Disable Entry

            #Update new slider ranges
            for material in self.materials:
                self.materials[material]["slider_id"].config(from_=1, to=int(self.materials["substrate"]["thickness"]))

        #Update the text of switch_layout_label and enable "substrate" slider and entry
        elif(self.switch_layout_counter % 3 == 1):
            self.switch_layout_label.config(text="Realistic")
            # self.materials["substrate"]["slider_id"].config(state="normal")                                 #Enable slider
            # self.materials["substrate"]["entry_id"].config(state= "normal")                                 #Enable Entry
            # self.materials["substrate"]["entry_id"].delete(0, tk.END)                                       #Disable entry value
            # self.materials["substrate"]["entry_id"].insert(0, self.materials["substrate"]["thickness"])     #Display entry value

            #Update new slider ranges
            for material in self.materials:
                self.materials[material]["slider_id"].config(from_=1, to=int(self.materials["substrate"]["thickness"]))
        
        #Update the text of switch_layout_label and enable "substrate" slider and entry
        else:
            self.switch_layout_label.config(text="Stepped")
            # self.materials["substrate"]["slider_id"].config(state="disabled") #Disable slider
            # self.materials["substrate"]["entry_id"].delete(0, tk.END)        #Disable Entry
            # self.materials["substrate"]["entry_id"].insert(0, "Disabled")    #Disable Entry
            # self.materials["substrate"]["entry_id"].config(state= "disabled")#Disable Entry

    """Reads the given excel-file and populates the self.materials dictionary with info about each material"""
    def load_materials_from_excel(self, excel_file):
        try:
            #Read given excel file into Pandas dataframe
            excel_data = pd.read_excel(excel_file)

            #Open excel-file to read background colors of each cell
            work_book = openpyxl.load_workbook(excel_file, data_only=True)
            fs = work_book.active

            #Loop through the rows in excel_file and populate "self.materials"
            i = 2
            for column, row in excel_data.iterrows():
                layer = row["Layer"]
                material_name = row["Material"]
                material_thickness = row["Thickness"]
                material_unit = row["Unit"]
                material_indent = row["Indent"]
                material_color = row["Color"]
                rectangle_id = None
                text_id = None
                text_bbox_id = None
                line_id = None
                entry_id = None
                slider_id = None

                #Check the background color of the cell
                background_color = fs.cell(column=2, row=i).fill.bgColor.index
                if(background_color == "FFFFFF00"):
                    status = "disabled"
                else:
                    status = "active"
                
                i+=1

                #Create dictionary with these value
                info = {
                    "layer": layer,
                    "name": material_name,
                    "thickness": material_thickness,
                    "unit": material_unit,
                    "indent": material_indent,
                    "color": material_color,
                    "status": status,
                    "rectangle_id": rectangle_id,
                    "text_id": text_id,
                    "text_bbox_id" : text_bbox_id,
                    "line_id": line_id,
                    "entry_id": entry_id,
                    "slider_id": slider_id
                }

                #Put "info" dictionary into self.materials
                self.materials[material_name] = info
                                            
        #Handle errors
        except Exception as error:
            messagebox.showerror("Error", "Could not load materials from Excel-file")
                        
    """Draws the rectangle stack either filled or realistic based on the "switch_layout_counter"""
    def draw_material_stack(self):
        #Clear all rectangle, text, line elements in self.materials
        for material in self.materials:
            self.materials[material]["rectangle_id"] = None  #rectangle_id
            self.materials[material]["text_id"] = None  #rectangle_text_id
            self.materials[material]["line_id"] = None  #arrow_line_id

        #Reset text_size
        self.current_text_size = self.original_text_size

        #Decide which type of stack should be drawn
        if(self.switch_layout_counter % 3 == 0):
            self.draw_material_stack_filled(self.canvas)
        elif(self.switch_layout_counter % 3 == 1):
            self.draw_material_stack_realistic(self.canvas)
        else:
            self.draw_material_stack_stepped(self.canvas)
        
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
            rectangle_height = int(self.materials[material]["thickness"])
            sum_of_all_materials += rectangle_height
        
        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = round((self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0) * 0.9)

        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = canvas_height
        rectangle_x1 = self.visible_canvas_bbox_x1 - 150
        rectangle_y1 = None #Calculated later
        
        #Draw rectangles on canvas
        for material in self.materials:
            #"substrate" will be drawn on the bottom 1/10 of the canvas
            if(material == "substrate"):
                continue    #Skip "substrate"

            #find how many percent the current rectangle's height is of the total sum of materials
            rectangle_height = int(self.materials[material]["thickness"])
            rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
            #Convert rectangle percentage to pixels
            rectangle_height_pixels = (rectangle_percentage/100)*canvas_height


            #draw rectangle from top of canvas to its number of pixles in height
            rectangle_y1 = rectangle_y0 - rectangle_height_pixels
            created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material]["color"], tags="material_rectangle")

            #Add rectangle_id to its place in self.materials
            self.materials[material]["rectangle_id"] = created_rectangle

            #Add rectangle height to prevent overlaping
            rectangle_y0 -= rectangle_height_pixels
        
        #Draw "substrate" on 1/10 of the canvas
        created_rectangle = canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y1, rectangle_x1, canvas_height, fill=self.materials["substrate"]["color"], tags="material_rectangle")
        #Add rectangle_id to its place in self.materials
        self.materials["substrate"]["rectangle_id"] = created_rectangle

        #Draw text on rectangles
        self.write_text_on_materials(self.current_text_size)

    """Draws the rectangle stack in a realistic way"""
    def draw_material_stack_realistic(self, canvas):
        #Clear all existing elements on canvas
        canvas.delete("all")

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black", tags="canvas_bounding_box_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in self.materials:
            rectangle_height = int(self.materials[material]["thickness"])
            sum_of_all_materials += rectangle_height
        
        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y1
        rectangle_x1 = self.visible_canvas_bbox_x1 - 150
        rectangle_y1 = None #Calculated later

        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = (self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0)
        
        #Draw rectangles on canvas
        for material in self.materials:
            #find how many percent the current rectangle's height is of the total sum of materials
            rectangle_height = int(self.materials[material]["thickness"])
            rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
            #Convert rectangle percentage to pixels
            rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

            #draw rectangle from top of canvas to its number of pixles in height
            rectangle_y1 = rectangle_y0 - rectangle_height_pixels
            created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material]["color"], tags="material_rectangle")

            #Add rectangle_id to its place in self.materials
            self.materials[material]["rectangle_id"] = created_rectangle

            #Add rectangle height to prevent overlaping
            rectangle_y0 -= rectangle_height_pixels
        
        #Draw text on rectangles
        self.write_text_on_materials(self.current_text_size)

    """Draws the rectangle stack with "substrate" as 1/10 of the canvas"""
    def draw_material_stack_stepped(self, canvas):
        #Clear all existing elements on canvas
        canvas.delete("all")

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black", tags="canvas_bounding_box_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in self.materials:
            if(material=="substrate"):
                continue    #Skip substrate
            rectangle_height = int(self.materials[material]["thickness"])
            sum_of_all_materials += rectangle_height
        
        #Find the biggest material
        biggest_material = 0
        for material in self.materials:
            if(material == "substrate"):
                continue    #Skip "substrate"
            if(int(self.materials[material]["thickness"]) > biggest_material):
                biggest_material = int(self.materials[material]["thickness"])
            
        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = round((self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0) * 0.9)
        canvas_width = self.visible_canvas_bbox_x1 - self.visible_canvas_bbox_x0
        
        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = canvas_height
        rectangle_x1 = self.visible_canvas_bbox_x1
        rectangle_y1 = None #Calculated later
        
        #Draw rectangles on canvas
        for material in self.materials:
            #"substrate" will be drawn on the bottom 1/10 of the canvas
            if(material == "substrate"):
                continue    #Skip "substrate"

            #find how many percent the current rectangle's height is of the total sum of materials
            rectangle_height = int(self.materials[material]["thickness"])
            rectangle_height_percentage = (rectangle_height/sum_of_all_materials)*100
            #Convert rectangle percentage to pixels
            rectangle_height_pixels = (rectangle_height_percentage/100)*canvas_height

            #Find how much of the canvas width the rectangle should cover
            rectangle_width = int(self.materials[material]["thickness"])
            rectangle_width_percentage = (rectangle_width/biggest_material)
            #Convert width_percentage to pixels
            rectangle_width_pixels = canvas_width*rectangle_width_percentage

            #draw rectangle from bottom of canvas to its number of pixles in height
            rectangle_y1 = rectangle_y0 - rectangle_height_pixels
            rectangle_x1 = rectangle_x0 + rectangle_width_pixels
            created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material]["color"], tags="material_rectangle")

            #Add rectangle_id to its place in self.materials
            self.materials[material]["rectangle_id"] = created_rectangle

            #Add rectangle height to prevent overlaping
            rectangle_y0 -= rectangle_height_pixels
        
        #Draw "substrate" on 1/10 of the canvas
        created_rectangle = canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y1, self.visible_canvas_bbox_x1, canvas_height, fill=self.materials["substrate"]["color"], tags="material_rectangle")
        #Add rectangle_id to its place in self.materials
        self.materials["substrate"]["rectangle_id"] = created_rectangle

        self.write_text_on_materials(self.current_text_size)

    """Writes text on rectangles in the material stack"""
    def write_text_on_materials(self, text_size):
        #Find out the height of a potential text's bounding box
        text_font = font.Font(family=self.text_font, size=text_size)
        text_height = text_font.metrics()['linespace']
        
        for material in self.materials:
            #Find coordinates and height of current material_rectangle
            rectangle_x0 = self.canvas.bbox(self.materials[material]["rectangle_id"])[0]
            rectangle_y0 = self.canvas.bbox(self.materials[material]["rectangle_id"])[1]
            rectangle_x1 = self.canvas.bbox(self.materials[material]["rectangle_id"])[2]
            rectangle_y1 = self.canvas.bbox(self.materials[material]["rectangle_id"])[3]
            rectangle_height = rectangle_y1-rectangle_y0
            rectangle_middle_x = (rectangle_x0 + rectangle_x1)/2
            rectangle_middle_y = (rectangle_y0 + rectangle_y1) / 2

            #Text is drawn inside rectangle if it fits
            if(text_height < rectangle_height):
                created_text = self.canvas.create_text(rectangle_middle_x, rectangle_middle_y, text=f"{material} - {self.materials[material]['thickness']}nm", fill="black", font=(self.text_font, text_size), anchor="center", tags="Material_label")
                
                #If text is outside leftside of canvas, place it on the left canvas side
                if(self.canvas.bbox(created_text)[0] < self.visible_canvas_bbox_x0):
                    margin = self.visible_canvas_bbox_x0 - self.canvas.bbox(created_text)[0] 
                    self.canvas.coords(created_text, rectangle_middle_x+margin, rectangle_middle_y)
                
                #If text is outside rightside of canvas, place it on the right canvas side
                if(self.canvas.bbox(created_text)[2] > self.visible_canvas_bbox_x1):
                    margin = self.canvas.bbox(created_text)[2] - self.visible_canvas_bbox_x1 
                    self.canvas.coords(created_text, rectangle_middle_x-margin, rectangle_middle_y)
                #Add text element to dictionary
                self.materials[material]["text_id"] = created_text

            #Text must be drawn outside rectangle
            else:
                created_text = self.canvas.create_text(rectangle_x1 + 20, rectangle_middle_y, text=f"{material} - {self.materials[material]['thickness']}nm", fill="black", font=(self.text_font, text_size), anchor="w", tags="Material_label")
                created_text_bbox = self.canvas.create_rectangle(self.canvas.bbox(created_text), outline='black', tags="text_bbox")     
                text_bbox_x0 = self.canvas.bbox(created_text)[0]
                text_bbox_y0 = self.canvas.bbox(created_text)[1]
                text_bbox_x1 = self.canvas.bbox(created_text)[2]
                text_bbox_y1 = self.canvas.bbox(created_text)[3]
                text_bbox_middle_y = (text_bbox_y0 + text_bbox_y1) / 2
                created_arrow_line = self.canvas.create_line((text_bbox_x0, text_bbox_middle_y), (rectangle_x1, rectangle_middle_y), arrow=tk.LAST, tags="arrow_line")

                self.materials[material]["text_id"] = created_text
                self.materials[material]["text_bbox_id"] = created_text_bbox
                self.materials[material]["line_id"] = created_arrow_line


        #Loop through every material and make sure none of the texts are overlaping each other or canvas
        previous_material = None
        for material in self.materials:
            if(material == "t_Au"):
                #Get the bounding box of the materials text
                text_bbox_x0 = self.canvas.bbox(self.materials[material]["text_id"])[0]
                text_bbox_y0 = self.canvas.bbox(self.materials[material]["text_id"])[1]
                text_bbox_x1 = self.canvas.bbox(self.materials[material]["text_id"])[2]
                text_bbox_y1 = self.canvas.bbox(self.materials[material]["text_id"])[3]
                text_bbox_middle_y = (text_bbox_y0 + text_bbox_y1) / 2

                #Get the bounding box of the previous materials text
                if(previous_material is not None):
                    previous_text_bbox_x0 = self.canvas.bbox(self.materials[previous_material]["text_id"])[0]
                    previous_text_bbox_y0 = self.canvas.bbox(self.materials[previous_material]["text_id"])[1]
                    previous_text_bbox_x1 = self.canvas.bbox(self.materials[previous_material]["text_id"])[2]
                    previous_text_bbox_y1 = self.canvas.bbox(self.materials[previous_material]["text_id"])[3]

                #if(text overlaps with canvas top):
                if(text_bbox_y0 < self.visible_canvas_bbox_y0):
                    #Find how much is overlapping
                    overlap = self.visible_canvas_bbox_y0 - text_bbox_y0
                    #Move text down
                    self.canvas.move(self.materials[material]["text_id"], 0, overlap)
                    #Delete and create new bounding box for text
                    self.canvas.delete(self.materials[material]["text_bbox_id"])
                    new_text_bbox = self.canvas.create_rectangle(self.canvas.bbox([self.materials[material]["text_id"]]), outline="black", tags="text_bbox")
                    self.materials[material]["text_bbox_id"] = new_text_bbox
                    #Move the arrow line for the text
                    #Find coordinates of text bounding box
                    tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    #Find coordinates of rectangle
                    rx0, ry0, rx1, ry1 = self.canvas.bbox(self.materials[material]["rectangle_id"])
                    #Delete the arrow line
                    self.canvas.delete(self.materials[material]["line_id"])
                    #Create new arrow line
                    created_arrow_line = self.canvas.create_line(tx0, (ty0+ty1)/2, rx1, (ry0+ry1)/2, arrow=tk.LAST, tags="arrow_line")
                    #Add the new line to dictionary

                    #CONTINUE HEREEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!
                    

                #if(Text overlaps with canvas bottom):
                if(text_bbox_y1 > self.visible_canvas_bbox_y1):
                    #Find how much is overlapping
                    #Move text up
                    pass
                
                #if(Text overlaps with the left side of the canvas):
                if(text_bbox_x0 < self.visible_canvas_bbox_x0):
                    #Find how much is overlapping
                    #Move text right
                    pass

                #if(Text overlaps with the right side of the canvas):
                if(text_bbox_x1 > self.visible_canvas_bbox_x1):
                    #Find how much is overlapping
                    #Move text left
                    pass

                #if(Text top overlaps with previous text bottom):
                if(previous_material is not None and text_bbox_y0 < previous_text_bbox_y1):
                    #Find how much is overlapping
                    #Move text down
                    pass

                #if(Text bottom overlaps with previous text top):
                if(previous_material is not None and text_bbox_y1 < previous_text_bbox_y1):
                    #Find how much is overlapping
                    #Move text down
                    pass

                previous_material = material

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

        #Find all elements currently on canvas
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
        #Specify a folder where the SVG-files should be saved
        folder_path = "svg_exports"
        #Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #Each SVG-file is assigned a number based on how many layers are in each file
        layer_counter = 1
        previously_created_elements = []

        #Iterate through all the materials
        for material in self.materials:
            #Create a name for the SVG file for the current layer
            filename = f"{layer_counter}_layers.svg"

            #Create the file path by joining the folder path and the filename
            file_path = os.path.join(folder_path, filename)

            #Open file for writing
            with open(file_path, 'w') as f:
                #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
                f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
                f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.canvas.winfo_reqwidth()+1000, self.canvas.winfo_reqheight()))
                
                #DO STUFF
                if(len(previously_created_elements) != 0):
                    for element in previously_created_elements:
                        f.write(element)

                #[material_thickness, material_color, rectangle_id, slider_id, entry_id, text_id, line_id]

                #Create SVG-element of rectangle and write it to file
                rect_x0, rect_y0, rect_x1, rect_y1 = self.canvas.coords(self.materials[material]["rectangle_id"])
                fill_color = self.canvas.itemcget(self.materials[material]["rectangle_id"], 'fill')  # Retrieve fill color of the rectangle from the canvas
                svg_rectangle_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, fill_color)
                f.write(svg_rectangle_element)
                previously_created_elements.append(svg_rectangle_element)

                #Create SVG-element for the rectangle bounding box and write it to file
                svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0)
                f.write(svg_bbox_element)
                previously_created_elements.append(svg_bbox_element)

                #Create SVG-element for text and write it to file
                if(self.materials[material]["text_id"] is not None):
                    text_x0, text_y0 = self.canvas.coords(self.materials[material]["text_id"])
                    text_content = self.canvas.itemcget(self.materials[material]["text_id"], 'text')
                    # svg_text_element = '<text x="{}" y="{}" fill="black" font-size="14" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(text_x0, text_y0, text_content)
                    svg_text_element = '<text x="{}" y="{}" fill="black" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(text_x0, text_y0, self.current_text_size, text_content)
                    f.write(svg_text_element)
                    previously_created_elements.append(svg_text_element)
                

                #Add arrow lines
                #Add text bounding boxes

                #END STUFF

                #Write the closing SVG tag to the file, completing the SVG file
                f.write('</svg>\n')
            
            #Close the svg file
            f.close()

            #Increment layer_counter
            layer_counter += 1

#Main start point of program
if __name__ == "__main__":
    window = tk.Tk()
    
    #Create instance of class and run application
    app = App(window)

    #Closes the program if "esc" key is pressed
    window.bind("<Escape>", lambda event: window.destroy())

    window.bind('<KeyPress-r>', app.reset_canvas)

    window.mainloop()