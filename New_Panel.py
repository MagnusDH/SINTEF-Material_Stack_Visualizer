import tkinter
import customtkinter
import settings #File containing settings
import globals  #File containing global variables
import helper_functions


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
        # print("CREATE_NEW_PANEL()")


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

            #Define the row&column layout of the new_panel
            new_panel_frame.columnconfigure(0, weight=50, uniform="group1")
            new_panel_frame.columnconfigure(1, weight=50, uniform="group1")

            new_panel_frame.rowconfigure((0,1,2,3,), weight=20, uniform="group1")    
            new_panel_frame.rowconfigure((4), weight=20, uniform="group1")
        

            #Create "W μm" label
            W_label = customtkinter.CTkLabel(
                master=new_panel_frame, 
                text="W [μm]", 
                fg_color=settings.new_panel_background_color,
                text_color=settings.new_panel_text_color
            )
            W_label.grid(
                row=0, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )

            #Create Entry
            W_entry = customtkinter.CTkEntry(
                master=new_panel_frame,
                textvariable=tkinter.StringVar(value=0),
                fg_color = settings.new_panel_entry_background_color,
                border_color=settings.new_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.new_panel_entry_text_color,
                justify="center"
            )
            W_entry.grid(
                row=0, 
                column=1,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            # W_entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))


            #Create "L μm" label
            L_label = customtkinter.CTkLabel(
                master=new_panel_frame, 
                text="L [μm]", 
                fg_color=settings.new_panel_background_color,
                text_color=settings.new_panel_text_color
            )
            L_label.grid(
                row=1, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )

            #Create "L μm" Entry
            L_entry = customtkinter.CTkEntry(
                master=new_panel_frame,
                textvariable=tkinter.StringVar(value=0),
                fg_color = settings.new_panel_entry_background_color,
                border_color=settings.new_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.new_panel_entry_text_color,
                justify="center"
            )
            L_entry.grid(
                row=1, 
                column=1,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            # W_entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))#Create "W μm" label
            
            #Create "rᵢ μm" label
            ri_label = customtkinter.CTkLabel(
                master=new_panel_frame, 
                text="rᵢ [μm]", 
                fg_color=settings.new_panel_background_color,
                text_color=settings.new_panel_text_color
            )
            ri_label.grid(
                row=2, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )

            #Create ri Entry
            ri_entry = customtkinter.CTkEntry(
                master=new_panel_frame,
                textvariable=tkinter.StringVar(value=0),
                fg_color = settings.new_panel_entry_background_color,
                border_color=settings.new_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.new_panel_entry_text_color,
                justify="center"
            )
            ri_entry.grid(
                row=2, 
                column=1,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            #ri_entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))#Create "W μm" label
            
            #Create "r₀ [μm]"
            ro_label = customtkinter.CTkLabel(
                master=new_panel_frame, 
                text=" r₀ [μm]", 
                fg_color=settings.new_panel_background_color,
                text_color=settings.new_panel_text_color
            )
            ro_label.grid(
                row=3, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )

            #Create Entry
            ro_entry = customtkinter.CTkEntry(
                master=new_panel_frame,
                textvariable=tkinter.StringVar(value=0),
                fg_color = settings.new_panel_entry_background_color,
                border_color=settings.new_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.new_panel_entry_text_color,
                justify="center"
            )
            ro_entry.grid(
                row=3, 
                column=1,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            # ro_entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))

            #Create Slider
            self.V_value = tkinter.StringVar(value=0)
            V_slider = customtkinter.CTkSlider(
                master=new_panel_frame, 
                from_=settings.new_panel_slider_range_min, 
                to=settings.new_panel_slider_range_max, 
                fg_color=settings.new_panel_slider_background_color,
                button_color=settings.new_panel_slider_button_color,
                progress_color=settings.new_panel_slider_progress_color,
                button_hover_color=settings.new_panel_slider_hover_color,
                command=lambda value: self.V_slider_updated(value)
            )
            V_slider.grid(
                row=4, 
                column=0,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            V_slider.set(helper_functions.convert_decimal_string_to_float(self.V_value.get()))

            #Create slider Entry
            V_entry = customtkinter.CTkEntry(
                master=new_panel_frame,
                textvariable=self.V_value,
                fg_color = settings.new_panel_entry_background_color,
                border_color=settings.new_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.new_panel_entry_text_color,
                justify="center"
            )
            V_entry.grid(
                row=4, 
                column=1,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            V_entry.bind("<Return>", lambda event, entry_id=V_entry, slider_id=V_slider: self.V_entry_updated(entry_id, slider_id))


        return new_panel_frame
        
    
    def V_slider_updated(self, value):
        """
        Updates the value in the 'V_slider' so that it corresponds to the 'V_entry'
        """
        # print("V_SLIDER UPDATED()")

        self.V_value.set(round(value, 1))


    def V_entry_updated(self, entry_id, slider_id):
        """
        Updates the value in the 'V_entry' so that it corresponds to the 'V_slider'
        """
        # print("V_ENTRY_UPDATED()")
        
        #Find entered value
        entered_value = entry_id.get()
        #Update the V_slider corresponding to entry
        slider_id.set(helper_functions.convert_decimal_string_to_float(entered_value))
