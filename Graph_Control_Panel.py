import tkinter
from tkinter import StringVar
import customtkinter
import settings
import os
from tkinter import filedialog

# from matplotlib.figure import Figure                            #For creating graphs
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import globals

class Graph_Control_Panel:
    def __init__(self, window):
        # print("CLASS: GRAPH_CONTROL_PANEL_INIT()")
        
        self.window = window

        self.graph_control_panel = self.create_graph_control_panel()
    
    def create_graph_control_panel(self):

        #Create Frame for the graph and place it within given window
        graph_control_panel_frame = customtkinter.CTkFrame(
            master=self.window,
            width=settings.graph_control_panel_width,
            height=settings.graph_control_panel_height,
            fg_color=settings.graph_control_panel_background_color,
        )
        graph_control_panel_frame.grid(
            row=1,
            column=2,
            padx=(settings.graph_control_panel_padding_left, settings.graph_control_panel_padding_right),
            pady=(settings.graph_control_panel_padding_top, settings.graph_control_panel_padding_bottom),
            sticky="nw",
        )

        #Prevent the frame to downsize itself to fit widgets placed inside
        graph_control_panel_frame.grid_propagate(False)
        # graph_control_panel.grid_rowconfigure(0, weight=1)
        # graph_control_panel.grid_columnconfigure(0, weight=1)


        #Export graph button
        export_graph_button = customtkinter.CTkButton(
            master=graph_control_panel_frame,
            text="Export graph",
            width=10,
            height=10,
            command=self.export_graph
        )

        export_graph_button.grid(
            row=2,
            column=0,
            sticky="",
            padx=(0,0),
            pady=(0,0)
        )


        #R slider label
        r_slider_label = customtkinter.CTkLabel(
            master=graph_control_panel_frame, 
            text="R slider", 
            text_color="white"
        )
        r_slider_label.grid(
            row=2,
            column=1,
            padx=(0,0),
            pady=(0,0)
        )

        #Slider for r value 
        self.r_slider = customtkinter.CTkSlider(
            master=graph_control_panel_frame, 
            width=settings.graph_control_panel_slider_width,
            height=settings.graph_control_panel_slider_height,
            from_=settings.graph_control_panel_slider_range_min, 
            to=settings.graph_control_panel_slider_range_max,
            progress_color=settings.graph_control_panel_slider_progress_color,
            fg_color=settings.graph_control_panel_slider_background_color,
            button_hover_color=settings.graph_control_panel_slider_hover_color,
            command=globals.graph.draw_curvature_graph
        )
        self.r_slider.grid(
            row=2, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )

        return graph_control_panel_frame

    """Exports the graph as either """
    def export_graph(self):
        # print("EXPORT_GRAPH()")

        #CREATE FOLDER HIERARCHY
        main_folder = "exports"

        # #Create folder if it does not exist
        # if not os.path.exists(main_folder):
        #     os.makedirs(main_folder)


        #Create sub_folder
        sub_folder = "graph"

        #Create sub_folder if it does not exist
        # sub_folder_path = os.path.join(main_folder, sub_folder)
        if not os.path.exists(f"{main_folder}/{sub_folder}"):
            os.makedirs(f"{main_folder}/{sub_folder}")
        
        #Create name for the file
        filename = "graph.svg"

        #Save the file
        # file_path = filedialog.asksaveasfilename(
        # defaultextension=".png", 
        # filetypes=[
        #     ("PNG files", "*.png"), 
        #     ("JPEG files", "*.jpg"), 
        #     ("PDF files", "*.pdf"),
        #     ("SVG files", "*.svg"), 
        #     ("All files", "*.*")]
        # )

        # if file_path:
            # globals.graph.graph.savefig(file_path)
        
        #Save the graph as svg file
        globals.graph.graph.savefig(f"{main_folder}/{sub_folder}/{filename}")
