import tkinter
import customtkinter
import settings
import globals


class Graph_Control_Panel:
    def __init__(self, window):
        print("CLASS: GRAPH_CONTROL_PANEL_INIT()")
        
        self.window = window

        self.graph_control_panel = self.create_graph_control_panel()
    
    def create_graph_control_panel(self):

        #Create Frame for the graph and place it within given window
        graph_control_panel = customtkinter.CTkFrame(
            master=self.window,
            width=settings.graph_control_panel_width,
            height=settings.graph_control_panel_height,
            fg_color=settings.graph_control_panel_background_color
        )
        graph_control_panel.grid(
            row=1,
            column=2,
            padx=(settings.graph_control_panel_padding_left, settings.graph_control_panel_padding_right),
            pady=(settings.graph_control_panel_padding_top, settings.graph_control_panel_padding_bottom),
            sticky="nw"
        )

        #Prevent the frame to downsize itself to fit widgets placed inside
        graph_control_panel.grid_propagate(False)
        # graph_control_panel.grid_rowconfigure(0, weight=1)
        # graph_control_panel.grid_columnconfigure(0, weight=1)

        #TEMPORARY LABEL
        temporary_label = customtkinter.CTkLabel(
            master=graph_control_panel, 
            text="GRAPH CONTROLS", 
            fg_color=settings.material_control_panel_background_color,
            text_color="#55b6ff",
            font=(settings.text_font, 20, "bold")
        )
        temporary_label.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,0),
            pady=(0,0)
        )

        return graph_control_panel