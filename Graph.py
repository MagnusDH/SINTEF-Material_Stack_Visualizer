import tkinter
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

        self.graph_canvas, self.graph = self.create_graph()


    def create_graph(self):
        # print("CREATE_GRAPH()")

        #Create a figure object
        figure = Figure(
            figsize=(settings.graph_width/100, settings.graph_height/100),
            dpi=settings.graph_dpi
        )

        #Create a canvas to draw the graph on and place it
        figure_canvas = FigureCanvasTkAgg(figure, master=globals.main_frame)
        figure_canvas.get_tk_widget().grid(
            row=0,
            column=2,
            sticky="nw",
            padx=(5,0),
            pady=(5,0)
        )

        #Explanation of digits: (1)Number of rows in the grid, (2) number of columns in the grid, (3)position of this subplot within the grid (counting starts from 1 in the top-left
        self.ax = figure.add_subplot(111)    

        #Set labels for the graph
        # self.ax.set_title("This is a simple graph")
        # self.ax.set_xlabel("This is the x line")
        # self.ax.set_ylabel("This is the y line")
        
        # #Set the display limits of the x and y axises 
        self.ax.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])
        self.ax.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])

        # #Display the grid of the graph
        self.ax.grid(True)

        # #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        return figure_canvas, figure
    

    """
    RUNAR
    """
    def draw_curvature_graph(self, val=None):
        # # print("DRAW_CURVATURE_GRAPH()")
        
        #Clear the graph
        self.ax.clear()

        #Fetch the R-value from the slider and round it to 3 decimal places
        r_value = round(globals.graph_control_panel.r_slider.get(), 3)

        #Display the R-value directly on the graph
        self.ax.text(
            0.85, 1.1,                              # X and Y Coordinates of the text (relative to axes in percentages)
            f"R = {r_value}",                       # Text
            transform=self.ax.transAxes,            # Transform to make the coordinates relative to the axes
            fontsize=12,                            # Set the font size
            verticalalignment='top',                # Align text to the top
            bbox=dict(facecolor='white', alpha=0.5) # Add a background box for readability
        )

        #Set title and names for x/y axes
        self.ax.set_title("Curvature")
        self.ax.set_xlabel("Some name for x line")
        self.ax.set_ylabel("Some name for y line")

        #Set the limit for the x and y axes
        self.ax.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])
        self.ax.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])



        ######################  CALCULATE VALUES FOR X AND Y ########################

        #Fetch values from excel sheet (for context, not really used here)
        # E = globals.materials["substrate"]["E"]
        # rho = globals.materials["substrate"]["rho"]
        # sigma = globals.materials["substrate"]["sigma"]
        # nu =  globals.materials["substrate"]["nu"]
        
        #Create an array of fixed values for x (from, to, number of spots)
        x = numpy.linspace(settings.graph_x_axis_range_min, settings.graph_x_axis_range_max, 50)

        #Adjust 'a' based on the slider value
        a = globals.graph_control_panel.r_slider.get() / (100 ** 2)  # Scaling factor to make the curve fit the range

        #Calculate y values - peak in the middle, and y = 0 at x = -100 and x = 100
        y = a * (x ** 2) - a * (100 ** 2)  # Subtract constant to ensure y=0 at x=-100 and x=100
        
        ############################################################################

        #Split the x and y data into positive and negative segments
        positive_x = x[y >= 0]
        positive_y = y[y >= 0]

        negative_x = x[y < 0]
        negative_y = y[y < 0]

        #Plot positive values in red
        self.ax.plot(positive_x, positive_y, marker="o", label="Positive values", color="red")

        #Plot negative values in blue
        self.ax.plot(negative_x, negative_y, marker="o", label="Negative values", color="blue")

        #Redraw grid and axes
        self.ax.grid(True)
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        #Redraw the graph
        self.graph_canvas.draw_idle()


            

            













































































    # def draw_circle_graph(self, val=None):
    # #Formel for sirkel: (x^2 - h) + (y^2 - k) = r^2

    # # print("DRAW_CIRCLE_FUNCTION()")
    
    # #Clear the graph
    # self.ax.clear()

    # #Set the display limits of the x and y axises 
    # self.ax.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])
    # self.ax.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])

    # print(globals.graph_control_panel.r_slider.get())
    # radius = globals.graph_control_panel.r_slider.get()

    # #Create a range of values for x
    # x = numpy.linspace(-radius, radius, 100)

    # #Find the positive and negative values for y
    # y_positive = numpy.sqrt(radius**2 - x**2)
    # y_negative = -numpy.sqrt(radius**2 - x**2)

    # #Plot the values in the graph
    # self.ax.plot(x, y_positive, marker="o", label="This is where the line name is put")
    # self.ax.plot(x, y_negative, marker="o", label="This is where the line name is put")

    # # Redraw grid and axes
    # self.ax.grid(True)
    # # self.ax.axhline(0, color="black", linewidth=1)
    # self.ax.axvline(0, color="black", linewidth=1)

    # #Redraw the canvas to update the graph
    # self.graph.draw_idle()