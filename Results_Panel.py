import tkinter
import customtkinter
import settings #File containing settings
import globals  #File containing global variables


class Results_Panel:
    def __init__(self, window, row_placement:int, column_placement:int):
        # print("CLASS RESULTS_PANEL INIT()")

        #Window where everything is placed
        self.program_window = window

        #Row/column placement in main program window
        self.row_placement = row_placement
        self.column_placement = column_placement

        #Create results_Panel
        self.results_panel_frame = self.create_results_panel()
    

    def create_results_panel(self):
        """
        """
        # print("CREATE_RESULTS_PANEL()")

        #if results_panel_frame has NOT been created before, create it
        if not hasattr(self, 'results_panel_frame'):
            self.results_panel_frame = customtkinter.CTkScrollableFrame(
                master=self.program_window,
                fg_color=settings.results_panel_background_color
            )
            self.results_panel_frame.grid(
                row=self.row_placement,
                column=self.column_placement,
                padx=(settings.results_panel_padding_left, settings.results_panel_padding_right),
                pady=(settings.results_panel_padding_top, settings.results_panel_padding_bottom),
                sticky="nswe"
            )

            #Define the row&column layout of the results_panel
            self.results_panel_frame.columnconfigure(0, weight=50, uniform="group1")
            self.results_panel_frame.columnconfigure(1, weight=50, uniform="group1")

            self.results_panel_frame.rowconfigure((0,1,2), weight=1, uniform="group1")


        #HEADLINE
        if not hasattr(self, "results_panel_headline"):
            self.results_panel_headline = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                text="Results", 
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color,
                font=(settings.results_panel_headline_font, settings.results_panel_headline_size, settings.results_panel_headline_weight) 
            )
            self.results_panel_headline.grid(
                row=0, 
                column=0,
                sticky="", 
                padx=(0,0),
                pady=(0,0),
                columnspan=2
            )


        #STRESS_NEUTRAL_SIO2_THICKNESS LABEL
        if not hasattr(self, "stress_neutral_SiO2_thickness_label1"):
            self.stress_neutral_SiO2_thickness_label1 = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                text=f"Stress-neutral SiO2-thickness:",
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color
            )
            self.stress_neutral_SiO2_thickness_label1.grid(
                row=1, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
            )
            self.stress_neutral_SiO2_thickness_label2 = customtkinter.CTkLabel(
                master=self.results_panel_frame,
                textvariable=globals.t_sol,
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color,
                anchor="w"
            )
            self.stress_neutral_SiO2_thickness_label2.grid(
                row=1, 
                column=1, 
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
            )
            

        #PIEZOELECTRIC_BENDING_MOMENT LABEL
        if not hasattr(self, "piezoelectric_bending_moment_label1"):
            self.piezoelectric_bending_moment_label1 = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                text=f"Piezoelectric bending moment:", 
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color,
            )
            self.piezoelectric_bending_moment_label1.grid(
                row=2, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
            )
            self.piezoelectric_bending_moment_label2 = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                textvariable=globals.M_p,
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color,
                anchor="w"
            )
            self.piezoelectric_bending_moment_label2.grid(
                row=2, 
                column=1, 
                sticky="nsew", 
                padx=(0,0),
                pady=(0,0),
            )
            

        #BLOCKING_FORCE_CANTILEVER LABEL
        if not hasattr(self, "blocking_force_cantilever_label1"):
            self.blocking_force_cantilever_label1 = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                text=f"Blocking force cantilever tip:", 
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color
            )
            self.blocking_force_cantilever_label1.grid(
                row=3, 
                column=0, 
                sticky="w", 
                padx=(0,0),
                pady=(0,0),
            )
            self.blocking_force_cantilever_label2 = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                textvariable=globals.blocking_force_cantilever, 
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color,
                anchor="w"
            )
            self.blocking_force_cantilever_label2.grid(
                row=3, 
                column=1, 
                sticky="nsew", 
                padx=(0,0),
                pady=(0,0),
            )


        #Update the values in the equation labels
        self.update_equation_labels()

        return self.results_panel_frame
        

    #ADD DESCRIPTION OF FUNCTION
    def update_equation_labels(self):
        """
        """

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
            self.blocking_force_cantilever_label2.configure(text="", textvariable=globals.blocking_force_cantilever, text_color=settings.results_panel_text_color)

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
            self.piezoelectric_bending_moment_label2.configure(text="", textvariable=globals.M_p, text_color=settings.results_panel_text_color)


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



