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
        Creates a Frame with widgets that gives the user more control over special attributes used for the graphs and equations\n
        """
        # print("CREATE_PARAMETERS_PANEL()")

        #if parameters_panel_frame has NOT been created before, create it
        if not hasattr(self, 'parameters_panel_frame'):
            parameters_panel_frame = customtkinter.CTkScrollableFrame(
                master=self.program_window,
                fg_color=settings.parameters_panel_background_color
            )
            parameters_panel_frame.grid(
                row=self.row_placement,
                column=self.column_placement,
                padx=(settings.parameters_panel_padding_left, settings.parameters_panel_padding_right),
                pady=(settings.parameters_panel_padding_top, settings.parameters_panel_padding_bottom),
                sticky="nswe"
            )

            #Define the row&column layout of the parameters_panel
            parameters_panel_frame.columnconfigure(0, weight=20, uniform="group1")
            parameters_panel_frame.columnconfigure(1, weight=40, uniform="group1")
            parameters_panel_frame.columnconfigure(2, weight=40, uniform="group1")

            parameters_panel_frame.rowconfigure((0,1,2,3,4,5,6), weight=1, uniform="group1")


            #HEADLINE
            self.parameters_panel_headline = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
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


            #PIEZO_MATERIAL_NAME VARIABLE
            self.piezo_material_name = tkinter.StringVar(value="PZT")
            self.piezo_material_name.trace_add("write", lambda *args, identifier="piezo_material_name": globals.app.variable_updated(identifier))


            #PIEZO_MATERIAL LABEL
            self.piezo_material_label = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text="Piezo material:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.piezo_material_label.grid(
                row=1, 
                column=0, 
                columnspan=2,
                sticky="w", 
                padx=(0,0),
                pady=(0,0)
            )
            

            #PIEZO_MATERIAL entry
            self.piezo_material_entry = customtkinter.CTkEntry(
                master=parameters_panel_frame,
                textvariable=self.piezo_material_name,
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.piezo_material_entry.grid(
                row=1, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            self.piezo_material_entry.bind("<Return>", lambda event, entry=self.piezo_material_entry: self.piezo_material_entry_updated(entry))


            #"L [μm]" VARIABLE
            self.L_value = tkinter.DoubleVar(value=1000)
            self.L_value.trace_add("write", lambda *args, identifier="L_value": globals.app.variable_updated(identifier))


            #Create "L μm" label
            L_label = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text="L [μm]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            L_label.grid(
                row=2, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )


            #"L [μm]" Entry
            self.L_entry = customtkinter.CTkEntry(
                master=parameters_panel_frame,
                textvariable=self.L_value,
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.L_entry.grid(
                row=2, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )


            #"rᵢ [μm]" LABEL
            self.ri_label = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text="rᵢ [μm]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.ri_label.grid(
                row=3, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )


            #"rᵢ [μm]" Entry
            self.ri_entry = customtkinter.CTkEntry(
                master=parameters_panel_frame,
                textvariable=tkinter.StringVar(value="not in use"),
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.ri_entry.grid(
                row=3, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )


            #"r₀ [μm]" LABEL
            self.ro_label = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text=" r₀ [μm]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.ro_label.grid(
                row=4, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )


            #"r₀ [μm]" ENTRY
            self.ro_entry = customtkinter.CTkEntry(
                master=parameters_panel_frame,
                textvariable=tkinter.StringVar(value="not in use"),
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.ro_entry.grid(
                row=4, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )

            
            #E_31_F VARIABLE
            self.e_31_f_value = tkinter.DoubleVar(value=18) 
            self.e_31_f_value.trace_add("write", lambda *args, identifier="e_31_f_value": globals.app.variable_updated(identifier))


            #E_31_F LABEL
            self.e_31_f_label = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text="e₃₁ [C/m²]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.e_31_f_label.grid(
                row=5, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )
            

            #e_31_f entry
            self.e_31_f_entry = customtkinter.CTkEntry(
                master=parameters_panel_frame,
                textvariable=self.e_31_f_value,
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.e_31_f_entry.grid(
                row=5, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )


            #VOLT LABEL
            self.volt_label = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text="Volt", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.volt_label.grid(
                row=6, 
                column=0, 
                sticky="", 
                padx=(0,0),
                pady=(0,0)
            )


            #VOLT SLIDER
            self.volt_value = tkinter.DoubleVar(value=0)
            self.volt_slider = customtkinter.CTkSlider(
                master=parameters_panel_frame, 
                from_=settings.parameters_panel_slider_range_min, 
                to=settings.parameters_panel_slider_range_max, 
                variable=self.volt_value,
                number_of_steps=100,
                fg_color=settings.parameters_panel_slider_background_color,
                button_color=settings.parameters_panel_slider_button_color,
                progress_color=settings.parameters_panel_slider_progress_color,
                button_hover_color=settings.parameters_panel_slider_hover_color,
            )
            self.volt_slider.grid(
                row=6, 
                column=1,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            self.volt_value.trace_add("write", lambda *args, identifier="volt_value": globals.app.variable_updated(identifier))


            #VOLT ENTRY
            self.volt_entry = customtkinter.CTkEntry(
                master=parameters_panel_frame,
                textvariable=self.volt_value,
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=0.4,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.volt_entry.grid(
                row=6, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )


            #STRESS_NEUTRAL_SIO2_THICKNESS VARIABLE
            self.stress_neutral_SiO2_thickness_value = tkinter.DoubleVar(value=0)
            self.stress_neutral_SiO2_thickness_value.trace_add("write", lambda *args, identifier="stress_neutral_SiO2_thickness_value": globals.app.variable_updated(identifier))
            

            #STRESS_NEUTRAL_SIO2_THICKNESS LABEL
            self.stress_neutral_SiO2_thickness_label1 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text=f"Stress-neutral SiO2-thickness:",
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.stress_neutral_SiO2_thickness_label1.grid(
                row=7, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
                columnspan=3
            )
            self.stress_neutral_SiO2_thickness_label2 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                textvariable=self.stress_neutral_SiO2_thickness_value,
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.stress_neutral_SiO2_thickness_label2.grid(
                row=7, 
                column=2, 
                sticky="nsew", 
                padx=(0,0),
                pady=(0,0),
                columnspan=3
            )
            

            #PIEZOELECTRIC_BENDING_MOMENT VARIABLE
            self.piezoelectric_bending_moment_value = tkinter.DoubleVar(value=0)
            self.piezoelectric_bending_moment_value.trace_add("write", lambda *args, identifier="piezoelectric_bending_moment_value": globals.app.variable_updated(identifier))
            

            #PIEZOELECTRIC_BENDING_MOMENT LABEL
            self.piezoelectric_bending_moment_label1 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text=f"Piezoelectric bending moment:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.piezoelectric_bending_moment_label1.grid(
                row=8, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
                columnspan=3
            )
            self.piezoelectric_bending_moment_label2 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                textvariable=self.piezoelectric_bending_moment_value,
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.piezoelectric_bending_moment_label2.grid(
                row=8, 
                column=2, 
                sticky="nsew", 
                padx=(0,0),
                pady=(0,0),
                columnspan=3
            )
            

            #BLOCKING_FORCE_CANTILEVER VARIABLE
            self.blocking_force_cantilever_value = tkinter.DoubleVar(value=0)
            self.blocking_force_cantilever_value.trace_add("write", lambda *args, identifier="blocking_force_cantilever_value": globals.app.variable_updated(identifier))
            

            #BLOCKING_FORCE_CANTILEVER LABEL
            self.blocking_force_cantilever_label1 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text=f"Blocking force cantilever tip:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.blocking_force_cantilever_label1.grid(
                row=9, 
                column=0, 
                columnspan=3,
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
            )
            self.blocking_force_cantilever_label2 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                textvariable=self.blocking_force_cantilever_value, 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.blocking_force_cantilever_label2.grid(
                row=9, 
                column=2, 
                columnspan=3,
                sticky="nsew", 
                padx=(0,0),
                pady=(0,0),
            )


            #INITIAL_CURVATURE VARIABLE
            self.initial_curvature_value = tkinter.DoubleVar(value=0)
            self.initial_curvature_value.trace_add("write", lambda *args, identifier="initial_curvature_value": globals.app.variable_updated(identifier))
            

            #INITIAL_CURVATURE LABEL
            self.initial_curvature_label1 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text="Initial curvature:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.initial_curvature_label1.grid(
                row=10, 
                column=0, 
                columnspan=3,
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
            )
            self.initial_curvature_label2 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                textvariable=self.initial_curvature_value, 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.initial_curvature_label2.grid(
                row=10, 
                column=2, 
                columnspan=3,
                sticky="nsew", 
                padx=(0,0),
                pady=(0,0),
            )


            #FINAL_CURVATURE VARIABLE
            self.final_curvature_value = tkinter.DoubleVar(value=0)
            self.final_curvature_value.trace_add("write", lambda *args, identifier="final_curvature_value": globals.app.variable_updated(identifier))            

            #FINAL_CURVATURE LABEL
            self.final_curvature_label1 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                text="Final curvature:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.final_curvature_label1.grid(
                row=11, 
                column=0, 
                columnspan=3,
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
            )
            self.final_curvature_label2 = customtkinter.CTkLabel(
                master=parameters_panel_frame, 
                textvariable=self.final_curvature_value, 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.final_curvature_label2.grid(
                row=11, 
                column=2, 
                columnspan=3,
                sticky="nsew", 
                padx=(0,0),
                pady=(0,0),
            )


        return parameters_panel_frame
  

    def piezo_material_entry_updated(self, entry_id):
        # print("PIEZO_MATERIAL_ENTRY_UPDATED()")

        if(entry_id.get() not in globals.materials):
            messagebox.showerror("Name error", f"Material '{entry_id.get()}' not found.\nMake sure it is spelled correctly")

        #Redraw Layer stack
        globals.layer_stack_canvas.draw_material_stack()

        #Redraw graphs
        globals.graph_canvas.draw_z_tip_is_graph()

