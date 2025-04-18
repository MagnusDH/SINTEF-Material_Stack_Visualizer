import tkinter
from tkinter import messagebox
import customtkinter
import settings
import globals
from matplotlib.figure import Figure                            #For creating graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #For creating graphs
import numpy
import helper_functions
from matplotlib.patches import FancyArrowPatch


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

        #Create subplots for graphs
        #Explanation of digits: (1)Number of rows in the grid, (2) number of columns in the grid, (3)position of this subplot within the grid (counting starts from 1 in the top-left)
        self.graph1 = self.graph_container.add_subplot(211)  
        self.graph2 = self.graph_container.add_subplot(212)  

        #Adjust the margins around the plots
        self.graph_container.subplots_adjust(
            left=0.2,     # Move plots to the right (default ~0.125)
            right=0.95,   # Leave space on the right
            top=0.95,     # Leave space at the top
            bottom=0.05    # Leave space at the bottom
        )

        #Set the display limits of the x and y axises 
        self.graph1.set_xlim([-100, 100])
        self.graph1.set_ylim([-100, 100])

        self.graph2.set_xlim([-100, 100])
        self.graph2.set_ylim([-100, 100])
        
        # #Display the grid of the graph
        self.graph1.grid(True)
        self.graph2.grid(True)

        
        #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.graph1.axhline(0, color="black", linewidth=1)
        self.graph1.axvline(0, color="black", linewidth=1)

        self.graph2.axhline(0, color="black", linewidth=1)
        self.graph2.axvline(0, color="black", linewidth=1)


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
        self.graph1.clear()

        #Set labels for the graph
        # self.graph.set_title("This is a simple graph")
        self.graph1.set_xlabel("X [mm]", fontsize=10, labelpad=3)
        self.graph1.set_ylabel("Height [μm]", fontsize=10, labelpad=-5)
        
        # #Set the display limits of the x and y axises 
        self.graph1.set_xlim([settings.stoney_graph_x_axis_range_min, settings.stoney_graph_x_axis_range_max])
        self.graph1.set_ylim([settings.stoney_graph_y_axis_range_min, settings.stoney_graph_y_axis_range_max])

        # #Display the grid of the graph
        self.graph1.grid(True)

        # #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.graph1.axhline(0, color="black", linewidth=1)
        self.graph1.axvline(0, color="black", linewidth=1)

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
        self.graph1.text(
            -0.0, 1.15,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"R0 = {R0}",                         # Text
            color="blue",
            transform=self.graph1.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=10,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )

        #Display the R value in the graph
        self.graph1.text(
            0.3, 1.15,
            f"R = {R}",                     
            color="red",
            transform=self.graph1.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(facecolor='white', alpha=0.5)
        )

        self.graph1.text(
            0.6, 1.15,
            f"σR = {sigma_R}MPa",
            transform=self.graph1.transAxes,
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
        self.graph1.plot(x_values, y0, color="red")
        self.graph1.plot(x_values, y1, color="blue")

        # # Redraw the canvas to display the updates (check if this draws only this graph)
        self.graph1.figure.canvas.draw()

        #Draw the created elements in the graph (check if this draws both of the graphs)
        # self.graph_translator.draw()


    def draw_z_tip_is_graph(self):
        """
        -Draws the 'z_tip_is' graph
        """
        # Clear the graph
        self.graph1.clear()
    
        # Fetch the 'L' value from new_panel
        L = helper_functions.convert_decimal_string_to_float(globals.new_panel.L_value.get())
        
        if(L == 0 or L == False):
            messagebox.showerror("ERROR", "'L [μm]' entry can not be zero or empty")
            return None
    
        # Set labels for the graph
        self.graph1.set_title("Cantilever bending")
        self.graph1.set_xlabel("X [μm]", fontsize=10, labelpad=3)
        self.graph1.set_ylabel("Tip displacement [μm]", fontsize=10, labelpad=8)
        
        # Set display limits of the x axis
        self.graph1.set_xlim([settings.z_tip_is_graph_x_axis_range_min, L*1.05])
        
        # -- Calculate the x and y values first --
        x_values = numpy.linspace(0, L, 100)
        y_values = []
        for x in x_values:
            y = globals.equations.calculate_tip_placement(x)
            y_values.append(y)
        
        # Get the tip displacement (last y value)
        y_tip = y_values[-1]
        
        # Adjust the y-axis limits based on the tip displacement:
        if y_tip >= 0:
            # For positive tip displacement, initial upper limit is 25
            y_limit = 25
            if y_tip > y_limit:
                y_limit = 100  # increase to 50 if tip exceeds 25
                while y_tip > y_limit:
                    candidate = y_limit * 2
                    if candidate > 100:
                        y_limit = globals.equations.calculate_tip_placement(L) * 1.05
                        break
                    else:
                        y_limit = candidate
            # Use the settings value for the lower limit (often 0) 
            self.graph1.set_ylim([settings.z_tip_is_graph_y_axis_range_min, y_limit])
        else:
            # For negative tip displacement, initial lower limit is -25
            y_limit = -25
            if y_tip < y_limit:
                y_limit = -100  # decrease to -50 if tip is lower than -25
                while y_tip < y_limit:
                    candidate = y_limit * 2  # doubling a negative number doubles its magnitude
                    if abs(candidate) > 100:
                        y_limit = globals.equations.calculate_tip_placement(L) * 1.05
                        break
                    else:
                        y_limit = candidate
            # Set ylim so that the upper bound comes from settings (often 0)
            self.graph1.set_ylim([y_limit, settings.z_tip_is_graph_y_axis_range_min])
    
        # Display the grid on the graph
        self.graph1.grid(True)
        
        # Display the x and y axis lines in the grid
        self.graph1.axhline(0, color="black", linewidth=1)
        self.graph1.axvline(0, color="black", linewidth=1)
    
        # Plot the curve
        self.graph1.plot(x_values, y_values, color="k")
    
        # Get the highest x and y values for the tip marker
        x_tip = x_values[-1]
        y_tip = y_values[-1]
    
        # Create an arrow to show the height of the curve
        height_arrow = FancyArrowPatch(
            (x_tip, 0),       # start point (on x-axis)
            (x_tip, y_tip),   # end point (at tip of curve)
            arrowstyle='<->', # arrowheads on both ends
            color='k',
            linewidth=1.5,
            mutation_scale=10  # size of the arrowheads
        )
        self.graph1.add_patch(height_arrow)
    
        # Add text to show the height
        self.graph1.text(
            0.95*x_tip, (0 + y_tip) / 2,
            f"{round(y_tip,1)}",
            fontsize=9,
            color='k',
            va='center',
            bbox=dict(facecolor='white', edgecolor='k', boxstyle='round,pad=0.5')
        )
    
        # Draw the canvas to display the updates
        self.graph1.figure.canvas.draw()
