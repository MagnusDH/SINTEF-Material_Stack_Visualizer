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

                    #STATUS
                    row["status"] = tkinter.StringVar(value="active")


                    
                    #ADD TRACES TO ALL VARIABLES
                    # Trace changes to trigger canvas redraw
                    row["material"].trace_add("write", lambda *args, identifier="Name": self.update_widgets(identifier))
                    row["layer"].trace_add("write", lambda *args, identifier="Layer": self.update_widgets(identifier))
                    row["thickness [nm]"].trace_add("write", lambda *args, identifier="Thickness [nm]": self.update_widgets(identifier))
                    row["unit"].trace_add("write", lambda *args, identifier="Unit": self.update_widgets(identifier))
                    row["indent [nm]"].trace_add("write", lambda *args, identifier="Indent [nm]": self.update_widgets(identifier))
                    row["color"].trace_add("write", lambda *args, identifier="Color": self.update_widgets(identifier))
                    row["status"].trace_add("write", lambda *args, identifier="Status": self.update_widgets(identifier))
                    row["modulus [gpa]"].trace_add("write", lambda *args, identifier="Modulus [GPa]": self.update_widgets(identifier))
                    row["cte [ppm/deg]"].trace_add("write", lambda *args, identifier="CTE [ppm/deg]": self.update_widgets(identifier))
                    row["density [kg/m3]"].trace_add("write", lambda *args, identifier="Density [kg/m3]": self.update_widgets(identifier))
                    row["stress_x [mpa]"].trace_add("write", lambda *args, identifier="Stress_x [MPa]": self.update_widgets(identifier))
                    row["poisson"].trace_add("write", lambda *args, identifier="Poisson": self.update_widgets(identifier))
                    row["r0"].trace_add("write", lambda *args, identifier="R0": self.update_widgets(identifier))
                    row["r"].trace_add("write", lambda *args, identifier="R": self.update_widgets(identifier))

                    
                    #Create an "info" dictionary to contain all info from excel-file
                    info = {
                        "Name": row["material"],
                        "Layer": row["layer"],
                        "Thickness [nm]": row["thickness [nm]"],
                        "Unit": row["unit"],
                        "Indent [nm]": row["indent [nm]"],
                        "Color": row["color"],
                        "Status": row["status"],
                        "Modulus [GPa]": row["modulus [gpa]"],
                        "CTE [ppm/deg]": row["cte [ppm/deg]"],
                        "Density [kg/m3]": row["density [kg/m3]"],
                        "Stress_x [MPa]": row["stress_x [mpa]"],
                        "Poisson": row["poisson"],
                        "R0": row["r0"],
                        "R": row["r"],
                        "Label_name_id": None,
                        "Delete_material_button_id": None,
                        "Move_down_button_id": None,
                        "Move_up_button_id": None,
                        "Entry_id": None,
                        "Slider_id": None,
                        "Checkbox_id": None,
                        "Rectangle_id": None,
                        "Text_id": None,
                        "Text_bbox_id" : None,
                        "Line_id": None,
                        "Indent_text_id": None,
                        "Indent_text_bbox_id": None,
                        "Indent_line_id": None,
                        "Indent_arrow_pointer_id": None
                    }

                    #Put "info" dictionary into self.materials dictionary
                    globals.materials[row["material"].get()] = info

                    layer -= 1
                
                #Sort the materials dictionary
                self.sort_dictionary()

            except Exception as error:
                messagebox.showerror("Error", "Could not load materials from Excel-file")
                traceback.print_exc()
                return
    

    def update_widgets(self, identifier:str, *args):
        """
        Updates widgets based on which tkinter.variable name is provided to the function\n

        PARAMETERS:
            identifier: name of updated variable
        """
        # print("UPDATE_WIDGETS()")

        match identifier:
            case "Name":
                print("name variable updated")

            case "Thickness [nm]":
                print("Thickness value updated")
                globals.layer_stack_canvas.draw_material_stack()
                globals.graph_canvas.draw_graphs()

                #Update equation labels in parameters panel
                #update "Blocking force"

            case "Layer":
                print("Layer variable is updated")
                #Redraw stack
                #Redraw graph
                #Update equation labels
            
            case "Indent [nm]":
                print("Indent variable is updated")

            case "Unit":
                print("Unit variable is updated")
                
            case "Color":
                print("Color variable is updated")
                
            case "Status":                             
                print("Status variable is updated")
            
            case "Modulus [GPa]":
                print("Modulus variable is updated")
                
            case "CTE [ppm/deg]":
                print("CTE variable is updated")
                
            case "Density [kg/m3]":
                print("Density variable is updated")
                
            case "Stress_x [MPa]":
                print("Stress_x variable is updated")
                
            case "Poisson":
                print("Poisson variable is updated")
            
            case "R0":
                print("R0 variable is updated")
            
            case "R":
                print("R variable is updated")
            
            case "piezo_material_name":
                print("piezo_material_name variable is updated")
                globals.layer_stack_canvas.draw_material_stack()
                globals.graph_canvas.draw_graphs()
                
                #update "Blocking force"

            case "L_value":
                print("L_value variable is updated")
                globals.graph_canvas.draw_graphs()
                #update "Blocking force"

            case "e_31_f_value":
                print("e_31_f_value variable is updated")
                globals.graph_canvas.draw_graphs()

                #Update graphs
                #update "Blocking force"
            
            case "volt_value":
                print("volt_value variable is updated")
                globals.graph_canvas.draw_graphs()

                #update "Blocking force"

            case "stress_neutral_SiO2_thickness_value":
                print("stress_neutral_SiO2_thickness_value updated")

            case "piezoelectric_bending_moment_value":
                print("piezoelectric_bending_moment_value updated")

            case "blocking_force_cantilever":
                print("blocking_force_cantilever_value variable is updated")
            
            case "initial_curvature_value":
                print("initial_curvature_value updated")

            case "final_curvature_value":
                print("final_curvature_value updated")

            case _:
                print("There is not a match-case for this variable:", identifier)



        #When a material is deleted:
            #Redraw stack
            #Redraw graph
            #Update equation labels

        #When a material is modified:
            #Redraw stack
            #Redraw graph
            #Update equation labels


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
        match globals.current_view:
            case "Stacked" | "Realistic":
                self.program_window.update()
                #Change the layout of the program_window to only two columns
                self.program_window.columnconfigure(0, weight=10, minsize=500, uniform="group1")
                self.program_window.columnconfigure(1, weight=90, uniform="group1")


                self.program_window.rowconfigure(0, weight=90, uniform="group1")    
                self.program_window.rowconfigure(1, weight=10, minsize=100, uniform="group1")

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
                self.program_window.columnconfigure(0, weight=10, minsize=500, uniform="group1")
                self.program_window.columnconfigure(1, weight=45, uniform="group1")  
                self.program_window.columnconfigure(2, weight=45, uniform="group1")  

                self.program_window.rowconfigure(0, weight=45, uniform="group1")    
                self.program_window.rowconfigure(1, weight=45, uniform="group1")
                self.program_window.rowconfigure(2, weight=10, minsize=100, uniform="group1")


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


                #MATERIAL_CONTROL_PANEL
                if(globals.material_control_panel == None):
                    globals.material_control_panel = Material_Control_Panel(self.program_window, 2, 0)
                else:
                    globals.material_control_panel.material_control_panel_frame.grid(row=2,column=0)


                #LAYER_STACK_CANVAS
                if(globals.layer_stack_canvas == None):
                    globals.layer_stack_canvas = Layer_Stack_Canvas(self.program_window, 0, 1)
                    globals.layer_stack_canvas.layer_stack_canvas.grid(rowspan=2)
                else:
                    globals.layer_stack_canvas.layer_stack_canvas.grid(row=0, column=1, rowspan = 2)
                    globals.layer_stack_canvas.layer_stack_canvas.grid(rowspan=2)


                #CANVAS_CONTROL_PANEL
                if(globals.canvas_control_panel == None):
                    globals.canvas_control_panel = Canvas_Control_Panel(self.program_window, 2, 1)
                else:
                    globals.canvas_control_panel.canvas_control_panel_frame.grid(row=2, column=1)


                #GRAPH_CANVAS
                if(globals.graph_canvas == None):
                    globals.graph_canvas = Graph_Canvas(self.program_window, 0, 2)
                    globals.graph_canvas.graph_translator.get_tk_widget().grid(rowspan=2)
                    globals.graph_canvas.draw_graphs()
                else:
                    globals.graph_canvas.graph_translator.get_tk_widget().grid(row=0, column=2, rowspan=2)
                    globals.graph_canvas.draw_graphs()


                #GRAPH_CONTROL_PANEL
                if(globals.graph_control_panel == None):
                    globals.graph_control_panel = Graph_Control_Panel(self.program_window, 2, 2)
                else:
                    globals.graph_control_panel.graph_control_panel_frame.grid(row=2, column=2)


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
        """Returns True if given color string is a valid color. Return False if invalid"""
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
            globals.materials[material]["Layer"] = tkinter.IntVar(value=layer_counter)
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
            print("Status:", globals.materials[material]["Status"].get(), "     |   ", type(globals.materials[material]["Status"]))  
            print("Modulus [GPa]:", globals.materials[material]["Modulus [GPa]"].get(), "   |   ", type(globals.materials[material]["Modulus [GPa]"]))  
            print("CTE [ppm/deg]:", globals.materials[material]["CTE [ppm/deg]"].get(), "   |   ", type(globals.materials[material]["CTE [ppm/deg]"]))  
            print("Density [kg/m3]:", globals.materials[material]["Density [kg/m3]"].get(), "   |   ", type(globals.materials[material]["Density [kg/m3]"]))  
            print("Stress_x [MPa]:", globals.materials[material]["Stress_x [MPa]"].get(), "     |   ", type(globals.materials[material]["Stress_x [MPa]"]))  
            print("Poisson:", globals.materials[material]["Poisson"].get(), "   |   ", type(globals.materials[material]["Poisson"]))  
            print("R0:", globals.materials[material]["R0"].get(), "     |   ", type(globals.materials[material]["R0"]))  
            print("R:", globals.materials[material]["R"].get(), "   |   ", type(globals.materials[material]["R"]))  
            
            print("\n")


    def program_window_resized(self, event): 
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



