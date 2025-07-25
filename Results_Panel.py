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
    
 
    #ADD FUNCTION COMMENT
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
            self.results_panel_frame.columnconfigure(0, weight=1, uniform="group1")
            self.results_panel_frame.columnconfigure(1, weight=1, uniform="group1")
            self.results_panel_frame.columnconfigure(2, weight=1, uniform="group1")
            self.results_panel_frame.columnconfigure(3, weight=1, uniform="group1")
            self.results_panel_frame.columnconfigure(4, weight=1, uniform="group1")
            self.results_panel_frame.columnconfigure(5, weight=1, uniform="group1")

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
            columnspan=6
        )


        #STRESS_NEUTRAL_SIO2_THICKNESS LABEL
        if not hasattr(self, "stress_neutral_SiO2_thickness_label1"):
            self.stress_neutral_SiO2_thickness_label1 = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                text=f"Stress-neutral SiO2-thickness:",
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color
            )
            self.stress_neutral_SiO2_thickness_label2 = customtkinter.CTkLabel(
                master=self.results_panel_frame,
                textvariable=globals.t_sol,
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color,
                anchor="w"
            )

        self.stress_neutral_SiO2_thickness_label1.grid(
            row=1, 
            column=0, 
            sticky="w", 
            padx=(0,0),
            pady=(0,0),
            columnspan=3,
        )
        self.stress_neutral_SiO2_thickness_label2.grid(
            row=1, 
            column=3, 
            sticky="w", 
            padx=(0,0),
            pady=(0,0),
            columnspan=3
        )
            
        
        #PIEZOELECTRIC_BENDING_MOMENT LABELS
        if not hasattr(self, "piezo_electric_bending_moment_label"):
            self.piezo_electric_bending_moment_label = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                text=f"Piezo electric bending moment:",
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color,
                # text_color="#49910d",
                font=(settings.results_panel_headline_font, settings.results_panel_headline_size, settings.results_panel_headline_weight) 
            )
        self.piezo_electric_bending_moment_label.grid(
            row=2, 
            column=0, 
            sticky="nsew", 
            padx=(0,0),
            pady=(0,0),
            columnspan=6,
        )

        row_counter = 3
        column_counter = 0
        #Counter to check if ALL piezo_checkboxes are "off"
        checkbox_counter = 0

        #Loop through all materials:
        for material in dict(reversed(globals.materials.items())):
            if("Piezo_checkbox_id" in globals.materials[material]):
                #Remove label_name and label_value widget if piezo material was selected before, but not anymore
                if globals.materials[material]["Piezo_checkbox_id"].get() == "off":
                    checkbox_counter += 1
                    if("Results_panel_Mp_material_name_label_id" in globals.materials[material]):
                        globals.materials[material]["Results_panel_Mp_material_name_label_id"].destroy()
                        del globals.materials[material]["Results_panel_Mp_material_name_label_id"]
                    
                    if("Results_panel_Mp_value_label_id" in globals.materials[material]):
                        globals.materials[material]["Results_panel_Mp_value_label_id"].destroy()
                        del globals.materials[material]["Results_panel_Mp_value_label_id"]
                    

                #material->piezo_checkbox is "on":
                if(globals.materials[material]["Piezo_checkbox_id"].get() == "on"):
                    #Check if label for this material has been created before
                    if("Results_panel_Mp_material_name_label_id" not in globals.materials[material]):
                        #create label for material_name in row and column
                        material_name_label = customtkinter.CTkLabel(
                            master=self.results_panel_frame, 
                            text=f"{material}", 
                            fg_color=settings.results_panel_background_color,
                            text_color=globals.materials[material]["Color"].get(),
                        )
                        material_name_label.grid(
                            row=row_counter, 
                            column=column_counter, 
                            sticky="nsew", 
                            padx=(0,0),
                            pady=(0,0),
                        )

                        #Store the label
                        globals.materials[material]["Results_panel_Mp_material_name_label_id"] = material_name_label
                    #Label exists, move it
                    else:
                        globals.materials[material]["Results_panel_Mp_material_name_label_id"].grid(row=row_counter, column=column_counter)

                    

                    #create label for value in row+1 and column
                    if("Results_panel_Mp_value_label_id" not in globals.materials[material]):                  
                        Mp_value_label = customtkinter.CTkLabel(
                        master=self.results_panel_frame, 
                        # textvariable=(is set in later function),
                        fg_color="#49910d",
                        text_color=settings.results_panel_text_color,
                        )
                        Mp_value_label.grid(
                            row=row_counter+1, 
                            column=column_counter, 
                            sticky="nsew", 
                            padx=(0,2),
                            pady=(0,0),
                        )
                        #Store the label
                        globals.materials[material]["Results_panel_Mp_value_label_id"] = Mp_value_label
                    else:
                        globals.materials[material]["Results_panel_Mp_value_label_id"].grid(row=row_counter+1, column=column_counter)


                    column_counter += 1

                    if(column_counter >= 6):
                        #Reset column_counter
                        column_counter = 0
                        row_counter += 2


            #Display error message if no piezo materials have been chosen
            if(checkbox_counter == len(globals.materials)):
                self.error_label = customtkinter.CTkLabel(
                    master=self.results_panel_frame, 
                    text=f"No piezo material selected", 
                    fg_color=settings.results_panel_background_color,
                    text_color="red",
                )
                self.error_label.grid(
                    row=row_counter, 
                    column=0, 
                    sticky="nsew", 
                    padx=(0,0),
                    pady=(0,0),
                    columnspan=6
                )
            else:
                if hasattr(self, "error_label"):                  
                    self.error_label.destroy()



        #Increment row_counter for next label
        row_counter += 2




        #BLOCKING_FORCE_CANTILEVER LABELS
        if not hasattr(self, "blocking_force_cantilever_label"):
            self.blocking_force_cantilever_label = customtkinter.CTkLabel(
                master=self.results_panel_frame, 
                text=f"Blocking force cantilever tip:", 
                fg_color=settings.results_panel_background_color,
                text_color=settings.results_panel_text_color,
                # text_color="#ba3609",
                font=(settings.results_panel_headline_font, settings.results_panel_headline_size, settings.results_panel_headline_weight) 
            )
        self.blocking_force_cantilever_label.grid(
            row=row_counter, 
            column=0, 
            sticky="nsew", 
            padx=(0,0),
            pady=(0,0),
            columnspan=6
        )
        
        row_counter+=1
        column_counter = 0
        #Counter to check if ALL piezo_checkboxes are "off"
        checkbox_counter = 0

        #Loop through all materials:
        for material in dict(reversed(globals.materials.items())):
            if("Piezo_checkbox_id" in globals.materials[material]):
                #Remove label_name and label_value widget if piezo material was selected before, but not anymore
                if globals.materials[material]["Piezo_checkbox_id"].get() == "off":
                    checkbox_counter += 1
                    if("Results_panel_blocking_force_material_name_label_id" in globals.materials[material]):
                        globals.materials[material]["Results_panel_blocking_force_material_name_label_id"].destroy()
                        del globals.materials[material]["Results_panel_blocking_force_material_name_label_id"]
                    
                    if("Results_panel_blocking_force_value_label_id" in globals.materials[material]):
                        globals.materials[material]["Results_panel_blocking_force_value_label_id"].destroy()
                        del globals.materials[material]["Results_panel_blocking_force_value_label_id"]

                #material->piezo_checkbox is "on":
                if(globals.materials[material]["Piezo_checkbox_id"].get() == "on"):
                    #Check if label for this material has been created before
                    if("Results_panel_blocking_force_material_name_label_id" not in globals.materials[material]):
                        #create label for material_name in row and column
                        material_name_label = customtkinter.CTkLabel(
                            master=self.results_panel_frame, 
                            text=f"{material}", 
                            fg_color=settings.results_panel_background_color,
                            text_color=globals.materials[material]["Color"].get(),
                        )
                        material_name_label.grid(
                            row=row_counter, 
                            column=column_counter, 
                            sticky="nsew", 
                            padx=(0,0),
                            pady=(0,0),
                        )

                        #Store the label
                        globals.materials[material]["Results_panel_blocking_force_material_name_label_id"] = material_name_label
                    #Label exists, move it
                    else:
                        globals.materials[material]["Results_panel_blocking_force_material_name_label_id"].grid(row=row_counter, column=column_counter)

                    

                    #create label for value in row+1 and column
                    if("Results_panel_blocking_force_value_label_id" not in globals.materials[material]):                  
                        blocking_force_value_label = customtkinter.CTkLabel(
                        master=self.results_panel_frame, 
                        # textvariable=(is set in later function),
                        fg_color="#ba3609",
                        text_color=settings.results_panel_text_color,
                        )
                        blocking_force_value_label.grid(
                            row=row_counter+1, 
                            column=column_counter, 
                            sticky="nsew", 
                            padx=(0,2),
                            pady=(0,0),
                        )
                        #Store the label
                        globals.materials[material]["Results_panel_blocking_force_value_label_id"] = blocking_force_value_label
                    else:
                        globals.materials[material]["Results_panel_blocking_force_value_label_id"].grid(row=row_counter+1, column=column_counter)


                    column_counter += 1

                    if(column_counter >= 6):
                        #Reset column_counter
                        column_counter = 0
                        row_counter += 2


            #Display error message if no piezo materials have been chosen
            if(checkbox_counter == len(globals.materials)):
                self.error_label2 = customtkinter.CTkLabel(
                    master=self.results_panel_frame, 
                    text=f"No piezo material selected", 
                    fg_color=settings.results_panel_background_color,
                    text_color="red",
                )
                self.error_label2.grid(
                    row=row_counter, 
                    column=0, 
                    sticky="nsew", 
                    padx=(0,0),
                    pady=(0,0),
                    columnspan=6
                )
            else:
                if hasattr(self, "error_label2"):                  
                    self.error_label2.destroy()


        #Update the values in the equation labels
        self.update_equation_labels()

        return self.results_panel_frame
        

    #ADD DESCRIPTION OF FUNCTION
    def update_equation_labels(self):
        """
        """

        print("UPDATE_EQUATION_LABELS()")

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
        
        #Volt value
        V_p = globals.volt_value.get()

        #e_31_f value
        e_31_f = globals.e_31_f_value.get()

        #L value
        L = globals.L_value.get()


        #CALCULATE BLOCKING FORCE CANTILEVER
        for material in globals.materials:
            if("Piezo_checkbox_id" in globals.materials[material]):
                if(globals.materials[material]["Piezo_checkbox_id"].get() == "on"):
                    piezo_thickness = globals.materials[material]["Thickness [nm]"].get() / 1e9
                    
                    #Total thickness of materials from substrate up to (but not including) chosen piezo material
                    h_Si = 0 
                    for material2 in globals.materials:
                        if(material2 == material):
                            break
                        h_Si += globals.materials[material2]["Thickness [nm]"].get()
                    
                    blocking_force = globals.equations.calculate_blocking_force(E, t, V_p, e_31_f, piezo_thickness, h_Si, W, L)
                    if("Results_panel_blocking_force_value_label_id" in globals.materials[material]):
                        if(isinstance(blocking_force, Exception)):
                            print(blocking_force)
                            globals.materials[material]["Results_panel_blocking_force_value_label_id"].configure(text=f"ERROR")
                        else:
                            globals.materials[material]["Results_panel_blocking_force_value_label_id"].configure(text=f"{blocking_force:.2e}")
                            globals.materials[material]["Blocking_force_value"] = tkinter.DoubleVar(value=blocking_force)


        #CALCULATE ZN
        Zn = globals.equations.calculate_Zn(E, t, nu)

        for material in globals.materials: 
            if("Piezo_checkbox_id" in globals.materials[material]):
                if(globals.materials[material]["Piezo_checkbox_id"].get() == "on"):
                    piezo_thickness = globals.materials[material]["Thickness [nm]"].get() / 1e9

                    #CALCULATE ZP
                    Zp = globals.equations.calculate_mid_piezo(t, Zn, piezo_thickness)

                    globals.materials[material]["Zp_value"] = tkinter.DoubleVar(value=Zp)

                    #CALCULATE M_p
                    Mp = globals.equations.calculate_Mp_cantilever(Zp, W, V_p, e_31_f)
                    if("Results_panel_Mp_value_label_id" in globals.materials[material]):
                        if(isinstance(Mp, Exception)):
                            globals.materials[material]["Results_panel_Mp_value_label_id"].configure(text=f"ERROR")
                        else:
                            globals.materials[material]["Results_panel_Mp_value_label_id"].configure(text=f"{Mp:.2e}")
                            globals.materials[material]["Mp_value"] = tkinter.DoubleVar(value=Mp)




        # try:
            #CALCULATE M_IS
            # M_is = globals.equations.calculate_M_is_cantilever(Zn, sigma_i, t, W) 

            #CALCULATE M_TOT
            # M_tot = globals.equations.calculate_M_tot_cantilever(M_is, M_p)

        #     #CALCULATE EI
        #     EI = globals.equations.calculate_EI(E, t, nu, W, Zn)

        #     #CALCULATE CURV_IS
        #     curv_is = globals.equations.calculate_curvature(M_tot, EI)

        #     #Neutralizing material thickness
        #     try:
        #         neutralizing_material_thickness = globals.materials[globals.neutralizing_material_name.get()]["Thickness [nm]"].get() / 1e9     
        #     except:
        #         raise ValueError("Select neutralizing material")      

        #     #CALCULATE T_SOL
        #     t_sol = globals.equations.find_t_solution(t, L, curv_is, neutralizing_material_thickness)
        #     globals.t_sol.set(t_sol)
        #     # self.stress_neutral_SiO2_thickness_label2.configure(text="", textvariable=globals.t_sol, text_color=settings.parameters_panel_text_color)

        #     #REMOVE THIS WHEN NEUTRFALIZE GLOBAL STRESS IS FIXED
        #     self.stress_neutral_SiO2_thickness_label2.configure(text=f"fix neutralize_global_stress()", textvariable="", text_color="red")
        #     self.stress_neutral_SiO2_thickness_label2.configure(text=f"fix neutralize_global_stress()", textvariable="")
        #     ##########################################################

        # except Exception as error:
        #     #Set t_sol to error
        #     # self.stress_neutral_SiO2_thickness_label2.configure(text=f"{error}", textvariable="", text_color="red")
        #     # self.stress_neutral_SiO2_thickness_label2.configure(text=f"{error}", textvariable="")

        #     #REMOVE THIS WHEN NEUTRFALIZE GLOBAL STRESS IS FIXED
        #     self.stress_neutral_SiO2_thickness_label2.configure(text=f"fix neutralize_global_stress()", textvariable="", text_color="red")
        #     self.stress_neutral_SiO2_thickness_label2.configure(text=f"fix neutralize_global_stress()", textvariable="")
        #     ##########################################################

        #     return



