import tkinter
from tkinter import messagebox
import customtkinter
import pyautogui  # For better user interface visual effects
import os
import pandas   #Excel-file reading
import openpyxl #Excel-file reading
import settings
import globals
from Material_Adjustment_Panel import Material_Adjustment_Panel
from Layer_Stack_Canvas import Layer_Stack_Canvas
from Material_Control_Panel import Material_Control_Panel
from Canvas_Control_Panel import Canvas_Control_Panel
from Equations import Equations


import traceback

#Main application class
class App:
    def __init__(self, program_window):
        # print("CLASS APP INIT()")

        #Program window
        self.program_window = program_window

        #If excel file exists, load it into globals.materials
        if(os.path.isfile("Materials.xlsx")):
            self.load_materials_from_excel()

        #??????????????????????????????????????????????????????????????
        globals.equations = Equations()

        #Create a panel that controls the properties of each material
        globals.material_adjustment_panel = Material_Adjustment_Panel(self.program_window)

        #Create canvas to draw materials on. This class also creates a control panel to control the layer_stack_canvas
        globals.layer_stack_canvas = Layer_Stack_Canvas(self.program_window)

        #Create a panel that controls the properties of each material
        globals.material_control_panel = Material_Control_Panel(self.program_window)

        #Create a panel that controls the actions of the layer_stack_canvas
        globals.canvas_control_panel = Canvas_Control_Panel(self.program_window)

    
    """Reads the given excel-file and populates the self.materials dictionary with info about each material"""
    def load_materials_from_excel(self):
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

                    #If some cells are left empty, has an invalid value or headline does not exist -> apply default value
                    #MATERIAL NAME CHECK
                    if("material" in row.index):
                        if((pandas.isna(row["material"])) or str(row["material"]).isspace()):
                            row["material"] = "No name"
                    else:
                        row["material"] = "No name"


                    #THICKNESS CHECK
                    if("thickness" in row.index):
                        if(pandas.isna(row["thickness"])):
                            row["thickness"] = 0
                        thickness_conversion = self.convert_decimal_string_to_float(row["thickness"]) 
                        if((thickness_conversion != False) and (thickness_conversion >= 0)):
                            row["thickness"] = thickness_conversion
                        else:
                            row["thickness"] = 0
                    else:
                        row["thickness"] = 0


                    #UNIT CHECK
                    if("unit" in row.index):
                        if((pandas.isna(row["unit"])) or (row["unit"].isspace())):
                            row["unit"] = "No value"
                    else:
                        row["unit"] = "No value"


                    #INDENT CHECK
                    if("indent [nm]" in row.index):
                        if(pandas.isna(row["indent [nm]"])):
                            row["indent [nm]"] = 0
                        indent_conversion = self.convert_decimal_string_to_float(row["indent [nm]"]) 
                        if((indent_conversion != False) and (indent_conversion >= 0)):
                            row["indent [nm]"] = indent_conversion
                        else:
                            row["indent [nm]"] = 0
                    else:
                        row["indent [nm]"] = 0
                    


                    #COLOR CHECK
                    if("color" in row.index):
                        if((pandas.isna(row["color"])) or (self.is_valid_color(row["color"]) == False)):
                            row["color"] = "white"
                    else:
                        row["color"] = "white"


                    #MODULUS CHECK
                    if("modulus [gpa]" in row.index):
                        if(pandas.isna(row["modulus [gpa]"])):
                            row["modulus [gpa]"] = 0
                        modulus_conversion = self.convert_decimal_string_to_float(row["modulus [gpa]"]) 
                        if(modulus_conversion != False):
                            row["modulus [gpa]"] = abs(modulus_conversion)
                        else:
                            row["modulus [gpa]"] = 0  
                    else:
                        row["modulus [gpa]"] = 0    



                    #CTE CHECK
                    if("cte [ppm/deg]" in row.index):
                        if(pandas.isna(row["cte [ppm/deg]"])):
                            row["cte [ppm/deg]"] = 0
                        cte_conversion = self.convert_decimal_string_to_float(row["cte [ppm/deg]"]) 
                        if(cte_conversion != False):
                            row["cte [ppm/deg]"] = abs(cte_conversion)
                        else:
                            row["cte [ppm/deg]"] = 0 
                    else:
                        row["cte [ppm/deg]"] = 0 



                    #DENSITY CHECK
                    if("density [kg/m3]" in row.index):
                        if(pandas.isna(row["density [kg/m3]"])):
                            row["density [kg/m3]"] = 0
                        density_conversion = self.convert_decimal_string_to_float(row["density [kg/m3]"]) 
                        if(density_conversion != False):
                            row["density [kg/m3]"] = abs(density_conversion)
                        else:
                            row["density [kg/m3]"] = 0 
                    else:
                        row["density [kg/m3]"] = 0 



                    #STRESS CHECK
                    if("stress_x [mpa]" in row.index):
                        if(pandas.isna(row["stress_x [mpa]"])):
                            row["stress_x [mpa]"] = 0
                        stress_conversion = self.convert_decimal_string_to_float(row["stress_x [mpa]"]) 
                        if(stress_conversion != False):
                            row["stress_x [mpa]"] = stress_conversion
                        else:
                            row["stress_x [mpa]"] = 0 
                    else:
                        row["stress_x [mpa]"] = 0 


                    #POISSON CHECK
                    if("poisson" in row.index):
                        if(pandas.isna(row["poisson"])):
                            row["poisson"] = 0
                        poisson_conversion = self.convert_decimal_string_to_float(row["poisson"]) 
                        if(poisson_conversion != False):
                            row["poisson"] = abs(poisson_conversion)
                        else:
                            row["poisson"] = 0
                    else:
                        row["poisson"] = 0


                    #R0 CHECK
                    if("r0" in row.index):
                        if(pandas.isna(row["r0"])):
                            row["r0"] = 0
                        R0_conversion = self.convert_decimal_string_to_float(row["r0"]) 
                        if(R0_conversion != False):
                            row["r0"] = R0_conversion
                        else:
                            row["r0"] = 0
                    else:
                        row["r0"] = 0


                    #R CHECK
                    if("r" in row.index):
                        if(pandas.isna(row["r"])):
                            row["r"] = 0
                        R_conversion = self.convert_decimal_string_to_float(row["r"]) 
                        if(R_conversion != False):
                            row["r"] = R_conversion
                        else:
                            row["r"] = 0 
                    else:
                        row["r"] = 0 

                    
                    #Create an "info" dictionary to contain all info from excel-file
                    info = {
                        "Name": str(row["material"]),
                        "Layer": int(layer),
                        "Thickness": float(row["thickness"]),
                        "Unit": row["unit"],
                        "Indent [nm]": float(row["indent [nm]"]),
                        "Color": row["color"],
                        "Status": "active",
                        "Modulus [GPa]": float(row["modulus [gpa]"]),
                        "CTE [ppm/deg]": float(row["cte [ppm/deg]"]),
                        "Density [kg/m3]": float(row["density [kg/m3]"]),
                        "Stress_x [MPa]": float(row["stress_x [mpa]"]),
                        "Poisson": float(row["poisson"]),
                        "R0": float(row["r0"]),
                        "R": float(row["r"]),
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
                    globals.materials[str(row["material"])] = info

                    layer -= 1
                
                #Sort the materials dictionary
                self.sort_dictionary()
                
            except Exception as error:
                messagebox.showerror("Error", "Could not load materials from Excel-file")
                traceback.print_exc()
                return

    
    """
    -Converts a string to float no matter if it is written with "," or "." 
    -Returns the float is sucessfull, returns False if not sucessfull
    """
    def convert_decimal_string_to_float(self, string_number):
        # print("CINVERT_DECIMAL_STRING_TO_FLOAT()")
        try:
            new_float = float(string_number)
            return new_float
        
        except:
            if((isinstance(string_number, str)) and ("," in string_number)):
                try:
                    new_float = string_number.replace(",", ".")
                    new_float = float(new_float)
                    return new_float

                except:
                    return False
            else:
                return False


    """Returns True if given color string is a valid color. Return False if invalid"""
    def is_valid_color(self, color):
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


    """
    -Gives each material a layer value based on the order they are in globals.materials{}. (The top layer is assigned as "layer 1")
    -Places 'substrate' as the lowest layer
    """
    def sort_dictionary(self):
        # print("SORT_DICTIONARY()")

        #create a layer counter variable starting at 1
        layer_counter = len(globals.materials)
        #Loop through the dictionary
        for material in globals.materials:
            #If the material is "substrate"
            if(material.lower() == "substrate"):
                #set its layer value to be the length of materials{}
                globals.materials[material]["Layer"] = 1

            else:
                #set material->layer value to be layer_counter
                globals.materials[material]["Layer"] = layer_counter
                #increment layer_counter
                layer_counter -= 1

        #Sort the materials dictionary after the "layer" value
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["Layer"]))


    """Prints the globals.materials dictionary specifily"""
    def print_dictionary(self):
        for material in globals.materials:
            print("Dictionary key:", material, "    |", type(material))
            print("Name:", globals.materials[material]["Name"], "   |", type(globals.materials[material]["Name"]))
            print("Layer:", globals.materials[material]["Layer"], "     |", type(globals.materials[material]["Layer"]))
            print("Thickness:", globals.materials[material]["Thickness"], "     |", type(globals.materials[material]["Thickness"]))  
            print("Unit:", globals.materials[material]["Unit"], "   |", type(globals.materials[material]["Unit"]))  
            print("Indent [nm]:", globals.materials[material]["Indent [nm]"], "     |", type(globals.materials[material]["Indent [nm]"]))  
            print("Color:", globals.materials[material]["Color"], "     |", type(globals.materials[material]["Color"]))  
            print("Status:", globals.materials[material]["Status"], "   |", type(globals.materials[material]["Status"]))  
            print("Modulus [GPa]:", globals.materials[material]["Modulus [GPa]"], "     |", type(globals.materials[material]["Modulus [GPa]"]))  
            print("CTE [ppm/deg]:", globals.materials[material]["CTE [ppm/deg]"], "     |", type(globals.materials[material]["CTE [ppm/deg]"]))  
            print("Density [kg/m3]:", globals.materials[material]["Density [kg/m3]"], "     |", type(globals.materials[material]["Density [kg/m3]"]))  
            print("Stress_x [MPa]:", globals.materials[material]["Stress_x [MPa]"], "   |", type(globals.materials[material]["Stress_x [MPa]"]))  
            print("Poisson:", globals.materials[material]["Poisson"], "     |", type(globals.materials[material]["Poisson"]))  
            print("R0:", globals.materials[material]["R0"], "   |", type(globals.materials[material]["R0"]))  
            print("R:", globals.materials[material]["R"], "     |", type(globals.materials[material]["R"]))  
            
            print("\n")


    """Scales the layer_stack_canvas correctly based on the size of the program_window"""
    def program_window_resized(self, event): 

        #Check if the program window is actually resized
        if((self.program_window.winfo_width() != globals.current_program_window_width) or (self.program_window.winfo_height() != globals.current_program_window_height)):
            # print("PROGRAM_WINDOW_RESIZED()")
            self.program_window.update_idletasks()
            
            #Update the new sizes to globals
            globals.current_program_window_height = self.program_window.winfo_height()
            globals.current_program_window_width = self.program_window.winfo_width()

            #Update the boundaries of the layer_stack_canvas
            globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_width() - 1
            globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_height() - 1

            globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0
            globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0

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

    #Define the row&column layout of the program window
    program_window.columnconfigure(0, weight=1, minsize=500, uniform="group1")  #set this column to a specific size that won't change
    program_window.columnconfigure(1, weight=9, uniform="group1")  

    program_window.rowconfigure(0, weight=9, uniform="group1")    
    program_window.rowconfigure(1, weight=1, minsize=100, uniform="group1")   #set this row to a specific size that won't change
    

    #Set the main window background color
    program_window.configure(bg=settings.program_window_background_color)
        
    #Create keyboard shortcuts for the main window
    program_window.bind("<Escape>", lambda event: program_window.destroy())

    #Create an instance of App and run it
    globals.app = App(program_window)
    
    # #Checks if the program window is being resized
    globals.current_program_window_height = program_window.winfo_height()
    globals.current_program_window_width = program_window.winfo_width()
    program_window.bind("<Configure>", lambda event: globals.app.program_window_resized(event))


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

