if __name__ == "__main__":
    #Create the main program window
    program_window = tkinter.Tk()
    
    #Set the dimensions of the program window
    # program_window.state("zoomed")
    program_window.geometry(f"{settings.program_window_width}x{settings.program_window_height}")
    
    #Set the program window title
    program_window.title(settings.program_window_title)

    #Set the main window background color
    program_window.configure(bg=settings.program_window_background_color)
        
    #Create keyboard shortcuts for the main window
    program_window.bind("<Escape>", lambda event: program_window.destroy())
    
    #Initialize global variables
    globals.initialize_globals(program_window)

    #Create an instance of App and run it
    globals.app = App(program_window)

    #Checks if the program window is being resized
    globals.current_program_window_height = program_window.winfo_height()
    globals.current_program_window_width = program_window.winfo_width()
    program_window.bind("<Configure>", lambda event: globals.app.program_window_resized(event))

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


    #Start the main loop of the program
    program_window.mainloop()






###################COMMENTED CODE FOR CREATING A SCROLLABLE MAIN_FRAME#####################

#Create background_canvas and main_frame where every widgets is placed
# self.main_frame, self.background_canvas = self.create_scrollable_frame(self.program_window)

# """
# -Creates a scrollable frame on the window given in the class
# -(To be able to do this a "canvas" is made and a "frame" is placed on top of the canvas. 
# -(Then scrollbars are placed in the main window which controls scrolling on the canvas)
# """
# def create_scrollable_frame(self, window):
    #     #print("CREATE_SCROLLABLE_FRAME()")
    #     #Create a background canvas (Scrollbars can only be used with a canvas)
    #     background_canvas = customtkinter.CTkCanvas(
    #         master=window,
    #         height=window.winfo_height()-settings.scrollbar_width-5,
    #         width=window.winfo_width()-settings.scrollbar_width-5,
    #         bg=settings.background_canvas_background_color,
    #         highlightthickness=0
    #     )
    #     background_canvas.grid(
    #         row=0, 
    #         column=0, 
    #         sticky="nsew",
    #     )

    #     #Prevent the background_canvas to automaticly resize itself to the size of the children widgets inside it
    #     background_canvas.grid_propagate(False)

    #     #Create a frame inside the canvas to hold all the widgets
    #     main_frame = customtkinter.CTkFrame(
    #         master=background_canvas, 
    #         width=max(settings.main_frame_minimum_width*0.8, window.winfo_width()*0.8 - settings.scrollbar_width),     #Has to be 80% to get correct size for some reason
    #         height=max(settings.main_frame_minimum_height*0.8, window.winfo_height()*0.8 - settings.scrollbar_width),   #Has to be 80% to get correct size for some reason
    #         fg_color=settings.main_frame_background_color,
    #     )
    #     main_frame.grid(
    #         row=0,
    #         column=0
    #     )

    #     #Prevent the main_frame window to downsize itself to fit widgets placed inside
    #     main_frame.grid_propagate(False)

    #     #Add main_frame to a window in the background_canvas to enable scrolling
    #     background_canvas.create_window(
    #         (0, 0), 
    #         window=main_frame, 
    #         anchor="nw"
    #     )

    #     ####### UNNECESSARY STUFF? ##########

    #     #Configure the main_frame to expand with the background_canvas
    #     # main_frame.bind("<Configure>", self.on_frame_configure(background_canvas))

    #     # background_canvas.configure(scrollregion=background_canvas.bbox("all"))

    #     # background_canvas.configure(
    #     #     scrollregion=(0, 0, max(500, background_canvas.winfo_width()), max(500, background_canvas.winfo_height()))
    #     # )
    #     ####################################

        

    #     #Add scrollbars to the background_canvas
    #     canvas_vertical_scrollbar = customtkinter.CTkScrollbar(
    #         master=window,
    #         orientation="vertical",
    #         width=settings.scrollbar_width,
    #         border_spacing=settings.scrollbar_border_spacing,
    #         fg_color=settings.scrollbar_background_color,
    #         command=background_canvas.yview
    #     )
    #     canvas_vertical_scrollbar.grid(
    #         row=0, 
    #         column=1,
    #         sticky="ns",
    #     )

    #     canvas_horizontal_scrollbar = customtkinter.CTkScrollbar(
    #         master=window,
    #         orientation="horizontal", 
    #         width=settings.scrollbar_width,
    #         border_spacing=settings.scrollbar_border_spacing,
    #         fg_color=settings.scrollbar_background_color,
    #         command=background_canvas.xview
    #     )
    #     canvas_horizontal_scrollbar.grid(
    #         row=1, 
    #         column=0, 
    #         sticky="ew"
    #     )

    #     #Set the scrollregion for the scrollbars (x0,y0 to x1,y1) and activate the scrollbars
    #     background_canvas.configure(
    #         scrollregion=(0, 0, settings.main_frame_minimum_width, settings.main_frame_minimum_height),
    #         yscrollcommand=canvas_vertical_scrollbar.set, 
    #         xscrollcommand=canvas_horizontal_scrollbar.set
    #     )

    #     return main_frame, background_canvas



#
# """Dynamically adjusts the scrollable area of the background_canvas
# Ensures that the scrollbars correctly reflect the size of the content inside the canvas
# """
# def on_frame_configure(self, canvas, event=None):
    #     #Update the scroll region of the canvas to encompass the entire frame
    #     canvas.configure(scrollregion=canvas.bbox("all"))

###################END COMMENTED CODE FOR CREATING A SCROLLABLE MAIN_FRAME#####################
