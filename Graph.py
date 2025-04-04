import tkinter
from tkinter import messagebox
import customtkinter
import settings
import globals
from matplotlib.figure import Figure                            #For creating graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #For creating graphs
import numpy


class Graph:
    def __init__(self, program_window, row_placement:int, column_placement:int):
        # print("CLASS: GRAPH_INIT()")
        
        self.program_window = program_window

        #Row/column placement in main program window
        self.row_placement = row_placement
        self.column_placement = column_placement

        self.graph_translator = self.create_graph_canvas()


    def create_graph_canvas(self):
        """Creates a figure/canvas where the graph can be drawn"""
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
                row=self.row_placement,
                column=self.column_placement,
                sticky="nsew",
                padx=(settings.graph_padding_left, settings.graph_padding_right),
                pady=(settings.graph_padding_top, settings.graph_padding_bottom),
            )

        
        
        #Adjust the margins around the plot
        # self.graph_container.subplots_adjust(left=0.3, right, top, bottom)

        # #Create details in graph
        # #Explanation of digits: (1)Number of rows in the grid, (2) number of columns in the grid, (3)position of this subplot within the grid (counting starts from 1 in the top-left)
        self.stoney_graph = self.graph_container.add_subplot(211)  
        self.stress_graph = self.graph_container.add_subplot(212)  

        # self.graph_container.tight_layout()


        # #Make each side of the graph equal, making the graph a square
        # stoney_graph.set_aspect('equal')
        
        # #Set labels for the graph
        # # self.graph.set_title("This is a simple graph")
        # graph.set_xlabel("X [mm]", fontsize=10, labelpad=3)
        # graph.set_ylabel("Height [μm]", fontsize=10, labelpad=-5)
        
        #Set the display limits of the x and y axises 
        self.stoney_graph.set_xlim([settings.stoney_graph_x_axis_range_min, settings.stoney_graph_x_axis_range_max])
        self.stoney_graph.set_ylim([settings.stoney_graph_y_axis_range_min, settings.stoney_graph_y_axis_range_max])

        self.stress_graph.set_xlim([settings.stress_graph_x_axis_range_min, settings.stress_graph_x_axis_range_max])
        self.stress_graph.set_ylim([settings.stress_graph_y_axis_range_min, settings.stress_graph_y_axis_range_max])
        
        # #Display the grid of the graph
        self.stoney_graph.grid(True)
        self.stress_graph.grid(True)

        
        #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.stoney_graph.axhline(0, color="black", linewidth=1)
        self.stoney_graph.axvline(0, color="black", linewidth=1)

        self.stress_graph.axhline(0, color="black", linewidth=1)
        self.stress_graph.axvline(0, color="black", linewidth=1)

        #Create legends to display more info about each element in the graph
        # stoney_graph.legend()
        # stress_graph.legend()

        ########## THIS IS A WORK AROUND TO MAKE THE GRAPH RESIZE TO PROPERLY FIT THE WINDOW ##########
        self.program_window.update()
        #Upscale and downscale the program window so that the graph adjusts properly  
        self.program_window.geometry(f"{self.program_window.winfo_width()+1}x{self.program_window.winfo_height()+1}")
        self.program_window.geometry(f"{self.program_window.winfo_width()-1}x{self.program_window.winfo_height()-1}")
        ########## END OF WORK AROUND ##########

        return self.graph_translator


    def draw_stoney_graph(self):
        """Draws the stoney graph with materials that are "active" in the materials dictionary"""
        
        # print("DRAW_STONEY_GRAPH()")

        #Clear the graph
        self.stoney_graph.clear()

        #Set labels for the graph
        # self.graph.set_title("This is a simple graph")
        self.stoney_graph.set_xlabel("X [mm]", fontsize=10, labelpad=3)
        self.stoney_graph.set_ylabel("Height [μm]", fontsize=10, labelpad=-5)
        
        # #Set the display limits of the x and y axises 
        self.stoney_graph.set_xlim([settings.stoney_graph_x_axis_range_min, settings.stoney_graph_x_axis_range_max])
        self.stoney_graph.set_ylim([settings.stoney_graph_y_axis_range_min, settings.stoney_graph_y_axis_range_max])

        # #Display the grid of the graph
        self.stoney_graph.grid(True)

        # #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.stoney_graph.axhline(0, color="black", linewidth=1)
        self.stoney_graph.axvline(0, color="black", linewidth=1)

        #Fetch the correct materials by checking which are "active"
        material_counter = 0
        chosen_material = None
        lowest_material = None
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == 1):
                lowest_material = material
                continue

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
        Es = globals.materials[lowest_material]["Modulus [GPa]"] * 1000000000
        #Vs = poisson til substratet
        Vs = globals.materials[lowest_material]["Poisson"]
        #Ts = thickness for the substrate in nanometers (value divided by 1billion)
        Ts = globals.materials[lowest_material]["Thickness"] / 1000000000
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
            messagebox.showerror("Division by zero Error", f"The 'poisson' value for '{lowest_material}' can not be 1.\nCalculation (1 - Vs) resulted in zero")
            return
        
        #Calculate the sigma_R value
        sigma_R = ( (Es* (Ts**2)) / (6*(1-Vs)*Tf)) * ( (1/R) - (1/R0) )
        #Convert to correct value
        sigma_R = sigma_R/1000000
        #Limit value to 2 decimals
        sigma_R = round(sigma_R, 2)

        #Display the R0 value in the graph
        self.stoney_graph.text(
            -0.0, 1.15,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"R0 = {R0}",                         # Text
            color="blue",
            transform=self.stoney_graph.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=10,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )

        #Display the R value in the graph
        self.stoney_graph.text(
            0.3, 1.15,
            f"R = {R}",                     
            color="red",
            transform=self.stoney_graph.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.5)
        )

        self.stoney_graph.text(
            0.6, 1.15,
            f"σR = {sigma_R}MPa",
            transform=self.stoney_graph.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.5)
        )


        #Create a  range of X values 
        x_values = numpy.linspace(-min(R, R0), min(R, R0), 100)

        #Create values to plot in the graph
        y0 = R0 - numpy.sqrt(R0**2 - x_values**2)
        y1 = R - numpy.sqrt(R**2 - x_values**2)

        #Plot y1 and y0 values
        self.stoney_graph.plot(x_values, y0, color="red")
        self.stoney_graph.plot(x_values, y1, color="blue")

        # # Redraw the canvas to display the updates (check if this draws only this graph)
        self.stoney_graph.figure.canvas.draw()

        #Draw the created elements in the graph (check if this draws both of the graphs)
        # self.graph_translator.draw()


    """????????????????????????????????????????????????"""
    def draw_stress_graph(self):
        print("DRAW_STRESS_GRAPH()")

        #Clear the graph
        self.stress_graph.clear()

        #Set labels for the graph
        # self.stress_graph.set_title("This is a simple graph")
        # self.stress_graph.set_xlabel("X [mm]", fontsize=10, labelpad=3)
        # self.stress_graph.set_ylabel("Height [μm]", fontsize=10, labelpad=-5)
        
        # #Set the display limits of the x and y axises 
        self.stress_graph.set_xlim([settings.stress_graph_x_axis_range_min, settings.stress_graph_x_axis_range_max])
        self.stress_graph.set_ylim([settings.stress_graph_y_axis_range_min, settings.stress_graph_y_axis_range_max])

        # #Display the grid of the graph
        self.stress_graph.grid(True)

        # #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.stress_graph.axhline(0, color="black", linewidth=1)
        self.stress_graph.axvline(0, color="black", linewidth=1)

        #Fetch some values?

        
        #Display some text?
        # self.stress_graph.text(
        #     0.0, 1.15,                              # X and Y Coordinates of the text (relative to axes in percentages)
        #     f"Some example text",                         # Text
        #     color="blue",
        #     transform=self.stress_graph.transAxes,            # Transform to make the coordinates relative to the axes
        #     fontsize=10,                            # Set the font size
        #     verticalalignment='top',                # Align text to the top
        #     bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        # )

        #Create some x_values values? 
        # x_values = numpy.linspace(-min(100, 100), min(100, 100), 100)

        # #Create some y values?
        # y0 = 50 - numpy.sqrt(50**2 - x_values**2)
        # y1 = 60 - numpy.sqrt(60**2 - x_values**2)

        # #Plot some values? 
        # self.stress_graph.plot(x_values, y0, color="red")
        # self.stress_graph.plot(x_values, y1, color="blue")

        # #Redraw the canvas to display the updates (check if this draws only this graph)
        # self.stress_graph.figure.canvas.draw()

        #Draw the created elements in the graph (check if this draws both of the graphs)
        # self.graph_translator.draw()
