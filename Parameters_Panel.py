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

            self.parameters_panel_frame.rowconfigure((0,1,2,3,4,5,6), weight=1, uniform="group1")


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


        #"rᵢ [μm]" LABEL
        if not hasattr(self, "ri_label"):
            self.ri_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="rᵢ [μm]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.ri_label.grid(
                row=2, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1)
            )


        #"rᵢ [μm]" ENTRY
        if not hasattr(self, "ri_entry"):
            self.ri_entry = customtkinter.CTkEntry(
                master=self.parameters_panel_frame,
                textvariable=tkinter.StringVar(value="not in use"),
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=1,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.ri_entry.grid(
                row=2, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,1)
            )


        #"r₀ [μm]" LABEL
        if not hasattr(self, "ro_label"):
            self.ro_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text=" r₀ [μm]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.ro_label.grid(
                row=3, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1)
            )


        #"r₀ [μm]" ENTRY
        if not hasattr(self, "ro_entry"):
            self.ro_entry = customtkinter.CTkEntry(
                master=self.parameters_panel_frame,
                textvariable=tkinter.StringVar(value="not in use"),
                fg_color = settings.parameters_panel_entry_background_color,
                border_color=settings.parameters_panel_entry_border_color,
                border_width=1,
                text_color=settings.parameters_panel_entry_text_color,
                justify="center"
            )
            self.ro_entry.grid(
                row=3, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,1)
            )

            
        #E_31_F LABEL
        if not hasattr(self, "e_31_f_label"):
            self.e_31_f_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="e₃₁ [C/m²]", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.e_31_f_label.grid(
                row=4, 
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
                row=4, 
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
                row=5, 
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
                row=5, 
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
                row=5, 
                column=2,
                sticky="",
                padx=(0,0),
                pady=(0,1)
            )

        #PIEZO_MATERIAL LABEL
        if not hasattr(self, "piezo_material_label"):
            self.piezo_material_label = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text="Piezo material:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.piezo_material_label.grid(
                row=6, 
                column=0, 
                columnspan=2,
                sticky="w", 
                padx=(0,0),
                pady=(0,1)
            )
            

        #PIEZO_MATERIAL COMBOBOX
        if not hasattr(self, "piezo_material_combobox"):
            self.piezo_material_combobox = customtkinter.CTkComboBox(
                master=self.parameters_panel_frame,
                variable=globals.piezo_material_name,
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
            self.piezo_material_combobox.grid(
                row=6, 
                column=2, 
                sticky="",
                padx=(0,0),
                pady=(0,1),
            )
        else:
            if(self.piezo_material_combobox.get() not in globals.materials.keys()):
                self.piezo_material_combobox.set("")
            self.piezo_material_combobox.configure(
                values=list(reversed((globals.materials.keys())))
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
                row=7, 
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
                row=7, 
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
                row=8, 
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
                row=8, 
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


        #STRESS_NEUTRAL_SIO2_THICKNESS LABEL
        if not hasattr(self, "stress_neutral_SiO2_thickness_label1"):
            self.stress_neutral_SiO2_thickness_label1 = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text=f"Stress-neutral SiO2-thickness:",
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.stress_neutral_SiO2_thickness_label1.grid(
                row=9, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1),
                columnspan=3
            )
            self.stress_neutral_SiO2_thickness_label2 = customtkinter.CTkLabel(
                master=self.parameters_panel_frame,
                textvariable=globals.t_sol,
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color,
                anchor="w"
            )
            self.stress_neutral_SiO2_thickness_label2.grid(
                row=9, 
                column=2, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1),
                columnspan=3,
            )
            

        #PIEZOELECTRIC_BENDING_MOMENT LABEL
        if not hasattr(self, "piezoelectric_bending_moment_label1"):
            self.piezoelectric_bending_moment_label1 = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text=f"Piezoelectric bending moment:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color,
            )
            self.piezoelectric_bending_moment_label1.grid(
                row=10, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,1),
                columnspan=3
            )
            self.piezoelectric_bending_moment_label2 = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                textvariable=globals.M_p,
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color,
                anchor="w"
            )
            self.piezoelectric_bending_moment_label2.grid(
                row=10, 
                column=2, 
                sticky="nsew", 
                padx=(0,0),
                pady=(0,1),
                columnspan=3
            )
            

        #BLOCKING_FORCE_CANTILEVER LABEL
        if not hasattr(self, "blocking_force_cantilever_label1"):
            self.blocking_force_cantilever_label1 = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                text=f"Blocking force cantilever tip:", 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color
            )
            self.blocking_force_cantilever_label1.grid(
                row=11, 
                column=0, 
                columnspan=3,
                sticky="w", 
                padx=(0,0),
                pady=(0,1),
            )
            self.blocking_force_cantilever_label2 = customtkinter.CTkLabel(
                master=self.parameters_panel_frame, 
                textvariable=globals.blocking_force_cantilever, 
                fg_color=settings.parameters_panel_background_color,
                text_color=settings.parameters_panel_text_color,
                anchor="w"
            )
            self.blocking_force_cantilever_label2.grid(
                row=11, 
                column=2, 
                columnspan=3,
                sticky="nsew", 
                padx=(0,0),
                pady=(0,1),
            )


        #Update the values in the equation labels
        self.update_equation_labels()


        return self.parameters_panel_frame


    #ADD DESCRIPTION OF FUNCTION
    def update_equation_labels(self):
        """
        """

       





        #lag en try-except block for hver label
        #finn ut hvilke verdier er nødvendige før hver label, slik at hvis en verdi er feil så kan de tilsvarende labelene også feile



        print("UPDATE_EQUATION_LABELS()")

        # # try:
        # #     # E
        # #     # t
        # #     # W
        # #     # piezo_thickness    
        # #     # V_p
        # #     # e_31_f
        # #     # L
        # #     # h_Si
        # #     #calculate blocking
        # #     #set blocking label
        # # except
        # #     #set all labels to error
        # #     return

        # try:
        #     # nu
        #     # Zn
        #     # Zp
        #     #calucalte M_p
        #     #set M_p label

        # except
        #     #set M_p and t_sol label to error
        #     return 

        # try:
        #     # sigma_i
        #     # M_is
        #     # M_p
        #     # M_tot
        #     # EI
        #     # curv_is
        #     # neutralizing_material_thickness
        #     #calculate t_sol
        #     #set t_sol
        # except
        #     #set t_sol label to error


        try:
            #Fetch necessary values and calculations
            W = 160 / 1e6
            t = []
            sigma_i = []
            E = []
            nu = []
            for material in globals.materials:
                t.append(globals.materials[material]["Thickness [nm]"].get() / 1e9)
                sigma_i.append(globals.materials[material]["Stress_x [MPa]"].get() * 1e6)
                E.append(globals.materials[material]["Modulus [GPa]"].get() * 1e9)
                nu.append(globals.materials[material]["Poisson"].get())
            

            #piezo material thickness
            try:
                piezo_thickness = globals.materials[globals.piezo_material_name.get()]["Thickness [nm]"].get() / 1e9
            except:
                raise ValueError("Select piezo material")
            
            #Volt value
            V_p = globals.volt_value.get()

            #e_31_f value
            e_31_f = globals.e_31_f_value.get()

            #L value
            L = globals.L_value.get()

            #Total thickness of materials from substrate up to (but not including) chosen piezo material
            h_Si = 0 
            for material in globals.materials:
                if(material == globals.piezo_material_name.get()):
                    break
                h_Si += globals.materials[material]["Thickness [nm]"].get()
                
            #CALCULATE BLOCKING FORCE CANTILEVER
            blocking_force = globals.equations.calculate_blocking_force(E, t, V_p, e_31_f, piezo_thickness, h_Si, W, L)
            globals.blocking_force_cantilever.set(f"{blocking_force:.2e}")
            self.blocking_force_cantilever_label2.configure(text="", textvariable=globals.blocking_force_cantilever, text_color=settings.parameters_panel_text_color)

        except Exception as error:
            #Set M_p to error
            self.piezoelectric_bending_moment_label2.configure(text=f"{error}", textvariable="", text_color="red")
            self.piezoelectric_bending_moment_label2.configure(text=f"{error}", textvariable="")

            #Set blocking force to error
            self.blocking_force_cantilever_label2.configure(text=f"{error}", textvariable="", text_color="red")
            self.blocking_force_cantilever_label2.configure(text=f"{error}", textvariable="")

            #Set t_sol to error
            self.stress_neutral_SiO2_thickness_label2.configure(text=f"{error}", textvariable="", text_color="red")
            self.stress_neutral_SiO2_thickness_label2.configure(text=f"{error}", textvariable="")

            return
        
        try:
            #CALCULATE ZN
            Zn = globals.equations.calculate_Zn(E, t, nu)
            
            #CALCULATE ZP
            Zp = globals.equations.calculate_mid_piezo(t, Zn, piezo_thickness)

            #CALCULATE M_p
            M_p = globals.equations.calculate_M_p_cantilever(Zp, W, V_p, e_31_f)
            globals.M_p.set(f"{M_p:.2e}")
            self.piezoelectric_bending_moment_label2.configure(text="", textvariable=globals.M_p, text_color=settings.parameters_panel_text_color)


        except Exception as error:
            #Set M_p to error
            self.piezoelectric_bending_moment_label2.configure(text=f"{error}", textvariable="", text_color="red")
            self.piezoelectric_bending_moment_label2.configure(text=f"{error}", textvariable="")

            #Set t_sol to error
            self.stress_neutral_SiO2_thickness_label2.configure(text=f"{error}", textvariable="", text_color="red")
            self.stress_neutral_SiO2_thickness_label2.configure(text=f"{error}", textvariable="")
            
            return 
        
        try:
            #CALCULATE M_IS
            M_is = globals.equations.calculate_M_is_cantilever(Zn, sigma_i, t, W) 

            #CALCULATE M_TOT
            M_tot = globals.equations.calculate_M_tot_cantilever(M_is, M_p)

            #CALCULATE EI
            EI = globals.equations.calculate_EI(E, t, nu, W, Zn)

            #CALCULATE CURV_IS
            curv_is = globals.equations.calculate_curvature(M_tot, EI)

            #Neutralizing material thickness
            try:
                neutralizing_material_thickness = globals.materials[globals.neutralizing_material_name.get()]["Thickness [nm]"].get() / 1e9     
            except:
                raise ValueError("Select neutralizing material")      

            #CALCULATE T_SOL
            t_sol = globals.equations.find_t_solution(t, L, curv_is, neutralizing_material_thickness)
            globals.t_sol.set(t_sol)
            # self.stress_neutral_SiO2_thickness_label2.configure(text="", textvariable=globals.t_sol, text_color=settings.parameters_panel_text_color)

            #REMOVE THIS WHEN NEUTRFALIZE GLOBAL STRESS IS FIXED
            self.stress_neutral_SiO2_thickness_label2.configure(text=f"fix neutralize_global_stress()", textvariable="", text_color="red")
            self.stress_neutral_SiO2_thickness_label2.configure(text=f"fix neutralize_global_stress()", textvariable="")
            ##########################################################

        except Exception as error:
            #Set t_sol to error
            # self.stress_neutral_SiO2_thickness_label2.configure(text=f"{error}", textvariable="", text_color="red")
            # self.stress_neutral_SiO2_thickness_label2.configure(text=f"{error}", textvariable="")

            #REMOVE THIS WHEN NEUTRFALIZE GLOBAL STRESS IS FIXED
            self.stress_neutral_SiO2_thickness_label2.configure(text=f"fix neutralize_global_stress()", textvariable="", text_color="red")
            self.stress_neutral_SiO2_thickness_label2.configure(text=f"fix neutralize_global_stress()", textvariable="")
            ##########################################################

            return