#LOAD MATERIAL FROM EXCEL ORIGINAL#
# """Reads the given excel-file and populates the self.materials dictionary with info about each material"""
#     def load_materials_from_excel(self):
#         #print("LOAD_MATERIALS_FROM_EXCEL()")

#         excel_file = "Materials.xlsx"

#         #If there is a "materials" file in the folder, read it and populate the self.materials dictionary 
#         if(os.path.isfile(excel_file)):
#             try:
#                 #Read given excel file into Pandas dataframe
#                 excel_data = pandas.read_excel(excel_file)

#                 # Convert column names to lowercase
#                 # excel_data.columns = excel_data.columns.str.lower()

#                 #Open excel-file to read background colors of each cell
#                 work_book = openpyxl.load_workbook(excel_file, data_only=True)
#                 fs = work_book.active

#                 #Loop through the rows in excel_file
#                 i = 2
#                 layer = 1
#                 for column, row in excel_data.iterrows():
#                     #Increment "i" to go to the next row
#                     i+=1

#                     #If some cells are left empty, has an invalid value or headline does not exist -> apply default value
#                     #MATERIAL NAME CHECK
#                     if("Material" in row.index):
#                         if(pandas.isna(row["Material"])):
#                             row["Material"] = "No name"
#                     else:
#                         row["Material"] = "No name"


