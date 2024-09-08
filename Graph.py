import tkinter
import customtkinter
import settings
import globals


class Graph:
    def __init__(self, window):
        print("CLASS: GRAPH_INIT()")
        
        self.window = window

        self.graph = self.create_graph()
    
    def create_graph(self):

        #Create Frame for the graph and place it within given window
        graph_frame = customtkinter.CTkFrame(
            master=self.window,
            width=settings.graph_frame_width,
            height=settings.graph_frame_height,
            fg_color=settings.graph_frame_background_color
        )
        graph_frame.grid(
            row=0,
            column=2,
            padx=(settings.graph_frame_padding_left, settings.graph_frame_padding_right),
            pady=(settings.graph_frame_padding_top, settings.graph_frame_padding_bottom),
            sticky="nw"
        )

        #Prevent the frame to downsize itself to fit widgets placed inside
        graph_frame.grid_propagate(False)
        graph_frame.grid_rowconfigure(0, weight=1)
        graph_frame.grid_columnconfigure(0, weight=1)

        #TEMPORARY LABEL
        temporary_label = customtkinter.CTkLabel(
            master=graph_frame, 
            text="GRAPH", 
            fg_color=settings.graph_frame_background_color,
            text_color="black",
            font=(settings.text_font, 20, "bold")
        )
        temporary_label.grid(
            # row=0,
            # column=0,
            sticky="nsew",
            padx=(0,0),
            pady=(0,0)
        )

        return graph_frame