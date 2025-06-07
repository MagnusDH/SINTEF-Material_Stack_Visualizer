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


class Graph_Canvas:
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
                padx=(settings.graph_canvas_padding_left, settings.graph_canvas_padding_right),
                pady=(settings.graph_canvas_padding_top, settings.graph_canvas_padding_bottom),
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


        #Adjust the position of graph2
        old_pos = self.graph2.get_position()
        new_pos = [old_pos.x0, old_pos.y0, old_pos.width, old_pos.height-0.1]
        self.graph2.set_position(new_pos)

        #Set the display limits of the x and y axises 
        self.graph1.set_xlim([-100, 100])
        self.graph1.set_ylim([-100, 100])

        self.graph2.set_title("Stoney")
        self.graph2.set_xlabel("X [mm]", fontsize=10, labelpad=3)
        self.graph2.set_ylabel("Height [μm]", fontsize=10, labelpad=8)

        
        #Set the display limits of the x and y axises 
        self.graph2.set_xlim([settings.stoney_graph_x_axis_range_min, settings.stoney_graph_x_axis_range_max])
        self.graph2.set_ylim([settings.stoney_graph_y_axis_range_min, settings.stoney_graph_y_axis_range_max])

        #Display the grid of the graph
        self.graph2.grid(True)

        #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.graph2.axhline(0, color="black", linewidth=1)
        self.graph2.axvline(0, color="black", linewidth=1)
        
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


    #ADD EXPLANATION
    def draw_stoney_graph(self):
        """
        
        """
        # print("DRAW_STONEY_GRAPH()")


        # print("DRAW_STONEY_GRAPH()")
        try:
            #Clear the graph
            self.graph2.clear()

            #Check for errors
            if(len(globals.materials) == 0):
                raise ValueError("No materials")

            if(globals.stoney_substrate.get()==""):
                raise ValueError("No substrate selected")
            
            if(globals.stoney_filament.get()==""):
                raise ValueError("No filament selected")

        
            #Set labels for the graph
            self.graph2.set_title("Stoney")
            self.graph2.set_xlabel("X [mm]", fontsize=10, labelpad=3)
            self.graph2.set_ylabel("Height [μm]", fontsize=10, labelpad=8)

            #Display the grid of the graph
            self.graph2.grid(True)

            #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
            self.graph2.axhline(0, color="black", linewidth=1)
            self.graph2.axvline(0, color="black", linewidth=1)

            #Fetch necessary values
            #Modulus value for substrate in pascals
            Es = globals.materials[globals.stoney_substrate.get()]["Modulus [GPa]"].get() * 1000000000
            #Poisson value for substrate
            Vs = globals.materials[globals.stoney_substrate.get()]["Poisson"].get()
            #Thickness for substrate in meters
            Ts = globals.materials[globals.stoney_substrate.get()]["Thickness [nm]"].get() / 1000000000
            
            #Thickness for filament in meters
            Tf = globals.materials[globals.stoney_filament.get()]["Thickness [nm]"].get() / 1000000000
            #R0 value for filament
            R0 = globals.materials[globals.stoney_filament.get()]["R0"].get()
            #R value for filament
            R = globals.materials[globals.stoney_filament.get()]["R"].get()


            #Check for division by zero errors
            if(Tf) == 0:
                raise ValueError(f"The 'thickness' of '{globals.stoney_filament.get()}' can not be zero")

            if(R == 0):
                raise ValueError(f"The 'R' value for '{globals.stoney_filament.get()}' can not be zero")

            if(R0 == 0):
                raise ValueError(f"The 'R0' value for '{globals.stoney_filament.get()}' can not be zero")
            
            if(1-Vs) == 0:
                raise ValueError(f"The 'poisson' value for '{globals.stoney_substrate.get()}' can not be 1")
            
            #Calculate the sigma_R value
            sigma_R = ( (Es* (Ts**2)) / (6*(1-Vs)*Tf)) * ( (1/R) - (1/R0) )
            #Convert to correct value ????? which unit????
            sigma_R = sigma_R/1000000
            #Limit value to 2 decimals
            sigma_R = round(sigma_R, 2)

            #Display the R0 value in the graph
            self.graph2.text(
                0.0, -0.25,                              # X and Y Coordinates of the text (relative to axes in percentages)
                f"R0 = {R0}",                         # Text
                color="blue",
                transform=self.graph1.transAxes,            # Transform to make the coordinates relative to the axes
                fontsize=10,                            # Set the font size
                verticalalignment='top',                # Align text to the top
                bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
            )

            #Display the R value in the graph
            self.graph2.text(
                0.3, -0.25,
                f"R = {R}",                     
                color="red",
                transform=self.graph1.transAxes,
                fontsize=10,
                verticalalignment='top',
                bbox=dict(facecolor='white', alpha=0.5)
            )

            self.graph2.text(
                0.6, -0.25,
                f"σR = {sigma_R}MPa",
                transform=self.graph1.transAxes,
                fontsize=10,
                verticalalignment='top',
                bbox=dict(facecolor='white', alpha=0.5)
            )

            #Create a  range of X values 
            x_values = numpy.linspace(-min(R, R0), min(R, R0), 100)

            #Create values to plot in the graph
            y0 = self.stoney(R0, x_values)
            y1 = self.stoney(R, x_values)
            
            #Set the display limits of the x and y axises 
            self.graph2.set_xlim([settings.stoney_graph_x_axis_range_min, settings.stoney_graph_x_axis_range_max])
            # self.graph2.set_ylim([0, max(self.stoney(R0,settings.stoney_graph_y_axis_range_min), self.stoney(R,settings.stoney_graph_y_axis_range_max))])
            self.graph2.set_ylim([0, max(self.stoney(R0,25), self.stoney(R,25))])


            #Plot y1 and y0 values
            self.graph2.plot(x_values, y0, color="red")
            self.graph2.plot(x_values, y1, color="blue")

            #Redraw the canvas to display the updates (check if this draws only this graph)
            self.graph2.figure.canvas.draw()
        
        except Exception as error:
            #Clear the graph
            self.graph2.clear()

            #Add error text
            self.graph2.text(
                0.5, 0.5,
                f"Could not draw Stoney graph\n\n{error}",
                fontsize=9,
                color="red",
                transform=self.graph2.transAxes,
                ha="center",
                va="center"
            )

            #Draw the canvas to display the updates
            self.graph2.figure.canvas.draw()

    def stoney(self, R0, x):
        return R0 - numpy.sqrt(R0**2 - x**2)


    def draw_z_tip_is_graph(self):
        """
        -Draws the 'z_tip_is' graph
        """

        # print("DRAW_Z_TIP_IS_GRAPH()")
        

        try:
            #Clear the graph
            self.graph1.clear()

            #Check for errors
            if(len(globals.materials) == 0):
                raise ValueError("No materials")

            if(globals.piezo_material_name.get() == ""):
                raise ValueError("No Piezo material selected")


            
            #Set labels for the graph
            self.graph1.set_title("Cantilever bending")
            self.graph1.set_xlabel("X [μm]", fontsize=10, labelpad=3)
            self.graph1.set_ylabel("Tip displacement [μm]", fontsize=10, labelpad=8)

            #Fetch L value
            L = globals.L_value.get()

            #Set display limits of the x axis
            self.graph1.set_xlim([settings.z_tip_is_graph_x_axis_range_min, L*1.05])
            
            #########################################################################
            #Fetch necessary values
            E = []
            t = []
            nu = []
            sigma_i = []
            for material in globals.materials:
                E.append(globals.materials[material]["Modulus [GPa]"].get() * 1e9)
                t.append(float(globals.materials[material]["Thickness [nm]"].get()) / 1e9)
                nu.append(globals.materials[material]["Poisson"].get())
                sigma_i.append(float(globals.materials[material]["Stress_x [MPa]"].get()) * 1e6)


            W = 160 / 1e6 #In micrometers
            piezo_thickness = float(globals.materials[globals.piezo_material_name.get()]["Thickness [nm]"].get()) / 1e9

            Zn = globals.equations.calculate_Zn(E, t, nu)
            if(isinstance(Zn, Exception)):
                raise ValueError(f"Zn could not be calculated.\nerror:'{Zn}'")
            
            Zp = globals.equations.calculate_mid_piezo(t, Zn, piezo_thickness)
            if(isinstance(Zp, Exception)):
                raise ValueError(f"Zp could not be calculated.\nerror:'{Zp}'")
            
            V_p = globals.volt_value.get()
            e_31_f = globals.e_31_f_value.get()

            M_p = globals.equations.calculate_M_p_cantilever(Zp, W, V_p, e_31_f)
            if(isinstance(M_p, Exception)):
                raise ValueError(f"M_p could not be calculated.\nerror:'{M_p}'")
            
            M_is = globals.equations.calculate_M_is_cantilever(Zn, sigma_i, t, W)
            if(isinstance(M_is, Exception)):
                raise ValueError(f"M_is could not be calculated.\nerror:'{M_is}'")
            
            M_tot = globals.equations.calculate_M_tot_cantilever(M_is, M_p)
            if(isinstance(M_tot, Exception)):
                raise ValueError(f"M_tot could not be calculated.\nerror:'{M_tot}'")
            
            EI = globals.equations.calculate_EI(E, t, nu, W, Zn)
            if(isinstance(EI, Exception)):
                raise ValueError(f"EI could not be calculated.\nerror:'{EI}'")
            
            curv_is = globals.equations.calculate_curvature(M_tot, EI)
            if(isinstance(curv_is, Exception)):
                raise ValueError(f"curv_is could not be calculated.\nerror:'{curv_is}'")
            
            ##########################################################################

            L = L/1e6

            #Calculate x and y values
            x_values = numpy.linspace(0, L, 100)
            y_values = []
            for x in x_values:
                y = globals.equations.calculate_tip_placement(curv_is, x)
                if(isinstance(y, Exception)):
                    raise ValueError(f"Could not calculate tip_placement.\nerror:'{y}'")
                y_values.append(y)
            

            ############ RUNAR START ####################################
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
                            y_limit = globals.equations.calculate_tip_placement(curv_is, L) * 1.05
                            if(isinstance(y_limit, Exception)):
                                raise ValueError(f"Could not calculate tip_placement.\nerror:'{y_limit}'")
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
                            y_limit = globals.equations.calculate_tip_placement(curv_is, L) * 1.05
                            if(isinstance(y_limit, Exception)):
                                raise ValueError(f"Could not calculate tip_placement.\nerror:'{y_limit}'")
                            break
                        else:
                            y_limit = candidate
                # Set ylim so that the upper bound comes from settings (often 0)
                self.graph1.set_ylim([y_limit, settings.z_tip_is_graph_y_axis_range_min])
        
            ##################RUNAR SLUTT######################

            #Display the grid on the graph
            self.graph1.grid(True)
            
            # Display the x and y axis lines in the grid
            self.graph1.axhline(0, color="black", linewidth=1)
            self.graph1.axvline(0, color="black", linewidth=1)
        
            # Plot the curve
            self.graph1.plot(x_values*1e6, y_values, color="k")
        
            # Get the highest x and y values for the tip marker
            x_tip = x_values[-1] * 1e6
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

            #Draw the canvas to display the updates
            self.graph1.figure.canvas.draw()
        
        except Exception as error:
            #Clear the graph
            self.graph1.clear()
            
            #Add error text
            self.graph1.text(
                0.5, 0.5,
                f"Could not draw curvature graph\n\n{error}",
                fontsize=9,
                color="red",
                transform=self.graph1.transAxes,
                ha="center",
                va="center"
            )

            #Draw the canvas to display the updates
            self.graph1.figure.canvas.draw()
