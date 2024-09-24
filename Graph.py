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
            dpi=100 #Dots Per Inch in the graph
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
    

    def draw_circle_function(self, val=None):
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
        self.ax.axhline(0, color="black", linewidth=1)
        self.ax.axvline(0, color="black", linewidth=1)

        #Redraw the canvas to update the graph
        self.graph.draw_idle()

    #Radius of curvature from fitting:
    def draw_curvature(self):
        ############
        
        #Formula
        """
        1/r = (y'') / ( sqrt(   (1+ (y')^2 ) ^3    ) )
        
        find: 
        - y''
        - (y')^2
        - r        
        """



        # Generate x values
        x = np.linspace(-10, 10, 400)
        
        # Compute y values for the curve and curvature values
        y_values = x**2

        # Define the function and its derivatives
        y_prime = 2*x

        y_double_prime = 2

        # Curvature formula
        curvature = y_double_prime / (1 + (y_prime**2)**(3/2))


        curvature_values = curvature(x)

        # Plot the original function (y = x^2)
        plt.plot(x, y_values, label='y = x^2', color='blue')

        # Plot the curvature (1/r) values on the same plot
        plt.plot(x, curvature_values, label='Curvature 1/r', color='red')

        # Add labels and title
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Plot of y = x^2 and Curvature (1/r)')
        plt.axhline(0, color='black',linewidth=0.5)
        plt.axvline(0, color='black',linewidth=0.5)
        plt.grid(True)
        plt.legend()

        # Show the plot
        plt.show()

        ############


    def update_graph(self, val=None):
        print("UPDATE_GRAPH()")

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

        
        