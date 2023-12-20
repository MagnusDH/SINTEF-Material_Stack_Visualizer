import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL, Frame, Entry, StringVar, Label, Button
from PIL import ImageGrab, Image
import pandas as pd
import pygetwindow
import pyautogui
import os


class App:
    def __init__(self, window):
        
        #SETTINGS
        self.app_title = "Material Measurements"
        self.window_width = 800                     #Start width of app window
        self.window_height = 800                    #Start height of app window
        self.canvas_width = 800                     #Width of the canvas where things are drawn
        self.canvas_height = 800                    #Height of the canvas where things are drawn
        self.material_min_thickness = 0             #Minimum thickness of materials
        self.material_max_thickness = 3000          #Maximum thickness of materials
        self.excel_file = "Materials.xlsx"          #Excel-file to load materials from

        #Dictionary for all materials. KEY: "material_name" ---VALUES: list of [thickness, color]
        self.materials = {}

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
        self.create_canvas(self.canvas_width, self.canvas_height)       

        #Draw the material stack
        self.draw_rectangle_stack()


    """Creates a canvas to draw rectangle stack on"""
    def create_canvas(self, canvas_width, canvas_height):
        #Create canvas with the given height&width and attack it to the top of the window
        self.canvas = Canvas(self.window, width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=1, sticky="n")

        #Draw lines around the created canvas
        self.draw_canvas_boundaries()


    """Creates sliders, input and color boxes based on the number of materials in self.materials"""
    def create_user_interface(self):
        #Create frame within the main window to contain sliders, color&input widgets
        self.slider_frame = Frame(self.window)
        self.slider_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')
        self.total_padding_x += (10 * 2)  #Add padding for this widget (+10 for both sides of the widget)
        self.total_padding_y += (10 * 2)  #Add padding for this widget (+10 for both sides of the widget)

        
        #Create color boxes, sliders, input boxes and labels
        i = 0 #Row counter
        for material in self.materials:

            #Create color boxes and place them on grid
            color_box = Label(self.slider_frame, bg=self.materials[material][1], width=2)                           #Creation of color box in the slider frame
            color_box.grid(row=i, column=0, padx=5, pady=5)                                                         #Color box placement
            self.total_padding_y += (5*2)  #Add padding for this widget (+10 for both sides of the widget)
            

            #Create sliders
            slider = Scale(self.slider_frame, from_=self.material_min_thickness, to=self.material_max_thickness,
                       orient=HORIZONTAL, label=material, resolution=1,
                       command=lambda value, label=material: self.slider_updated(value, label))             #Creation of slider and listening to slider adjustments
            slider.grid(row=i, column=1, pady=5, padx=5)                                                            #Slider placement
            slider.set(self.materials[material][0])                                                                 #Set the initial value of the slider
            self.total_padding_y += (5*2)  #Add padding for this widget (+10 for both sides of the widget)


            #Create input boxes
            height_var = StringVar(value=str(self.materials[material][0]))                                          
            entry = Entry(self.slider_frame, textvariable=height_var, width=6)                                      #Creation of entry box in the slider frame
            entry.grid(row=i, column=2, padx=5)                                                                     #Entry box placement
            entry.bind("<Return>", lambda event, s=slider, e=entry: self.entry_updated(event, e, s))                #Listens to updates in the entry/input box
            
            #Create "nm" label next to slider
            nm_label = Label(self.slider_frame, text="nm")                                                          #Creation of label in the slider frame
            nm_label.grid(row=i, column=3)                                                                          #Label placement

            #Increment row-counter
            i += 1

        #Add padding for the widgets (x-padding is only applied once compared to Y-padding, because the slider frame doesn't get wider for each widget)
        self.total_padding_x += (5*2)
        
        #Create button which calls "export_stack_as_svg" function
        self.export_layers_button = Button(self.slider_frame, text = "Export stack-svg", command=self.export_stack_as_svg)
        self.export_layers_button.grid(row=len(self.materials), column=1, padx=5)
        self.total_padding_x += (5 * 2)  #Add padding for this widget (+10 for both sides of the widget)

         #Create button which calls "export_all_as_jpg" function
        self.export_layers_button = Button(self.slider_frame, text = "Export layers-svg", command=self.export_layers_as_svg)
        self.export_layers_button.grid(row=len(self.materials), column=2, padx=5)
        self.total_padding_x += (5 * 2)  #Add padding for this widget (+10 for both sides of the widget)

        # #Create button which calls "export_stack_as_jpg" function
        # self.export_stack_button = Button(self.slider_frame, text="Export stack-jpg", command=self.export_stack_as_jpg)
        # self.export_stack_button.grid(row=len(self.materials)+1, column=1)

        # #Create button which calls "export_layers_as_jpg" function
        # self.export_layers_button = Button(self.slider_frame, text = "Export layers-jpg", command=self.export_layers_as_jpg)
        # self.export_layers_button.grid(row=len(self.materials)+1, column=2, padx=5)
        # self.total_padding_x += (5 * 2)  #Add padding for this widget (+10 for both sides of the widget)


        
    """
    -Is called if the slider is adjusted
    -Updates the self.materials dictionary with the new slider value for its corresponding material
    -Calls draw_rectangle_stack to redraw the rectangle stack with the new value"""
    def slider_updated(self, value, material_label):
        #Get the new value of the slider
        slider_value = int(value)
        
        #Check if slider value is acceptable
        if self.material_min_thickness <= slider_value <= self.material_max_thickness:
            self.materials[material_label][0] = slider_value                            #Assign the value of the slider to its position in the materials dictionary
            self.draw_rectangle_stack()                                                 #Redraw the rectangle stack with the new value
        else:
            print("Error: Slider value is out of range")


    """
    -Is called if the entry box is adjusted
    -Updates the self.materials dictionary with the new entry value for its corresponding material
    -Calls draw_rectangle_stack to redraw the rectangle stack with the new value """
    def entry_updated(self, event, entry_box, slider):
        
        #Get the value entered in the entry box
        entry_value = int(entry_box.get())

        #Check if entered value is acceptable
        if self.material_min_thickness <= entry_value <= self.material_max_thickness:       
            slider_name = slider.cget("label")                  #Get the label/name of the slider
            self.materials[slider_name][0] = entry_value        #Assign the value of the entry box to its position in the materials dictionary
            slider.set(entry_value)                             #Apply the value change to the corresponding slider also
            self.draw_rectangle_stack()                         #Redraw the rectangle stack

        else:
            print("Error: Entry box value is out of range")


    """Calls draw_rectangle_stack when the program window is adjusted"""
    def window_resized(self, event):        
        #Create the new canvas sizes        
        self.canvas_width = self.window.winfo_width() - self.slider_frame.winfo_width() - self.total_padding_x   #Subtract slider_frame width and extra padding used for each widget 
        self.canvas_height = self.window.winfo_height() - 15                                                     #Subtract 15 to keep a little space in the bottom of the window

        #Apply the new dimensions for the canvas
        self.canvas.config(width = self.canvas_width, height = self.canvas_height)

        #Redraw the rectangle stack based on the new width and height of the program window
        self.draw_rectangle_stack()


    """Draws lines around the canvas showing where things can be drawn"""
    def draw_canvas_boundaries(self):
        #Draw lines around canvas (top left x,y MUST be 2,2, some of the values must be manually adjusted to fit the window)
        self.canvas.create_line(2,2, self.canvas.winfo_reqwidth(), 2, fill="green")
        self.canvas.create_line(2,2, 2, self.canvas.winfo_reqheight(), fill="black")
        self.canvas.create_line(2, self.canvas.winfo_reqheight()-3, self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()-3, fill="blue")        
        self.canvas.create_line(self.canvas.winfo_reqwidth()-3,2, self.canvas.winfo_reqwidth()-3, self.canvas.winfo_reqheight()-3, fill="black")


    """Draws rectangles in the rectangle stack for each material in self.materials"""
    def draw_rectangle_stack(self):
        #Clear all existing rectangles
        self.canvas.delete("all")

        #Draw lines around the new canvas
        self.draw_canvas_boundaries()

        #Main drawing point of stack and width of stack 
        rectangle_x0 = 2                                    #Top-left X-coordinate of rectangle
        rectangle_y0 = 2                                    #Top-left Y-coordinate of rectangle       
        rectangle_x1 = self.canvas.winfo_reqwidth() - 100   #Bottom-right X-coordinate of rectangle (leave a little space for text
        rectangle_y1 = self.canvas.winfo_reqheight() - 3    #Bottom-right Y-coordinate of rectangle (-3 is a manually added variable to keep the rectanlge inside the canvas)
       
        #Scaling factor decides the size of each rectangle when drawn. The current algorithm ensures that the rectangle stack is not drawn out of bounds 
        scaling_factor = (self.canvas.winfo_reqheight()/(self.material_max_thickness+18))/len(self.materials)   #The +18 value is a manual fix so that the rectangle is not drawn outside the canvas
        
        #Variables to prevent text box overlapping
        previous_text_bbox_y0 = None                  #Keep track of the height of the text boxes so that they don't overlap each other
        first_material_drawn = False                #Keep track if the first material is created to draw the text boxes correctly

        #Loop through all the materials and draw rectangle and labels for each
        for material in self.materials:
            rectangle_height = int(self.materials[material][0]) * scaling_factor        #How tall the rectangle should be drawn, adjusted by the scaling factor (thickness * scaling_factor)

            #Draw rectangles on top of the other
            rectangle_y0 = rectangle_y1 - rectangle_height
            self.canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material][1], tags="material_rectangle")  # Draw rectangle and fill it with a color


            #####   DRAW TEXT, BOXES AND ARROW SOLUTIONS   ##### 
            
            label_text = str(material) + "\n" + str(self.materials[material][0]) + "nm"                                             #Text to be written
            
            #if the rectangle height is big enough, write material name in middle of rectangle
            if(rectangle_height >=30):
                label_x_pos = (rectangle_x0 + rectangle_x1) / 2                                                                         #X-position of label
                label_y_pos = (rectangle_y0 + rectangle_y1) / 2                                                                         #Y-position of label
                self.canvas.create_text(label_x_pos, label_y_pos, text=label_text, fill="black", font=("Arial", 8), anchor="center")    #Creation of text

            #if the rectangle height is to low to display text, write material name on side of box
            else:
                #Calculate what the current text position should be
                label_x_pos = rectangle_x1 + 60                                                                                         #Text x-position (+50 to leave a little space from the rectangle)
                label_y_pos = (rectangle_y0 + rectangle_y1) / 2                                                                         #Text y-position
                
                #Write text - might end up being modified by the code below
                text = self.canvas.create_text(label_x_pos, label_y_pos, text=label_text, fill="black", font=("Arial", 8), anchor="center")
                                
                #if this is the first text to be written:
                if(first_material_drawn == False):
                    #Find the bounding box coordinates of text
                    text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = self.canvas.bbox(text) #Get bounding box of text

                    #if the bounding box coordinates of text are lower then the canvas line
                    if(text_bbox_y1 > self.canvas_height):
                        #Get the height of the text's bounding box
                        text_bbox_height = text_bbox_y1 - text_bbox_y0
                        #Update the text coordinates so that the bounding box is not under the canvas
                        self.canvas.coords(text, label_x_pos, self.canvas_height - (text_bbox_height/2))
                        #Draw box around the text
                        self.canvas.create_rectangle(self.canvas.bbox(text), outline='black', tags="text_box")
                        #Get new bounding box coordinates of text
                        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = self.canvas.bbox(text) #Get bounding box of text
                        #Draw arrow from middle of text box to middle of rectangle
                        self.canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y0 = text_bbox_y0
                        #Confirm that the first text is written
                        first_material_drawn = True

                    #The bounding box coordinates is NOT lower than the canvas line
                    else:
                        #Draw box around text
                        self.canvas.create_rectangle(self.canvas.bbox(text), outline='black', tags="text_box")
                        #Get the height of the text's bounding box
                        text_bbox_height = text_bbox_y1 - text_bbox_y0
                        #Draw arrow from middle of text box to middle of rectangle
                        self.canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y0 = text_bbox_y0
                        #Confirm that the first text is written
                        first_material_drawn = True


                #This is not the first text to be written
                else:
                    #Find the bounding box coordinates of text
                    text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = self.canvas.bbox(text) #Get bounding box of text
                    #Get the height of the text's bounding box
                    text_bbox_height = text_bbox_y1 - text_bbox_y0
                    
                    #if this text's bounding box is overlapping the previous bounding box
                    if(text_bbox_y1 > previous_text_bbox_y0):
                        #Update the text coordinates so that the bounding box is not overlapping the previous text box
                        self.canvas.coords(text, label_x_pos, previous_text_bbox_y0 - (text_bbox_height/2))
                        #Draw box around text
                        self.canvas.create_rectangle(self.canvas.bbox(text), outline='black', tags="text_box")
                        #Find the NEW bounding box coordinates of text
                        text_bbox_x0, text_bbox_y0, text_bbox_x1, text_bbox_y1 = self.canvas.bbox(text) #Get bounding box of text
                        #Draw arrow from box to rectangle
                        self.canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y0 = text_bbox_y0
                    
                    #This text bbox is NOT overlapping with the previous text
                    else:
                        #Draw box around the text
                        self.canvas.create_rectangle(self.canvas.bbox(text), outline='black', tags="text_box")
                        #Draw arrow from box to rectangle
                        self.canvas.create_line((text_bbox_x0, text_bbox_y0+text_bbox_height/2), (rectangle_x1,label_y_pos), arrow=tk.LAST, tags="arrow_line")
                        #Set the "previous_bbox_y0" to whatever this bounding box y0 is
                        previous_text_bbox_y0 = text_bbox_y0

            #Update the rectangle coordinates so that the rectangles are not overlapping each other
            rectangle_y1 = rectangle_y0


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


    """Takes a screenshot of the entire rectangle stack and saves it as .jpg"""
    def export_stack_as_jpg(self):
        #Get window of app
        window = pygetwindow.getWindowsWithTitle(self.app_title)[0]

        #Get current positions of open window
        window_x0_pos, window_y0_pos = window.topleft
        window_x1_pos, window_y1_pos = window.bottomright

        rec_stack_x0 = window_x0_pos + 260
        rec_stack_y0 = window_y0_pos + 39
        rec_stack_x1 = window_x1_pos 
        rec_stack_y1 = window_y1_pos
        
        #Use the (x0,y0)(x1,y1) coordinates to screenshot the entire rectangle stack
        screenshot = ImageGrab.grab(bbox = (rec_stack_x0, rec_stack_y0, rec_stack_x1, rec_stack_y1))
        
        #Save screenshot as .jpg in specified folder
        folder_path = "jpg_saves"

        if os.path.exists(folder_path) == False:    #Create the folder if it doesn't exist
            os.makedirs(folder_path)
            
        file_path = os.path.join(folder_path, "Stack-jpg.jpg")
        screenshot.save(file_path)


        # #Get window of app
        # window = pygetwindow.getWindowsWithTitle(self.app_title)[0]

        # # #Find the height of the red part of open window
        # # #Find the small padding between the end of the red part of window and the start of the canvas top
        # # #find the width of the slider frame + total x-padding
        # # #Find the width and heigh of the canvas

        # #Get current positions of open window
        # main_window_x0_pos = window.topleft[0]              #FIGURE OUT IF THIS GIVES THE CORRECT COORDNIATE
        # main_window_y0_pos = window.topleft[1]              #FIGURE OUT IF THIS GIVES THE CORRECT COORDNIATE
        # main_window_x1_pos = window.bottomright[0]          #FIGURE OUT IF THIS GIVES THE CORRECT COORDNIATE
        # main_window_y1_pos = window.bottomright[1]          #FIGURE OUT IF THIS GIVES THE CORRECT COORDNIATE

        # main_window_width = self.window.winfo_width()       #FIGURE OUT WHICH FUNCTION ACTUALLY WORKS
        # main_window_height = window.height                  #FIGURE OUT WHICH FUNCTION ACTUALLY WORKS
        # title_bar_height = window.height - self.window.winfo_height()   #FIGURE OUT THIS ONE LATER
        
        # #FROM HERE EVERYTHING SHOULD WORK

        # #Use the (x0,y0)(x1,y1) coordinates to screenshot the entire rectangle stack
        # screenshot = ImageGrab.grab(bbox = (main_window_x0_pos, main_window_y0_pos, main_window_x1_pos, main_window_y1_pos))

        # #Save screenshot as .jpg in specified folder
        # folder_path = "screenshots"

        # #Create folder to save screenshot to, if it doesn't exist
        # if os.path.exists(folder_path) == False:
        #     os.makedirs(folder_path)
            
        # file_path = os.path.join(folder_path, "All_Materials.jpg")
        # screenshot.save(file_path)


    """Takes a screenshot of every layer in the rectangle in an ascending order and saves each screenshot as .jpg"""
    def export_layers_as_jpg(self):
        #Get window of app
        window = pygetwindow.getWindowsWithTitle(self.app_title)[0]

        #Get current positions of open window
        window_x0_pos, window_y0_pos = window.topleft
        window_x1_pos, window_y1_pos = window.bottomright

        #Find positions of canvas/rectangles
        rec_stack_x0 = window_x0_pos + 260
        rec_stack_x1 = window_x1_pos 
        rec_stack_y1 = window_y1_pos - 17   #Lowest line of rectangle stack
        rec_stack_y0 = rec_stack_y1         #Must be the lowest line before the loop

        #Find the height of the rectangle based on the scaling factor
        scaling_factor = (self.canvas.winfo_reqheight()/(self.material_max_thickness+18))/len(self.materials)   #The +18 value is a manual fix because the rectangle would be drawn outside the canvas  (See the original line in draw_rectangle_stack)
        
        i = 1

        #Loop through akk the materials in self.materials
        for material in self.materials:

            #Calculate the height of the material based on the scaling factor
            rectangle_height = int(self.materials[material][0]) * scaling_factor

            #Add height to take screenshot of incrementing rectangles
            rec_stack_y0 -= rectangle_height

            #The x0, x1 and y1 coordinates must always stay the same
            #The y0 coordinate must change

            #Take screenshot of layer(s)
            screenshot = ImageGrab.grab(bbox=(rec_stack_x0, rec_stack_y0, rec_stack_x1, rec_stack_y1))

            #Save screenshot as .jpg in specified folder
            folder_path = "jpg_saves"

            #Create the folder if it doesn't exist
            if os.path.exists(folder_path) == False:
                os.makedirs(folder_path)
            
            file_path = os.path.join(folder_path, f"{i}_Layers-jpg.jpg")
            screenshot.save(file_path)

            i += 1


    """Exports the stack without material names as SVG file"""
    def export_stack_as_svg(self):
        #Define the name of the svg file to be created
        filename = "stack-svg.svg"
        
        #XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
        xml_declaration = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'

        #Creates the opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
        svg_open_tag = '<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight())

        #Represents the closing tag for the SVG file.
        svg_close_tag = '</svg>\n'

        #Retrieve all elements on the canvas
        elements = self.canvas.find_all()

        #Specify a folder where the SVG-file should be saved
        folder_path = "svg_saves"

        #Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #Create the file path by joining the folder path and the filename
        file_path = os.path.join(folder_path, filename)

        #Open the file for writing using a context manager, ensuring proper handling and closure of the file
        with open(file_path, 'w') as f:
            f.write(xml_declaration)    #Writes the XML declaration to the file.
            f.write(svg_open_tag)           #Writes the opening SVG tag to the file

            #Iterate through all the elements found in the canvas
            for element in elements:
                
                #Check the type of canvas item
                item_type = self.canvas.type(element)


                #Constructs an SVG <rect> element for rectangles. (If the outline of a rectangle is "black" then it is considered as a text-box rectangle and is NOT included)
                if item_type == "rectangle" and self.canvas.itemcget(element, 'outline') != 'black':
                    svg_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(
                        self.canvas.coords(element)[0],                                     #Retrieves the coordinates of the rectangle
                        self.canvas.coords(element)[1],                                     #Retrieves the coordinates of the rectangle
                        self.canvas.coords(element)[2] - self.canvas.coords(element)[0],    #Retrieves the coordinates of the rectangle
                        self.canvas.coords(element)[3] - self.canvas.coords(element)[1],    #Retrieves the coordinates of the rectangle
                        self.canvas.itemcget(element, 'fill')                               #fill color of the rectangle from the canvas
                    )

                    #Write the SVG representation of the rectangle to the file.
                    f.write(svg_element)

            #Writes the closing SVG tag to the file, completing the SVG file.
            f.write(svg_close_tag)

        #Close the svg file
        f.close()


    """Exports each layer of the stack with names and arrows as SVG-file"""
    def export_layers_as_svg(self):
        #Retrieve all elements on the canvas
        canvas_elements = self.canvas.find_all()

        #Filter out the elements needed
        rectangles_on_canvas = []
        text_boxes_on_canvas = []
        labels_on_canvas = []
        arrows_on_canvas = []

        #Filter out the elements needed
        for element in canvas_elements:
            #Get the tag for each element (when some of the elements were created, I set a tag for each item)
            tags = self.canvas.gettags(element)
            if(self.canvas.type(element) == "rectangle"):
                if("material_rectangle" in tags):
                    rectangles_on_canvas.append(element) 
                elif("text_box" in tags):
                    text_boxes_on_canvas.append(element)
            elif(self.canvas.type(element) == "text"):
                labels_on_canvas.append(element)
            elif(self.canvas.type(element) == "line"):
                if("arrow_line" in tags):
                    arrows_on_canvas.append(element)

        #Specify a folder where the SVG-file should be saved
        folder_path = "svg_saves"
        #Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #Iterate through all the rectangles found in the canvas
        for i in range(len(rectangles_on_canvas)):
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
                    rectangle_id = rectangles_on_canvas[j]
                    rect_x0, rect_y0, rect_x1, rect_y1 = self.canvas.coords(rectangle_id)  # Retrieve the coordinates of the rectangle
                    fill_color = self.canvas.itemcget(rectangle_id, 'fill')  # Retrieve fill color of the rectangle from the canvas

                    #Construct an SVG <rect> element for rectangles
                    if self.canvas.itemcget(rectangle_id, 'outline') == 'black':
                        svg_element = '<rect x="{}" y="{}" width="{}" height="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0)
                    else:
                        svg_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, fill_color)

                    # Write the SVG representation of the rectangle to the file
                    f.write(svg_element)

                
                #Iterate through all text elements up to the current layer and create SVG text
                for j in range(min(len(labels_on_canvas), i+1)):
                    text_id = labels_on_canvas[j]
                    label_x, label_y = self.canvas.coords(text_id)  # Retrieve the coordinates of the text
                    text_content = self.canvas.itemcget(text_id, 'text')  # Retrieve text content from the canvas

                    # Construct an SVG <text> element for text
                    svg_text_element = '<text x="{}" y="{}" fill="black" font-size="8" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(label_x+5, label_y, text_content)

                    # Write the SVG representation of the text to the file
                    f.write(svg_text_element)
                
                #Iterate through all arrow_lines up to the current layer and create SVG lines
                for j in range(min(len(arrows_on_canvas), i+1)):
                    arrow_id = arrows_on_canvas[j]
                    arrow_coords = self.canvas.coords(arrow_id)  # Retrieve the coordinates of the arrow

                    # Construct an SVG <line> element for arrows
                    svg_arrow_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black" />\n'.format(arrow_coords[0], arrow_coords[1], arrow_coords[2], arrow_coords[3])

                    # Write the SVG representation of the arrow to the file
                    f.write(svg_arrow_element)

                    

                #Write the closing SVG tag to the file, completing the SVG file
                f.write('</svg>\n')
            
                # #Close the svg file
                f.close()


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