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
from Canvas_Control_Panel import Canvas_Control_Panel
from Graph import Graph
from Graph_Control_Panel import Graph_Control_Panel
from Material_Control_Panel import Material_Control_Panel


#Main application class
class App:
    def __init__(self, program_window):
        #print("CLASS APP INIT()")

        #Program window
        self.program_window = program_window

        #If excel file exists and user wants to open load it, then load materials.xlsx
        if(os.path.isfile("Materials.xlsx")):
            self.load_materials_from_excel()

        #Main frame where every widgets is placed
        self.main_frame = self.create_scrollable_frame(self.program_window)
        globals.main_frame = self.main_frame

        #Create canvas to draw materials on. This class also creates a control panel to control the layer_stack_canvas
        globals.layer_stack_canvas = Layer_Stack_Canvas(self.main_frame)

        #Create a panel that controls the properties of each material
        globals.material_adjustment_panel = Material_Adjustment_Panel(self.main_frame)

        #Create a panel that controls the properties of each material
        globals.material_control_panel = Material_Control_Panel(self.main_frame)

        #Create a panel that controls the actions of the layer_stack_canvas
        globals.canvas_control_panel = Canvas_Control_Panel(self.main_frame)


    """
    -Creates a scrollable frame on the window given in the class
    -(To be able to do this a "canvas" is made and a "frame" is placed on top of the canvas. 
    -(Then scrollbars are placed in the main window which controls scrolling on the canvas)
    """
    def create_scrollable_frame(self, window):
        # print("CREATE_SCROLLABLE_FRAME()")
        #Create a background canvas (Scrollbars can only be used with a canvas)
        background_canvas = customtkinter.CTkCanvas(
            master=window,
            bg=settings.background_canvas_background_color,
            highlightthickness=0
        )
        background_canvas.grid(
            row=0, 
            column=0, 
            sticky="nsew",
        )

        #Create a frame inside the canvas to hold all the widgets and enable scrolling
        main_frame = customtkinter.CTkFrame(
            master=background_canvas, 
            width=settings.main_frame_width, 
            height=settings.main_frame_height, 
            fg_color=settings.main_frame_background_color,
        )
        main_frame.grid(
            row=0,
            column=0
        )

        #Add the frame to a window in the background_canvas
        background_canvas.create_window(
            (0, 0), 
            window=main_frame, 
            anchor="nw"
        )

        #Configure the main_frame to expand with the program_window/background_canvas
        main_frame.bind("<Configure>", self.on_frame_configure(background_canvas))

        #Prevent the main_frame window to downsize itself to fit widgets placed inside
        main_frame.grid_propagate(False)

        background_canvas.configure(scrollregion=background_canvas.bbox("all"))


        #Add scrollbars to the background_canvas
        canvas_vertical_scrollbar = customtkinter.CTkScrollbar(
            master=window,
            orientation="vertical",
            width=settings.scrollbar_width,
            border_spacing=settings.scrollbar_border_spacing,
            fg_color=settings.scrollbar_background_color,
            command=background_canvas.yview
        )
        canvas_vertical_scrollbar.grid(
            row=0, 
            column=1,
            sticky="ns",
        )

        canvas_horizontal_scrollbar = customtkinter.CTkScrollbar(
            master=window,
            orientation="horizontal", 
            width=settings.scrollbar_width,
            border_spacing=settings.scrollbar_border_spacing,
            fg_color=settings.scrollbar_background_color,
            command=background_canvas.xview
        )
        canvas_horizontal_scrollbar.grid(
            row=1, 
            column=0, 
            sticky="ew"
        )

        #Configure the background_canvas to use the scrollbars
        background_canvas.configure(
            yscrollcommand=canvas_vertical_scrollbar.set, 
            xscrollcommand=canvas_horizontal_scrollbar.set
        )

        #Make the frame resize properly
        background_canvas.grid_rowconfigure(0, weight=1)
        background_canvas.grid_columnconfigure(0, weight=1)

        return main_frame


    """
    Dynamically adjusts the scrollable area of the background_canvas
    Ensures that the scrollbars correctly reflect the size of the content inside the canvas
    """
    def on_frame_configure(self, canvas, event=None):
        #Update the scroll region of the canvas to encompass the entire frame
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    
    """Reads the given excel-file and populates the self.materials dictionary with info about each material"""
    def load_materials_from_excel(self):
        #print("LOAD_MATERIALS_FROM_EXCEL()")
        
        excel_file = "Materials.xlsx"

        #If there is a "materials" file in the folder, read it and populate the self.materials dictionary 
        if(os.path.isfile(excel_file)):
            try:
                #Read given excel file into Pandas dataframe
                excel_data = pandas.read_excel(excel_file)

                #Open excel-file to read background colors of each cell
                work_book = openpyxl.load_workbook(excel_file, data_only=True)
                fs = work_book.active

                #Loop through the rows in excel_file
                i = 2
                layer = 1
                for column, row in excel_data.iterrows():
                    #Increment "i" to go to the next row
                    i+=1

                    #If some cells are left empty, apply default value
                    if(pandas.isna(row["Material"])):
                        row["Material"] = "No name"
                    if(pandas.isna(row["Thickness"])):
                        row["Thickness"] = 0                    
                    if(pandas.isna(row["Unit"])):
                        row["Unit"] = "No value"
                    if(pandas.isna(row["Indent [nm]"])):
                        row["Indent [nm]"] = 0
                    if(pandas.isna(row["Color"])):
                        row["Color"] = "white"
                    if(pandas.isna(row["Modulus [GPa]"])):
                        row["Modulus [GPa]"] = 0
                    if(pandas.isna(row["CTE [ppm/deg]"])):
                        row["CTE [ppm/deg]"] = 0
                    if(pandas.isna(row["Density [kg/m3]"])):
                        row["Density [kg/m3]"] = 0
                    if(pandas.isna(row["Stress_x [MPa]"])):
                        row["Stress_x [MPa]"] = 0
                    if(pandas.isna(row["Poisson"])):
                        row["Poisson"] = 0
                    if(pandas.isna(row["R0"])):
                        row["R0"] = 0
                    if(pandas.isna(row["R"])):
                        row["R"] = 0

                    #Create an "info" dictionary to contain all info from excel-file
                    info = {
                        "Name": row["Material"],
                        "Layer": int(layer),
                        "Thickness": int(row["Thickness"]),
                        "Unit": row["Unit"],
                        "Indent [nm]": int(row["Indent [nm]"]),
                        "Color": row["Color"],
                        "Status": "active",
                        "Modulus [GPa]": int(row["Modulus [GPa]"]),
                        "CTE [ppm/deg]": int(row["CTE [ppm/deg]"]),
                        "Density [kg/m3]": int(row["Density [kg/m3]"]),
                        "Stress_x [MPa]": int(row["Stress_x [MPa]"]),
                        "Poisson": int(row["Poisson"]),
                        "R0": int(row["R0"]),
                        "R": int(row["R"]),
                        "Label_name_id": None,
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
                    globals.materials[row["Material"]] = info

                    layer += 1
                
                #Sort the materials dictionary
                self.sort_dictionary()
                
            except Exception as error:
                messagebox.showerror("Error", "Could not load materials from Excel-file")
                return


    """Places 'substrate' as the lowest layer and sorts the materials{} dictionary after the 'layer' value of each material"""
    def sort_dictionary(self):
        # print("SORT_DICTIONARY()")

        #If "substrate" is in dictionary
        for key in globals.materials:
            if(key.lower() == "substrate"):
                #if "substrate" is not the lowest layer
                if(globals.materials[key]["Layer"] < len(globals.materials)):
                    substrate_orig_place = globals.materials[key]["Layer"] 
                    #place "substrate" as the lowest layer
                    globals.materials[key]["Layer"] = len(globals.materials)

                    #Decrement the "layer" value of other materials that was higher than the "substrate" layer
                    for material in globals.materials:
                        if(material.lower() != "substrate"):
                            if(globals.materials[material]["Layer"] > substrate_orig_place):
                                globals.materials[material]["Layer"] -= 1

        #Sort the materials dictionary after the "layer" value
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["Layer"]))


    """Prints the globals.materials dictionary specifily"""
    def print_dictionary(self):
        for material in globals.materials:
            print("Name: ", globals.materials[material]["Name"])
            print("Layer: ", globals.materials[material]["Layer"])
            print("Thickness: ", globals.materials[material]["Thickness"])  
            print("Unit: ", globals.materials[material]["Unit"])  
            print("Indent [nm]: ", globals.materials[material]["Indent [nm]"])  
            print("Color: ", globals.materials[material]["Color"])  
            print("Status: ", globals.materials[material]["Status"])  
            print("Modulus [GPa]: ", globals.materials[material]["Modulus [GPa]"])  
            print("CTE [ppm/deg]: ", globals.materials[material]["CTE [ppm/deg]"])  
            print("Density [kg/m3]: ", globals.materials[material]["Density [kg/m3]"])  
            print("Stress_x [MPa]: ", globals.materials[material]["Stress_x [MPa]"])  
            print("Poisson: ", globals.materials[material]["Poisson"])  
            print("R0: ", globals.materials[material]["R0"])  
            print("R: ", globals.materials[material]["R"])  
            
            print("\n")



