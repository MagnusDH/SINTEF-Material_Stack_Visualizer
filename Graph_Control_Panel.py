import tkinter
import customtkinter
import settings
import os
import globals

import matplotlib
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk #For creating graphs
matplotlib.use('TkAgg')


class Graph_Control_Panel:
    def __init__(self, program_window, row_placement:int, column_placement:int):
        # print("CLASS: GRAPH_CONTROL_PANEL_INIT()")
        
        self.program_window = program_window

        #Row/column placement in main program window
        self.row_placement = row_placement
        self.column_placement = column_placement

        self.graph_control_panel_frame = self.create_graph_control_panel()
    

    def create_graph_control_panel(self):
        """Creates a frame with widgets that performs actions on the graph"""
        
        #print("CREATE_GRAPH_CONTROL_PANEL()")
        
        #Create Frame for the graph and place it within given window
        if not hasattr(self, 'graph_control_panel_frame'):
            graph_control_panel_frame = customtkinter.CTkFrame(
                master=self.program_window,
                fg_color=settings.graph_control_panel_background_color,
            )
            graph_control_panel_frame.grid(
                row=self.row_placement,
                column=self.column_placement,
                padx=(settings.graph_control_panel_padding_left, settings.graph_control_panel_padding_right),
                pady=(settings.graph_control_panel_padding_top, settings.graph_control_panel_padding_bottom),
                sticky="nsew"
            )

        
            #Define the row&column layout of the graph_control_panel_frame
            graph_control_panel_frame.columnconfigure(0, weight=100, uniform="group1")
            graph_control_panel_frame.rowconfigure(0, weight=100, uniform="group1")   

        #Create a toolbar for the graph
        toolbar = NavigationToolbar2Tk(
            globals.graph_canvas.graph_translator,
            graph_control_panel_frame,
        )
        toolbar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,0),
            pady=(0,0),
        )
        toolbar.config(
            background=settings.graph_control_panel_background_color,
        )

        for widget in toolbar.winfo_children():
            widget.config(
                background=settings.graph_control_panel_button_color, 
            )

        return graph_control_panel_frame
