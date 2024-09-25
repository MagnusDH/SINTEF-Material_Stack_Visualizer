import tkinter
import customtkinter
import settings
import globals

from matplotlib.figure import Figure                            #For creating graphs
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #For creating graphs

import numpy

class Graph:
    def __init__(self, window):
        print("CLASS: GRAPH_INIT()")
        
        self.window = window

        self.graph = self.create_graph()

        # self.draw_circle_function()

        # self.update_graph()


    """Decalration of a function to be displayed"""
    def function(self, x):
        return x**2
        

    def create_graph(self):
        # print("CREATE_GRAPH()")

        #Create a figure object
        figure = Figure(
            figsize=(settings.graph_width/100, settings.graph_height/100),
            dpi=settings.graph_dpi
        )

        #Create a canvas to draw the graph on and place it
        figure_canvas = FigureCanvasTkAgg(figure, master=self.window)
        figure_canvas.get_tk_widget().grid(
            row=0,
            column=2,
            sticky="nw",
            padx=(5, 0),
            pady=(5,0)
        )


        #????????????????
        self.ax = figure.add_subplot(111)    #Explanation of digits: (1)Number of rows in the grid, (2) number of columns in the grid, (3)position of this subplot within the grid (counting starts from 1 in the top-left

        #Set labels for the graph
        self.ax.set_title("This is a simple graph")
        self.ax.set_xlabel("This is the x line")
        self.ax.set_ylabel("This is the y line")
        
        #Set the display limits of the x and y axises 
        self.ax.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])
        self.ax.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])

        #Display the grid of the graph
        self.ax.grid(True)

        #Display the x and y axis lines in the grid (the first argument is the value on the x and y grid)
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        return figure_canvas
    

    def draw_circle_graph(self, val=None):
        #Formel for sirkel: (x^2 - h) + (y^2 - k) = r^2

        print("DRAW_CIRCLE_FUNCTION()")
        
        #Clear the graph
        self.ax.clear()

        #Set the display limits of the x and y axises 
        self.ax.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])
        self.ax.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])

        print(globals.graph_control_panel.r_slider.get())
        radius = globals.graph_control_panel.r_slider.get()

        #Create a range of values for x
        x = numpy.linspace(-radius, radius, 100)

        #Find the positive and negative values for y
        y_positive = numpy.sqrt(radius**2 - x**2)
        y_negative = -numpy.sqrt(radius**2 - x**2)

        #Plot the values in the graph
        self.ax.plot(x, y_positive, marker="o", label="This is where the line name is put")
        self.ax.plot(x, y_negative, marker="o", label="This is where the line name is put")

        # Redraw grid and axes
        self.ax.grid(True)
        # self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        #Redraw the canvas to update the graph
        self.graph.draw_idle()


    def draw_curvature_graph(self, val=None):
        print("DRAW_CURVATURE_GRAPH()")
        # Clear the graph
        self.ax.clear()

        #Set title and names for x/y axes
        self.ax.set_title("This is a curvature graph")
        self.ax.set_xlabel("Some name for x line")
        self.ax.set_ylabel("Some name for y line")

        #Set the display limits of the x and y axes
        self.ax.set_xlim([settings.graph_x_axis_range_min, settings.graph_x_axis_range_max])
        self.ax.set_ylim([settings.graph_y_axis_range_min, settings.graph_y_axis_range_max])

        #Create a fixed range of values for x (from, to, number of spots)
        x = numpy.linspace(settings.graph_x_axis_range_min, settings.graph_x_axis_range_max, 50)

        #Calculate y values
        # y = numpy.linspace(0, globals.graph_control_panel.r_slider.get(), 50)
        # print(globals.graph_control_panel.r_slider.get())
        
    #CHATGPT#
        
        # Adjust 'a' based on the slider value
        a = globals.graph_control_panel.r_slider.get() / (100 ** 2)  # Scaling factor to make the curve fit the range

        # Calculate y values - peak in the middle, and y = 0 at x = -100 and x = 100
        y = a * (x ** 2) - a * (100 ** 2)  # Subtract constant to ensure y=0 at x=-100 and x=100

    #END CHATGPT#

        #Plot the values in the graph
        self.ax.plot(x, y, marker="o", label="This should be the Y line", color="black")

        #Redraw grid and axes
        self.ax.grid(True)
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        #Redraw the graph
        self.graph.draw_idle()


    def draw_simple_graph(self, val=None):
        print("DRAW_SIMPLE_GRAPH()")

        #Clear the graph
        self.ax.clear()
        
        #Create som e values for x
        x = [-10, -5, 0, 5, 10, 15, 20]

        #Get the current x and y values from sliders
        # print(globals.graph_control_panel.y_slider.get())
        # x = globals.graph_control_panel.x_slider.get()
        y = []
        
        #Calculate the corresponding y values using the function(x)
        for value in x:
            y.append(self.function(value))

        #Plot the values in the graph
        self.ax.plot(
            x, 
            y,
            marker="o", 
            label="This is where the line name is put")

        # Redraw grid and axes
        self.ax.grid(True)
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        # Redraw the canvas to update the graph
        self.graph.draw_idle()

        
        