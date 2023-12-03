import tkinter as tk
from tkinter import Canvas, Scale, HORIZONTAL, Frame, Entry, StringVar, Label, Button
from PIL import ImageGrab, Image
import pandas as pd
import pygetwindow
import pyautogui

"""
To do:    
    *Fix "export figure" button to only export the drawn figure, not the whole screen 

    *Create "export all" button to export several figures of each layer in an incremental order
"""

class App:
    def __init__(self, window):
        
        #SETTINGS
        self.app_title = "Material Measurements"
        self.window_width = 800                     #Start width of app window
        self.window_height = 800                    #Start height of app window
        self.material_min_thickness = 0             #Minimum thickness of materials
        self.material_max_thickness = 3000          #Maximum thickness of materials
        self.excel_file = "Materials.xlsx"          #Excel-file to load materials from

        #Dictionary for all materials. KEY: "material_name" ---VALUES: list of [thickness, color]
        self.materials = {}
         

    """Runs the application by:
        -Creating the main canvas/window
        -Creating sliders, color boxes, input boxes and export button
        -Drawing the rectangle stack for each material"""
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
        self.create_canvas(self.window_width-4, self.window_height-4)       

        #Create export button which calls "export_as_jpg" function
        self.export_button = Button(self.slider_frame, text="Export as JPG", command=self.export_as_jpg)
        self.export_button.grid(row=len(self.materials), columnspan=4, pady=10)

        #Draw the material stack
        self.draw_rectangle_stack()


    """Creates a canvas based on the given width/height variables"""
    def create_canvas(self, canvas_width, canvas_height):
        self.canvas = Canvas(self.window, width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=1, sticky="n")


    """Creates sliders, input and color boxes based on the number of materials in self.materials"""
    def create_user_interface(self):

        #Create frame within the main window to contain sliders, color&input widgets
        self.slider_frame = Frame(self.window)
        self.slider_frame.grid(row=0, column=0, padx=10, pady=10, sticky='n')
        
        #Create color boxes, sliders, input boxes and labels
        i = 0 #Row counter
        for material in self.materials:

            #Create color boxes and place them on grid
            color_box = Label(self.slider_frame, bg=self.materials[material][1], width=2)                                                                           #Creation of color box in the slider frame
            color_box.grid(row=i, column=0, padx=5, pady=5, sticky='n')                                                                                             #Color box placement
            
            #Create sliders
            slider = Scale(self.slider_frame, from_=self.material_min_thickness, to=self.material_max_thickness, orient=HORIZONTAL, label=material, resolution=1)   #Creation of slider in the slider frame
            slider.grid(row=i, column=1, pady=5, padx=5)                                                                                                            #Slider placement
            slider.set(self.materials[material][0])                                                                                                                 #Set the initial value of the slider
            slider.bind("<Motion>", lambda event, s=slider: self.slider_updated(event, s))                                                                          #listens to motion on the sliders

            #Create input boxes
            height_var = StringVar(value=str(self.materials[material][0]))
            entry = Entry(self.slider_frame, textvariable=height_var, width=6)                                                                                      #Creation of entry box in the slider frame
            entry.grid(row=i, column=2, padx=5)                                                                                                                     #Entry box placement
            entry.bind("<Return>", lambda event, s=slider, e=entry: self.entry_updated(event, e, s))                                                                #Listens to updates in the entry/input box
            
            #Create "nm" label next to slider
            nm_label = Label(self.slider_frame, text="nm")                                                                                                          #Creation of label in the slider frame
            nm_label.grid(row=i, column=3)                                                                                                                          #Label placement

            #Increment row-counter
            i += 1


    """
    -Is called if the slider is adjusted
    -Updates the self.materials dictionary with the new slider value for its corresponding material
    -Calls draw_rectangle_stack to redraw the rectangle stack with the new value"""
    def slider_updated(self, event, slider):

        #Get the new value of the slider
        slider_value = slider.get()
        
        #Check if slider value is acceptable
        if self.material_min_thickness <= slider_value <= self.material_max_thickness:
            slider_name = slider.cget("label")              #Get the label/name of the slider                
            self.materials[slider_name][0] = slider_value   #Assign the value of the slider to its position in the materials dictionary
            self.draw_rectangle_stack()                     #Redraw the rectangle stack with the new value

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


    """Draws rectangles in the rectangle stack for each material in self.materials"""
    def draw_rectangle_stack(self):
        #Clear all existing rectangles
        self.canvas.delete("all")
        
        #Draw lines aorund canvas (top left x,y MUST be 2,2
        self.canvas.create_line(2,2, self.canvas.winfo_reqwidth(), 2, fill="green")
        self.canvas.create_line(2,2, 2, self.canvas.winfo_reqheight(), fill="black")
        self.canvas.create_line(2, self.canvas.winfo_reqheight()-3, self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()-3, fill="blue")        
        self.canvas.create_line(self.canvas.winfo_reqwidth()-3,2, self.canvas.winfo_reqwidth()-3, self.canvas.winfo_reqheight()-3, fill="black")

        #Main drawing point of stack and width of stack 
        rectangle_x0 = 2        #Top-left X-coordinate of rectangle
        rectangle_y0 = 2        #Top-left Y-coordinate of rectangle       
        rectangle_x1 = self.canvas.winfo_reqwidth() - 3    #Bottom-right X-coordinate of rectangle (leave a little space for text
        rectangle_y1 = self.canvas.winfo_reqheight() - 3                     #Bottom-right Y-coordinate of rectangle
       
        #Scaling factor decides the size of each rectangle when drawn. The current algorithm ensures that the rectangle stack is not drawn out of bounds 
        scaling_factor = (self.canvas.winfo_reqheight()/self.material_max_thickness)/len(self.materials)
        
        #Loop through all the materials and draw rectangle and labels for each
        for material in self.materials:
            rectangle_height = int(self.materials[material][0]) * scaling_factor        #How tall the rectangle should be drawn, adjusted by the scaling factor (thickness * scaling_factor)

            #Draw rectangles on top of the other
            rectangle_y0 = rectangle_y1 - rectangle_height
            self.canvas.create_rectangle(rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, fill=self.materials[material][1])  # Draw rectangle and fill it with a color

            #if the rectangle height is big enoug, draw text in middle of rectangle
            if(rectangle_height >=30):
                label_text = str(material) + "\n" + str(self.materials[material][0]) + "nm"                                             #Text to be written
                label_x_pos = (rectangle_x0 + rectangle_x1) / 2                                                                         #X-position of label
                label_y_pos = (rectangle_y0 + rectangle_y1) / 2                                                                         #Y-position of label
                self.canvas.create_text(label_x_pos, label_y_pos, text=label_text, fill="black", font=("Arial", 8), anchor="center")    #Creation of text

            #if the rectangle height is to low to display text, draw text on side of box
            else:
                label_text = str(material) + "\n" + str(self.materials[material][0]) + "nm"                                             #Text to be written
                label_x_pos = rectangle_x1 - 30                                                                                         #Text x-position (minus 30 to leave a little space on the side)
                label_y_pos = (rectangle_y0 + rectangle_y1) / 2                                                                         #Text y-position
                self.canvas.create_text(label_x_pos, label_y_pos, text=label_text, fill="black", font=("Arial", 8), anchor="center")    #Creation of text

            rectangle_y1 = rectangle_y0


    """Calls draw_rectangle_stack when the program window is adjusted"""
    def window_resized(self, event):        

        #Create the new canvas sizes        
        new_canvas_width = self.window.winfo_width() - 270      #Subtract 270 because the slider_frame is 237 pixels
        new_canvas_height = self.window.winfo_height() - 10     #Subtract 10 to keep a little space in the bottom of the window

        #Apply the new dimensions for the canvas
        self.canvas.config(width = new_canvas_width, height = new_canvas_height)

        #Redraw the rectangle stack based on the new width and height of the program window
        self.draw_rectangle_stack()


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


    """
    -Gets coordinates from open window
    -Uses coordniates to take screenshot and save it as .jpg"""
    def export_as_jpg(self):
        
        #Get window of app
        window = pygetwindow.getWindowsWithTitle(self.app_title)[0]

        #Get current positions of open window
        window_x0_pos, window_y0_pos = window.topleft
        window_x1_pos, window_y1_pos = window.bottomright

        """Ny mate a gjore det pa:
            -Finn topLeft koordinater til åpent vindu
                -Legg til vidden til slider frame for å finne start på rectangle stack
                -Legg til enten: bredden på det lille røde på vinduet eller hele veien ned til toppen av rectangle stack

            -Finn bottomRight koordinater til åpent vindu
                -trekk fra den lille delen som er hvit fra bunnen av vinduet til der rectangle stack starter
                -Trenger kanskje ikke trekke fra det hvite fra høyre side fordi teksten må være her?

            -Ta screenshot med nye koordinater    
        """

        #Find width of slider frame
        # slider_frame_width = self.slider_frame.winfo_reqwidth()
        
        # #FIX THE ADDED VALUES AT THE END OF EACH COORDINATE!!!!!!!!!!!
        # #Find TopLeft coordinates of rectangle stack based on where the open window is
        # rec_stack_x0 = window_x0_pos + slider_frame_width + 30
        # rec_stack_y0 = window_y0_pos + 39

        # #Find BottomRight coordinates of rectangle stack based on where the open window is
        # rec_stack_x1 = window_x0_pos + slider_frame_width + self.rectangle_stack_width + 100
        # rec_stack_y1 = window_y0_pos + self.canvas_height + 100
        
        #Use the (x0,y0)(x1,y1) coordinates to screenshot the entire rectangle stack
        screenshot = ImageGrab.grab(bbox = (rec_stack_x0, rec_stack_y0, rec_stack_x1, rec_stack_y1))
        
        #Save screenshot as .jpg
        screenshot.save("All_Materials.jpg")


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