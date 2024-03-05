import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL, Frame, Entry, StringVar, Label, Button, messagebox, font
from PIL import ImageGrab, Image
import pandas as pd
import pygetwindow
import pyautogui
import os
import math
import openpyxl
from settings import Settings

class App:
    def __init__(self, window):       
        self.program_title = Settings.PROGRAM_TITLE
        self.program_window_width = Settings.PROGRAM_WINDOW_WIDTH
        self.program_window_height = Settings.PROGRAM_WINDOW_HEIGHT
        self.excel_file = Settings.EXCEL_FILE
        self.original_text_size = Settings.TEXT_SIZE
        self.current_text_size = self.original_text_size
        self.text_font = Settings.TEXT_FONT
        self.stack_text_indent = Settings.STACK_TEXT_INDENT
        self.stepped_stack_indent = Settings.INDENT_RANGE
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
        user_interface_frame.configure(bg=Settings.UI_FRAME_BACKGROUND_COLOR)
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
                command=lambda value, identifier=material: self.material_slider_updated(value, identifier),
                bg=None#Settings.SLIDER_BACKGROUND_COLOR 
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
        switch_layout_button.grid(row=1, column=1, sticky="ne", padx=(5, 5))
        self.switch_layout_label = Label(window, text="Filled", font="bold")
        self.switch_layout_label.grid(row=2, column=1, sticky="e", padx=(0, 5))

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
        canvas = Canvas(window, 
            height=Settings.CANVAS_HEIGHT,#self.user_interface_frame.winfo_reqheight()-300, 
            width=self.program_window_width-self.user_interface_frame.winfo_width(), 
            bg=Settings.CANVAS_BACKGROUND_COLOR
            )
        canvas.grid(row=0, column=1, sticky="s")

        #Set bbox coordinates for later use
        self.visible_canvas_bbox_x0 = 2
        self.visible_canvas_bbox_y0 = 2
        self.visible_canvas_bbox_x1 = canvas.winfo_reqwidth() - 5 - Settings.CANVAS_PROGRAM_BORDER_WIDTH
        self.visible_canvas_bbox_y1 = canvas.winfo_reqheight() - 3 - Settings.CANVAS_PROGRAM_BORDER_HEIGHT
        self.canvas_height = self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0
        self.canvas_width = self.visible_canvas_bbox_x1 - self.visible_canvas_bbox_x0

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

        #Create new canvas
        self.canvas = Canvas(window, 
            height=Settings.CANVAS_HEIGHT,#self.user_interface_frame.winfo_reqheight(), 
            width=self.program_window_width-self.user_interface_frame.winfo_width(), 
            bg=Settings.CANVAS_BACKGROUND_COLOR
            )
        self.canvas.grid(row=0, column=1, sticky="s")

        #Set bbox coordinates for later use
        self.visible_canvas_bbox_x0 = 2
        self.visible_canvas_bbox_y0 = 2
        self.visible_canvas_bbox_x1 = self.canvas.winfo_reqwidth() - 5 - Settings.CANVAS_PROGRAM_BORDER_WIDTH
        self.visible_canvas_bbox_y1 = self.canvas.winfo_reqheight() - 3 - Settings.CANVAS_PROGRAM_BORDER_HEIGHT
        self.canvas_height = self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0
        self.canvas_width = self.visible_canvas_bbox_x1 - self.visible_canvas_bbox_x0

        #Draw bounding box around canvas
        self.canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black")

        #Listen to mouse buttonpress, motion and zoom events
        self.canvas.bind("<ButtonPress-1>", lambda event, canvas=self.canvas: self.click_on_canvas(event, self.canvas))
        self.canvas.bind("<B1-Motion>", lambda event, canvas=self.canvas: self.canvas_drag(event, self.canvas))
        self.canvas.bind("<MouseWheel>", lambda event, canvas=self.canvas: self.canvas_zoom(event, self.canvas))

        #Reset the text size back to original
        self.current_text_size = self.original_text_size
        
        # #Draw rectangle stack
        # self.draw_material_stack()

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

        #Redraw text on stack
        if(self.switch_layout_counter % 3 == 0):
            self.write_text_on_stack(self.current_text_size)
        elif(self.switch_layout_counter % 3 == 1):
            self.write_text_on_stack(self.current_text_size)
        else:
            self.write_text_on_stepped_stack(self.current_text_size)

    """Scales the material stack according to the program window"""
    def program_window_resized(self, event):
        #Update the variable that tracks th window_width
        self.program_window_width = window.winfo_width()

        #Set the new width of the canvas
        self.canvas.config(width=self.program_window_width-self.user_interface_frame.winfo_width())

        #Update the variables that track the actual visible parts of the canvas
        self.visible_canvas_bbox_x1 = self.program_window_width-self.user_interface_frame.winfo_width() - 5 - Settings.CANVAS_PROGRAM_BORDER_WIDTH
        # self.visible_canvas_bbox_y1 = 

        #Redraw the material stack
        self.draw_material_stack()
    
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

            #Update new slider ranges
            for material in self.materials:
                self.materials[material]["slider_id"].config(from_=1, to=int(self.materials["substrate"]["thickness"]))

        #Update the text of switch_layout_label and enable "substrate" slider and entry
        elif(self.switch_layout_counter % 3 == 1):
            self.switch_layout_label.config(text="Realistic")

            #Update new slider ranges
            for material in self.materials:
                self.materials[material]["slider_id"].config(from_=1, to=int(self.materials["substrate"]["thickness"]))
        
        #Update the text of switch_layout_label and enable "substrate" slider and entry
        else:
            self.switch_layout_label.config(text="Stepped")

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
                indent_text_id = None
                indent_arrow_id = None

                #Check the background color of the cell
                background_color = fs.cell(column=2, row=i).fill.bgColor.index
                if(background_color == "FFFFFF00"):
                    status = "disabled"
                else:
                    status = "active"
                
                i+=1

                #Create dictionary with these value
                info = {
                    "name": material_name,
                    "layer": layer,
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
                    "slider_id": slider_id,
                    "indent_text_id": indent_text_id,
                    "indent_arrow_id": indent_arrow_id
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
        
    """Draws the rectangle stack where "substrate" is 1/10 of the canvas no matter what"""
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
        canvas_height = round(self.canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y0 + (self.canvas_height*0.9)
        rectangle_x1 = self.visible_canvas_bbox_x1 - self.stack_text_indent
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
        self.write_text_on_stack(self.current_text_size)

    """Draws a realistic version of the rectangle stack"""
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
        rectangle_x1 = self.visible_canvas_bbox_x1 - self.stack_text_indent
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
        self.write_text_on_stack(self.current_text_size)

    """Draws a stepped rectangle stack where the "indent" is equal to the rectangles height"""
    def draw_material_stack_stepped(self, canvas):
        #Clear all existing elements on canvas
        canvas.delete("all")

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black", tags="canvas_bounding_box_rectangle")
        
        #Find the total height of all materials combined and the thickest material
        sum_of_all_materials = 0
        biggest_material = 0
        for material in self.materials:
            if(material=="substrate"):
                continue    #Skip substrate
            sum_of_all_materials += int(self.materials[material]["thickness"])
            if(biggest_material < int(self.materials[material]["thickness"])):
                biggest_material = int(self.materials[material]["thickness"])

        #Create new boundaries within main canvas to draw stepped stack
        stepped_stack_x0 = self.visible_canvas_bbox_x0 + self.stack_text_indent
        stepped_stack_y0 = self.visible_canvas_bbox_y0
        stepped_stack_x1 = self.visible_canvas_bbox_x1
        stepped_stack_y1 = round(self.canvas_height * 0.9)
        stepped_stack_height = round(self.canvas_height * 0.9)
        stepped_stack_width = stepped_stack_x1 - stepped_stack_x0
        previous_rectangle_width_pixels = 0

        #Prepare first rectangle drawing coordinates (from bottom left corner)
        rectangle_x0 = stepped_stack_x0
        rectangle_y0 = self.visible_canvas_bbox_y0 + round(self.canvas_height*0.9)
        rectangle_x1 = self.visible_canvas_bbox_x1
        rectangle_y1 = self.visible_canvas_bbox_y0

        #Draw rectangles on canvas
        for material in self.materials:
            #"substrate" will be drawn on the bottom 1/10 of the canvas
            if(material == "substrate"):
                created_rectangle = canvas.create_rectangle(stepped_stack_x0, round(self.canvas_height*0.9), stepped_stack_x1, self.visible_canvas_bbox_y1, fill="grey", tags="material_rectangle")
                self.materials["substrate"]["rectangle_id"] = created_rectangle

            else:
                #find how many percent the current rectangle's height is of the total sum of materials
                rectangle_height = int(self.materials[material]["thickness"])
                rectangle_height_percentage = (rectangle_height/sum_of_all_materials)*100
                #Convert rectangle percentage to pixels
                rectangle_height_pixels = (rectangle_height_percentage/100)*stepped_stack_height

                #Set the y1 coordinate of the rectangle
                rectangle_y1 = rectangle_y0 - rectangle_height_pixels

                #Calculate the width of the current material
                rectangle_x1 = rectangle_x1 - previous_rectangle_width_pixels

                #Store this width for the next rectangle (must be done now to get the height and the width of the rectangle to be equal)
                previous_rectangle_width_pixels = rectangle_height_pixels

                #Create rectangle
                created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material]["color"], tags="material_rectangle")

                #Add rectangle_id to its place in self.materials
                self.materials[material]["rectangle_id"] = created_rectangle

                #Add rectangle height to prevent overlaping
                rectangle_y0 -= rectangle_height_pixels
        
        self.write_text_on_stepped_stack(self.current_text_size)

    """Draws a stepped rectangle stack where the rectangle width is a percentage of the stack width"""
    def draw_material_stack_stepped_percentage(self, canvas):
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
    def write_text_on_stack(self, text_size):
        #Delete all texts on canvas and draw them again
        for material in self.materials:
            self.canvas.delete(self.materials[material]["text_id"])
            self.canvas.delete(self.materials[material]["text_bbox_id"])
            self.canvas.delete(self.materials[material]["line_id"])
        
        #Find out the height of a potential text's bounding box
        text_font = font.Font(family=self.text_font, size=text_size)
        text_height = text_font.metrics()['linespace']
        previous_material = None
        
        #for material in self.materials:
        for material in dict(reversed(self.materials.items())):
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
                created_text = self.canvas.create_text(self.visible_canvas_bbox_x1-5, rectangle_middle_y, text=f"{material} - {self.materials[material]['thickness']}nm", fill="black", font=(self.text_font, text_size), anchor="e", tags="Material_label")
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
                    #Move text and bbox down
                    self.canvas.move(self.materials[material]["text_id"], 0, overlap)
                    self.canvas.move(self.materials[material]["text_bbox_id"], 0, overlap)
                    #Find coordinates of text bounding box
                    tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    #Delete the arrow line
                    self.canvas.delete(self.materials[material]["line_id"])
                    #Create new arrow line
                    created_arrow_line = self.canvas.create_line(tx0, (ty0+ty1)/2, rectangle_x1, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                    #Add the new line to dictionary
                    self.materials[material]["line_id"] = created_arrow_line

                #if(Text overlaps with canvas bottom):
                if(text_bbox_y1 > self.visible_canvas_bbox_y1):
                    #Find how much is overlapping
                    overlap = text_bbox_y1 - self.visible_canvas_bbox_y1
                    #Move text up
                    self.canvas.move(self.materials[material]["text_id"], 0, -overlap)
                    self.canvas.move(self.materials[material]["text_bbox_id"], 0, -overlap)
                    #Find coordinates of text bounding box
                    tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    #Delete the arrow line
                    self.canvas.delete(self.materials[material]["line_id"])
                    #Create new arrow line
                    created_arrow_line = self.canvas.create_line(tx0, (ty0+ty1)/2, rectangle_x1, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                    #Add the new line to dictionary
                    self.materials[material]["line_id"] = created_arrow_line

                # if(Text top overlaps with previous text bottom):
                if(previous_material is not None and text_bbox_y0 < previous_text_bbox_y1):
                    #Find how much is overlapping
                    overlap = previous_text_bbox_y1 - text_bbox_y0
                    #Move text down
                    self.canvas.move(self.materials[material]["text_id"], 0, overlap)
                    self.canvas.move(self.materials[material]["text_bbox_id"], 0, overlap)
                    #Find coordinates of text bounding box
                    tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    #Delete the arrow line
                    self.canvas.delete(self.materials[material]["line_id"])
                    #Create new arrow line
                    created_arrow_line = self.canvas.create_line(tx0, (ty0+ty1)/2, rectangle_x1, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                    #Add the new line to dictionary
                    self.materials[material]["line_id"] = created_arrow_line

                    # #if(Text bottom overlaps with previous text top):
                    # if(previous_material is not None and text_bbox_y1 < previous_text_bbox_y1):
                    #     #Find how much is overlapping
                    #     overlap = previous_text_bbox_y1 - text_bbox_y1
                    #     #Move text down
                    #     self.canvas.move(self.materials[material]["text_id"], 0, overlap)
                    #     self.canvas.move(self.materials[material]["text_bbox_id"], 0, overlap)
                    #     #Find coordinates of text bounding box
                    #     tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    #     #Delete the arrow line
                    #     self.canvas.delete(self.materials[material]["line_id"])
                    #     #Create new arrow line
                    #     created_arrow_line = self.canvas.create_line(tx0, (ty0+ty1)/2, rectangle_x1, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                    #     #Add the new line to dictionary
                    #     self.materials[material]["line_id"] = created_arrow_line

                previous_material = material

    """Writes text on the left side of the material stack"""
    def write_text_on_stepped_stack(self, text_size):
        #Delete all texts on canvas and draw them again
        for material in self.materials:
            self.canvas.delete(self.materials[material]["text_id"])
            self.canvas.delete(self.materials[material]["text_bbox_id"])
            self.canvas.delete(self.materials[material]["line_id"])

        #Find out the height of a potential text's bounding box
        text_font = font.Font(family=self.text_font, size=text_size)
        text_height = text_font.metrics()['linespace']
        previous_material = None
        
        #for material in self.materials:
        for material in dict(reversed(self.materials.items())):
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
                created_text = self.canvas.create_text(self.visible_canvas_bbox_x0+5, rectangle_middle_y, text=f"{material} - {self.materials[material]['thickness']}nm", fill="black", font=(self.text_font, text_size), anchor="w", tags="Material_label")
                created_text_bbox = self.canvas.create_rectangle(self.canvas.bbox(created_text), outline='black', tags="text_bbox")     
                text_bbox_x0 = self.canvas.bbox(created_text)[0]
                text_bbox_y0 = self.canvas.bbox(created_text)[1]
                text_bbox_x1 = self.canvas.bbox(created_text)[2]
                text_bbox_y1 = self.canvas.bbox(created_text)[3]
                text_bbox_middle_y = (text_bbox_y0 + text_bbox_y1) / 2
                created_arrow_line = self.canvas.create_line((text_bbox_x1, text_bbox_middle_y), (rectangle_x0, rectangle_middle_y), arrow=tk.LAST, tags="arrow_line")

                #Add text ID, bbox ID and arrow line ID to dictionary 
                self.materials[material]["text_id"] = created_text
                self.materials[material]["text_bbox_id"] = created_text_bbox
                self.materials[material]["line_id"] = created_arrow_line

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
                    #Move text and bbox down
                    self.canvas.move(self.materials[material]["text_id"], 0, overlap)
                    self.canvas.move(self.materials[material]["text_bbox_id"], 0, overlap)
                    #Find coordinates of text bounding box
                    tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    #Delete the arrow line
                    self.canvas.delete(self.materials[material]["line_id"])
                    #Create new arrow line
                    created_arrow_line = self.canvas.create_line(tx1, (ty0+ty1)/2, rectangle_x0, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                    #Add the new line to dictionary
                    self.materials[material]["line_id"] = created_arrow_line

                #if(Text overlaps with canvas bottom):
                if(text_bbox_y1 > self.visible_canvas_bbox_y1):
                    #Find how much is overlapping
                    overlap = text_bbox_y1 - self.visible_canvas_bbox_y1
                    #Move text up
                    self.canvas.move(self.materials[material]["text_id"], 0, -overlap)
                    self.canvas.move(self.materials[material]["text_bbox_id"], 0, -overlap)
                    #Find coordinates of text bounding box
                    tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    #Delete the arrow line
                    self.canvas.delete(self.materials[material]["line_id"])
                    #Create new arrow line
                    created_arrow_line = self.canvas.create_line(tx1, (ty0+ty1)/2, rectangle_x0, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                    #Add the new line to dictionary
                    self.materials[material]["line_id"] = created_arrow_line

                #if(Text top overlaps with previous text bottom):
                if(previous_material is not None and text_bbox_y0 < previous_text_bbox_y1):
                    #Find how much is overlapping
                    overlap = previous_text_bbox_y1 - text_bbox_y0
                    #Move text down
                    self.canvas.move(self.materials[material]["text_id"], 0, overlap)
                    self.canvas.move(self.materials[material]["text_bbox_id"], 0, overlap)
                    #Find coordinates of text bounding box
                    tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    #Delete the arrow line
                    self.canvas.delete(self.materials[material]["line_id"])
                    #Create new arrow line
                    created_arrow_line = self.canvas.create_line(tx1, (ty0+ty1)/2, rectangle_x0, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                    #Add the new line to dictionary
                    self.materials[material]["line_id"] = created_arrow_line

                    #if(Text bottom overlaps with previous text top):
                    if(previous_material is not None and text_bbox_y1 < previous_text_bbox_y1):
                        #Find how much is overlapping
                        overlap = previous_text_bbox_y1 - text_bbox_y1
                        #Move text down
                        self.canvas.move(self.materials[material]["text_id"], 0, overlap)
                        self.canvas.move(self.materials[material]["text_bbox_id"], 0, overlap)
                        #Find coordinates of text bounding box
                        tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                        #Delete the arrow line
                        self.canvas.delete(self.materials[material]["line_id"])
                        #Create new arrow line
                        created_arrow_line = self.canvas.create_line(tx1, (ty0+ty1)/2, rectangle_x0, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                        #Add the new line to dictionary
                        self.materials[material]["line_id"] = created_arrow_line

                #if text is overlaps with the left side of the canvas
                # if(text_bbox_x0 < self.visible_canvas_bbox_x0):
                    # self.canvas.move(self.materials[material]["text_id"], 100, 0)
                    # self.canvas.move(self.materials[material]["text_bbox_id"], 0, overlap)
                    # #Find coordinates of text bounding box
                    # tx0, ty0, tx1, ty1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    # #Delete the arrow line
                    # self.canvas.delete(self.materials[material]["line_id"])
                    # #Create new arrow line
                    # created_arrow_line = self.canvas.create_line(tx1, (ty0+ty1)/2, rectangle_x0, (rectangle_y0+rectangle_y1)/2, arrow=tk.LAST, tags="arrow_line")
                    # #Add the new line to dictionary
                    # self.materials[material]["line_id"] = created_arrow_line


                previous_material = material
        
        #Write the given indent ranges    
        self.write_indent_range_on_stepped_stack()

    """Writes the indent ranges on the stepped material stack"""
    def write_indent_range_on_stepped_stack(self):
        #Delete all texts on canvas and draw them again
        for material in self.materials:
            self.canvas.delete(self.materials[material]["indent_text_id"])
            self.canvas.delete(self.materials[material]["indent_arrow_id"])
        
        previous_rectangle_x1 = None
        previous_rectangle_y1 = None
        previous_material = None

        #Loop through all the materials
        for material in dict(reversed(self.materials.items())):
            #Find x1 and y1 coordinates of current material_rectangle
            current_rectangle_x1 = self.canvas.bbox(self.materials[material]["rectangle_id"])[2]
            current_rectangle_y1 = self.canvas.bbox(self.materials[material]["rectangle_id"])[3]

            if(previous_rectangle_x1 is not None): #and previous_rectangle_x1-current_rectangle_x1 != 0):
                #Create a two sided arrow line between the differense of the two rectangles
                created_arrow_line = self.canvas.create_line(current_rectangle_x1, previous_rectangle_y1-5, previous_rectangle_x1, previous_rectangle_y1-5, arrow=tk.BOTH)
                #Write indent number over line
                indent_number = int(self.materials[material]["indent"])

                created_indent_text = self.canvas.create_text(previous_rectangle_x1, previous_rectangle_y1-15, text=f"{indent_number}nm", fill="black", font=(self.text_font, self.current_text_size), anchor="w", tags="double_arrow_indent")
                
                #Add created elements to dictionary
                self.materials[material]["indent_text_id"] = created_indent_text
                self.materials[material]["indent_arrow_id"] = created_arrow_line

            #Set new "previous_rectangle" coordinates
            previous_rectangle_x1 = current_rectangle_x1
            previous_rectangle_y1 = current_rectangle_y1
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
            # f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()))
            f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(window.winfo_reqwidth(), window.winfo_reqheight()))


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
                # f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.canvas.winfo_reqwidth()+1000, self.canvas.winfo_reqheight()))
                f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(window.winfo_reqwidth(), window.winfo_reqheight()))

                
                #Write the previous created elements to the current file
                if(len(previously_created_elements) != 0):
                    for element in previously_created_elements:
                        f.write(element)

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
                    if(self.switch_layout_counter % 3 == 2):    #The text is written on the right side of the stack
                        text_x0, text_y0 = self.canvas.coords(self.materials[material]["text_id"])
                        text_content = self.canvas.itemcget(self.materials[material]["text_id"], 'text')
                        svg_text_element = '<text x="{}" y="{}" fill="black" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="west">{}</text>\n'.format(text_x0, text_y0, Settings.SVG_TEXT_SIZE, text_content)
                        
                        f.write(svg_text_element)
                        previously_created_elements.append(svg_text_element)
                    else:   
                        text_x0, text_y0 = self.canvas.coords(self.materials[material]["text_id"])
                        text_content = self.canvas.itemcget(self.materials[material]["text_id"], 'text')
                        svg_text_element = '<text x="{}" y="{}" fill="black" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(text_x0, text_y0, Settings.SVG_TEXT_SIZE, text_content)
                        
                        f.write(svg_text_element)
                        previously_created_elements.append(svg_text_element)
                
                #Create SVG-element for text bounding box
                if(self.materials[material]["text_bbox_id"] is not None):
                    #The text is written on the left side of the stack
                    if(self.switch_layout_counter % 3 == 2):
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                        svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black" />\n'.format(bbox_x0, bbox_y0, bbox_x1 - bbox_x0, bbox_y1 - bbox_y0)
                        
                        # Write the SVG representation of the bounding box to the file
                        f.write(svg_bbox_element)
                        previously_created_elements.append(svg_bbox_element)
                    #The text is written on the right side of the stack
                    else:
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                        svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black" />\n'.format(bbox_x0+(bbox_x1-bbox_x0)/2, bbox_y0, bbox_x1 - bbox_x0, bbox_y1 - bbox_y0)
                        
                        # Write the SVG representation of the bounding box to the file
                        f.write(svg_bbox_element)
                        previously_created_elements.append(svg_bbox_element)

                #Create SVG-element for arrow line pointing from box to rectangle
                if(self.materials[material]["line_id"] is not None):
                    #The text is written on the left side of the stack
                    if(self.switch_layout_counter % 3 == 2):
                        line_coords = self.canvas.coords(self.materials[material]["line_id"])
                        #Construct an SVG <line> element for arrows
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                        svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black" />\n'.format(bbox_x1, line_coords[1], line_coords[2], line_coords[3])
                        
                        #Write the SVG representation of the arrow to the file
                        f.write(svg_line_element)
                        previously_created_elements.append(svg_line_element)
                    #The text is written on the right side of the stack
                    else:
                        line_coords = self.canvas.coords(self.materials[material]["line_id"])
                        #Construct an SVG <line> element for arrows
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                        svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black" />\n'.format(bbox_x1-(bbox_x1-bbox_x0)/2, line_coords[1], line_coords[2], line_coords[3])
                        #Write the SVG representation of the arrow to the file
                        f.write(svg_line_element)
                        previously_created_elements.append(svg_line_element)

                #Create SVG-element for indent_text
                if(self.materials[material]["indent_text_id"] is not None):
                    indent_text_x0, indent_text_y0 = self.canvas.coords(self.materials[material]["indent_text_id"])
                    indent_text_content = self.canvas.itemcget(self.materials[material]["indent_text_id"], 'text')
                    svg_indent_text_element = '<text x="{}" y="{}" fill="black" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(rect_x1-10, indent_text_y0, Settings.SVG_TEXT_SIZE, indent_text_content)
                        
                    f.write(svg_indent_text_element)
                    previously_created_elements.append(svg_indent_text_element)

                #Create SVG-element for indent_arrow_line
                if(self.materials[material]["indent_arrow_id"] is not None):
                    indent_line_coords = self.canvas.coords(self.materials[material]["indent_arrow_id"])
                    #Construct an SVG <line> element for arrows
                    svg_indent_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />\n'.format(indent_line_coords[0]-10, indent_line_coords[1], indent_line_coords[2]+10, indent_line_coords[3])
                    
                    #Add arrowheads on both sides of the line
                    svg_indent_line_element += (
                        '<defs>\n'
                        '    <marker id="arrow-start" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="0" markerUnits="userSpaceOnUse">\n'
                        '        <path d="M0,0 L0,6 L9,3 z" fill="black" />\n'
                        '    </marker>\n'
                        '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="0" markerUnits="userSpaceOnUse">\n'
                        '        <path d="M0,3 L9,0 L9,6 z" fill="black" />\n'
                        '    </marker>\n'
                        '</defs>\n'
                    )
                    
                    #Write the SVG representation of the arrow to the file
                    f.write(svg_indent_line_element)
                    previously_created_elements.append(svg_indent_line_element)

                #Write the closing SVG tag to the file, completing the SVG file
                f.write('</svg>\n')
            
            #Close the svg file
            f.close()

            #Increment layer_counter
            layer_counter += 1

#Main start point of program
if __name__ == "__main__":
    window = tk.Tk()
    window.configure(bg=Settings.PROGRAM_BACKGROUND_COLOR)
    
    #Create instance of class and run application
    app = App(window)

    #Closes the program if "esc" key is pressed
    window.bind("<Escape>", lambda event: window.destroy())

    #Resets the canvas position if "r" is pressed
    window.bind('<KeyPress-r>', app.reset_canvas)

    #Checks if the program window is being resized
    window.bind("<Configure>", app.program_window_resized)

    window.mainloop()






    
# def draw_material_stack_stepped_orig(self, canvas):
#         print("ORIGINAL")
#         #Clear all existing elements on canvas
#         canvas.delete("all")

#         #Draw bounding box around canvas
#         canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black", tags="canvas_bounding_box_rectangle")
        
#         #Find the total height of all materials combined and the thickest material
#         sum_of_all_materials = 0
#         biggest_material = 0
#         for material in self.materials:
#             if(material=="substrate"):
#                 continue    #Skip substrate
#             sum_of_all_materials += int(self.materials[material]["thickness"])
#             if(biggest_material < int(self.materials[material]["thickness"])):
#                 biggest_material = int(self.materials[material]["thickness"])

#         #Create new boundaries within main canvas to draw stepped stack
#         stepped_stack_x0 = self.visible_canvas_bbox_x0 + self.stack_text_indent
#         stepped_stack_y0 = self.visible_canvas_bbox_y0
#         stepped_stack_x1 = self.visible_canvas_bbox_x1
#         stepped_stack_y1 = round(self.canvas_height * 0.9)
#         stepped_stack_height = round(self.canvas_height * 0.9)
#         stepped_stack_width = stepped_stack_x1 - stepped_stack_x0
#         previous_rectangle_width_pixels = stepped_stack_width

#         #Prepare first rectangle drawing coordinates (from bottom left corner)
#         rectangle_x0 = stepped_stack_x0
#         rectangle_y0 = self.visible_canvas_bbox_y0 + round(self.canvas_height*0.9)
#         rectangle_x1 = self.visible_canvas_bbox_x1
#         rectangle_y1 = self.visible_canvas_bbox_y0

#         #Draw rectangles on canvas
#         for material in self.materials:
#             #"substrate" will be drawn on the bottom 1/10 of the canvas
#             if(material == "substrate"):
#                 created_rectangle = canvas.create_rectangle(stepped_stack_x0, round(self.canvas_height*0.9), stepped_stack_x1, self.visible_canvas_bbox_y1, fill="grey", tags="material_rectangle")
#                 self.materials["substrate"]["rectangle_id"] = created_rectangle

#             else:
#                 #find how many percent the current rectangle's height is of the total sum of materials
#                 rectangle_height = int(self.materials[material]["thickness"])
#                 rectangle_height_percentage = (rectangle_height/sum_of_all_materials)*100
#                 #Convert rectangle percentage to pixels
#                 rectangle_height_pixels = (rectangle_height_percentage/100)*stepped_stack_height
#                 #Set the y1 coordinate of the rectangle
#                 rectangle_y1 = rectangle_y0 - rectangle_height_pixels

#                 #Calculate nanometers per pixel ratio from the "INDENT_RANGE" variable
#                 nanometers_per_pixel = Settings.INDENT_RANGE/stepped_stack_width
                    
#                 #Calculate how many pixels the given material_indent is
#                 indent_pixels = int(self.materials[material]["indent"]) / nanometers_per_pixel

#                 # rectangle_x1 = rectangle_x1 - indent_pixels
#                 rectangle_x1 = rectangle_x1 - rectangle_height_pixels

#                 previous_rectangle_width_pixels = rectangle_x1

#                 #Create rectangle
#                 created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material]["color"], tags="material_rectangle")

#                 #Add rectangle_id to its place in self.materials
#                 self.materials[material]["rectangle_id"] = created_rectangle

#                 #Add rectangle height to prevent overlaping
#                 rectangle_y0 -= rectangle_height_pixels
        
#         self.write_text_on_stepped_stack(self.current_text_size)