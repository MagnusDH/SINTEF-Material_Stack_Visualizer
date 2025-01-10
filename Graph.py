import tkinter
from tkinter import messagebox
import customtkinter
import settings
import globals

from matplotlib.figure import Figure                            #For creating graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #For creating graphs
import numpy

class Graph:
    def __init__(self, window):
        # print("CLASS: GRAPH_INIT()")
        
        self.window = window

        self.create_graph_canvas()

        # self.x_values = numpy.linspace(-50, 50, 100)  #Generate 100 evenly values from -50 to 50



    """Creates a figure/canvas where the graph can be drawn"""
    def create_graph_canvas(self):
        # print("CREATE_GRAPH()")

        #Create a drawing space for the graph
        self.graph_canvas = Figure(
            figsize=(settings.graph_width/100, settings.graph_height/100),
            dpi=settings.graph_dpi
        )

        #Create a "figure/translator" so that matplotlib can render in tkinter GUI
        self.graph_translator = FigureCanvasTkAgg(self.graph_canvas, master=globals.main_frame)
        self.graph_translator.get_tk_widget().grid(
            row=0,
            column=2,
            sticky="nw",
            padx=(5,0),
            pady=(5,0)
        )

        #Create details in graph
        #Explanation of digits: (1)Number of rows in the grid, (2) number of columns in the grid, (3)position of this subplot within the grid (counting starts from 1 in the top-left
        self.graph = self.graph_canvas.add_subplot(111)    

        #Set labels for the graph
        # self.graph.set_title("This is a simple graph")
        self.graph.set_xlabel("X")
        self.graph.set_ylabel("Y")
        
        #Set the display limits of the x and y axises 
        self.graph.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])
        self.graph.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])

        #Display the grid of the graph
        self.graph.grid(True)

        #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.graph.axhline(0, color="black", linewidth=1)
        self.graph.axvline(0, color="black", linewidth=1)


    """Draws the graph with materials that are "active" in the materials dictionary"""
    def draw_graph(self):
        # print("DRAW_GRAPH()")

        #Clear the graph
        self.graph.clear()

        #Create details in graph
        #Set labels for the graph
        # self.graph.set_title("This is a simple graph")
        self.graph.set_xlabel("X")
        self.graph.set_ylabel("Y")
        
        #Set the display limits of the x and y axises 
        self.graph.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])
        self.graph.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])

        #Display the grid of the graph
        self.graph.grid(True)

        #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.graph.axhline(0, color="black", linewidth=1)
        self.graph.axvline(0, color="black", linewidth=1)

        #Fetch the correct materials by checking which are "active"
        material_counter = 0
        for material in globals.materials:
            if(material.lower() == "substrate"):
                substrate_material = material
                continue     #Skip to next material

            if(globals.materials[material]["Status"] == "active"):
                chosen_material = material
                material_counter += 1
        
        #Raise error if there are more than two selected materials/filaments
        if(material_counter > 1):
            print("ERROR: MORE THAN TWO FILAMENTS SELECTED!!!!!!!!!")

        #Fetch necessary values
        #Es = modulus til substratet
        Es = globals.materials[substrate_material]["Modulus [GPa]"]
        #Vs = poisson til substratet
        Vs = globals.materials[substrate_material]["Poisson"]
        #Ts = tykkelse til substratet
        Ts = globals.materials[substrate_material]["Thickness"]
        #Tf = tykkelse til gitt materiale/filament
        Tf = globals.materials[chosen_material]["Thickness"]
        #R0 = R0 til substratet
        R0 = globals.materials[substrate_material]["R0"]
        #R = R til materialet/filament
        R = globals.materials[chosen_material]["R"]

        #Check for division by zero errors
        if(Tf) == 0:
            messagebox.showerror("Division by zero Error", "The 'thickness' of a filament can not be zero")
            return
        if(R == 0):
            messagebox.showerror("Division by zero Error", "The 'R' value for chosen filament can not be zero")
            return
        if(R0 == 0):
            messagebox.showerror("Division by zero Error", "The 'R0' value for 'substrate' can not be zero")
            return
        if(6* (1-Vs) *Tf) == 0:
            messagebox.showerror("Division by zero Error", "The calculation: '6*(1-Vs) *Tf' resulted in zero")
            return
        
        #Calculate the sigma_R value
        sigma_R = ( (Es* (Ts**2)) / (6*(1-Vs)*Tf)) * ( (1/R) - (1/R0) )
        
        #Display the sigma_R value in the graph
        self.graph.text(
            0.0, 1.1,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"σR = {sigma_R}",                      # Text
            transform=self.graph.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=12,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )

        #Display the R0 value in the graph
        self.graph.text(
            0.05, 0.98,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"R0 = {R0}",                         # Text
            color="blue",
            transform=self.graph.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=12,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )

        #Display the R value in the graph
        self.graph.text(
            0.05, 0.90,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"R = {R}",                      # Text
            color="red",
            transform=self.graph.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=12,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )



        #Plot the following values in the graph
            # y1 = sqrt((R**2) - (x**2)) 
            # y0 = sqrt((R0**2) - (x**2)) 

        #Create a  range of X values 
        x_values = numpy.linspace(-min(R, R0), min(R, R0), 100)

        #calculate values for y1 and y0
        y0 = numpy.sqrt((R0**2) - (x_values**2))
        y1 = -numpy.sqrt((R**2) - (x_values**2))

        #Plot y1 and y0 values
        self.graph.plot(x_values, y0, label=r"$y_0 = \sqrt{R_0^2 - x^2}$", color="red")
        self.graph.plot(x_values, y1, label=r"$y_1 = -\sqrt{R^2 - x^2}$", color="blue")

        #Add a legend???????
        # self.graph.legend()

        # Redraw the canvas to display the updates
        # self.graph.figure.canvas.draw()

        #Draw the created elements in the graph
        self.graph_translator.draw() 
    