#                     #THICKNESS CHECK
#                     if("Thickness" in row.index):
#                         if(pandas.isna(row["Thickness"])):
#                             row["Thickness"] = 0
#                         thickness_conversion = self.convert_decimal_string_to_float(row["Thickness"]) 
#                         if((thickness_conversion != False) and (thickness_conversion >= 0)):
#                             row["Thickness"] = thickness_conversion
#                         else:
#                             row["Thickness"] = 0
#                     else:
#                         row["Thickness"] = 0


#                     #UNIT CHECK
#                     if("Unit" in row.index):
#                         if(pandas.isna(row["Unit"])):
#                             row["Unit"] = "No value"
#                     else:
#                         row["Unit"] = "No value"


#                     #INDENT CHECK
#                     if("Unit" in row.index):
#                         if(pandas.isna(row["Indent [nm]"])):
#                             row["Indent [nm]"] = 0
#                         indent_conversion = self.convert_decimal_string_to_float(row["Indent [nm]"]) 
#                         if((indent_conversion != False) and (indent_conversion >= 0)):
#                             row["Indent [nm]"] = indent_conversion
#                         else:
#                             row["Indent [nm]"] = 0
#                     else:
#                         row["Indent [nm]"] = 0
                    


#                     #COLOR CHECK
#                     if("Color" in row.index):
#                         if((pandas.isna(row["Color"])) or (self.is_valid_color(row["Color"]) == False)):
#                             row["Color"] = "white"
#                     else:
#                         row["Color"] = "white"


