import tkinter
from tkinter import StringVar
import customtkinter
import settings
import globals


class Graph_Control_Panel:
    def __init__(self, window):
        # print("CLASS: GRAPH_CONTROL_PANEL_INIT()")
        
        self.window = window

        self.graph_control_panel = self.create_graph_control_panel()
    
    def create_graph_control_panel(self):

        #Create Frame for the graph and place it within given window
        graph_control_panel = customtkinter.CTkFrame(
            master=self.window,
            width=settings.graph_control_panel_width,
            height=settings.graph_control_panel_height,
            fg_color=settings.graph_control_panel_background_color,
        )
        graph_control_panel.grid(
            row=1,
            column=2,
            padx=(settings.graph_control_panel_padding_left, settings.graph_control_panel_padding_right),
            pady=(settings.graph_control_panel_padding_top, settings.graph_control_panel_padding_bottom),
            sticky="nw",
        )

        #Prevent the frame to downsize itself to fit widgets placed inside
        graph_control_panel.grid_propagate(False)
        # graph_control_panel.grid_rowconfigure(0, weight=1)
        # graph_control_panel.grid_columnconfigure(0, weight=1)

        #X slider label
        # x_slider_label = customtkinter.CTkLabel(
        #     master=graph_control_panel, 
        #     text="X slider", 
        #     text_color="white"
        # )
        # x_slider_label.grid(
        #     row=0,
        #     column=0,
        #     padx=(0,0),
        #     pady=(0,0)
        # )

        # #Slider for x value
        # self.x_slider = customtkinter.CTkSlider(
        #     master=graph_control_panel, 
        #     width=settings.graph_control_panel_slider_width,
        #     height=settings.graph_control_panel_slider_height,
        #     from_=settings.graph_control_panel_slider_range_min, 
        #     to=settings.graph_control_panel_slider_range_max,
        #     progress_color=settings.graph_control_panel_slider_progress_color,
        #     fg_color=settings.graph_control_panel_slider_background_color,
        #     button_hover_color=settings.graph_control_panel_slider_hover_color,
        #     command=globals.graph.draw_curvature_graph
        # )
        # self.x_slider.grid(
        #     row=0, 
        #     column=1,
        #     sticky="e",
        #     padx=(0,0),
        #     pady=(0,0)
        # )

        # #Y slider label
        # y_slider_label = customtkinter.CTkLabel(
        #     master=graph_control_panel, 
        #     text="Y slider", 
        #     text_color="white"
        # )
        # y_slider_label.grid(
        #     row=1,
        #     column=0,
        #     padx=(0,0),
        #     pady=(0,0)
        # )

        # #Slider for y value 
        # self.y_slider = customtkinter.CTkSlider(
        #     master=graph_control_panel, 
        #     width=settings.graph_control_panel_slider_width,
        #     height=settings.graph_control_panel_slider_height,
        #     from_=settings.graph_control_panel_slider_range_min, 
        #     to=settings.graph_control_panel_slider_range_max,
        #     progress_color=settings.graph_control_panel_slider_progress_color,
        #     fg_color=settings.graph_control_panel_slider_background_color,
        #     button_hover_color=settings.graph_control_panel_slider_hover_color,
        #     command=globals.graph.draw_curvature_graph
        # )
        # self.y_slider.grid(
        #     row=1, 
        #     column=1,
        #     sticky="e",
        #     padx=(0,0),
        #     pady=(0,0)
        # )


        #R slider label
        r_slider_label = customtkinter.CTkLabel(
            master=graph_control_panel, 
            text="R slider", 
            text_color="white"
        )
        r_slider_label.grid(
            row=2,
            column=0,
            padx=(0,0),
            pady=(0,0)
        )

        #Slider for r value 
        self.r_slider = customtkinter.CTkSlider(
            master=graph_control_panel, 
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

        return graph_control_panel