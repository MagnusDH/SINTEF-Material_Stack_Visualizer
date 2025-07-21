import tkinter
from tkinter import messagebox
import customtkinter
import settings #File containing settings
import globals  #File containing global variables
import helper_functions


class Parameters_Panel:
    def __init__(self, window, row_placement:int, column_placement:int):
        # print("CLASS PARAMETERS_PANEL INIT()")

        #Window where everything is placed
        self.program_window = window

        #Row/column placement in main program window
        self.row_placement = row_placement
        self.column_placement = column_placement

        #Create Parameters_Panel
        self.parameters_panel_frame = self.create_parameters_panel()


    def create_parameters_panel(self):
        """
        Creates or updates a Frame/panel with widgets that gives the user control over attributes used for the graphs and equations\n
        """
        # print("CREATE_PARAMETERS_PANEL()")

        #if parameters_panel_frame has NOT been created before, create it
        if not hasattr(self, 'parameters_panel_frame'):
            self.parameters_panel_frame = customtkinter.CTkScrollableFrame(
                master=self.program_window,
                fg_color=settings.parameters_panel_background_color
            )
            self.parameters_panel_frame.grid(
                row=self.row_placement,
                column=self.column_placement,
                padx=(settings.parameters_panel_padding_left, settings.parameters_panel_padding_right),
                pady=(settings.parameters_panel_padding_top, settings.parameters_panel_padding_bottom),
                sticky="nswe"
            )

            #Define the row&column layout of the parameters_panel
            self.parameters_panel_frame.columnconfigure(0, weight=20, uniform="group1")
            self.parameters_panel_frame.columnconfigure(1, weight=40, uniform="group1")
            self.parameters_panel_frame.columnconfigure(2, weight=40, uniform="group1")

            self.parameters_panel_frame.rowconfigure((0,1,2,3,4,5), weight=1, uniform="group1")


        #HEADLINE
        if not hasattr(self, "parameters_panel_headline"):
            self.parameters_panel_headline = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="Parameters", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color,
                font=(settings.parameters_panel_headline_font, settings.parameters_panel_headline_size, settings.parameters_panel_headline_weight)
            )
            self.parameters_panel_headline.grid(
                row=0, 
                column=0,
                columnspan=3, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )


        #"L μm" LABEL
        if not hasattr(self, "L_label"):
            self.L_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="L [μm]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.L_label.grid(
                row=1, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1)
            )


        #"L [μm]" ENTRY
        if not hasattr(self, "L_entry"):
            self.L_entry = customtkinter.CTkEntry(
                master=self.parameters_panel_frame,
                textvariable=globals.L_value,
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                # border_width=0.4,
                border_width=1,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.L_entry.grid(
                row=1, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,1)
            )


        # #"rᵢ [μm]" LABEL
        # if not hasattr(self, "ri_label"):
        #     self.ri_label = customtkinter.CTkLabel(
        #         master=self.parameters_panel_frame, 
        #         text="rᵢ [μm]", 
        #         fg_color=settings.parameters_panel_background_color,
        #         text_color=settings.parameters_panel_text_color
        #     )
        #     self.ri_label.grid(
        #         row=2, 
        #         column=0, 
        #         sticky="w", 
        #         padx=(0,0),
        #         pady=(0,1)
        #     )


        # #"rᵢ [μm]" ENTRY
        # if not hasattr(self, "ri_entry"):
        #     self.ri_entry = customtkinter.CTkEntry(
        #         master=self.parameters_panel_frame,
        #         textvariable=tkinter.StringVar(value="not in use"),
        #         fg_color = settings.parameters_panel_entry_background_color,
        #         border_color=settings.parameters_panel_entry_border_color,
        #         border_width=1,
        #         text_color=settings.parameters_panel_entry_text_color,
        #         justify="center"
        #     )
        #     self.ri_entry.grid(
        #         row=2, 
        #         column=2,
        #         sticky="",
        #         padx=(0,0),
        #         pady=(0,1)
        #     )


        # #"r₀ [μm]" LABEL
        # if not hasattr(self, "ro_label"):
        #     self.ro_label = customtkinter.CTkLabel(
        #         master=self.parameters_panel_frame, 
        #         text=" r₀ [μm]", 
        #         fg_color=settings.parameters_panel_background_color,
        #         text_color=settings.parameters_panel_text_color
        #     )
        #     self.ro_label.grid(
        #         row=3, 
        #         column=0, 
        #         sticky="w", 
        #         padx=(0,0),
        #         pady=(0,1)
        #     )


        # #"r₀ [μm]" ENTRY
        # if not hasattr(self, "ro_entry"):
        #     self.ro_entry = customtkinter.CTkEntry(
        #         master=self.parameters_panel_frame,
        #         textvariable=tkinter.StringVar(value="not in use"),
        #         fg_color = settings.parameters_panel_entry_background_color,
        #         border_color=settings.parameters_panel_entry_border_color,
        #         border_width=1,
        #         text_color=settings.parameters_panel_entry_text_color,
        #         justify="center"
        #     )
        #     self.ro_entry.grid(
        #         row=3, 
        #         column=2,
        #         sticky="",
        #         padx=(0,0),
        #         pady=(0,1)
        #     )

            
        #E_31_F LABEL
        if not hasattr(self, "e_31_f_label"):
            self.e_31_f_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="e₃₁ [C/m²]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.e_31_f_label.grid(
                row=2, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1)
            )
            

        #e_31_f ENTRY
        if not hasattr(self, "e_31_f_entry"):
            self.e_31_f_entry = customtkinter.CTkEntry(
                master=self.parameters_panel_frame,
                textvariable=globals.e_31_f_value,
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=1,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.e_31_f_entry.grid(
                row=2, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,1)
            )


        #VOLT LABEL
        if not hasattr(self, "volt_label"):
            self.volt_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="Volt", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.volt_label.grid(
                row=3, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1)
            )


        #VOLT SLIDER
        if not hasattr(self, "volt_slider"):
            self.volt_slider = customtkinter.CTkSlider(
                master=self.parameters_panel_frame, 
                from_=settings.parameters_panel_slider_range_min, 
                to=settings.parameters_panel_slider_range_max, 
                variable=globals.volt_value,
                number_of_steps=100,
                fg_color=settings.parameters_panel_slider_background_color,
                button_color=settings.parameters_panel_slider_button_color,
                progress_color=settings.parameters_panel_slider_progress_color,
                button_hover_color=settings.parameters_panel_slider_hover_color,
            )
            self.volt_slider.grid(
                row=3, 
                column=1,
                sticky="",
                padx=(0,0),
                pady=(0,1)
            )
            

        #VOLT ENTRY
        if not hasattr(self, "volt_entry"):
            self.volt_entry = customtkinter.CTkEntry(
                master=self.parameters_panel_frame,
                textvariable=globals.volt_value,
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=1,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.volt_entry.grid(
                row=3, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,1)
            )


        #NEUTRALIZING_MATERIAL LABEL
        if not hasattr(self, "neutralizing_material_label"):
            self.neutralizing_material_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="Neutralizing material:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.neutralizing_material_label.grid(
                row=4, 
                column=0, 
                columnspan=2,
                sticky="w", 
                padx=(0,0),
                pady=(0,1)
            )
            

        #NEUTRALIZING_MATERIAL COMBOBOX
        if not hasattr(self, "neutralizing_material_combobox"):
            self.neutralizing_material_combobox = customtkinter.CTkComboBox(
                master=self.parameters_panel_frame,
                variable=globals.neutralizing_material_name,
                values=list(reversed((globals.materials.keys()))),
                border_width=1,
                border_color=settings.parameters_panel_combobox_border_color,
                fg_color=settings.parameters_panel_combobox_background_color,
                text_color=settings.parameters_panel_combobox_text_color,
                button_color=settings.parameters_panel_combobox_button_color,
                button_hover_color=settings.parameters_panel_combobox_button_hover_color,
                dropdown_fg_color=settings.parameters_panel_combobox_dropdown_fg_color,
                dropdown_hover_color=settings.parameters_panel_combobox_dropdown_hover_color,
                dropdown_text_color=settings.parameters_panel_combobox_dropdown_text_color
            )
            self.neutralizing_material_combobox.grid(
                row=4, 
                column=2, 
                sticky="",
                padx=(0,0),
                pady=(0,1),
            )
        else:
            if(self.neutralizing_material_combobox.get() not in globals.materials.keys()):
                self.neutralizing_material_combobox.set("")
            self.neutralizing_material_combobox.configure(
                values=list(reversed((globals.materials.keys())))
            )


        #STONEY FILAMENT LABEL
        if not hasattr(self, "stoney_filament_label"):
            self.stoney_filament_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="Stoney filament", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.stoney_filament_label.grid(
                row=5, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1),
                columnspan=2,
            )
        

        #STONEY FILAMENT COMBOBOX
        if not hasattr(self, "stoney_filament_combobox"):
            self.stoney_filament_combobox = customtkinter.CTkComboBox(
                master=self.parameters_panel_frame,
                variable=globals.stoney_filament,
                values=list(reversed((globals.materials.keys()))),
                border_width=1,
                border_color=settings.parameters_panel_combobox_border_color,
                fg_color=settings.parameters_panel_combobox_background_color,
                text_color=settings.parameters_panel_combobox_text_color,
                button_color=settings.parameters_panel_combobox_button_color,
                button_hover_color=settings.parameters_panel_combobox_button_hover_color,
                dropdown_fg_color=settings.parameters_panel_combobox_dropdown_fg_color,
                dropdown_hover_color=settings.parameters_panel_combobox_dropdown_hover_color,
                dropdown_text_color=settings.parameters_panel_combobox_dropdown_text_color
            )
            self.stoney_filament_combobox.grid(
                row=5, 
                column=2, 
                sticky="", 
                padx=(0,0),
                pady=(0,1),
            )
        else:
            if(self.stoney_filament_combobox.get() not in globals.materials.keys()):
                self.stoney_filament_combobox.set("")
            self.stoney_filament_combobox.configure(
                values=list(reversed((globals.materials.keys())))
            )


        return self.parameters_panel_frame