#                     #MODULUS CHECK
#                     if("Modulus [GPa]" in row.index):
#                         if(pandas.isna(row["Modulus [GPa]"])):
#                             row["Modulus [GPa]"] = 0
#                         modulus_conversion = self.convert_decimal_string_to_float(row["Modulus [GPa]"]) 
#                         if(modulus_conversion != False):
#                             row["Modulus [GPa]"] = abs(modulus_conversion)
#                         else:
#                             row["Modulus [GPa]"] = 0  
#                     else:
#                         row["Modulus [GPa]"] = 0    



#                     #CTE CHECK
#                     if("CTE [ppm/deg]" in row.index):
#                         if(pandas.isna(row["CTE [ppm/deg]"])):
#                             row["CTE [ppm/deg]"] = 0
#                         cte_conversion = self.convert_decimal_string_to_float(row["CTE [ppm/deg]"]) 
#                         if(cte_conversion != False):
#                             row["CTE [ppm/deg]"] = abs(cte_conversion)
#                         else:
#                             row["CTE [ppm/deg]"] = 0 
#                     else:
#                         row["CTE [ppm/deg]"] = 0 



#                     #DENSITY CHECK
#                     if("Density [kg/m3]" in row.index):
#                         if(pandas.isna(row["Density [kg/m3]"])):
#                             row["Density [kg/m3]"] = 0
#                         density_conversion = self.convert_decimal_string_to_float(row["Density [kg/m3]"]) 
#                         if(density_conversion != False):
#                             row["Density [kg/m3]"] = abs(density_conversion)
#                         else:
#                             row["Density [kg/m3]"] = 0 
#                     else:
#                         row["Density [kg/m3]"] = 0 



