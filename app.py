import tkinter
from tkinter import messagebox
import tkinter.dialog
import customtkinter
import pyautogui  # For better user interface visual effects
import os
import pandas   #Excel-file reading
import openpyxl #Excel-file reading
import globals
import settings
from Material_Adjustment_Panel import Material_Adjustment_Panel
from Layer_Stack_Canvas import Layer_Stack_Canvas
from Material_Control_Panel import Material_Control_Panel
from Parameters_Panel import Parameters_Panel
from Results_Panel import Results_Panel
from Canvas_Control_Panel import Canvas_Control_Panel
from Graph_Canvas import Graph_Canvas
from Graph_Control_Panel import Graph_Control_Panel
from Equations import Equations
import traceback
import helper_functions



#Main application class
class App:
    def __init__(self, program_window):
        # print("CLASS APP INIT()")

        #Program window
        self.program_window = program_window

        #If excel file exists, load it into globals.materials
        if(os.path.isfile("Materials.xlsx")):
            self.load_materials_from_excel()
        
        #Initialize global variables
        globals.initialize_globals(self.program_window)

        #Class for easy access to calculation of important equations
        globals.equations = Equations()

        #Set correct row/column configuration and widget layout based on the "view"
        self.set_layout()
    
    
    def load_materials_from_excel(self):
        """Reads the excel-file in the folder and populates the self.materials dictionary with info about each material"""
        #print("LOAD_MATERIALS_FROM_EXCEL()")

        excel_file = "Materials.xlsx"

        #If there is a "materials" file in the folder, read it and populate the self.materials dictionary 
        if(os.path.isfile(excel_file)):
            try:
                #Read given excel file into Pandas dataframe
                excel_data = pandas.read_excel(excel_file)

                #Convert column names to lowercase
                excel_data.columns = excel_data.columns.str.lower()

                #Open excel-file to read background colors of each cell
                work_book = openpyxl.load_workbook(excel_file, data_only=True)
                fs = work_book.active

                #Loop through the rows in excel_file
                i = 2
                layer = len(excel_data)
                for column, row in excel_data.iterrows():
                    #Increment "i" to go to the next row
                    i+=1

                    #MATERIAL NAME CHECK
                    #If there is a headline called "material"                    
                    if("material" in row.index):
                        #If the value in the cell is empty or just spaces
                        if((pandas.isna(row["material"])) or str(row["material"]).isspace()):
                            row["material"] = tkinter.StringVar(value="No name")
                        #There is a value in the cell
                        else:
                            row["material"] = tkinter.StringVar(value=row["material"])
                    #If headline does not exist -> apply default value
                    else:
                        row["material"] = tkinter.StringVar(value="No name")


                    #THICKNESS CHECK
                    #If there is a headline called "thickness [nm]"
                    if("thickness [nm]" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["thickness [nm]"])):
                            row["thickness [nm]"] = tkinter.DoubleVar(value=0)
                        #There is a value in the cell
                        else:
                            thickness_conversion = helper_functions.convert_decimal_string_to_float(row["thickness [nm]"])
                            #If the value is invalid 
                            if((thickness_conversion == False) or (thickness_conversion < 0)):
                                row["thickness [nm]"] = tkinter.DoubleVar(value=0)
                            #The value in the cell is valid
                            else:
                                row["thickness [nm]"] = tkinter.DoubleVar(value=thickness_conversion)
                    #If excel headline does not exist -> apply default value
                    else:
                        row["thickness [nm]"] = tkinter.DoubleVar(value=0)


                    #UNIT CHECK
                    #If there is a headline called "unit"
                    if("unit" in row.index):
                        #If cell is empty or just spaces
                        if((pandas.isna(row["unit"])) or (row["unit"].isspace())):
                            row["unit"] = tkinter.StringVar(value="No value")
                        #There is a valid value in cell
                        else:
                            row["unit"] = tkinter.StringVar(value=row["unit"])
                    #There is no headline called "unit" -> apply default value
                    else:
                        row["unit"] = tkinter.StringVar(value="No value")


                    #INDENT CHECK
                    #If there is a headline called "indent [nm]"
                    if("indent [nm]" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["indent [nm]"])):
                            row["indent [nm]"] = tkinter.DoubleVar(value=0)
                        #There is a value in the cell
                        else:
                            indent_conversion = helper_functions.convert_decimal_string_to_float(row["indent [nm]"]) 
                            #If value in cell is not valid
                            if((indent_conversion == False) or (indent_conversion < 0)):
                                row["indent [nm]"] = tkinter.DoubleVar(value=0)
                            #The value in the cell is valid
                            else:
                                row["indent [nm]"] = tkinter.DoubleVar(value=indent_conversion)
                    #There excel headline does not exist -> apply default value
                    else:
                        row["indent [nm]"] = tkinter.DoubleVar(value=0)
                  

                    #COLOR CHECK
                    #If there is a headline called "color"
                    if("color" in row.index):
                        #If there is no valid value in the cell 
                        if((pandas.isna(row["color"])) or (self.is_valid_color(row["color"]) == False)):
                            row["color"] = tkinter.StringVar(value="white")
                        #There is a valid value in the cell
                        else:
                            row["color"] = tkinter.StringVar(value=row["color"])
                    #If there is no excel headline
                    else:
                        row["color"] = tkinter.StringVar(value="white")


                    #MODULUS CHECK
                    #If there is a headline called "modulus [gpa]"
                    if("modulus [gpa]" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["modulus [gpa]"])):
                            row["modulus [gpa]"] = tkinter.DoubleVar(value=0)
                        #If there is a value in the cell
                        else:
                            modulus_conversion = helper_functions.convert_decimal_string_to_float(row["modulus [gpa]"]) 
                            #If the value is invalid
                            if(modulus_conversion == False):
                                row["modulus [gpa]"] = tkinter.DoubleVar(value=0)
                            #If the value is valid
                            else:
                                row["modulus [gpa]"] = tkinter.DoubleVar(value=abs(modulus_conversion))
                    #If there is no headline -> apply default value
                    else:
                        row["modulus [gpa]"] = tkinter.DoubleVar(value=0)  


                    #CTE CHECK
                    #If there is a headline called "cte [ppm/deg]"
                    if("cte [ppm/deg]" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["cte [ppm/deg]"])):
                            row["cte [ppm/deg]"] = tkinter.DoubleVar(value=0)
                        #There is a value in the cell
                        else:
                            cte_conversion = helper_functions.convert_decimal_string_to_float(row["cte [ppm/deg]"])
                            #If the value is invalid 
                            if(cte_conversion == False):
                                row["cte [ppm/deg]"] = tkinter.DoubleVar(value=0)
                            #The value in the cell is valid
                            else:
                                row["cte [ppm/deg]"] = tkinter.DoubleVar(value=abs(cte_conversion))
                    #If excel headline does not exist -> apply default value
                    else:
                        row["cte [ppm/deg]"] = tkinter.DoubleVar(value=0)
                    
                    
                    #DENSITY CHECK
                    #If there is a headline called "density [kg/m3]"
                    if("density [kg/m3]" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["density [kg/m3]"])):
                            row["density [kg/m3]"] = tkinter.DoubleVar(value=0)
                        #There is a value in the cell
                        else:
                            density_conversion = helper_functions.convert_decimal_string_to_float(row["density [kg/m3]"])
                            #If the value is invalid 
                            if(density_conversion == False):
                                row["density [kg/m3]"] = tkinter.DoubleVar(value=0)
                            #The value in the cell is valid
                            else:
                                row["density [kg/m3]"] = tkinter.DoubleVar(value=abs(density_conversion))
                    #If excel headline does not exist -> apply default value
                    else:
                        row["density [kg/m3]"] = tkinter.DoubleVar(value=0)


                    #STRESS CHECK
                    #If there is a headline called "stress_x [mpa]"
                    if("stress_x [mpa]" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["stress_x [mpa]"])):
                            row["stress_x [mpa]"] = tkinter.DoubleVar(value=0)
                        #There is a value in the cell
                        else:
                            stress_conversion = helper_functions.convert_decimal_string_to_float(row["stress_x [mpa]"])
                            #If the value is invalid 
                            if(stress_conversion == False):
                                row["stress_x [mpa]"] = tkinter.DoubleVar(value=0)
                            #The value in the cell is valid
                            else:
                                row["stress_x [mpa]"] = tkinter.DoubleVar(value=stress_conversion)
                    #If excel headline does not exist -> apply default value
                    else:
                        row["stress_x [mpa]"] = tkinter.DoubleVar(value=0)


                    #POISSON CHECK
                    #If there is a headline called "poisson"
                    if("poisson" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["poisson"])):
                            row["poisson"] = tkinter.DoubleVar(value=0)
                        #There is a value in the cell
                        else:
                            poisson_conversion = helper_functions.convert_decimal_string_to_float(row["poisson"])
                            #If the value is invalid 
                            if(poisson_conversion == False):
                                row["poisson"] = tkinter.DoubleVar(value=0)
                            #The value in the cell is valid
                            else:
                                row["poisson"] = tkinter.DoubleVar(value=poisson_conversion)
                    #If excel headline does not exist -> apply default value
                    else:
                        row["poisson"] = tkinter.DoubleVar(value=0)


                    #R0 CHECK
                    #If there is a headline called "r0"
                    if("r0" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["r0"])):
                            row["r0"] = tkinter.DoubleVar(value=0)
                        #There is a value in the cell
                        else:
                            R0_conversion = helper_functions.convert_decimal_string_to_float(row["r0"])
                            #If the value is invalid 
                            if(R0_conversion == False):
                                row["r0"] = tkinter.DoubleVar(value=0)
                            #The value in the cell is valid
                            else:
                                row["r0"] = tkinter.DoubleVar(value=R0_conversion)
                    #If excel headline does not exist -> apply default value
                    else:
                        row["r0"] = tkinter.DoubleVar(value=0)


                    #R CHECK
                    #If there is a headline called "r"
                    if("r" in row.index):
                        #If there is no value in the cell -> apply default value
                        if(pandas.isna(row["r"])):
                            row["r"] = tkinter.DoubleVar(value=0)
                        #There is a value in the cell
                        else:
                            R_conversion = helper_functions.convert_decimal_string_to_float(row["r"])
                            #If the value is invalid 
                            if(R_conversion == False):
                                row["r"] = tkinter.DoubleVar(value=0)
                            #The value in the cell is valid
                            else:
                                row["r"] = tkinter.DoubleVar(value=R_conversion)
                    #If excel headline does not exist -> apply default value
                    else:
                        row["r"] = tkinter.DoubleVar(value=0)

                    
                    #LAYER
                    row["layer"] = tkinter.IntVar(value=int(layer))

                    #ADD TRACES TO ALL VARIABLES
                    # Trace changes to trigger canvas redraw
                    row["material"].trace_add("write", lambda *args, identifier="material_name_updated": self.update_widgets(identifier))
                    # row["layer"].trace_add("write", lambda *args, identifier="material_layer_updated": self.update_widgets(identifier))
                    row["thickness [nm]"].trace_add("write", lambda *args, identifier="material_thickness_updated": self.update_widgets(identifier))
                    # row["unit"].trace_add("write", lambda *args, identifier="material_unit_updated": self.update_widgets(identifier))
                    row["indent [nm]"].trace_add("write", lambda *args, identifier="material_indent_updated": self.update_widgets(identifier))
                    row["color"].trace_add("write", lambda *args, identifier="material_color_updated": self.update_widgets(identifier))
                    row["modulus [gpa]"].trace_add("write", lambda *args, identifier="material_modulus_updated": self.update_widgets(identifier))
                    row["cte [ppm/deg]"].trace_add("write", lambda *args, identifier="material_cte_updated": self.update_widgets(identifier))
                    row["density [kg/m3]"].trace_add("write", lambda *args, identifier="material_density_updated": self.update_widgets(identifier))
                    row["stress_x [mpa]"].trace_add("write", lambda *args, identifier="material_stress_x_updated": self.update_widgets(identifier))
                    row["poisson"].trace_add("write", lambda *args, identifier="material_poisson_updated": self.update_widgets(identifier))
                    row["r0"].trace_add("write", lambda *args, identifier="material_R0_updated": self.update_widgets(identifier))
                    row["r"].trace_add("write", lambda *args, identifier="material_R_updated": self.update_widgets(identifier))

                    
                    #Create an "info" dictionary to contain all info from excel-file
                    info = {
                        "Name": row["material"],
                        "Layer": row["layer"],
                        "Thickness [nm]": row["thickness [nm]"],
                        "Unit": row["unit"],
                        "Indent [nm]": row["indent [nm]"],
                        "Color": row["color"],
                        "Modulus [GPa]": row["modulus [gpa]"],
                        "CTE [ppm/deg]": row["cte [ppm/deg]"],
                        "Density [kg/m3]": row["density [kg/m3]"],
                        "Stress_x [MPa]": row["stress_x [mpa]"],
                        "Poisson": row["poisson"],
                        "R0": row["r0"],
                        "R": row["r"],
                    }

                    #Put "info" dictionary into self.materials dictionary
                    globals.materials[row["material"].get()] = info

                    layer -= 1
                
                #Sort the materials dictionary
                self.sort_dictionary()

                #Update widgets
                self.update_widgets("all")

            except Exception as error:
                messagebox.showerror("Error", "Could not load materials from Excel-file")
                traceback.print_exc()
                return
    

    def update_widgets(self, identifier:str, *args):
        """
        Updates widgets based on which identifier word is provided to the function\n

        PARAMETERS:
            identifier: name of updated variable or performed action
        """
        # print("UPDATE_WIDGETS()")

        match identifier:
            case "all":
                print("all widgets updated")
                if(globals.material_adjustment_panel != None):
                    globals.material_adjustment_panel.create_material_adjustment_panel()
                
                if(globals.parameters_panel != None):
                    globals.parameters_panel.create_parameters_panel()
                
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
                
            case "current_view_updated":
                print("current view_updated")
                self.set_layout()
            
            case "material_added":
                print("material_added")

                if(globals.material_adjustment_panel != None):
                    globals.material_adjustment_panel.create_material_adjustment_panel()

                if(globals.parameters_panel != None):
                    globals.parameters_panel.create_parameters_panel()
                
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
            
            case "material_deleted":
                # print("material_deleted")
                if(globals.material_adjustment_panel != None):
                    globals.material_adjustment_panel.create_material_adjustment_panel()

                if(globals.parameters_panel != None):
                    globals.parameters_panel.create_parameters_panel()
                
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
                
            case "material_modified":
                print("Material_modified")
                if(globals.material_adjustment_panel != None):
                    globals.material_adjustment_panel.create_material_adjustment_panel()

                if(globals.parameters_panel != None):
                    globals.parameters_panel.create_parameters_panel()

                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()

            case "material_moved":
                print("material_moved")
                if(globals.material_adjustment_panel != None):
                    globals.material_adjustment_panel.create_material_adjustment_panel()

                if(globals.parameters_panel != None):
                    globals.parameters_panel.create_parameters_panel()

                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()

            case "material_name_updated":
                print("name variable updated")
                if(globals.material_adjustment_panel != None):
                    globals.material_adjustment_panel.create_material_adjustment_panel()

                if(globals.parameters_panel != None):
                    globals.parameters_panel.create_parameters_panel()
                
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

            case "material_thickness_updated":
                print("Thickness value updated")

                if(globals.current_view.get() == "Stacked" or globals.current_view.get() == "Realistic"):
                    if(globals.layer_stack_canvas != None):
                        globals.layer_stack_canvas.draw_material_stack()
                else:
                    if(globals.layer_stack_canvas != None):
                        globals.layer_stack_canvas.draw_material_stack()

                    if(globals.parameters_panel != None):
                        globals.parameters_panel.create_parameters_panel()

                    if(globals.results_panel != None):
                        globals.results_panel.create_results_panel()

                    if(globals.graph_canvas != None):
                        globals.graph_canvas.draw_z_tip_is_graph()
                        globals.graph_canvas.draw_stoney_graph()

            case "material_layer_updated":
                print("Layer variable is updated")
                if(globals.parameters_panel != None):
                    globals.parameters_panel.create_parameters_panel()
                
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.material_adjustment_panel != None):
                    globals.material_adjustment_panel.create_material_adjustment_panel()
                
                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
            
            case "material_indent_updated":
                print("Indent variable is updated")
                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

            case "material_unit_updated":
                print("Unit variable is updated")
                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()
                
            case "material_color_updated":
                print("Color variable is updated")
                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()
                
            case "material_modulus_updated":
                print("Modulus variable is updated")
                
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
                
            case "material_cte_updated":
                print("CTE [ppm/deg] variable is updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
                
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
                
            case "material_density_updated":
                print("Density [kg/m3] variable is updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
                
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
                
            case "material_stress_x_updated":
                print("Stress_x_[MPa] variable is updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
                
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
                
            case "material_poisson_updated":
                print("Poisson variable is updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
                
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
            
            case "material_R0_updated":
                print("R0 variable is updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
                
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
            
            case "material_R_updated":
                print("R variable is updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
                
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
            
            case "piezo_material_updated":
                print("piezo_material variable is updated")

                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

                if(globals.layer_stack_canvas != None):
                    globals.layer_stack_canvas.draw_material_stack()

                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()

            case "L_value_updated":
                print("L_value variable is updated")
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()
                
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

            case "e_31_f_value_updated":
                print("e_31_f_value variable is updated")
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()

                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
            
            case "volt_value_updated":
                print("volt_value variable is updated")
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_z_tip_is_graph()

                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
                
            case "stress_neutral_SiO2_thickness_value_updated":
                print("stress_neutral_SiO2_thickness_value updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

            case "piezoelectric_bending_moment_value_updated":
                print("piezoelectric_bending_moment_value updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()

            case "blocking_force_cantilever_updated":
                print("blocking_force_cantilever_value variable is updated")
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
            
            case "stoney_filament_updated":
                print("stoney_filament updated")
                if(globals.graph_canvas != None):
                    globals.graph_canvas.draw_stoney_graph()

            case "neutralizing_material_updated":
                print("neutralizing_material_name updated")
                
                if(globals.results_panel != None):
                    globals.results_panel.create_results_panel()
            
            case "Zn":
                # print("Zn updated. nothing here is being updated")
                pass

            case "t_sol":
                # print("t_sol updated. nothing here is being updated")
                # if(globals.results_panel != None):
                #     globals.results_panel.create_results_panel()
                pass

            # case "M_p":
                # print("M_p updated")
                # if(globals.parameters_panel != None):
                #     globals.parameters_panel.create_parameters_panel()

            case "cumulative_Mp_cantilever":
                # print("cumulative_Mp_cantilever updated")
                pass
            
            case "M_is":
                # print("M_is updated")
                pass

            case "M_tot":
                # print("M_tot updated")
                pass
            
            case "EI":
                # print("EI updated")
                pass

            case "curv_is":
                # print("curv_is updated")
                pass
            
            case _:
                print("app.UPDATE_WIDGETS(): There is not a match-case for this variable:", identifier)


    def set_layout(self):
        """
        -Sets the correct column and row configuration for the main program window based on the "view"\n
        -Creates the widgets in the main program window for the specific "view"
        -Adjusts sliders, entries, labels etc... for the sepcific view
        """
        # print("SET_LAYOUT()")

        #Remove all widgets from main program window
        for widget in self.program_window.winfo_children():
            widget.grid_remove()


        #Reset the grid in main program window
        num_columns = self.program_window.grid_size()[0]
        num_rows = self.program_window.grid_size()[1]
        for i in range(num_columns):
            self.program_window.columnconfigure(i, weight=0, minsize=0, uniform="reset")
        for i in range(num_rows):
            self.program_window.rowconfigure(i, weight=0, minsize=0, uniform="reset")

        #Set different layouts based on the current_view
        match globals.current_view.get():
            case "Stacked" | "Realistic":
                self.program_window.update()
                #Change the layout of the program_window to only two columns
                self.program_window.columnconfigure(0, weight=10, minsize=500, uniform="group1")
                self.program_window.columnconfigure(1, weight=90, uniform="group1")


                self.program_window.rowconfigure(0, weight=90, uniform="group1")    
                self.program_window.rowconfigure(1, weight=10, minsize=100, uniform="group1")

                globals.canvas_control_panel.export_graphs()

                #MATERIAL_ADJUSTMENT_PANEL
                if(globals.material_adjustment_panel == None):
                    globals.material_adjustment_panel = Material_Adjustment_Panel(self.program_window, 0, 0)
                else:
                    globals.material_adjustment_panel.create_material_adjustment_panel()
                    globals.material_adjustment_panel.material_adjustment_panel_frame.grid(row=0, column=0, sticky="nsew")
                
                #Set all material entry and slider values to "Thickness [nm]" value
                for material in globals.materials:
                    globals.materials[material]["Slider_id"].configure(variable=globals.materials[material]["Thickness [nm]"])
                    globals.materials[material]["Entry_id"].configure(textvariable=globals.materials[material]["Thickness [nm]"])

                
                #MATERIAL_CONTROL_PANEL
                if(globals.material_control_panel == None):
                    globals.material_control_panel = Material_Control_Panel(self.program_window, 1, 0)
                else:
                    globals.material_control_panel.material_control_panel_frame.grid(row=1,column=0, sticky="nsew")


                #LAYER_STACK_CANVAS
                if(globals.layer_stack_canvas == None):
                    globals.layer_stack_canvas = Layer_Stack_Canvas(self.program_window, 0, 1)
                else:
                    globals.layer_stack_canvas.layer_stack_canvas.grid(row=0, column=1, rowspan=1, sticky="nsew")
                

                #CANVAS_CONTROL_PANEL
                if(globals.canvas_control_panel == None):
                    globals.canvas_control_panel = Canvas_Control_Panel(self.program_window, 1, 1)
                else:
                    globals.canvas_control_panel.canvas_control_panel_frame.grid(row=1, column=1, sticky="nsew")

            case "Stepped":
                #Change the layout of the program_window to only two columns
                self.program_window.columnconfigure(0, weight=10, minsize=500, uniform="group1")  #set this column to a specific size that won't change
                self.program_window.columnconfigure(1, weight=90, uniform="group1")  

                self.program_window.rowconfigure(0, weight=90, uniform="group1")    
                self.program_window.rowconfigure(1, weight=10, minsize=100, uniform="group1")

                
                #Material_adjustment_panel
                if(globals.material_adjustment_panel == None):
                    globals.material_adjustment_panel = Material_Adjustment_Panel(self.program_window, 0, 0)
                else:
                    globals.material_adjustment_panel.create_material_adjustment_panel()
                    globals.material_adjustment_panel.material_adjustment_panel_frame.grid(row=0, column=0)

                #Set all material entry and slider values to "indent" value
                for material in globals.materials:
                    globals.materials[material]["Slider_id"].configure(variable=globals.materials[material]["Indent [nm]"])
                    globals.materials[material]["Entry_id"].configure(textvariable=globals.materials[material]["Indent [nm]"])


                #MATERIAL_CONTROL_PANEL
                if(globals.material_control_panel == None):
                    globals.material_control_panel = Material_Control_Panel(self.program_window, 1, 0)
                else:
                    globals.material_control_panel.material_control_panel_frame.grid(row=1,column=0)


                #LAYER_STACK_CANVAS
                if(globals.layer_stack_canvas == None):
                    globals.layer_stack_canvas = Layer_Stack_Canvas(self.program_window, 0, 1)
                else:
                    globals.layer_stack_canvas.layer_stack_canvas.grid(row=0, column=1, rowspan=1)


                #CANVAS_CONTROL_PANEL
                if(globals.canvas_control_panel == None):
                    globals.canvas_control_panel = Canvas_Control_Panel(self.program_window, 1, 1)
                else:
                    globals.canvas_control_panel.canvas_control_panel_frame.grid(row=1, column=1)
   
            case "Multi":
                self.program_window.columnconfigure(0, weight=33, minsize=500, uniform="group1")
                self.program_window.columnconfigure(1, weight=34, uniform="group1")  
                self.program_window.columnconfigure(2, weight=33, uniform="group1")  

                self.program_window.rowconfigure(0, weight=30, uniform="group1")    
                self.program_window.rowconfigure(1, weight=28, uniform="group1")
                self.program_window.rowconfigure(2, weight=32, uniform="group1")
                self.program_window.rowconfigure(3, weight=10, minsize=100, uniform="group1")


                #MATERIAL_ADJUSTMENT_PANEL
                if(globals.material_adjustment_panel == None):
                    globals.material_adjustment_panel = Material_Adjustment_Panel(self.program_window, 0, 0)
                else:
                    globals.material_adjustment_panel.create_material_adjustment_panel()
                    globals.material_adjustment_panel.material_adjustment_panel_frame.grid(row=0, column=0)

                
                #Set all material entry and slider values to "Thickness [nm]" value
                for material in globals.materials:
                    globals.materials[material]["Slider_id"].configure(variable=globals.materials[material]["Thickness [nm]"])
                    globals.materials[material]["Entry_id"].configure(textvariable=globals.materials[material]["Thickness [nm]"])


                #PARAMETERS_PANEL
                if(globals.parameters_panel == None):
                    globals.parameters_panel = Parameters_Panel(self.program_window, 1, 0)
                else:
                    globals.parameters_panel.parameters_panel_frame.grid(row=1, column=0)


                #RESULTS_PANEL
                if(globals.results_panel == None):
                    globals.results_panel = Results_Panel(self.program_window, 2, 0)
                else:
                    globals.results_panel.results_panel_frame.grid(row=2, column=0)


                #MATERIAL_CONTROL_PANEL
                if(globals.material_control_panel == None):
                    globals.material_control_panel = Material_Control_Panel(self.program_window, 3, 0)
                else:
                    globals.material_control_panel.material_control_panel_frame.grid(row=3,column=0)


                #LAYER_STACK_CANVAS
                if(globals.layer_stack_canvas == None):
                    globals.layer_stack_canvas = Layer_Stack_Canvas(self.program_window, 0, 1)
                    globals.layer_stack_canvas.layer_stack_canvas.grid(rowspan=3)
                else:
                    globals.layer_stack_canvas.layer_stack_canvas.grid(row=0, column=1, rowspan=3)
                    globals.layer_stack_canvas.layer_stack_canvas.grid(rowspan=3)


                #CANVAS_CONTROL_PANEL
                if(globals.canvas_control_panel == None):
                    globals.canvas_control_panel = Canvas_Control_Panel(self.program_window, 3, 1)
                else:
                    globals.canvas_control_panel.canvas_control_panel_frame.grid(row=3, column=1)


                #GRAPH_CANVAS
                if(globals.graph_canvas == None):
                    globals.graph_canvas = Graph_Canvas(self.program_window, 0, 2)
                    globals.graph_canvas.graph_translator.get_tk_widget().grid(rowspan=3)
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()
                else:
                    globals.graph_canvas.graph_translator.get_tk_widget().grid(row=0, column=2, rowspan=3)
                    globals.graph_canvas.draw_z_tip_is_graph()
                    globals.graph_canvas.draw_stoney_graph()


                #GRAPH_CONTROL_PANEL
                if(globals.graph_control_panel == None):
                    globals.graph_control_panel = Graph_Control_Panel(self.program_window, 3, 2)
                else:
                    globals.graph_control_panel.graph_control_panel_frame.grid(row=3, column=2)


        #Update the sizes for layer_stack_canvas         
        self.program_window.update()
        globals.layer_stack_canvas.visible_canvas_bbox_x0 = 0
        globals.layer_stack_canvas.visible_canvas_bbox_y0 = globals.layer_stack_canvas.layer_stack_canvas.winfo_height() - 1
        globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_width() - 1
        globals.layer_stack_canvas.visible_canvas_bbox_y1 = 0
        globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y0 - globals.layer_stack_canvas.visible_canvas_bbox_y1
        globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0

        #Draw the material stack
        globals.layer_stack_canvas.draw_material_stack()
    
    
    def is_valid_color(self, color:str):
        """
        Returns True if given color string is a valid color\n
        Returns False otherwise
        """
        # print("IS_VALID_COLOR()")
        
        #Check if color is accepted by tkinter
        try:
            self.program_window.winfo_rgb(color)
            return True
        
        except:
            #Check if color is valid hexadecimal value
            if(type(color)==str and color.startswith('#') and len(color)==7):
                return True
            else:
                return False


    def sort_dictionary(self):
        """
        -Sorts the materials in the materials dictionary after their layer value\n
        -Assigns new layer values based on the order of the materials in the dictionary. (First material in the dictionary is assigned as layer 1)
        """
        # print("SORT_DICTIONARY()")

        #Sort the materials dictionary after the "layer" value
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["Layer"].get()))

        #create a layer counter variable starting at 1
        layer_counter = 1
        #Loop through the dictionary
        for material in globals.materials:
            #set material->layer value to be layer_counter
            globals.materials[material]["Layer"].set(layer_counter)
            #increment layer_counter
            layer_counter += 1


    def print_dictionary(self):
        """Prints the globals.materials dictionary in its original order"""
        #print("PRINT_DICTIONARY()")

        for material in globals.materials:
            print("Dictionary key:", material, "    |   ", type(material))
            print("Name:", globals.materials[material]["Name"].get(), "     |   ", type(globals.materials[material]["Name"]))
            print("Layer:", globals.materials[material]["Layer"].get(), "   |   ", type(globals.materials[material]["Layer"]))
            print("Thickness [nm]:", globals.materials[material]["Thickness [nm]"].get(), "  |  ", type(globals.materials[material]["Thickness [nm]"]))  
            print("Unit:", globals.materials[material]["Unit"].get(), "     |   ", type(globals.materials[material]["Unit"]))  
            print("Indent [nm]:", globals.materials[material]["Indent [nm]"].get(), "   |   ", type(globals.materials[material]["Indent [nm]"]))  
            print("Color:", globals.materials[material]["Color"].get(), "   |   ", type(globals.materials[material]["Color"]))  
            print("Modulus [GPa]:", globals.materials[material]["Modulus [GPa]"].get(), "   |   ", type(globals.materials[material]["Modulus [GPa]"]))  
            print("CTE [ppm/deg]:", globals.materials[material]["CTE [ppm/deg]"].get(), "   |   ", type(globals.materials[material]["CTE [ppm/deg]"]))  
            print("Density [kg/m3]:", globals.materials[material]["Density [kg/m3]"].get(), "   |   ", type(globals.materials[material]["Density [kg/m3]"]))  
            print("Stress_x [MPa]:", globals.materials[material]["Stress_x [MPa]"].get(), "     |   ", type(globals.materials[material]["Stress_x [MPa]"]))  
            print("Poisson:", globals.materials[material]["Poisson"].get(), "   |   ", type(globals.materials[material]["Poisson"]))  
            print("R0:", globals.materials[material]["R0"].get(), "     |   ", type(globals.materials[material]["R0"]))  
            print("R:", globals.materials[material]["R"].get(), "   |   ", type(globals.materials[material]["R"]))  
            
            print("\n")


    def program_window_resized(self, *event): 
        """Scales the layer_stack_canvas correctly based on the size of the program_window"""
        # print("PROGRAM_WINDOW_RESIZED()")
        
        #Check if the program window is actually resized
        if((self.program_window.winfo_width() != globals.current_program_window_width) or (self.program_window.winfo_height() != globals.current_program_window_height)):
            # print("PROGRAM_WINDOW_RESIZED()")
            self.program_window.update_idletasks()
            
            #Update the new sizes to globals
            globals.current_program_window_height = self.program_window.winfo_height()
            globals.current_program_window_width = self.program_window.winfo_width()

            #Update the boundaries of the layer_stack_canvas
            globals.layer_stack_canvas.visible_canvas_bbox_x0 = 0
            globals.layer_stack_canvas.visible_canvas_bbox_y0 = globals.layer_stack_canvas.layer_stack_canvas.winfo_height() - 1
            globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_width() - 1
            globals.layer_stack_canvas.visible_canvas_bbox_y1 = 0
            

            globals.layer_stack_canvas.layer_stack_canvas_width =  globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0
            globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y0 - globals.layer_stack_canvas.visible_canvas_bbox_y1

            #Redraw the layer_stack_canvas
            globals.layer_stack_canvas.draw_material_stack()


    def calculate_all_equations(self):
        """
        -Calculates all equations with the current values in the main material dictionary\n
        -Values are stored in globals and in dictionary for each material
        -Returns error-message if something went wrong

        UPDATED VALUES:\n     
            -Zn\n
            -Zp (for each piezo material)\n
            -Mp (for each piezo material)\n
            -Blocking_force (for each piezo material)\n
            -Cumulative_Mp_cantilever\n
            -M_is_cantilever\n
            -M_tot_cantilever\n
            -EI\n
            -curv_is\n

        """
        # print("CALCULATE_ALL_EQUATIONS()")

        try:
            #Check for errors
            if(len(globals.materials) == 0):
                raise ValueError("No materials")

            #Fetch necessary values
            E = []
            t = []
            nu = []
            sigma_i = []
            for material in globals.materials:
                E.append(globals.materials[material]["Modulus [GPa]"].get() * 1e9)
                t.append(float(globals.materials[material]["Thickness [nm]"].get()) / 1e9)
                nu.append(globals.materials[material]["Poisson"].get())
                sigma_i.append(float(globals.materials[material]["Stress_x [MPa]"].get()) * 1e6)

            L = globals.L_value.get()
            W = 160 / 1e6 #In micrometers
            V_p = globals.volt_value.get()
            e_31_f = globals.e_31_f_value.get()


            #CALCULATE ZN
            Zn = globals.equations.calculate_Zn(E, t, nu)
            if(isinstance(Zn, Exception)):
                globals.Zn = tkinter.DoubleVar(value=float('nan'))
                raise ValueError(f"Zn could not be calculated.\nerror:'{Zn}'")
            else:
                globals.Zn.set(Zn)


            #CALCULATE ZP, MP AND BLOCKING_FORCE FOR EACH PIEZO MATERIAL
            zp_list = []
            for material in dict(reversed(globals.materials.items())):
                if("Piezo_checkbox_id" in globals.materials[material]):    
                    if(globals.materials[material]["Piezo_checkbox_id"].get() == "on"):
                        piezo_material = material

                        #Populate a list with thickness values from layer1 up until "PZT" material
                        t_piezo_list = []
                        for material in globals.materials:
                            if(material == piezo_material):
                                break

                            #Convert thickness to meters and append it to list
                            t_piezo_list.append(globals.materials[material]["Thickness [nm]"].get() / 1e9)
                            
                        #Fetch thickness value for Piezo material and convert it to "meters"
                        piezo_thickness = globals.materials[piezo_material]["Thickness [nm]"].get() / 1e9

                        Zp = globals.equations.calculate_mid_piezo(t_piezo_list, Zn, piezo_thickness)
                        if(isinstance(Zp, Exception)):
                            globals.materials[material]["Zp_value"] = tkinter.DoubleVar(value=float('nan'))
                            raise ValueError(f"Zp for {material} could not be calculated.\nerror:'{Zp}'")
                        else:
                            globals.materials[material]["Zp_value"] = tkinter.DoubleVar(value=Zp)                       
                            zp_list.append(Zp)
                        

                        #CALCULATE M_p
                        Mp = globals.equations.calculate_Mp_cantilever(Zp, W, V_p, e_31_f)
                        if(isinstance(Mp, Exception)):
                            globals.materials[material]["Mp_value"] = tkinter.DoubleVar(value=float('nan'))
                            raise ValueError(f"Mp for {material} could not be calculated.\nerror:'{Mp}'")
                        else:
                            globals.materials[material]["Mp_value"] = tkinter.DoubleVar(value=Mp)

                        #CALCULATE BLOCKING FORCE
                        #Total thickness of materials from substrate up to (but not including) chosen piezo material
                        h_Si = 0 
                        for material2 in globals.materials:
                            if(material2 == material):
                                break
                            h_Si += globals.materials[material2]["Thickness [nm]"].get() / 1e9
                        
                        blocking_force = globals.equations.calculate_blocking_force(E, t, V_p, e_31_f, piezo_thickness, h_Si, W, L)
                        if(isinstance(blocking_force, Exception)):
                            globals.materials[material]["Blocking_force_value"] = tkinter.DoubleVar(value=float('nan'))
                            raise ValueError(f"blocking_force could not be calculated.\nerror:'{blocking_force}'")
                        else:
                            globals.materials[material]["Blocking_force_value"] = tkinter.DoubleVar(value=blocking_force)

            
            #CALCULATE CUMULATIVE_MP_CANTILEVER
            cumulative_Mp = globals.equations.calculate_cumulative_Mp_cantilever(zp_list, W, V_p, e_31_f)
            if(isinstance(cumulative_Mp, Exception)):
                globals.cumulative_Mp_cantilever = tkinter.DoubleVar(value=float('nan'))
                raise ValueError(f"Cumulative_Mp could not be calculated.\nerror:'{cumulative_Mp}'")
            else:
                globals.cumulative_Mp_cantilever.set(cumulative_Mp)
        
        
            #CALCULATE M_IS_CANTILEVER
            M_is = globals.equations.calculate_M_is_cantilever(Zn, sigma_i, t, W)
            if(isinstance(M_is, Exception)):
                globals.M_is = tkinter.DoubleVar(value=float('nan'))
                raise ValueError(f"M_is could not be calculated.\nerror:'{M_is}'")
            else:
                globals.M_is.set(M_is)


            #CALCULATE M_TOT_CANTILEVER
            M_tot = globals.equations.calculate_M_tot_cantilever(M_is, cumulative_Mp)
            if(isinstance(M_tot, Exception)):
                globals.M_tot = tkinter.DoubleVar(value=float('nan'))
                raise ValueError(f"M_tot could not be calculated.\nerror:'{M_tot}'")
            else:
                globals.M_tot.set(M_tot)


            #CALCULATE EI
            EI = globals.equations.calculate_EI(E, t, nu, W, Zn)
            if(isinstance(EI, Exception)):
                globals.EI = tkinter.DoubleVar(value=float('nan'))
                raise ValueError(f"EI could not be calculated.\nerror:'{EI}'")
            else:
                globals.EI.set(EI)


            #CALCULATE CURV_IS
            curv_is = globals.equations.calculate_curvature(M_tot, EI)
            if(isinstance(curv_is, Exception)):
                globals.curv_is = tkinter.DoubleVar(value=float('nan'))
                raise ValueError(f"curv_is could not be calculated.\nerror:'{curv_is}'")
            else:
                globals.curv_is.set(curv_is)

        
        # calculate_tip_placement???
        # neutralize_global_stress???
        # find_t_solution???

        except Exception as error:
            print(f"There was an error in 'app.calculate_all_equations()'.\nERROR:\n{error}")
            return error
        


if __name__ == "__main__":
    #Create the main program window
    program_window = tkinter.Tk()
    
    #Set the dimensions of the program window
    program_window.state("zoomed")
    # program_window.geometry(f"{settings.program_window_width}x{settings.program_window_height}")
    
    #Set the program window title
    program_window.title(settings.program_window_title)

    #Set the main window background color
    program_window.configure(bg=settings.program_window_background_color)
        
    #Create keyboard shortcuts for the main window
    program_window.bind("<Escape>", lambda event: program_window.destroy())
    
    #Create an instance of App and run it
    globals.app = App(program_window)

    #Checks if the program window is being resized
    globals.current_program_window_height = program_window.winfo_height()
    globals.current_program_window_width = program_window.winfo_width()
    program_window.bind("<Configure>", lambda event: globals.app.program_window_resized(event))

    #Start the main loop of the program
    program_window.mainloop()




    #CODE TO CHANGE TITLE BAR COLOR
    # import ctypes
    # # Convert hex color to BGR format
    # color_hex = "#ffffff"
    # color_bgr = int(color_hex[1:], 16)  # Convert "#RRGGBB" to integer 0xBBGGRR
    # # Set title bar color
    # ctypes.windll.dwmapi.DwmSetWindowAttribute(
    #     ctypes.windll.user32.GetForegroundWindow(), 35, 
    #     ctypes.byref(ctypes.c_int(color_bgr)), 4
    # )
    #END TITLE BAR CODE#