if __name__ == "__main__":
    #Create the main application window
    program_window = tkinter.Tk()
    
    #Other classes needs access to this window 
    globals.program_window = program_window

    customtkinter.set_widget_scaling(settings.widget_scaling)
    customtkinter.set_window_scaling(settings.program_window_scaling)

    #Tells row 0 and column 0 in the main_window to expand to the size of the main_window
    #This makes a widget (background_canvas) placed in (row0,column0) expand with the main_window
    program_window.grid_rowconfigure(0, weight=1)
    program_window.grid_columnconfigure(0, weight=1)

    #Set the main window title, dimensions, and background color
    program_window.title(settings.program_window_title)
    program_window.geometry(f"{settings.program_window_width}x{settings.program_window_height}")
    program_window.configure(bg=settings.program_window_background_color)
        

    #Create keyboard shortcuts for the main window
    program_window.bind("<Escape>", lambda event: program_window.destroy())

    # #Resets the canvas position if "r" is pressed
    # program_window.bind('<KeyPress-r>', app.reset_canvas)

    # #Checks if the program window is being resized
    # program_window.bind("<Configure>", lambda event: app.program_window_resized(event))
    
    # Create an instance of App and run it
    app = App(program_window)   
    globals.app = app

    #Start the main loop of the program
    program_window.mainloop()

               