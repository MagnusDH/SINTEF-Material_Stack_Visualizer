import tkinter
from tkinter import messagebox, Frame, Label, Entry, StringVar, Scale, font
import customtkinter
import pyautogui
import pandas   #Excel-file reading
import openpyxl #Excel-file reading
import os
import json

class Material_stack_visualizer_app:
    def __init__(self):
        print("INIT()")

        #Create a dictionary to hold ALL the information about a material
        self.materials = {}

        #Read the given excel-file and populate the materials dictionary
        self.load_materials_from_excel(SETTINGS["EXCEL_FILE"])

        #Create a user interface
        self.user_interface_frame = self.create_user_interface()

        #Create canvas
        self.canvas = self.create_canvas()

        #Draw material stack
        self.draw_material_stack()

    """Reads the given excel-file and populates the self.materials dictionary with info about each material"""
    def load_materials_from_excel(self, excel_file):
        print("LOAD_MATERIALS_FROM_EXCEL()")
        
        try:
            #Read given excel file into Pandas dataframe
            excel_data = pandas.read_excel(excel_file)

            #Open excel-file to read background colors of each cell
            work_book = openpyxl.load_workbook(excel_file, data_only=True)
            fs = work_book.active

            #Loop through the rows in excel_file
            i = 2
            for column, row in excel_data.iterrows():
                #Check the background color of the cell
                background_color = fs.cell(column=2, row=i).fill.bgColor.index
                if(background_color == "FFFFFF00"):
                    status = "disabled"
                else:
                    status = "active"
                #Increment "i" to go to the next row
                i+=1

                #Create an "info" dictionary to contain all info from excel-file
                info = {
                    "name": row["Material"],
                    "layer": row["Layer"],
                    "thickness": row["Thickness"],
                    "unit": row["Unit"],
                    "indent": row["Indent"],
                    "color": row["Color"],
                    "status": status,
                    "rectangle_id": None,
                    "text_id": None,
                    "text_bbox_id" : None,
                    "line_id": None,
                    "entry_id": None,
                    "slider_id": None,
                    "indent_text_id": None,
                    "indent_arrow_id": None
                }

                #Put "info" dictionary into self.materials dictionary
                self.materials[row["Material"]] = info

        except Exception as error:
            messagebox.showerror("Error", "Could not load materials from Excel-file")
            window.destroy()

    """Creates a Frame with sliders, entries and buttons"""
    def create_user_interface(self):
        print("CREATE_USER_INTERFACE()")
        
        #Create Frame and place it
        user_interface_frame = customtkinter.CTkScrollableFrame(
            master=window, 
            width=SETTINGS["UI_FRAME_WIDTH"], 
            height=SETTINGS["UI_FRAME_HEIGHT"],
            fg_color=SETTINGS["UI_FRAME_BACKGROUND_COLOR"]
        )
        user_interface_frame.grid(
            row=0, 
            column=0, 
            padx=(0,5), 
            pady=(0,5),
            sticky="n"
        )

        #Used to avoid overlaping of widgets
        row_counter = 0

        #Create label to display material name
        material_label = customtkinter.CTkLabel(
            master=user_interface_frame, 
            text="Material", 
            fg_color=SETTINGS["UI_FRAME_BACKGROUND_COLOR"],
            text_color="#55b6ff",
            font=(SETTINGS["TEXT_FONT"], 20, "bold")
        )
        material_label.grid(
            row=row_counter,
            column=0,
            sticky="n",
            padx=(0,0),
            pady=(0,0)
        )

        #Create label to display slider functionality
        self.slider_label = customtkinter.CTkLabel(
            master=user_interface_frame, 
            text="Thickness", 
            fg_color=SETTINGS["UI_FRAME_BACKGROUND_COLOR"],
            text_color="#55b6ff",
            font=(SETTINGS["TEXT_FONT"], 20, "bold")
        )
        self.slider_label.grid(
            row=row_counter,
            column=2,
            sticky="n",
            padx=(0,0),
            pady=(0,0)
        )

        row_counter+=1
        #Create sliders, buttons etc for each material
        for material in dict(reversed(self.materials.items())):
            #Create label and place it
            label = tkinter.Label(
                user_interface_frame, 
                text=material, 
                bg=SETTINGS["UI_LABEL_BACKGROUND_COLOR"],
                fg=SETTINGS["UI_FRAME_TEXT_COLOR"]
            )
            label.grid(
                row=row_counter, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )

            #Create Entry, customize it and add it to dictionary
            entry = customtkinter.CTkEntry(
                master=user_interface_frame,
                textvariable=StringVar(value=str(self.materials[material]["thickness"])),
                fg_color = SETTINGS["UI_ENTRY_BACKGROUND_COLOR"],
                text_color="black",
                width=70,
                justify="center"
            )
            entry.grid(
                row=row_counter, 
                column=1,
                sticky="e",
                padx=(0,0),
                pady=(0,0)
            )
            entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))
            self.materials[material]["entry_id"] = entry

            #Create Slider, customize it and add it to dictionary
            slider = customtkinter.CTkSlider(
                master=user_interface_frame, 
                from_=SETTINGS["UI_SLIDER_RANGE_MIN"], 
                to=SETTINGS["UI_SLIDER_RANGE_MAX"],
                progress_color=self.materials[material]["color"],
                fg_color=SETTINGS["UI_SLIDER_LINE_COLOR"],
                button_hover_color=SETTINGS["UI_BUTTON_HOVER_COLOR"],
                command=lambda value, identifier=material:self.material_slider_updated(round(value), identifier)
            )
            slider.grid(
                row=row_counter, 
                column=2,
                sticky="e",
                padx=(0,0),
                pady=(0,0)
            )
            slider.set(self.materials[material]["thickness"])
            self.materials[material]["slider_id"] = slider 
            #Disable slider and Entry if specified by the excel-file
            if(self.materials[material]["status"] == "disabled"):
                self.materials[material]["slider_id"].configure(state="disabled") #Disable slider
                self.materials[material]["entry_id"].delete(0, tkinter.END)     #Disable Entry
                self.materials[material]["entry_id"].insert(0, "Disabled")      #Disable Entry
                self.materials[material]["entry_id"].configure(state="disabled")#Disable Entry
            self.materials[material]["slider_id"] = slider 

            #Increment row_counter
            row_counter+=1

        #Reset canvas button
        reset_canvas_button = customtkinter.CTkButton(
            master=window, 
            text="Reset canvas", 
            fg_color=SETTINGS["UI_BUTTON_FG_COLOR"], 
            hover_color=SETTINGS["UI_BUTTON_HOVER_COLOR"], 
            text_color=SETTINGS["UI_FRAME_TEXT_COLOR"],
            width=15,
            command=self.reset_canvas)
        reset_canvas_button.grid(
            row=1, 
            column=1, 
            sticky="nw", 
            padx=(0,0), 
            pady=(0,0)
        )

        #Reset values button
        reset_values_button = customtkinter.CTkButton(
            master=window,
            text="Reset values",
            fg_color=SETTINGS["UI_BUTTON_FG_COLOR"], 
            hover_color=SETTINGS["UI_BUTTON_HOVER_COLOR"], 
            text_color=SETTINGS["UI_FRAME_TEXT_COLOR"],
            width=15,
            command=self.reset_values
        )
        reset_values_button.grid(
            row=1, 
            column=0, 
            sticky="n", 
            padx=(0,0), 
            pady=(0,0)
        )

        #Export stack button
        export_stack_button = customtkinter.CTkButton(
            master=window,
            text="Export stack",
            fg_color=SETTINGS["UI_BUTTON_FG_COLOR"], 
            hover_color=SETTINGS["UI_BUTTON_HOVER_COLOR"], 
            text_color=SETTINGS["UI_FRAME_TEXT_COLOR"],
            width=15,
            command=self.export_stack_as_svg
        )
        export_stack_button.grid(
            row=1, 
            column=1, 
            sticky="n", 
            padx=(0,0), 
            pady=(0,0)
        )
        
        #Export layers button
        export_layers_button = customtkinter.CTkButton(
            master=window,
            text="Export layers",
            fg_color=SETTINGS["UI_BUTTON_FG_COLOR"], 
            hover_color=SETTINGS["UI_BUTTON_HOVER_COLOR"], 
            text_color=SETTINGS["UI_FRAME_TEXT_COLOR"],
            width=15,
            command=self.export_layers_as_svg
        )
        export_layers_button.grid(
            row=2, 
            column=1, 
            sticky="n", 
            padx=(0, 0), 
            pady=(0,0)
        )

        view_label = customtkinter.CTkLabel(
            master=window, 
            text="View", 
            fg_color=SETTINGS["PROGRAM_BACKGROUND_COLOR"],
            text_color="#55b6ff",
            font=(SETTINGS["TEXT_FONT"], 20)
        )
        view_label.grid(
            row=1,
            column=1,
            sticky="ne",
            padx=(0,5),
            pady=(0,0)
        )
        #Switch layout ComboBox
        self.option_menu = customtkinter.CTkOptionMenu(
            master=window, 
            values=["Stacked", "Realistic", "Stepped"],
            width=30,
            fg_color=SETTINGS["UI_BUTTON_FG_COLOR"], 
            button_hover_color=SETTINGS["UI_BUTTON_HOVER_COLOR"],
            command=self.switch_layout
        )
        self.option_menu.grid(
            row=2, 
            column=1, 
            sticky="ne", 
            padx=(0,0), 
            pady=(0,0)
        )
        
        return user_interface_frame
    
    """Returns a canvas created in the program window"""
    def create_canvas(self):
        print("CREATE_CANVAS()")
        
        #Create canvas and place it
        canvas = tkinter.Canvas(
            master=window, 
            height=SETTINGS["CANVAS_HEIGHT"], 
            width=SETTINGS["CANVAS_WIDTH"],
            bg=SETTINGS["CANVAS_BACKGROUND_COLOR"],
            highlightbackground="red", 
            highlightthickness=0,
            )
        canvas.grid(
            row=0, 
            column=1, 
            sticky="s", 
            padx=(0,0), 
            pady=(0,0)
        )

        #Set canvas_bbox coordniates for later use
        self.visible_canvas_bbox_x0 = 0
        self.visible_canvas_bbox_y0 = 0
        self.visible_canvas_bbox_x1 = canvas.winfo_reqwidth() - 1
        self.visible_canvas_bbox_y1 = canvas.winfo_reqheight() - 1
        self.canvas_height = self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0
        self.canvas_width = self.visible_canvas_bbox_x1 - self.visible_canvas_bbox_x0
        #This is just a usefull function to find the bbox of the canvas: self.canvas.coords(self.canvas.find_withtag("canvas_bounding_box_rectangle"))[2]

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline=SETTINGS["CANVAS_OUTLINE_COLOR"], width=1)

        #Listen to mouse: buttonpress, motion and zoom events
        canvas.bind("<ButtonPress-1>", lambda event, canvas=canvas: self.click_on_canvas(event, canvas))
        canvas.bind("<B1-Motion>", lambda event, canvas=canvas: self.canvas_drag(event, canvas))
        canvas.bind("<MouseWheel>", lambda event, canvas=canvas: self.canvas_zoom(event, canvas))

        return canvas

    """Updates the thickness value in self.materials with the slider value and updates corresponding entry-widget"""
    def material_slider_updated(self, value, identifier): 
        print("MATERIAL_SLIDER_UPDATED()")
        
        #Update different values in self.materials based on option value
        match self.option_menu.get():
            case "Stacked"|"Realistic":
                #Update the thickness value in self.materials
                self.materials[identifier]["thickness"] = value

                #Update the entry corresponding to key
                self.materials[identifier]["entry_id"].delete(0, tkinter.END)
                self.materials[identifier]["entry_id"].insert(0, value)
            
            case "Stepped":
                #Update the "indent" value in self.materials
                self.materials[identifier]["indent"] = value

                #Update the entry corresponding to key
                self.materials[identifier]["entry_id"].delete(0, tkinter.END)
                self.materials[identifier]["entry_id"].insert(0, value)

        #Redraw material stack
        self.draw_material_stack()

    """Updates the thickness value in self.materials with the entered value and updates corresponding slider-widget"""
    def material_entry_updated(self, entry):
        print("MATERIAL_ENTRY_UPDATED()")

        #Update different values in self.materials based on option value
        match self.option_menu.get():
            case "Stacked"|"Realistic":
                #Find material that corresponds to "entry"
                for material in self.materials:
                    if(self.materials[material]["entry_id"] == entry):
                        #Find entered value
                        entered_value = int(entry.get())
                        #Update the thickness value in self.materials
                        self.materials[material]["thickness"] = entered_value

                        #Update the slider corresponding to the key
                        self.materials[material]["slider_id"].set(entered_value)

            case "Stepped":
                #Find material that corresponds to "entry"
                for material in self.materials:
                    if(self.materials[material]["entry_id"] == entry):
                        #Find entered value
                        entered_value = int(entry.get())
                        #Update the thickness value in self.materials
                        self.materials[material]["indent"] = entered_value

                        #Update the slider corresponding to the key
                        self.materials[material]["slider_id"].set(entered_value)
        
        
        #Redraw material stack
        self.draw_material_stack()
    
    """Deletes the current canvas and creates a new one in its original place"""
    def reset_canvas(self, *args):
        print("RESET_CANVAS")

        #Delete canvas from program window
        self.canvas.destroy()

        #Create new canvas in its original position
        self.canvas = self.create_canvas()

        #Redraw material stack
        self.draw_material_stack()

    """Reads the excel file again and repopulated the "thickness" in self.materials. Updates sliders and entries with new values"""
    def reset_values(self):
        print("RESET_VALUES")

        match self.option_menu.get():
            case "Stacked" | "Realistic":
                #Reload initial thickness values from given excel file
                try:
                    #Read given excel file into Pandas dataframe
                    excel_data = pandas.read_excel(SETTINGS["EXCEL_FILE"])

                    #Loop through the rows in excel_file and populate "self.materials"
                    for index, row in excel_data.iterrows():
                        material_name = row["Material"]
                        material_thickness = row["Thickness"]
                        
                        #Populate material dictionary
                        self.materials[material_name]["thickness"] = material_thickness
                        
                        #Update sliders and Entries
                        self.materials[material_name]["slider_id"].set(material_thickness)
                        self.materials[material_name]["entry_id"].delete(0, tkinter.END)
                        self.materials[material_name]["entry_id"].insert(0, material_thickness)
                    
                    # #Reset text_size
                    # self.current_text_size = self.original_text_size
                    
                    #Draw rectangle stack with original values
                    self.draw_material_stack()
        
                #Handle errors
                except Exception as error:
                    messagebox.showerror("Error", "Could not reset 'thickness' values\nMay be a issue with reading from excel-file")
        
            case "Stepped":
                #Reload initial thickness values from given excel file
                try:
                    #Read given excel file into Pandas dataframe
                    excel_data = pandas.read_excel(SETTINGS["EXCEL_FILE"])

                    #Loop through the rows in excel_file and populate "self.materials"
                    for index, row in excel_data.iterrows():
                        material_name = row["Material"]
                        material_indent = row["Indent"]
                        
                        #Populate material dictionary
                        self.materials[material_name]["indent"] = material_indent
                        
                        #Update sliders and Entries
                        self.materials[material_name]["slider_id"].set(material_indent)
                        self.materials[material_name]["entry_id"].delete(0, tkinter.END)
                        self.materials[material_name]["entry_id"].insert(0, material_indent)
                    
                    # #Reset text_size
                    # self.current_text_size = self.original_text_size
                    
                    #Draw rectangle stack with original values
                    self.draw_material_stack()
        
                #Handle errors
                except Exception as error:
                    messagebox.showerror("Error", "Could not reset 'thickness' values\nMay be a issue with reading from excel-file")

    """Remembers the initial mouse click-position on the canvas"""
    def click_on_canvas(self, event, canvas):
        print("CLICK_ON_CANVAS()")
        
        canvas.scan_mark(event.x, event.y)
    
    """Moves the position of the canvas"""
    def canvas_drag(self, event, canvas):
        print("CANVAS_DRAG()")
        
        canvas.scan_dragto(event.x, event.y, gain=1)

    """Scales all the elements on the canvas up or down"""
    def canvas_zoom(self, event, canvas):
        print("CANVAS_ZOOM()")
        zoom_factor = 1.05

        #Zoom in: Scale all items on the canvas around the mouse cursor
        if event.delta > 0:
            canvas.scale("all", event.x, event.y, zoom_factor, zoom_factor)

        #Zoom out: Scale all items on the canvas around the mouse cursor
        elif event.delta < 0:
            canvas.scale("all", event.x, event.y, 1.0/zoom_factor, 1.0/zoom_factor)

        #Redraw text on stack
        match self.option_menu.get():
            case "Stacked":
                self.write_text_on_stack()
            case "Realistic":
                self.write_text_on_stack()
            case "Stepped":
                self.write_text_on_stack()
                self.write_indent_on_stepped_stack()
    
    """Scales the material stack according to the program window"""
    def program_window_resized(self, event):
        #Only do something if the window size is changed. (The <configure> method calls this function everytime something about the program window is changed)
        if(event.width != SETTINGS["PROGRAM_WINDOW_WIDTH"] or event.height != SETTINGS["PROGRAM_WINDOW_HEIGHT"]):
            print("WINDOW RESIZED")
        
            #Set the new width of the canvas
            self.canvas.config(width=window.winfo_width() - self.user_interface_frame.winfo_reqwidth() - SETTINGS["CANVAS_PROGRAM_BORDER_WIDTH"])

            #Update the variables that track the actual visible parts of the canvas
            self.visible_canvas_bbox_x1 = self.canvas.winfo_reqwidth() - 1
            self.visible_canvas_bbox_y1 = self.canvas.winfo_reqheight() - 1

            #Redraw the material stack
            self.draw_material_stack()

    """ -Changes the Label explaining what is being modified by sliders and entries in the UI-frame
        -Changes the values for sliders and entries"""
    def switch_layout(self, *event):
        print("SWITCH_LAYOUT()")

        #Switch UI layout based on option value
        match self.option_menu.get():
            case "Stacked":
                #Change the label in user_interface_frame
                self.slider_label.configure(text="Thickness")

                #Set all material entry and slider values to "thickness" value, except the entries that are "disabled"
                for material in self.materials:
                    self.materials[material]["slider_id"].set(self.materials[material]["thickness"])
                    
                    if(self.materials[material]["status"] != "disabled"):
                        self.materials[material]["entry_id"].configure(textvariable=StringVar(value=str(self.materials[material]["thickness"])))
                
                #Draw material stack                
                self.draw_material_stack_stacked()

            case "Realistic":
                #Change the label in user_interface_frame
                self.slider_label.configure(text="Thickness")

                #Set all material entry and slider values to "thickness" value, except the entries that are "disabled"
                for material in self.materials:
                    self.materials[material]["slider_id"].set(self.materials[material]["thickness"])
                    
                    if(self.materials[material]["status"] != "disabled"):
                        self.materials[material]["entry_id"].configure(textvariable=StringVar(value=str(self.materials[material]["thickness"])))

                #Draw the material stack
                self.draw_material_stack_realistic()
            
            case "Stepped":
                #Change the label in UI frame
                self.slider_label.configure(text="Indent")

                #Set all material entry and slider values to "indent" value, except the entries that are "disabled"
                for material in self.materials:
                    self.materials[material]["slider_id"].set(self.materials[material]["indent"])

                    if(self.materials[material]["status"] != "disabled"):
                        self.materials[material]["entry_id"].configure(textvariable=StringVar(value=str(self.materials[material]["indent"])))
                    
                #Draw the material stack
                self.draw_material_stack_stepped()

    """Draws the material stack based on the value in the option box"""
    def draw_material_stack(self, *event):
        print("DRAW MATERIAL STACK()")
                
        #Draw stack based on option
        match self.option_menu.get():
            case "Stacked":
                self.draw_material_stack_stacked()
            case "Realistic":
                self.draw_material_stack_realistic()
            case "Stepped":
                self.draw_material_stack_stepped()

    """Draws the rectangle stack where "substrate" is 1/10 of the canvas no matter what"""
    def draw_material_stack_stacked(self):       
        print("DRAW_MATERIAL_STACK_STACKED()")
        
        #Clear all existing elements on canvas
        self.canvas.delete("all")

        #Draw bounding box around canvas
        self.canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline=SETTINGS["CANVAS_OUTLINE_COLOR"], tags="canvas_bounding_box_rectangle")

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
        rectangle_x1 = self.visible_canvas_bbox_x1 - SETTINGS["CANVAS_STACK_TEXT_INDENT"]
        rectangle_y1 = None #Calculated later
        
        #Draw rectangles on canvas
        for material in self.materials:
            #"substrate" will be drawn on the bottom 1/10 of the canvas
            if(material == "substrate"):
                # continue    #Skip "substrate"
                created_rectangle = self.canvas.create_rectangle(
                    # self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y1, rectangle_x1, canvas_height, 
                    self.visible_canvas_bbox_x0, round(self.canvas_height*0.9), rectangle_x1, self.visible_canvas_bbox_y1, 
                    fill=self.materials["substrate"]["color"], 
                    outline=SETTINGS["CANVAS_RECTANGLE_OUTLINE_COLOR"],
                    tags="material_rectangle"
                )
                #Add rectangle_id to its place in self.materials
                self.materials["substrate"]["rectangle_id"] = created_rectangle
            
            else:
                #find how many percent the current rectangle's height is of the total sum of materials
                rectangle_height = int(self.materials[material]["thickness"])
                rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
                #Convert rectangle percentage to pixels
                rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

                #draw rectangle from top of canvas to its number of pixles in height
                rectangle_y1 = rectangle_y0 - rectangle_height_pixels
                created_rectangle = self.canvas.create_rectangle(
                    rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                    fill=self.materials[material]["color"],
                    outline=SETTINGS["CANVAS_RECTANGLE_OUTLINE_COLOR"], 
                    tags="material_rectangle"
                )

                #Add rectangle_id to its place in self.materials
                self.materials[material]["rectangle_id"] = created_rectangle

                #Add rectangle height to prevent overlaping
                rectangle_y0 -= rectangle_height_pixels
            
        #Write text on the stack
        self.write_text_on_stack()
        
    """Draws a realistic version of the rectangle stack"""
    def draw_material_stack_realistic(self):
        print("DRAW_MATERIAL_STACK_REALISTIC()")
        
        #Clear all existing elements on canvas
        self.canvas.delete("all")

        #Draw bounding box around canvas
        self.canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline=SETTINGS["CANVAS_OUTLINE_COLOR"], tags="canvas_bounding_box_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in self.materials:
            rectangle_height = int(self.materials[material]["thickness"])
            sum_of_all_materials += rectangle_height
        
        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y1
        rectangle_x1 = self.visible_canvas_bbox_x1 - SETTINGS["CANVAS_STACK_TEXT_INDENT"]
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
            created_rectangle = self.canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material]["color"], tags="material_rectangle")

            #Add rectangle_id to its place in self.materials
            self.materials[material]["rectangle_id"] = created_rectangle

            #Add rectangle height to prevent overlaping
            rectangle_y0 -= rectangle_height_pixels
        
        #Write text on the stack
        self.write_text_on_stack()
    
    """Draws a stepped rectangle stack where "indent" decide the width of each rectangle"""
    def draw_material_stack_stepped(self):
        print("DRAW_MATERIAL_STACK_STEPPED()")

        #Clear all existing elements on canvas
        self.canvas.delete("all")

        #Draw bounding box around canvas
        self.canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline=SETTINGS["CANVAS_OUTLINE_COLOR"], tags="canvas_bounding_box_rectangle")
        
        #Find the total height of all materials combined and the thickest material
        sum_of_all_materials = 0
        biggest_material = 0
        for material in self.materials:
            if(material=="substrate"):
                continue    #Skip substrate
            sum_of_all_materials += int(self.materials[material]["thickness"])
            if(biggest_material < int(self.materials[material]["thickness"])):
                biggest_material = int(self.materials[material]["thickness"])
        
        #Find how many nanometers 1 pixel should represent
        nanometers_per_pixel = sum_of_all_materials/round(self.canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates (from bottom left corner)
        rectangle_x0 = self.visible_canvas_bbox_x0 + SETTINGS["STEPPED_CANVAS_INDENT_LEFT_SIDE"]
        rectangle_y0 = round(self.canvas_height*0.9) + SETTINGS["STEPPED_CANVAS_INDENT_TOP"]
        rectangle_x1 = self.visible_canvas_bbox_x1 - SETTINGS["STEPPED_CANVAS_INDENT_RIGHT_SIDE"]
        rectangle_y1 = None #calculated later
        previous_rectangle_x1 = self.visible_canvas_bbox_x1

        #Draw rectangles on canvas
        for material in self.materials:
            #Draw "substrate" on the bottom 1/10 of the canvas
            if(material == "substrate"):
                #Find how many pixels is needed to represent the indent of the current material
                indent_width_pixels = int(self.materials[material]["indent"])/nanometers_per_pixel

                #Set the width of the rectangle
                rectangle_x1 = rectangle_x1-indent_width_pixels

                created_rectangle = self.canvas.create_rectangle(
                    rectangle_x0, rectangle_y0, rectangle_x1, self.visible_canvas_bbox_y1,
                    fill=self.materials[material]["color"], 
                    tags="material_rectangle"
                )
                self.materials["substrate"]["rectangle_id"] = created_rectangle

            #Draw rectangles except "substrate"
            else:
                #Find how many pixels is needed to represent the height of the current material
                rectangle_height_pixels = int(self.materials[material]["thickness"])/nanometers_per_pixel
                
                #Set the y1 coordinate of the rectangle
                rectangle_y1 = rectangle_y0 - rectangle_height_pixels

                #Find how many pixels is needed to represent the indent of the current material
                indent_width_pixels = int(self.materials[material]["indent"])/nanometers_per_pixel

                #Set the indent width for the current rectangle
                rectangle_x1 =  rectangle_x1 - indent_width_pixels  

                #Create rectangle
                created_rectangle = self.canvas.create_rectangle(
                    rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                    fill=self.materials[material]["color"], 
                    outline=SETTINGS["CANVAS_RECTANGLE_OUTLINE_COLOR"],
                    tags="material_rectangle"
                )
                #Add rectangle_id to its place in self.materials
                self.materials[material]["rectangle_id"] = created_rectangle

                #Add rectangle height to prevent overlaping
                rectangle_y0 -= rectangle_height_pixels

        #Write text and indent on stack
        self.write_text_on_stack()
        self.write_indent_on_stepped_stack()
    
    """Writes text on rectangles in the material stack"""
    def write_text_on_stack(self):
        print("WRITE_TEXT_ON_STACK()")

        #Delete all texts from canvas and dictionary
        for material in self.materials:
            self.canvas.delete(self.materials[material]["text_id"])
            self.canvas.delete(self.materials[material]["text_bbox_id"])
            self.canvas.delete(self.materials[material]["line_id"])
            self.canvas.delete(self.materials[material]["indent_text_id"])
            self.canvas.delete(self.materials[material]["indent_arrow_id"])

            self.materials[material]["text_id"] = None
            self.materials[material]["text_bbox_id"] = None
            self.materials[material]["line_id"] = None
            self.materials[material]["indent_text_id"] = None
            self.materials[material]["indent_arrow_id"] = None
       
        #Write different texts based on current stack option
        match self.option_menu.get():
            case "Stacked" | "Realistic":
                #Find out the height of a potential text's bounding box
                text_font = font.Font(family=SETTINGS["TEXT_FONT"], size=SETTINGS["TEXT_SIZE"])
                text_height = text_font.metrics()['linespace']
                previous_material = None

                #Loop through all the materials:
                for material in dict(reversed(self.materials.items())):
                    #Only create text, bounding boxes and lines if the "thickness" is not zero
                    if(self.materials[material]["thickness"] > 0):
                        #Find coordinates and height of current material_rectangle
                        current_rectangle_x0, current_rectangle_y0, current_rectangle_x1, current_rectangle_y1 = self.canvas.bbox(self.materials[material]["rectangle_id"])
                        current_rectangle_height = current_rectangle_y1-current_rectangle_y0
                        current_rectangle_middle_x = (current_rectangle_x0 + current_rectangle_x1)/2
                        current_rectangle_middle_y = (current_rectangle_y0 + current_rectangle_y1)/2

                        #Text is drawn inside rectangle
                        if(text_height < current_rectangle_height):
                            created_text = self.canvas.create_text(
                                current_rectangle_middle_x, current_rectangle_middle_y, 
                                text=f"{material} - {self.materials[material]['thickness']}nm", 
                                fill=SETTINGS["TEXT_COLOR"], 
                                font=(SETTINGS["TEXT_FONT"], SETTINGS["TEXT_SIZE"]), 
                                # anchor="center", 
                                tags="Material_label"
                            )

                            #If text is outside leftside of canvas, place it on the left canvas side
                            if(self.canvas.bbox(created_text)[0] < self.visible_canvas_bbox_x0):
                                overlap = self.visible_canvas_bbox_x0 - self.canvas.bbox(created_text)[0] 
                                self.canvas.coords(created_text, current_rectangle_middle_x+overlap, current_rectangle_middle_y)
                            
                            #If text is outside rightside of canvas, place it on the right canvas side
                            if(self.canvas.bbox(created_text)[2] > self.visible_canvas_bbox_x1):
                                overlap = self.canvas.bbox(created_text)[2] - self.visible_canvas_bbox_x1 
                                self.canvas.coords(created_text, current_rectangle_middle_x-overlap, current_rectangle_middle_y)
                            
                            #Add text element to dictionary
                            self.materials[material]["text_id"] = created_text

                        #Text is drawn outside rectangle
                        else:
                            #Create text, bbox and line and place them
                            created_text = self.canvas.create_text(
                                self.visible_canvas_bbox_x1, current_rectangle_middle_y, 
                                text=f"{material} - {self.materials[material]['thickness']}nm", 
                                fill=SETTINGS["TEXT_COLOR"], 
                                font=(SETTINGS["TEXT_FONT"], SETTINGS["TEXT_SIZE"]), 
                                tags="Material_label"
                            )
                            created_text_bbox = self.canvas.create_rectangle(
                                self.canvas.bbox(created_text), 
                                outline=SETTINGS["TEXT_COLOR"], 
                                tags="text_bbox"
                            )
                            #Get coordinates of text bounding box
                            current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1  = self.canvas.bbox(created_text)
                            current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2

                            created_arrow_line = self.canvas.create_line(
                                (current_text_bbox_x0, current_text_bbox_middle_y), (current_rectangle_x1, current_rectangle_middle_y), 
                                arrow=tkinter.LAST, 
                                fill=SETTINGS["TEXT_COLOR"],
                                tags="arrow_line"
                            )

                            #Check for adjustments of text
                            #if(text top overlaps with canvas top):
                            if(current_text_bbox_y0 < self.visible_canvas_bbox_y0):
                                #Find how much is overlapping
                                overlap = self.visible_canvas_bbox_y0 - current_text_bbox_y0
                                #Move text and bbox down
                                self.canvas.move(created_text, 0, overlap)
                                self.canvas.move(created_text_bbox, 0, overlap)
                                #Find new coordinates of text bounding box
                                current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.canvas.bbox(created_text_bbox)
                                current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                                #Move the arrow line
                                self.canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)
                            
                            #if(Text bottom overlaps with canvas bottom):
                            if(current_text_bbox_y1 > self.visible_canvas_bbox_y1):
                                #Find how much is overlapping
                                overlap = current_text_bbox_y1 - self.visible_canvas_bbox_y1
                                #Move text and bounding box up
                                self.canvas.move(created_text, 0, -overlap)
                                self.canvas.move(created_text_bbox, 0, -overlap)
                                
                                #Find coordinates of new text bounding box
                                current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.canvas.bbox(created_text_bbox)
                                current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                                #Move the arrow line
                                self.canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)
                            
                            #if(text right side overlaps with canvas right side)
                            if(current_text_bbox_x1 > self.visible_canvas_bbox_x1):
                                #Find how much is overlapping
                                overlap = current_text_bbox_x1 - self.visible_canvas_bbox_x1
                                #Move text left
                                self.canvas.move(created_text, -overlap, 0)
                                self.canvas.move(created_text_bbox, -overlap, 0)
                                
                                #Find new coordinates of text bounding box
                                current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.canvas.bbox(created_text_bbox)
                                current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                                #Move the arrow line
                                self.canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)

                            #if(Text top overlaps with previous text bottom):
                            if(previous_material != None):
                                #If text, bounding box and lines has been created for this element
                                if(self.materials[previous_material]["text_id"] != None and self.materials[previous_material]["text_bbox_id"] != None and self.materials[previous_material]["line_id"] != None):
                                    #Find necessary coordinated for previous material
                                    previous_text_bbox_y1 = self.canvas.bbox(self.materials[previous_material]["text_id"])[3]
                                    #if(Text top overlaps with previous text bottom):
                                    if(current_text_bbox_y0 < previous_text_bbox_y1):
                                        #Find how much is overlapping
                                        overlap = previous_text_bbox_y1 - current_text_bbox_y0
                                        #Move text down
                                        self.canvas.move(created_text, 0, overlap)
                                        self.canvas.move(created_text_bbox, 0, overlap)
                                        #Find new coordinates of text bounding box
                                        current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.canvas.bbox(created_text_bbox)
                                        current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                                        #Move the arrow line
                                        self.canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)

                            #Add created elements to dictionary
                            self.materials[material]["text_id"] = created_text
                            self.materials[material]["text_bbox_id"] = created_text_bbox
                            self.materials[material]["line_id"] = created_arrow_line
                            
                        #Set previous material to the current one
                        previous_material = material

            case "Stepped":
                #Find out the height of a potential text's bounding box
                text_font = font.Font(family=SETTINGS["TEXT_FONT"], size=SETTINGS["TEXT_SIZE"])
                text_height = text_font.metrics()['linespace']
                previous_material = None

                #Loop through all the materials:
                for material in dict(reversed(self.materials.items())):
                    #Only create text, bounding boxes and lines if the "thickness" is not zero
                    if(self.materials[material]["thickness"] > 0):
                        #Find coordinates and height of current material_rectangle
                        current_rectangle_x0, current_rectangle_y0, current_rectangle_x1, current_rectangle_y1 = self.canvas.bbox(self.materials[material]["rectangle_id"])
                        current_rectangle_height = current_rectangle_y1-current_rectangle_y0
                        current_rectangle_middle_x = (current_rectangle_x0 + current_rectangle_x1)/2
                        current_rectangle_middle_y = (current_rectangle_y0 + current_rectangle_y1)/2

                        #Text is drawn inside rectangle
                        if(text_height < current_rectangle_height):
                            created_text = self.canvas.create_text(
                                current_rectangle_middle_x, current_rectangle_middle_y, 
                                text=f"{material} - {self.materials[material]['thickness']}nm", 
                                fill=SETTINGS["TEXT_COLOR"], 
                                font=(SETTINGS["TEXT_FONT"], SETTINGS["TEXT_SIZE"]), 
                                # anchor="center", 
                                tags="Material_label"
                            )

                            #If text is outside leftside of canvas, place it on the left canvas side
                            if(self.canvas.bbox(created_text)[0] < self.visible_canvas_bbox_x0):
                                overlap = self.visible_canvas_bbox_x0 - self.canvas.bbox(created_text)[0] 
                                self.canvas.coords(created_text, current_rectangle_middle_x+overlap, current_rectangle_middle_y)
                            
                            #If text is outside rightside of canvas, place it on the right canvas side
                            if(self.canvas.bbox(created_text)[2] > self.visible_canvas_bbox_x1):
                                overlap = self.canvas.bbox(created_text)[2] - self.visible_canvas_bbox_x1 
                                self.canvas.coords(created_text, current_rectangle_middle_x-overlap, current_rectangle_middle_y)
                            
                            #Add text element to dictionary
                            self.materials[material]["text_id"] = created_text

                        #Text is drawn outside rectangle
                        else:
                            #Create text, bbox and line and place them
                            created_text = self.canvas.create_text(
                                self.visible_canvas_bbox_x0, current_rectangle_middle_y, 
                                text=f"{material} - {self.materials[material]['thickness']}nm", 
                                fill=SETTINGS["TEXT_COLOR"], 
                                font=(SETTINGS["TEXT_FONT"], SETTINGS["TEXT_SIZE"]), 
                                tags="Material_label"
                            )
                            created_text_bbox = self.canvas.create_rectangle(
                                self.canvas.bbox(created_text), 
                                outline=SETTINGS["TEXT_COLOR"], 
                                tags="text_bbox"
                            )
                            #Get coordinates of text bounding box
                            current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1  = self.canvas.bbox(created_text)
                            current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2

                            created_arrow_line = self.canvas.create_line(
                                (current_text_bbox_x1, current_text_bbox_middle_y), (current_rectangle_x0, current_rectangle_middle_y), 
                                arrow=tkinter.LAST, 
                                fill=SETTINGS["TEXT_COLOR"],
                                tags="arrow_line"
                            )

                            #Check for adjustments of text
                            #if(text top overlaps with canvas top):
                            if(current_text_bbox_y0 < self.visible_canvas_bbox_y0):
                                #Find how much is overlapping
                                overlap = self.visible_canvas_bbox_y0 - current_text_bbox_y0
                                #Move text and bbox down
                                self.canvas.move(created_text, 0, overlap)
                                self.canvas.move(created_text_bbox, 0, overlap)
                                #Find new coordinates of text bounding box
                                current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.canvas.bbox(created_text_bbox)
                                current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                                #Move the arrow line
                                self.canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)
                            
                            #if(Text bottom overlaps with canvas bottom):
                            if(current_text_bbox_y1 > self.visible_canvas_bbox_y1):
                                #Find how much is overlapping
                                overlap = current_text_bbox_y1 - self.visible_canvas_bbox_y1
                                #Move text and bounding box up
                                self.canvas.move(created_text, 0, -overlap)
                                self.canvas.move(created_text_bbox, 0, -overlap)
                                
                                #Find coordinates of new text bounding box
                                current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.canvas.bbox(created_text_bbox)
                                current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                                #Move the arrow line
                                self.canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)
                            
                            #if(text left side overlaps with canvas left side)
                            if(current_text_bbox_x0 < self.visible_canvas_bbox_x0):
                                #Find how much is overlapping
                                overlap = self.visible_canvas_bbox_x0 - current_text_bbox_x0
                                #Move text to right
                                self.canvas.move(created_text, overlap, 0)
                                self.canvas.move(created_text_bbox, overlap, 0)
                                
                                #Find new coordinates of text bounding box
                                current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.canvas.bbox(created_text_bbox)
                                current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                                #Move the arrow line
                                self.canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)

                            #if(Text top overlaps with previous text bottom):
                            if(previous_material != None):
                                #If text, bounding box and lines has been created for this element
                                if(self.materials[previous_material]["text_id"] != None and self.materials[previous_material]["text_bbox_id"] != None and self.materials[previous_material]["line_id"] != None):
                                    #Find necessary coordinated for previous material
                                    previous_text_bbox_y1 = self.canvas.bbox(self.materials[previous_material]["text_id"])[3]
                                    #if(Text top overlaps with previous text bottom):
                                    if(current_text_bbox_y0 < previous_text_bbox_y1):
                                        #Find how much is overlapping
                                        overlap = previous_text_bbox_y1 - current_text_bbox_y0
                                        #Move text down
                                        self.canvas.move(created_text, 0, overlap)
                                        self.canvas.move(created_text_bbox, 0, overlap)
                                        #Find new coordinates of text bounding box
                                        current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.canvas.bbox(created_text_bbox)
                                        current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                                        #Move the arrow line
                                        self.canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)

                            #Add created elements to dictionary
                            self.materials[material]["text_id"] = created_text
                            self.materials[material]["text_bbox_id"] = created_text_bbox
                            self.materials[material]["line_id"] = created_arrow_line
                            
                        # #Set previous material to the current one
                        previous_material = material

    """Writes the indent ranges on the stepped material stack"""
    def write_indent_on_stepped_stack(self):
        print("WRITE_INDENT_ON_STEPPED_STACK()")

        #Delete all indet texts and arrows from canvas and dictionary
        for material in self.materials:
            self.canvas.delete(self.materials[material]["indent_text_id"])
            self.canvas.delete(self.materials[material]["indent_arrow_id"])
            self.materials[material]["indent_text_id"] = None
            self.materials[material]["indent_arrow_id"] = None
       
        previous_material = None

        #Loop through all the materials:
        for material in self.materials:
            #Do not create indent or text on the first rectangle
            if(previous_material != None):
                #Only create text and lines if the "thickness" is not zero
                if(int(self.materials[material]["thickness"]) > 0):
                    #Only create texts and lines if the "indent" is not zero
                    if(int(self.materials[material]["indent"]) > 0):
                        #Find usefull coordinates of current material_rectangle
                        current_rectangle_x1 = self.canvas.bbox(self.materials[material]["rectangle_id"])[2]
                        current_rectangle_y1 = self.canvas.bbox(self.materials[material]["rectangle_id"])[3]
        
                        #Find x1 coordinate of previous rectangle
                        previous_rectangle_x1 = self.canvas.bbox(self.materials[previous_material]["rectangle_id"])[2]
        
                        #Create a two sided arrow line between the differense of the two rectangles
                        created_indent_line = self.canvas.create_line(
                            current_rectangle_x1, current_rectangle_y1-5, previous_rectangle_x1, current_rectangle_y1-5, 
                            fill=SETTINGS["TEXT_COLOR"],
                            arrow=tkinter.BOTH
                        )

                        #Write indent number over line
                        indent_number = int(self.materials[material]["indent"])
                        created_indent_text = self.canvas.create_text(
                            (current_rectangle_x1+previous_rectangle_x1)/2, current_rectangle_y1-15,
                            text=f"{indent_number}nm", 
                            fill=SETTINGS["TEXT_COLOR"], 
                            font=(SETTINGS["TEXT_FONT"], SETTINGS["TEXT_SIZE"]), 
                        )
        
                        #if indent number overlaps with the rectangle_x1, then move it to the right
                        if(self.canvas.bbox(created_indent_text)[0] < current_rectangle_x1):
                            overlap = current_rectangle_x1 - self.canvas.bbox(created_indent_text)[0]
                            self.canvas.move(created_indent_text, overlap, 0)
                        
                        #Add created elements to dictionary
                        self.materials[material]["indent_text_id"] = created_indent_text
                        self.materials[material]["indent_arrow_id"] = created_indent_line

            #Set the "previous material" for use in the next loop
            previous_material = material
        
    """Exports the stack without material names as SVG file"""
    def export_stack_as_svg(self):
        print("EXPORT_STACK_AS_SVG")
        #Define the name of the svg file
        filename = "stack.svg"

        #Specify a folder where the SVG-file should be saved
        folder_path = "svg_exports"

        #Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #Create the file path by joining the folder path and the filename
        file_path = os.path.join(folder_path, filename)

        #Open the file for writing
        with open(file_path, 'w') as f:
            #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

            #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
            f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(window.winfo_reqwidth(), window.winfo_reqheight()))

            #Go through every rectangle found on canvas
            for material in self.materials:
                #Find the coordinates of the rectangle
                rect_x0, rect_y0, rect_x1, rect_y1 = self.canvas.coords(self.materials[material]["rectangle_id"])
                #Construct an SVG <rect> element for the rectangle
                svg_rect_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, self.materials[material]["color"])
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
    
    """Exports every layer of the stack with text and arrows as SVG-file"""
    def export_layers_as_svg(self):
        print("EXPORT_LAYERS_AS_SVG")

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
                f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(window.winfo_reqwidth(), window.winfo_reqheight()))

                #Write the previous created elements to the current file
                if(len(previously_created_elements) != 0):
                    for element in previously_created_elements:
                        f.write(element)

                #Create SVG-element of material rectangle
                if(self.materials[material]["rectangle_id"] is not None):
                    rect_x0, rect_y0, rect_x1, rect_y1 = self.canvas.coords(self.materials[material]["rectangle_id"])

                    svg_rectangle_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, self.materials[material]["color"])
                    f.write(svg_rectangle_element)
                    previously_created_elements.append(svg_rectangle_element)

                    #Create SVG-element for the rectangle bounding box and write it to file
                    svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, SETTINGS["CANVAS_RECTANGLE_OUTLINE_COLOR"])
                    f.write(svg_bbox_element)
                    previously_created_elements.append(svg_bbox_element)

                #Create SVG-element for material text
                if(self.materials[material]["text_id"] is not None):
                    text_x0, text_y0 = self.canvas.coords(self.materials[material]["text_id"])
                    text_content = self.canvas.itemcget(self.materials[material]["text_id"], 'text')
                    svg_text_element = '<text x="{}" y="{}" fill="{}" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(text_x0, text_y0, SETTINGS["TEXT_COLOR"], SETTINGS["SVG_TEXT_SIZE"], text_content)
                    f.write(svg_text_element)
                    previously_created_elements.append(svg_text_element)

                #Create SVG-element for text bounding box
                if(self.materials[material]["text_bbox_id"] is not None):
                    bbox_x0, bbox_y0, bbox_x1, bbox_y1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                    svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black"/>\n'.format(bbox_x0, bbox_y0, bbox_x1-bbox_x0, bbox_y1-bbox_y0, SETTINGS["TEXT_COLOR"])
                        
                    #Write the SVG representation of the bounding box to the file
                    f.write(svg_bbox_element)
                    previously_created_elements.append(svg_bbox_element)

                #Create SVG-element for arrow line pointing from box to rectangle
                if(self.materials[material]["line_id"] is not None):
                    #Line must be drawn from the right side of stack to left side of text
                    if(self.option_menu.get() == "Stacked" or self.option_menu.get() == "Realistic"):
                        line_coords = self.canvas.coords(self.materials[material]["line_id"])
                        #Construct an SVG <line> element for arrows
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                        svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" marker-end="url(#arrow-end)" />\n'.format(bbox_x0, line_coords[1], line_coords[2]+7, line_coords[3], SETTINGS["TEXT_COLOR"])

                        #Add arrowhead on the left side of the line
                        svg_line_element += (
                        '<defs>\n'
                        '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="180">\n'
                        '        <path d="M0,0 L0,6 L9,3 z" fill="black" />\n'
                        '    </marker>\n'
                        '</defs>\n'
                    )

                    # Line must be drawn from the left side of stack to right side of text
                    elif(self.option_menu.get() == "Stepped"):
                        line_x0, line_y0, line_x1, line_y1 = self.canvas.coords(self.materials[material]["line_id"])
                        #Construct an SVG <line> element for arrows
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = self.canvas.bbox(self.materials[material]["text_bbox_id"])
                        svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" marker-end="url(#arrow-end)" />\n'.format(bbox_x1, line_y0, line_x1-7, line_y1, SETTINGS["TEXT_COLOR"])
                        
                        #Add arrowhead on right side of the line
                        svg_line_element += (
                            '<defs>\n'
                            '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="180">\n'
                            '        <path d="M0,3 L9,0 L9,6 z" fill="black" />\n'
                            '    </marker>\n'
                            '</defs>\n'
                        )
                    #Write the SVG representation of the arrow to the file
                    f.write(svg_line_element)
                    previously_created_elements.append(svg_line_element)

                #Create SVG-element for indent_text
                if(self.materials[material]["indent_text_id"] is not None):
                    indent_text_x0, indent_text_y0 = self.canvas.coords(self.materials[material]["indent_text_id"])
                    indent_text_content = self.canvas.itemcget(self.materials[material]["indent_text_id"], 'text')
                    svg_indent_text_element = '<text x="{}" y="{}" fill="black" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(indent_text_x0, indent_text_y0, SETTINGS["SVG_TEXT_SIZE"], indent_text_content)
                        
                    f.write(svg_indent_text_element)
                    previously_created_elements.append(svg_indent_text_element)

                #Create SVG-element for indent_arrow_line
                if(self.materials[material]["indent_arrow_id"] is not None):
                    indent_line_x0, indent_line_y0, indent_line_x1, indent_line_y1 = self.canvas.coords(self.materials[material]["indent_arrow_id"])
                    #Construct an SVG <line> element for arrows
                    svg_indent_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />\n'.format(indent_line_x0+8, indent_line_y0, indent_line_x1-10, indent_line_y1)
                    
                    #Add arrowheads on both sides of the line
                    svg_indent_line_element += (
                        '<defs>\n'
                        '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="0">\n'
                        '        <path d="M0,0 L0,6 L9,3 z" fill="black" />\n'
                        '    </marker>\n'
                        '    <marker id="arrow-start" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="0">\n'
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

#Main starting point of program
if __name__ == "__main__":

    #Create a host tkinter program window
    window = tkinter.Tk()

    #Load settings from json-file
    with open('settings.json', 'r') as file:
            SETTINGS = json.load(file)

    #Create instance of Layer_stack_vizualiser class and run it
    material_stack_visualizer_app = Material_stack_visualizer_app()

    #Set program window title, dimensions and color
    window.title(SETTINGS["PROGRAM_TITLE"])
    window.geometry(f"{SETTINGS['PROGRAM_WINDOW_WIDTH']}x{SETTINGS['PROGRAM_WINDOW_HEIGHT']}")
    window.configure(bg=SETTINGS["PROGRAM_BACKGROUND_COLOR"])

    #Create keyboard shortcuts for program window
    window.bind("<Escape>", lambda event: window.destroy())

    #Resets the canvas position if "r" is pressed
    window.bind('<KeyPress-r>', material_stack_visualizer_app.reset_canvas)

    #Checks if the program window is being resized
    window.bind("<Configure>", lambda event: material_stack_visualizer_app.program_window_resized(event))
    
    #Start the main loop of the program
    window.mainloop()