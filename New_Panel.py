import tkinter
import customtkinter
import settings #File containing settings
import globals  #File containing global variables


class New_Panel:
    def __init__(self, window, row_placement:int, column_placement:int):
        # print("CLASS NEW_PANEL INIT()")

        #Window where everything is placed
        self.program_window = window

        #Row/column placement in main program window
        self.row_placement = row_placement
        self.column_placement = column_placement

        #Create new_panel
        self.new_panel_frame = self.create_new_panel()
    

    def create_new_panel(self):
        """
        -??????????????????????????????? 
        """
        print("CREATE_NEW_PANEL()")


        #if new_panel_frame has NOT been created before, create it
        if not hasattr(self, 'new_panel_frame'):
            new_panel_frame = customtkinter.CTkScrollableFrame(
                master=self.program_window,
                fg_color=settings.new_panel_background_color
            )
            new_panel_frame.grid(
                row=self.row_placement,
                column=self.column_placement,
                padx=(settings.new_panel_padding_left, settings.new_panel_padding_right),
                pady=(settings.new_panel_padding_top, settings.new_panel_padding_bottom),
                sticky="nswe"
            )

            #Define the row&column layout of the new panel
            new_panel_frame.columnconfigure(0, weight=100, uniform="group1")

            new_panel_frame.rowconfigure((0), weight=100, uniform="group1")    
        
        return new_panel_frame
        
        
        #TODO
            #Create labels, entries and slider
            #Create settings for frame
            #Return the frame
