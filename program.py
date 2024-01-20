import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL, Frame, Entry, StringVar, Label, Button, messagebox, font
from PIL import ImageGrab, Image
import pandas as pd
import pygetwindow
import pyautogui
import os

"""
-Ta en titt på hvorfor jeg har lagt til canvas_width og height i starten, fordi disse er unødvendig i starten

-Krympt alt på programmet slik at det passer i programvinduet
"""

class App:
    def __init__(self, window):
        
        #SETTINGS
        self.app_title = "Layer-stack visualizer"
        self.window_width = 800                     #Start width of app window
        self.window_height = 900                    #Start height of app window
        self.canvas_width = 600                     #Width of the canvas where things are drawn
        self.canvas_height = 600                    #Height of the canvas where things are drawn
        self.material_min_thickness = 1             #Minimum thickness of materials
        self.material_max_thickness = 6000          #Maximum thickness of materials
        self.excel_file = "Materials.xlsx"          #Excel-file to load materials from
        self.zoom_factor = 1.05                     #How fast you can zoom in and out
        self.text_size = 10

        #Dictionary for all materials. KEY: "material_name" ---VALUES: list of [thickness, color]
        self.materials = {}

        #A dictionary containing data for each layer on the canvas. Key is the layer number, value is a list[rectangle_id, text_id, text_box, line_id]
        self.canvas_layer_data = {}

        self.initial_canvas_state = {}

        #Necessary to draw the rectangles correctly on the canvas. The padding values are added manually in the code
        self.total_padding_x = 0
        self.total_padding_y = 0
         
    """Calls all functions"""
    def run_application(self):        
        #Main window for application
        self.window = window
        self.window.title(self.app_title)
        self.window.geometry(f"{self.window_width}x{self.window_height}")

        #Read the given excel-file and populate self.materials with: material_name, thickness and color
        self.load_materials_from_excel(self.excel_file)

        #Create color boxes, sliders and input boxes for each material
        self.create_user_interface()

        #Create canvas to draw everythig on
        self.canvas = Canvas(self.window, width=self.canvas_width, height=self.canvas_height)   
        self.canvas.grid(row=0, column=1, sticky="n")

        #Listen to mouse buttonpress, motion and zoom events
        self.canvas.bind("<ButtonPress-1>", lambda event, canvas=self.canvas: self.click_on_canvas(event, self.canvas))
        self.canvas.bind("<B1-Motion>", lambda event, canvas=self.canvas: self.canvas_drag(event, self.canvas))
        self.canvas.bind("<MouseWheel>", lambda event, canvas=self.canvas: self.canvas_zoom(event, self.canvas))

        #Draw the material stack
        self.draw_rectangle_stack_filled(self.canvas)
    
    """Creates sliders, input and color boxes based on the number of materials in self.materials"""
    def create_user_interface(self):
        #Create frame within the main window to contain sliders, color&input widgets
        self.slider_frame = Frame(self.window)
        self.slider_frame.grid(row=0, column=0, sticky='n')

        #Max material thickness entry box
        max_thickness_label = Label(self.slider_frame, text="Scaling:", font="bold")                                                          #Creation of label in the slider frame
        max_thickness_label.grid(row=0, column=0) 
        max_thickness_variable = StringVar(value=str(self.material_max_thickness))
        max_thickness_entry = Entry(self.slider_frame, textvariable=max_thickness_variable, justify=tk.CENTER, width=10)
        max_thickness_entry.grid(row=0, column=1)                                                                     #Entry box placement
        max_thickness_entry.bind("<Return>", lambda event, e=max_thickness_entry: self.update_max_thickness_entry(event, e))                #Listens to updates in the entry/input box

        #Slider for adjusting material_max_thickness
        self.max_thickness_slider = Scale(self.slider_frame, from_=self.material_min_thickness, to=self.material_max_thickness, orient=HORIZONTAL, command=self.update_max_thickness_slider)
        self.max_thickness_slider.grid(row=0, column=2)
        #Set slider to half the max_thickness
        self.max_thickness_slider.set(self.material_max_thickness/2)


        #Create color boxes, sliders, input boxes and labels
        row_counter = 1 #Row counter
        for material in self.materials:
            #Create sliders
            slider = Scale(self.slider_frame, from_=self.material_min_thickness, to=self.material_max_thickness,
                       orient=HORIZONTAL, label=material, command=lambda value, 
                       label=material: self.update_material_slider(value, label), background=self.materials[material][1])             #Creation of slider and listening to slider adjustments
            slider.grid(row=row_counter, column=0, pady=5, padx=5)                                                            #Slider placement
            slider.set(self.materials[material][0])                                                                 #Set the initial value of the slider
            self.total_padding_y += (5*2)  #Add padding for this widget (+10 for both sides of the widget)


            #Create input boxes
            height_var = StringVar(value=str(self.materials[material][0]))                                          
            entry = Entry(self.slider_frame, textvariable=height_var, width=6, justify=tk.CENTER)                                      #Creation of entry box in the slider frame
            entry.grid(row=row_counter, column=1, padx=5)                                                                     #Entry box placement
            entry.bind("<Return>", lambda event, s=slider, e=entry: self.update_material_entry(event, e, s))                #Listens to updates in the entry/input box
            
            #Create "nm" label next to slider
            nm_label = Label(self.slider_frame, text="nm", justify=tk.LEFT)                                                          #Creation of label in the slider frame
            nm_label.grid(row=row_counter, column=2)                                                                          #Label placement

            #Increment row-counter
            row_counter += 1

        #Add padding for the widgets (x-padding is only applied once compared to Y-padding, because the slider frame doesn't get wider for each widget)
        self.total_padding_x += (5*2)
        
        #Create button which calls "export_stack_as_svg" function
        self.export_layers_button = Button(self.slider_frame, text = "Export stack-svg", command=self.export_stack_as_svg)
        self.export_layers_button.grid(row=row_counter, column=0, padx=5)
        self.total_padding_x += (5 * 2)  #Add padding for this widget (+10 for both sides of the widget)

        #Create button which calls "export_all_as_jpg" function
        self.export_layers_button = Button(self.slider_frame, text = "Export layers-svg", command=self.export_layers_as_svg)
        self.export_layers_button.grid(row=row_counter, column=1, padx=5)
        self.total_padding_x += (5 * 2)  #Add padding for this widget (+10 for both sides of the widget)

        row_counter += 1

        #Reset canvas button
        self.reset_canvas_button = Button(self.slider_frame, text="Reset", command=self.reset_canvas)
        self.reset_canvas_button.grid(row=row_counter, column=0)

    """Draws lines around the canvas showing where things can be drawn"""
    def draw_canvas_boundaries(self, canvas):
        #Draw lines around canvas (top left x,y MUST be 2,2, some of the values must be manually adjusted to fit the window)
        x0 = 2
        y0 = 2
        x1 = canvas.winfo_reqwidth()-3
        y1 = canvas.winfo_reqheight()-3

        canvas.create_rectangle(x0, y0, x1, y1, outline='black', tags="canvas_bbox")

    def reset_canvas(self):
        #Reload initial values from Excel file
        self.load_materials_from_excel(self.excel_file)

        #Delete canvas from program window
        self.canvas.destroy()

        #Create new canvas
        self.canvas = Canvas(self.window, width=self.canvas_width, height=self.canvas_height)   
        self.canvas.grid(row=0, column=1, sticky="n")

        #Listen to mouse buttonpress, motion and zoom events
        self.canvas.bind("<ButtonPress-1>", lambda event, canvas=self.canvas: self.click_on_canvas(event, self.canvas))
        self.canvas.bind("<B1-Motion>", lambda event, canvas=self.canvas: self.canvas_drag(event, self.canvas))
        self.canvas.bind("<MouseWheel>", lambda event, canvas=self.canvas: self.canvas_zoom(event, self.canvas))

        # #Draw borders around new canvas
        self.draw_canvas_boundaries(self.canvas)

        #Redraw rectangle stack on canvas
        self.draw_rectangle_stack_filled(self.canvas) 

    """Remembers the initial mouse click-position on the canvas"""
    def click_on_canvas(self, event, canvas):
        # Remember the initial click position for dragging
        canvas.scan_mark(event.x, event.y)

    """Moves the position of the canvas"""
    def canvas_drag(self, event, canvas):
        # Drag the canvas to a new position
        canvas.scan_dragto(event.x, event.y, gain=1)

    """Scales all the elements on the canvas up or down"""
    def canvas_zoom(self, event, canvas):
        #Check if the mouse wheel is scrolled up or down
        if event.delta > 0:
            # Zoom in: Scale all items on the canvas around the mouse cursor
            canvas.scale("all", event.x, event.y, self.zoom_factor, self.zoom_factor)
        elif event.delta < 0:
            # Zoom out: Scale all items on the canvas around the mouse cursor
            canvas.scale("all", event.x, event.y, 1.0 / self.zoom_factor, 1.0 / self.zoom_factor)
        
    """Updates the Material_max_thickness variable and slider ranging values when the Max Thickness entry is updated"""
    def update_max_thickness_entry(self, event, entry_box):
        #Get the entered value
        entry_value = int(entry_box.get())

        #Set the new max thickness value
        self.material_max_thickness = entry_value

        #Set the max_thickness_slider to half of new value
        self.max_thickness_slider.set(self.material_max_thickness/2)

        #Update slider ranging values
        for element in self.slider_frame.winfo_children():
            if isinstance(element, tk.Scale):
                element.config(from_=self.material_min_thickness, to=self.material_max_thickness)

        #Redraw the rectangle stack according to the current max_thickness value
        self.draw_rectangle_stack_filled(self.canvas)

    def update_max_thickness_slider(self, slider_value):
            pass
            
            #Update material_max_thickness based on slider value
            # self.material_max_thickness = int(slider_value)

            #Update the entry box to reflect the slider's value
            # self.max_thickness_entry.delete(0, tk.END)
            # self.max_thickness_entry.insert(0, str(value))

            # # Update the maximum thickness for all material sliders
            # for slider in self.slider_widgets.values():
            #     slider.config(to=self.material_max_thickness)

            # # Redraw the rectangle stack with the updated max thickness
            # self.draw_rectangle_stack_filled()
    
    """
    -Is called if the slider is adjusted
    -Updates the self.materials dictionary with the new slider value for its corresponding material
    -Calls draw_rectangle_stack to redraw the rectangle stack with the new value"""
    def update_material_slider(self, value, material_label):
        #Get the new value of the slider
        slider_value = int(value)
        
        #Check if slider value is acceptable
        if self.material_min_thickness <= slider_value <= self.material_max_thickness:
            self.materials[material_label][0] = slider_value                            #Assign the value of the slider to its position in the materials dictionary
            self.draw_rectangle_stack_filled(self.canvas)                                                 #Redraw the rectangle stack with the new value
        else:
            messagebox.showerror("Error", "The slider value is out of range")

    """
    -Is called if the entry box is adjusted
    -Updates the self.materials dictionary with the new entry value for its corresponding material
    -Calls draw_rectangle_stack to redraw the rectangle stack with the new value """
    def update_material_entry(self, event, entry_box, slider):
        
        #Get the value entered in the entry box
        entry_value = int(entry_box.get())

        #Check if entered value is acceptable
        if self.material_min_thickness <= entry_value <= self.material_max_thickness:       
            slider_name = slider.cget("label")                  #Get the label/name of the slider
            self.materials[slider_name][0] = entry_value        #Assign the value of the entry box to its position in the materials dictionary
            slider.set(entry_value)                             #Apply the value change to the corresponding slider also
            self.draw_rectangle_stack_filled(self.canvas)                         #Redraw the rectangle stack

        else:
            messagebox.showerror("Error", "The value you entered is out of range")

    """Calls draw_rectangle_stack when the program window is adjusted"""
    def window_resized(self, event):        
        #Create the new canvas sizes        
        self.canvas_width = self.window.winfo_width() - self.slider_frame.winfo_width() - self.total_padding_x   #Subtract slider_frame width and extra padding used for each widget 
        self.canvas_height = self.window.winfo_height() - 15                                                     #Subtract 15 to keep a little space in the bottom of the window

        #Apply the new dimensions for the canvas
        self.canvas.config(width = self.canvas_width, height = self.canvas_height)

        #Redraw the rectangle stack based on the new width and height of the program window
        self.draw_rectangle_stack_filled(self.canvas)

    """Draws the rectangle stack so that it does not fill the entire canvas"""
    def draw_rectangle_stack(self, canvas):
        # #Clear all existing rectangles
        canvas.delete("all")
        
        # #Draw lines around the new canvas
        self.draw_canvas_boundaries(canvas)

        # #Main drawing point of stack and width of stack 
        rectangle_x0 = 2                                    #Top-left X-coordinate of rectangle
        rectangle_y0 = 2                                    #Top-left Y-coordinate of rectangle       
        rectangle_x1 = canvas.winfo_reqwidth() - 100   #Bottom-right X-coordinate of rectangle (leave a little space for text
        rectangle_y1 = canvas.winfo_reqheight() - 3    #Bottom-right Y-coordinate of rectangle (-3 is a manually added variable to keep the rectanlge inside the canvas)
       
        #Scaling factor decides the size of each rectangle when drawn. The current algorithm ensures that the rectangle stack is not drawn out of bounds 
        scaling_factor = canvas.winfo_reqheight() / ((self.material_max_thickness+18) * len(self.materials))   #The +18 value is a manual fix so that the rectangle is not drawn outside the canvas

        #Variables to prevent text box overlapping
        previous_text_bbox_y0 = None                  #Keep track of the height of the text boxes so that they don't overlap each other
        first_material_drawn = False                #Keep track if the first material is created to draw the text boxes correctly
        
        #Counter for adding elements to canvas_layer_data
        i = 0

        #Loop through all the materials and draw rectangle and labels for each
        for material in self.materials:
            rectangle_height = int(self.materials[material][0]) * scaling_factor        #How tall the rectangle should be drawn, adjusted by the scaling factor (thickness * scaling_factor)

            #Draw rectangles on top of the other
            rectangle_y0 = rectangle_y1 - rectangle_height
            created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material][1], tags="material_rectangle")  # Draw rectangle and fill it with a color
            
            #####   DRAW TEXT, BOXES AND ARROW SOLUTIONS   #####

            label_text = str(material) + "\n" + str(self.materials[material][0]) + "nm"                                             #Text to be written
            
            
            #if the rectangle height is big enough, write material name in middle of rectangle
            if(rectangle_height >=30):
                label_x_pos = (rectangle_x0 + rectangle_x1) / 2                                                                         #X-position of label
                label_y_pos = (rectangle_y0 + rectangle_y1) / 2                                                                         #Y-position of label
                created_text = canvas.create_text(label_x_pos, label_y_pos, text=label_text, fill="black", font=("Arial", 8), anchor="center")    #Creation of text
                created_arrow_line = None
                created_text_box = None
            #if the rectangle height is to low to display text, write material name on side of box
            else:
                #Calculate what the current text position should be
                label_x_pos = rectangle_x1 + 60                                                                                         #Text x-position (+50 to leave a little space from the rectangle)
                label_y_pos = (rectangle_y0 + rectangle_y1) / 2                                                                         #Text y-position
                
                #Write text - might end up being modified by the code below
                created_text = canvas.create_text(label_x_pos, label_y_pos, text=label_text, fill="black", font=("Arial", 8), anchor="center")
                                
                #if this is the first text to be written:
                if(first_material_drawn == False):
                    #Find the bounding box coordinates of text
                    text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text) #Get bounding box of text

                    #if the bounding box coordinates of text are lower then the canvas line
                    if(text_bbox_y1 > self.canvas_height):
                        #Get the height of the text's bounding box
                        text_bbox_height = text_bbox_y1 - text_bbox_y0
                        #Update the text coordinates so that the bounding box is not under the canvas
                        canvas.coords(created_text, label_x_pos, self.canvas_height - (text_bbox_height/2))
                        #Draw box around the text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Get new bounding box coordinates of text
                        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text) #Get bounding box of text
                        #Draw arrow from middle of text box to middle of rectangle
                        created_arrow_line = canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y0 = text_bbox_y0
                        #Confirm that the first text is written
                        first_material_drawn = True

                    #The bounding box coordinates is NOT lower than the canvas line
                    else:
                        #Draw box around text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Get the height of the text's bounding box
                        text_bbox_height = text_bbox_y1 - text_bbox_y0
                        #Draw arrow from middle of text box to middle of rectangle
                        created_arrow_line = canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y0 = text_bbox_y0
                        #Confirm that the first text is written
                        first_material_drawn = True


                #This is not the first text to be written
                else:
                    #Find the bounding box coordinates of text
                    text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text) #Get bounding box of text
                    #Get the height of the text's bounding box
                    text_bbox_height = text_bbox_y1 - text_bbox_y0
                    
                    #if this text's bounding box is overlapping the previous bounding box
                    if(text_bbox_y1 > previous_text_bbox_y0):
                        #Update the text coordinates so that the bounding box is not overlapping the previous text box
                        canvas.coords(created_text, label_x_pos, previous_text_bbox_y0 - (text_bbox_height/2))
                        #Draw box around text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Find the NEW bounding box coordinates of text
                        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text) #Get bounding box of text
                        #Draw arrow from box to rectangle
                        created_arrow_line = canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y0 = text_bbox_y0
                    
                    #This text bbox is NOT overlapping with the previous text
                    else:
                        #Draw box around the text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Draw arrow from box to rectangle
                        created_arrow_line = canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y0 = text_bbox_y0
            
            #Add newly created rectangle, text, text_box and line to canvas_layer_data dictionary
            self.canvas_layer_data[i] =[created_rectangle, created_text, created_text_box, created_arrow_line]

            #Update the rectangle coordinates so that the rectangles are not overlapping each other
            rectangle_y1 = rectangle_y0

            #Increment counter for adding elements to canvas_layer_data dictionary
            i+=1
    
    """Draws the rectangle stack so that it fills the entire canvas"""
    def draw_rectangle_stack_filled(self, canvas):
        #Variables to prevent text box overlapping
        previous_text_bbox_y0 = None                #Keep track of the height of the text boxes so that they don't overlap each other
        previous_text_bbox_y1 = None                #Keep track of the bottom of the text boxes so that they don't overlap each other
        first_material_drawn = False                #Keep track if the first material is created to draw the text boxes correctly
        #Counter for adding elements to canvas_layer_data
        i = 0
        
        #Clear all existing rectangles
        canvas.delete("all")
        
        # #Draw lines around the new canvas
        self.draw_canvas_boundaries(canvas)
        
        #Get the bounding box coordinates of the canvas
        canvas_bbox_x0 = canvas.bbox("all")[0] + 1
        canvas_bbox_y0 = canvas.bbox("all")[1] + 1
        canvas_bbox_x1 = canvas.bbox("all")[2] - 1
        canvas_bbox_y1 = canvas.bbox("all")[3] - 1

        #Get the height of the canvas
        canvas_height = canvas_bbox_y1 - canvas_bbox_y0
        
        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in self.materials:
            rectangle_height = int(self.materials[material][0])
            sum_of_all_materials += rectangle_height

        #Prepare rectangle drawing coordinates
        rectangle_x0 = canvas_bbox_x0
        rectangle_y0 = canvas_bbox_y0
        rectangle_x1 = canvas_bbox_x1 - 150
        rectangle_y1 = canvas_bbox_y1

        #Draw rectangles on canvas
        for material in self.materials:
            #Create name to be displayed in or outside rectangle
            material_text = str(material) + " " + str(self.materials[material][0]) + "nm"
            #find how many percent the current rectangle's height is of the total sum of materials
            rectangle_height = int(self.materials[material][0])
            rectangle_percentage = (rectangle_height/sum_of_all_materials)*100

            #Convert rectangle percentage to pixels
            rectangle_height_pixels = (rectangle_percentage/100)*canvas_height
            
            #draw rectangle from top of canvas to its number of pixles in height
            rectangle_y1 = rectangle_y0 + rectangle_height_pixels
            created_rectangle = canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material][1], tags="Rectangle")
            
            #If rectangle is high enough: Write material name and thickness inside rectangle
            if(rectangle_height_pixels > 35):
                label_x_pos = (rectangle_x0 + rectangle_x1) / 2
                label_y_pos = (rectangle_y0 + rectangle_y0+rectangle_height_pixels) / 2
                created_text = canvas.create_text(label_x_pos, label_y_pos, text=material_text, fill="black", font=("Arial", self.text_size), anchor="center", tags="Material_label")
                created_arrow_line = None
                created_text_box = None
            
            #If rectangle is to small: Write material name and thickness outside rectangle
            else:
                label_x_pos = rectangle_x1 + 100                                                                                         #+50 to leave a little space from the rectangle
                label_y_pos = (rectangle_y0 + rectangle_y0 + rectangle_height_pixels) / 2
                
                #Write text - might end up being modified by the code below
                created_text = canvas.create_text(label_x_pos, label_y_pos, text=material_text, fill="black", font=("Arial", self.text_size), anchor="center")

                #if this is the first text to be written:
                if(first_material_drawn == False):
                    #Find the bounding box coordinates of text
                    text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text)

                    #if the bounding box coordinates of text are higher than the top canvas line
                    if(text_bbox_y0 < canvas_bbox_y0):
                        #Find out how much of the bbox is over the canvas top line
                        margin = canvas_bbox_y0 - text_bbox_y0
                        #Move the text downwards with the calculated margin
                        canvas.coords(created_text, label_x_pos, label_y_pos+margin)
                        #Draw box around the text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Get new bounding box coordinates of text
                        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text) #Get bounding box of text
                        #Draw arrow from middle of text box to middle of rectangle
                        created_arrow_line = canvas.create_line(text_bbox_x0, ((text_bbox_y1-text_bbox_y0)/2), rectangle_x1, ((rectangle_y1-rectangle_y0)/2), arrow=tk.LAST, tags="arrow_line")

                        #Set the "previous_bbox_y1" to whatever this bounding box y1 is
                        previous_text_bbox_y1 = text_bbox_y1
                        previous_text_bbox_y0 = text_bbox_y0
                        #Confirm that the first text is written
                        first_material_drawn = True

                    #If the bottom of bounding box is lower than the bottom of canvas
                    elif(text_bbox_y1 > canvas_bbox_y1):
                        #Find how much lower the bbox is than the canvas bottom line
                        margin = text_bbox_y1 - canvas_bbox_y1
                        #Move the text uppwards with the calculated margin
                        canvas.coords(created_text, label_x_pos, label_y_pos-margin)
                        #Draw box around the text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Get new bounding box coordinates of text
                        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text)
                        #Draw arrow from middle of text box to middle of rectangle
                        created_arrow_line = canvas.create_line(text_bbox_x0, ((text_bbox_y1-text_bbox_y0)/2), rectangle_x1, ((rectangle_y1-rectangle_y0)/2), arrow=tk.LAST, tags="arrow_line")

                        #Set the "previous_bbox_y1" to whatever this bounding box y1 is
                        previous_text_bbox_y1 = text_bbox_y1
                        previous_text_bbox_y0 = text_bbox_y0
                        #Confirm that the first text is written
                        first_material_drawn = True

                    #The bounding box coordinates is NOT higher than the canvas line
                    else:
                        #Draw box around text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        # #Get the height of the text's bounding box
                        text_bbox_height = text_bbox_y1 - text_bbox_y0
                        #Draw arrow from middle of text box to middle of rectangle
                        created_arrow_line = canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y1" to whatever this bounding box y1 is
                        previous_text_bbox_y1 = text_bbox_y1
                        previous_text_bbox_y0 = text_bbox_y0
                        #Confirm that the first text is written
                        first_material_drawn = True

                #If this is not the first text to be written
                else:
                    #Find the bounding box coordinates of text
                    text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text) #Get bounding box of text
                    #Get the height of the text's bounding box
                    text_bbox_height = text_bbox_y1 - text_bbox_y0
                    
                    #if this text's bounding box bottom is overlapping the top of previous bounding box
                    if(text_bbox_y0 < previous_text_bbox_y1):
                        #Find how much of the bbox is overlapping
                        margin = previous_text_bbox_y1 - text_bbox_y0
                        #Update the text coordinates so that the bounding box is not overlapping the previous text box
                        canvas.coords(created_text, label_x_pos, label_y_pos+margin)
                        #Draw box around text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Find the NEW bounding box coordinates of text
                        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text)
                        #Draw arrow from box to rectangle
                        created_arrow_line = canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y1 = text_bbox_y1
                                    
                    #This text bbox is NOT overlapping with the previous text
                    else:
                        #Draw box around the text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Draw arrow from box to rectangle
                        created_arrow_line = canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y1 = text_bbox_y1
                    

                    #If the bottom of bounding box is lower than the bottom of canvas
                    if(text_bbox_y1 > canvas_bbox_y1):
                        print("SHIT")
                        #Find how much lower the bbox is than the canvas bottom line
                        margin = text_bbox_y1 - canvas_bbox_y1
                        #Move the text uppwards with the calculated margin
                        canvas.coords(created_text, label_x_pos, label_y_pos-margin)
                        #Draw box around the text
                        created_text_box = canvas.create_rectangle(canvas.bbox(created_text), outline='black', tags="text_box")
                        #Get new bounding box coordinates of text
                        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = canvas.bbox(created_text)
                        #Draw arrow from middle of text box to middle of rectangle
                        created_arrow_line = canvas.create_line(text_bbox_x0, ((text_bbox_y1-text_bbox_y0)/2), rectangle_x1, ((rectangle_y1-rectangle_y0)/2), arrow=tk.LAST, tags="arrow_line")

                        #Set the "previous_bbox_y1" to whatever this bounding box y1 is
                        previous_text_bbox_y1 = text_bbox_y1
                        previous_text_bbox_y0 = text_bbox_y0
            
            #Add newly created rectangle, text, text_box and line to canvas_layer_data dictionary
            self.canvas_layer_data[i] = [created_rectangle, created_text, created_text_box, created_arrow_line]

            #Increment counter for adding elements to canvas_layer_data dictionary
            i+=1

            #Add the number of pixels so that the next rectangle does not overlap this one
            rectangle_y0 += rectangle_height_pixels



            """
            if(first material not drawn)
                if(box is higher than canvas_top)
                elif(box is lower than canvas_bottom)

            else(first material is drawn)
                if(box is higher than canvas_top)
                elif(box_bottom is overlapping the next box_top)
                elif(box_top is overlapping the next box_bottom)
                elif(box is lower than canvas_bottom)
            """


            """
            if(first_material_drawn == False)
                if(text_bbox_y0 < canvas_bbox_y0)
                    -adjust text downwards
                elif(text_bbox_y1 > canvas_bbox_y1)
                    -adjust text upwards

            else(first_material_drawn == True)
                if(text_bbox_y0 < canvas_bbox_y0)
                    -adjust text downwards
                elif(text_bbox_y1 > canvas_bbox_y1)
                    -adjust text upwards
                elif(text_bbox_y0 < previous_text_bbox_y1)
                    -Adjust text downwards
                elif(text_bbox_y1 > previous_text_bbox_y0)
                    -Adjust text u
            """

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

        #Handle errors
        except Exception as error:
            print(f"Error loading materials from Excel: {error}")

    """Exports the stack without material names as SVG file"""
    def export_stack_as_svg(self):
        # Define the name of the svg file to be created
        filename = "stack.svg"

        # XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
        xml_declaration = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'

        # Creates the opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
        svg_open_tag = '<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight())

        # Represents the closing tag for the SVG file.
        svg_close_tag = '</svg>\n'

        # Retrieve all elements on the canvas
        elements = self.canvas.find_all()

        # Specify a folder where the SVG-file should be saved
        folder_path = "svg_exports"

        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Create the file path by joining the folder path and the filename
        file_path = os.path.join(folder_path, filename)

        # Open the file for writing using a context manager, ensuring proper handling and closure of the file
        with open(file_path, 'w') as f:
            f.write(xml_declaration)  # Writes the XML declaration to the file.
            f.write(svg_open_tag)  # Writes the opening SVG tag to the file

            # Iterate through all the elements found in the canvas
            for element in elements:

                # Check the type of canvas item
                item_type = self.canvas.type(element)

                # Constructs an SVG <rect> element for rectangles. (If the outline of a rectangle is "black" then it is considered as a text-box rectangle and is NOT included)
                if item_type == "rectangle" and self.canvas.itemcget(element, 'outline') != 'black':
                    # Retrieve the coordinates of the rectangle
                    rect_x0, rect_y0, rect_x1, rect_y1 = self.canvas.coords(element)

                    # Construct an SVG <rect> element for the rectangle
                    svg_rect_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(
                        rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, self.canvas.itemcget(element, 'fill')
                    )

                    # Write the SVG representation of the rectangle to the file
                    f.write(svg_rect_element)

                    # Construct an SVG <rect> element for the bounding box
                    bbox_x0, bbox_y0, bbox_x1, bbox_y1 = rect_x0, rect_y0, rect_x1, rect_y1
                    svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black" />\n'.format(
                        bbox_x0, bbox_y0, bbox_x1 - bbox_x0, bbox_y1 - bbox_y0
                    )

                    # Write the SVG representation of the bounding box to the file
                    f.write(svg_bbox_element)

            # Writes the closing SVG tag to the file, completing the SVG file.
            f.write(svg_close_tag)

        # Close the svg file
        f.close()

    """Exports each layer of the stack with names and arrows as SVG-file"""
    def export_layers_as_svg(self):
        #Retrieve all elements on the canvas
        canvas_elements = self.canvas.find_all()

        #Specify a folder where the SVG-file should be saved
        folder_path = "svg_exports"
        #Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #Iterate through all the rectangles found in the canvas
        for i in range(len(self.canvas_layer_data)):
            #Create a name for the SVG file for the current layer
            filename = f"{i+1}_layers.svg"
            #Create the file path by joining the folder path and the filename
            file_path = os.path.join(folder_path, filename)

            #Open a file to create an svg-file
            with open(file_path, 'w') as f:
                #Write the XML declaration to the file
                f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                #Write the opening SVG tag to the file
                f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.canvas.winfo_width()+100, self.canvas.winfo_reqheight()))   #Added +100 because the rectangle was cropped without it


                #Iterate through all rectangles up to the current layer and create SVG rectangles for each layer 
                for j in range(i+1):
                    #Draw rectangles from current layers
                    rectangle_id = self.canvas_layer_data[j][0]

                    rect_x0, rect_y0, rect_x1, rect_y1 = self.canvas.coords(rectangle_id)  # Retrieve the coordinates of the rectangle
                    fill_color = self.canvas.itemcget(rectangle_id, 'fill')  # Retrieve fill color of the rectangle from the canvas
                    svg_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, fill_color)

                    #Write the SVG representation of the rectangle to the file
                    f.write(svg_element)

                    #Construct an SVG <rect> element for the bounding box
                    svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0)

                    # Write the SVG representation of the bounding box to the file
                    f.write(svg_bbox_element)

                #Iterate through all text elements up to the current layer and create SVG text
                for j in range(i+1):
                    text_id = self.canvas_layer_data[j][1]
                    label_x, label_y = self.canvas.coords(text_id)  # Retrieve the coordinates of the text
                    text_content = self.canvas.itemcget(text_id, 'text')  # Retrieve text content from the canvas

                    # Construct an SVG <rect> element for the bounding box
                    bbox_x0, bbox_y0, bbox_x1, bbox_y1 = self.canvas.bbox(text_id)
                    svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black" />\n'.format(bbox_x0, bbox_y0, bbox_x1 - bbox_x0, bbox_y1 - bbox_y0)

                    # Write the SVG representation of the bounding box to the file
                    f.write(svg_bbox_element)

                    #Construct an SVG <text> element for text
                    svg_text_element = '<text x="{}" y="{}" fill="black" font-size="14" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(label_x, label_y, text_content)

                    #Write the SVG representation of the text to the file
                    f.write(svg_text_element)
                
                #Iterate through all arrow_lines up to the current layer and create SVG lines
                for j in range(i+1):
                    arrow_id = self.canvas_layer_data[j][3]
                    if(arrow_id != None):
                    
                        arrow_coords = self.canvas.coords(arrow_id)  # Retrieve the coordinates of the arrow

                        #Construct an SVG <line> element for arrows
                        svg_arrow_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black" />\n'.format(arrow_coords[0], arrow_coords[1], arrow_coords[2], arrow_coords[3])

                        #Write the SVG representation of the arrow to the file
                        f.write(svg_arrow_element)

                    

                #Write the closing SVG tag to the file, completing the SVG file
                f.write('</svg>\n')
            
                #Close the svg file
                f.close()

    """
    -Creates a text at a given position with a bounding box around it.
    -Creates an arrow pointing from the box to a given point on the canvas
    -Adds the text, bounding_box and arrow_line to canvas_layer_data
    """
    def create_PointingTextLabel(self, text, text_Xpos, text_Ypos, arrow_Xpoint=None, arrow_Ypoint=None):
        #Write text
        created_text = self.canvas.create_text(text_Xpos, text_Ypos, text=text, fill="black", font=("Arial", self.text_size), anchor="center", tags="material_text")
                                
        #Find the bounding box coordinates of text and height of bounding box
        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = self.canvas.bbox(created_text)
        text_bbox_height = text_bbox_y1 - text_bbox_y0

        #Draw box around the text
        created_bounding_box = self.canvas.create_rectangle(self.canvas.bbox(created_text), outline='black', tags="text_box")

        #Draw arrow line if coordinates are provided
        if(arrow_Xpoint and arrow_Ypoint):
            created_arrow_line = self.canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (arrow_Xpoint, arrow_Ypoint), arrow=tk.LAST, tags="arrow_line")

        # #Create a key in the canvas_layer_data for this layer if it does not exist
        # if(not text in self.canvas_layer_data):
        #     self.canvas_layer_data[text] = []

        # #Add newly created rectangle, text, text_box and line to canvas_layer_data dictionary
        # self.canvas_layer_data[text].insert(1, created_text)
        # self.canvas_layer_data[text].insert(2, created_bounding_box)
        # if(created_arrow_line):
        #     self.canvas_layer_data[text].insert(3, created_arrow_line)
        # else:
        #     self.canvas_layer_data[text].insert(3, None)


#Main start point of program
if __name__ == "__main__":
    window = tk.Tk()
    
    #Create instance of class and run application
    app = App(window)
    app.run_application()

    #Closes the program if "esc" key is pressed
    window.bind("<Escape>", lambda event: window.destroy())

    #Checks if the program window is being resized
    window.bind("<Configure>", app.window_resized)

    window.mainloop()