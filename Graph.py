import tkinter
from tkinter import messagebox
import customtkinter
import settings
import globals
from matplotlib.figure import Figure                            #For creating graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #For creating graphs
import numpy



class Graph:
    def __init__(self, program_window):
        # print("CLASS: GRAPH_INIT()")
        
        self.program_window = program_window

        self.graph = self.create_graph_canvas()


    """Creates a figure/canvas where the graph can be drawn"""
    def create_graph_canvas(self):
        # print("CREATE_GRAPH()")

        #Create an overall container for any created plots/graphs
        if not hasattr(self, 'graph_container'):
            self.graph_container = Figure(
                # figsize=(6, 4),       #Figure size of 600x400 pixels
                dpi=settings.graph_resolution    #Resolution of the graph. Higher number = more detailed graph
            )


        #Create a matplotlib widget that is compatible with Tkinter to be able to render a graph.
        if not hasattr(self, 'graph_translator'):
            self.graph_translator = FigureCanvasTkAgg(
                self.graph_container, 
                master=self.program_window,
            )
            self.graph_translator.get_tk_widget().grid(
                row=0,
                column=2,
                sticky="nsew",
                padx=(1,1),
                pady=(1,1),
            )

        
        
        #Adjust the margins around the plot
        # self.graph_container.subplots_adjust(left=0.3, right, top, bottom)

        #Create details in graph
        #Explanation of digits: (1)Number of rows in the grid, (2) number of columns in the grid, (3)position of this subplot within the grid (counting starts from 1 in the top-left)
        graph = self.graph_container.add_subplot(111)  

        #Make each side of the graph equal, making the graph a square
        graph.set_aspect('equal')
        
        #Set labels for the graph
        # self.graph.set_title("This is a simple graph")
        graph.set_xlabel("X [mm]", fontsize=10, labelpad=3)
        graph.set_ylabel("Height [μm]", fontsize=10, labelpad=-5)
        
        #Set the display limits of the x and y axises 
        graph.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])

        graph.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])
        
        #Display the grid of the graph
        graph.grid(True)
        
        #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        graph.axhline(0, color="black", linewidth=1)
        graph.axvline(0, color="black", linewidth=1)

        ########## THIS IS A WORK AROUND TO MAKE THE GRAPH RESIZE TO PROPERLY FIT THE WINDOW ##########
        self.program_window.update()
        #Upscale and downscale the program window so that the graph adjusts properly  
        self.program_window.geometry(f"{self.program_window.winfo_width()+1}x{self.program_window.winfo_height()+1}")
        self.program_window.geometry(f"{self.program_window.winfo_width()-1}x{self.program_window.winfo_height()-1}")
        ########## END OF WORK AROUND ##########

        return graph


    """Draws the graph with materials that are "active" in the materials dictionary"""
    def draw_graph(self):
        # print("DRAW_GRAPH()")

        #Clear the graph
        self.graph.clear()

        #Create details in graph
        #Set labels for the graph
        # self.graph.set_title("This is a simple graph")
        self.graph.set_xlabel("X [mm]", fontsize=10, labelpad=3)
        self.graph.set_ylabel("Height [μm]", fontsize=10, labelpad=-5)
        
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
        chosen_material = None
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
            return
        
        if(chosen_material == None):
            messagebox.showerror("No filament selected", f"Please select a filament")
            return




        #Fetch necessary values
        #Es = modulus for the substrate (multiplied by 1billion)
        Es = globals.materials[substrate_material]["Modulus [GPa]"] * 1000000000
        #Vs = poisson til substratet
        Vs = globals.materials[substrate_material]["Poisson"]
        #Ts = thickness for the substrate in nanometers (value divided by 1billion)
        Ts = globals.materials[substrate_material]["Thickness"] / 1000000000
        #Tf = thickness for material/filament in nanometers (value divided by 1billion)
        Tf = globals.materials[chosen_material]["Thickness"] / 1000000000
        #R0 = R0 til filamentet
        R0 = globals.materials[chosen_material]["R0"]
        #R = R til materialet/filament
        R = globals.materials[chosen_material]["R"]


        #Check for division by zero errors
        if(Tf) == 0:
            messagebox.showerror("Division by zero Error", f"The 'thickness' of '{chosen_material}' can not be zero")
            return
        if(R == 0):
            messagebox.showerror("Division by zero Error", f"The 'R' value for '{chosen_material}' can not be zero")
            return
        if(R0 == 0):
            messagebox.showerror("Division by zero Error", f"The 'R0' value for '{chosen_material}' can not be zero")
            return
        if(1-Vs) == 0:
            messagebox.showerror("Division by zero Error", "The calculation (1 - Vs) resulted in zero")
            return
        if(6* (1-Vs) *Tf) == 0:
            messagebox.showerror("Division by zero Error", "The calculation: '6*(1-Vs) *Tf' resulted in zero")
            return
        
        #Calculate the sigma_R value
        sigma_R = ( (Es* (Ts**2)) / (6*(1-Vs)*Tf)) * ( (1/R) - (1/R0) )
        #Convert to correct value
        sigma_R = sigma_R/1000000
        #Limit value to 2 decimals
        sigma_R = round(sigma_R, 2)

        #Display the sigma_R value in the graph
        self.graph.text(
            0.50, 1.10,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"σR = {sigma_R}MPa",                      # Text
            transform=self.graph.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=12,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )

        #Display the R0 value in the graph
        self.graph.text(
            0.00, 1.20,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"R0 = {R0}",                         # Text
            color="blue",
            transform=self.graph.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=12,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )

        #Display the R value in the graph
        self.graph.text(
            0.00, 1.10,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"R = {R}",                      # Text
            color="red",
            transform=self.graph.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=12,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )

        #Create a  range of X values 
        x_values = numpy.linspace(-min(R, R0), min(R, R0), 100)

        #Plot the following values in the graph
            # y0 = sqrt((R0**2) - (x**2)) 
            # y1 = sqrt((R**2) - (x**2)) 

        #calculate values for y1 and y0
        # y0 = numpy.sqrt((R0**2) - (x_values**2))
        # y1 = numpy.sqrt((R**2) - (x_values**2))


        y0 = R0 - numpy.sqrt(R0**2 - x_values**2)
        y1 = R - numpy.sqrt(R**2 - x_values**2)



        #Plot y1 and y0 values
        self.graph.plot(x_values, y0, color="red")
        self.graph.plot(x_values, y1, color="blue")

        # # #Add a legend???????
        # # # self.graph.legend()

        # # Redraw the canvas to display the updates
        # self.graph.figure.canvas.draw()

        #Draw the created elements in the graph
        self.graph_translator.draw()
    