#                     #STRESS CHECK
#                     if("Stress_x [MPa]" in row.index):
#                         if(pandas.isna(row["Stress_x [MPa]"])):
#                             row["Stress_x [MPa]"] = 0
#                         stress_conversion = self.convert_decimal_string_to_float(row["Stress_x [MPa]"]) 
#                         if(stress_conversion != False):
#                             row["Stress_x [MPa]"] = stress_conversion
#                         else:
#                             row["Stress_x [MPa]"] = 0 
#                     else:
#                         row["Stress_x [MPa]"] = 0 


#                     #POISSON CHECK
#                     if("Poisson" in row.index):
#                         if(pandas.isna(row["Poisson"])):
#                             row["Poisson"] = 0
#                         poisson_conversion = self.convert_decimal_string_to_float(row["Poisson"]) 
#                         if(poisson_conversion != False):
#                             row["Poisson"] = abs(poisson_conversion)
#                         else:
#                             row["Poisson"] = 0
#                     else:
#                         row["Poisson"] = 0


#                     #R0 CHECK
#                     if("R0" in row.index):
#                         if(pandas.isna(row["R0"])):
#                             row["R0"] = 0
#                         R0_conversion = self.convert_decimal_string_to_float(row["R0"]) 
#                         if(R0_conversion != False):
#                             row["R0"] = R0_conversion
#                         else:
#                             row["R0"] = 0
#                     else:
#                         row["R0"] = 0


#                     #R CHECK
#                     if("R" in row.index):
#                         if(pandas.isna(row["R"])):
#                             row["R"] = 0
#                         R_conversion = self.convert_decimal_string_to_float(row["R"]) 
#                         if(R_conversion != False):
#                             row["R"] = R_conversion
#                         else:
#                             row["R"] = 0 
#                     else:
#                         row["R"] = 0 

                    
#                     #Create an "info" dictionary to contain all info from excel-file
#                     info = {
#                         "Name": row["Material"],
#                         "Layer": int(layer),
#                         "Thickness": float(row["Thickness"]),
#                         "Unit": row["Unit"],
#                         "Indent [nm]": float(row["Indent [nm]"]),
#                         "Color": row["Color"],
#                         "Status": "active",
#                         "Modulus [GPa]": float(row["Modulus [GPa]"]),
#                         "CTE [ppm/deg]": float(row["CTE [ppm/deg]"]),
#                         "Density [kg/m3]": float(row["Density [kg/m3]"]),
#                         "Stress_x [MPa]": float(row["Stress_x [MPa]"]),
#                         "Poisson": float(row["Poisson"]),
#                         "R0": float(row["R0"]),
#                         "R": float(row["R"]),
#                         "Label_name_id": None,
#                         "Delete_material_button_id": None,
#                         "Move_down_button_id": None,
#                         "Move_up_button_id": None,
#                         "Entry_id": None,
#                         "Slider_id": None,
#                         "Checkbox_id": None,
#                         "Rectangle_id": None,
#                         "Text_id": None,
#                         "Text_bbox_id" : None,
#                         "Line_id": None,
#                         "Indent_text_id": None,
#                         "Indent_text_bbox_id": None,
#                         "Indent_line_id": None,
#                         "Indent_arrow_pointer_id": None
#                     }

#                     #Put "info" dictionary into self.materials dictionary
#                     globals.materials[row["Material"]] = info

#                     layer += 1
                
#                 #Sort the materials dictionary
#                 self.sort_dictionary()
                
#             except Exception as error:
#                 messagebox.showerror("Error", "Could not load materials from Excel-file")
#                 return

    