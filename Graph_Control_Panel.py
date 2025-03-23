import tkinter
import customtkinter
import settings
import os
import globals

import matplotlib
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk #For creating graphs
matplotlib.use('TkAgg')


class Graph_Control_Panel:
    def __init__(self, program_window):
        # print("CLASS: GRAPH_CONTROL_PANEL_INIT()")
        
        self.program_window = program_window

        self.graph_control_panel = self.create_graph_control_panel()
    

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
                row=1,
                column=2,
                padx=(settings.graph_control_panel_padding_left, settings.graph_control_panel_padding_right),
                pady=(settings.graph_control_panel_padding_top, settings.graph_control_panel_padding_bottom),
                sticky="nsew"
            )

        #Create a toolbar for the graph
        toolbar = NavigationToolbar2Tk(
            globals.graph.graph_translator,
            graph_control_panel_frame,
        )
        toolbar.pack(
            padx=(3,3),
            pady=(1,1),
        )
        toolbar.config(
            background=settings.graph_control_panel_background_color,
        )

        for widget in toolbar.winfo_children():
            widget.config(
                background=settings.graph_control_panel_button_color, 
            )


        #Export graph button
        export_graph_button = customtkinter.CTkButton(
            master=graph_control_panel_frame,
            text="Export graph",
            fg_color= settings.graph_control_panel_button_color, 
            hover_color=settings.graph_control_panel_button_hover_color, 
            text_color=settings.graph_control_panel_button_text_color,
            command=self.export_graph
        )
        export_graph_button.pack(
            padx=(0,0),
            pady=(5,0)
        )

        return graph_control_panel_frame


    def export_graph(self):
        """Exports the graph as svg file"""
        
        #print("EXPORT_GRAPH()")

        #CREATE FOLDER HIERARCHY
        main_folder = "exports"

        #Create folder if it does not exist
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        #Create sub_folder
        sub_folder = "graph"

        #Create sub_folder if it does not exist
        if not os.path.exists(f"{main_folder}/{sub_folder}"):
            os.makedirs(f"{main_folder}/{sub_folder}")
        
        #Create name for the file
        filename = "graph.svg"

        #Save the graph as svg file
        globals.graph.graph_container.savefig(f"{main_folder}/{sub_folder}/{filename}")
