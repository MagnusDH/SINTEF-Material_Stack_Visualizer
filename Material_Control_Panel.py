import tkinter
from tkinter import messagebox, StringVar
import customtkinter
import settings #File containing settings
import globals  #File containing global variables
import pandas   #Excel-file reading
import openpyxl #Excel-file reading
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Font, Alignment
from PIL import ImageGrab
from openpyxl.drawing.image import Image
import os
import settings


class Material_Control_Panel:
    def __init__(self, window):
        # print("CLASS MATERIAL_CONTROL_PANEL INIT()")

        #Window where everything is placed
        self.window = window

        self.create_material_control_panel()


    """Creates a control panel frame to control actions of materials"""
    def create_material_control_panel(self):
        # print("CREATE_MATERIAL_CONTROL_PANEL")

        #if material_control_frame has NOT been created before, create it
        if not hasattr(self, 'material_control_panel_frame'):
            #Create Frame from the control panel and place it within given window
            self.material_control_panel_frame = customtkinter.CTkFrame(
                master=self.window, 
                width=settings.material_control_panel_width,
                height=settings.material_control_panel_height,
                fg_color=settings.material_control_panel_background_color
            )
            self.material_control_panel_frame.grid(
                row=1,
                column=0,
                sticky="nw",
                padx=(settings.material_control_panel_padding_left, settings.material_control_panel_padding_right),
                pady=(settings.material_control_panel_padding_top, settings.material_control_panel_padding_bottom)
            )

        #Prevent the Frame from shrinking or expanding
        self.material_control_panel_frame.grid_propagate(False)

        #Create button to "add material" and place it
        add_material_button = customtkinter.CTkButton(
            master=self.material_control_panel_frame, 
            width=36,
            height=36,
            text="+", 
            fg_color="#008c00", #settings.material_control_panel_button_color,
            hover_color="#00cd00", #settings.material_control_panel_button_hover_color,
            text_color=settings.material_control_panel_text_color,
            font=(settings.text_font, -26),
            command=self.add_material
        )
        add_material_button.grid(
            row=0,
            column=0,
            sticky="",
            padx=(5,0),
            pady=(5,0)
        )

        #Create button to modify the order of materials, and place the button
        modify_material_button = customtkinter.CTkButton(
            master=self.material_control_panel_frame, 
            width=35,
            height=35,
            text="⚙️",
            text_color="white", 
            font=(settings.text_font, -18),
            fg_color=settings.material_control_panel_button_color,
            hover_color=settings.material_control_panel_button_hover_color,
            command=self.modify_material
        )
        modify_material_button.grid(
            row=0,
            column=1,
            sticky="",
            padx=(5,0),
            pady=(5,0)
        ) 

        #Create button to export materials{} and stack to a excel file
        export_as_excel_button = customtkinter.CTkButton(
            master=self.material_control_panel_frame, 
            width=100,
            height=25,
            text="Export values to excel", 
            fg_color=settings.material_control_panel_button_color,
            hover_color=settings.material_control_panel_button_hover_color,
            text_color=settings.material_control_panel_text_color,
            command=self.export_to_excel
        )
        export_as_excel_button.grid(
            row=0,
            column=2,
            sticky="",
            padx=(5,0),
            pady=(5,0)
        )


    
    """Creates a popup window with value entries to add a new material in 'materials{}'"""
    def add_material(self):
        # print("ADD_MATERIAL()")
        #Open up new program window
        self.add_material_window = tkinter.Toplevel(self.window)
        self.add_material_window.title("Add material")
        self.add_material_window.geometry(f"{settings.add_material_window_width}x{settings.add_material_window_height}")
        self.add_material_window.configure(bg=settings.add_material_window_background_color)

        #Create Labels and Entries for material properties 
        self.material_name_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Name", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.material_name_label.grid(
            row=0, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        #Name
        self.material_name_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color="white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.material_name_entry.grid(
            row=0, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )

        #Thickness
        self.material_thickness_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Thickness [nm]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.material_thickness_label.grid(
            row=1, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.material_thickness_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.material_thickness_entry.grid(
            row=1, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )

        # #Unit
        # self.material_unit_label = customtkinter.CTkLabel(
        #     master=self.add_material_window, 
        #     text="Measurement unit", 
        #     text_color=settings.add_material_window_text_color,
        #     fg_color=settings.add_material_window_background_color,
        # )
        
        # self.material_unit_label.grid(
        #     row=2, 
        #     column=0, 
        #     sticky="", 
        #     padx=(0,0),
        #     pady=(0,0)
        # )

        # self.material_unit_entry = customtkinter.CTkEntry(
        #     master=self.add_material_window,
        #     fg_color = "white",
        #     text_color="black",
        #     width=70,
        #     justify="center"
        # )
        # self.material_unit_entry.grid(
        #     row=2, 
        #     column=1,
        #     sticky="e",
        #     padx=(0,0),
        #     pady=(0,0)
        # )

        #Indent
        self.material_indent_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Indent [nm]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.material_indent_label.grid(
            row=3, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.material_indent_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.material_indent_entry.grid(
            row=3, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )

        #Color
        self.material_color_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Color", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.material_color_label.grid(
            row=4, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.material_color_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.material_color_entry.grid(
            row=4, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )


        #Modulus [GPa] value
        self.Modulus_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Modulus [GPa]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.Modulus_value_label.grid(
            row=5, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.Modulus_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.Modulus_value_entry.grid(
            row=5, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )

        #################################
        #CTE [ppm/deg] value
        self.CTE_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="CTE [ppm/deg]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.CTE_value_label.grid(
            row=6, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.CTE_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.CTE_value_entry.grid(
            row=6, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )
        #################################


        #Density [kg/m3] value
        self.Density_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Density [kg/m3]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.Density_value_label.grid(
            row=7, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.Density_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.Density_value_entry.grid(
            row=7, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )

        
        #Stress_x [MPa] value
        self.Stress_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Stress_x [MPa]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.Stress_value_label.grid(
            row=8, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.Stress_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.Stress_value_entry.grid(
            row=8, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )
            

        #Poisson value
        self.Poisson_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Poisson", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.Poisson_value_label.grid(
            row=9, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.Poisson_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.Poisson_value_entry.grid(
            row=9, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )

        #Confirm button
        confirm_button = customtkinter.CTkButton(
            master=self.add_material_window,
            text="Confirm",
            fg_color=settings.add_material_window_button_color,
            hover_color=settings.add_material_window_button_hover_color,
            text_color=settings.add_material_window_text_color,
            width=15,
            command=self.validate_add_material_inputs
        )
        confirm_button.grid(
            row=10,
            column=2,
            sticky="n",
            padx=(0,0),
            pady=(0,0)
        )


    """
    Checks if the inputs from the entries are valid.
    Calls 'add_material_to_dictionary' if inputs are valid
    """
    def validate_add_material_inputs(self):
        # print("VALIDATE_INPUTS()")

        #Check if no entries are empty
        if(not self.material_name_entry.get()):
            messagebox.showerror("ERROR", "'Name' can not be empty", parent=self.add_material_window)
            self.add_material_window.lift()
            return
        
        #Check if material_name already exists in materials dictionary
        if(self.material_name_entry.get() in globals.materials):
            messagebox.showerror("ERROR", "'Name' already exists", parent=self.add_material_window)
            return


        #If "thickness" value is entered, check if it is integer
        if(self.material_thickness_entry.get() != ""):
            try:
                thickness_value = self.material_thickness_entry.get() 
                thickness_value = int(thickness_value)
            except ValueError:
                messagebox.showerror("ERROR", "'Thickness' value has to be an integer", parent=self.add_material_window)
                return

        #if "indent" value is entered, check if it is integer
        if(self.material_indent_entry.get() != ""):
            try:
                indent_value = self.material_indent_entry.get() 
                indent_value = int(indent_value)
            except ValueError:
                messagebox.showerror("ERROR", "'Indent' value has to be an integer", parent=self.add_material_window)
                return


        #Color
        if(not self.material_color_entry.get()):
            messagebox.showerror("ERROR", "'Color' can not be empty", parent=self.add_material_window)
            self.add_material_window.lift()
            return
        
        #Check if input color is valid
        if(self.is_valid_color(self.material_color_entry.get()) == False):
            messagebox.showerror("ERROR", "Given color is not valid.\nValue must be valid string or hex-value ('#123456)", parent=self.add_material_window)
            self.add_material_window.lift()
            return

        #If "E" value is entered, check if it is integer
        if(self.Modulus_value_entry.get() != ""):
            try:
                Modulus_value = self.Modulus_value_entry.get() 
                Modulus_value = int(Modulus_value)
            except ValueError:
                messagebox.showerror("ERROR", "'Modulus [GPa]' value has to be an integer", parent=self.add_material_window)
                return
        
        #If "CTE" value is entered, check if it is integer
        if(self.CTE_value_entry.get() != ""):
            try:
                CTE_value = self.CTE_value_entry.get() 
                CTE_value = int(CTE_value)
            except ValueError:
                messagebox.showerror("ERROR", "'CTE [ppm/deg]' value has to be an integer", parent=self.add_material_window)
                return
        

        #If "Density" value is entered, check if it is integer
        if(self.Density_value_entry.get() != ""):
            try:
                Density_value = self.Density_value_entry.get() 
                Density_value = int(Density_value)
            except ValueError:
                messagebox.showerror("ERROR", "'Density [kg/m3]' value has to be an integer", parent=self.add_material_window)
                return


        #If 'Stress_x [MPa]' value is entered, check if it is integer 
        if(self.Stress_value_entry.get() != ""):
            try:
                Stress_value = self.Stress_value_entry.get() 
                Stress_value = int(Stress_value)
            except ValueError:
                messagebox.showerror("ERROR", "'Stress_x [MPa]' value has to be an integer", parent=self.add_material_window)
                return


        #If 'Poisson' value is entered, check if it is integer
        if(self.Poisson_value_entry.get() != ""):
            try:
                Poisson_value = self.Poisson_value_entry.get() 
                Poisson_value = int(Poisson_value)
            except ValueError:
                messagebox.showerror("ERROR", "'Poisson' value has to be an integer", parent=self.add_material_window)
                return


        #All inputs have been validated, add it to dictionary
        self.add_material_to_dictionary()
        self.add_material_window.destroy()
        
        #Update material_adjustment_panel
        globals.material_adjustment_panel.create_material_adjustment_panel()

        #Re-draw the material stack
        globals.layer_stack_canvas.draw_material_stack()


    
    """Returns True if given color string is a valid color. Return False if invalid"""
    def is_valid_color(self, color):
        #Check if color is accepted by tkinter
        try:
            self.window.winfo_rgb(color)
            return True
        
        except:
            #Check if color is valid hexadecimal value
            if(type(color)==str and color.startswith('#') and len(color)==7):
                return True
            else:
                return False
    

    """Adds values from entries to 'materials' dictionary"""
    def add_material_to_dictionary(self):
        # print("ADD_MATERIAL_TO_DICTIONARY")

        #If some entries in "add_material_window" are not set, the values is automaticly set to zero
        #THICKNESS
        if(self.material_thickness_entry.get() == ""):
            material_thickness = 1
        else:
            material_thickness = int(self.material_thickness_entry.get())

        #INDENT
        if(self.material_indent_entry.get() == ""):
            material_indent = 1
        else:
            material_indent = int(self.material_indent_entry.get())

        #Modulus [GPa] VALUE
        if(self.Modulus_value_entry.get() == ""):
            Modulus_value = 0
        else:
            Modulus_value = int(self.Modulus_value_entry.get())

        #CTE [ppm/deg] VALUE
        if(self.CTE_value_entry.get() == ""):
            CTE_value = 0
        else:
            CTE_value = int(self.CTE_value_entry.get())

        #Density [kg/m3] VALUE
        if(self.Density_value_entry.get() == ""):
            Density_value = 0
        else:
            Density_value = int(self.Density_value_entry.get())
        
        #Stress_x [MPa] VALUE
        if(self.Stress_value_entry.get() == ""):
            Stress_value = 0
        else:
            Stress_value = int(self.Stress_value_entry.get())
        
        #POISSON VALUE
        if(self.Poisson_value_entry.get() == ""):
            Poisson_value = 0
        else:
            Poisson_value = int(self.Poisson_value_entry.get())

        #Loop through all materials and increment "layer" with 1, assuring that the new material is placed on top of the stack
        for material in globals.materials:
            globals.materials[material]["Layer"] += 1

        #Add values to dictionary
        info = {
            "Name": str(self.material_name_entry.get()),
            "Layer": 1,
            "Thickness": material_thickness,
            "Unit": "nm",
            "Indent [nm]": material_indent,
            "Color": str(self.material_color_entry.get()),
            "Status": "active",
            "Modulus [GPa]": Modulus_value,
            "CTE [ppm/deg]": CTE_value,
            "Density [kg/m3]": Density_value,
            "Stress_x [MPa]": Stress_value,
            "Poisson": Poisson_value,
            "Label_name_id": None,
            "Rectangle_id": None,
            "Text_id": None,
            "Text_bbox_id" : None,
            "Line_id": None,
            "Entry_id": None,
            "Slider_id": None,
            "Indent_text_id": None,
            "Indent_text_bbox_id": None,
            "Indent_line_id": None,
            "Indent_arrow_pointer_id": None
        }
        
        #Put "info" dictionary into self.materials dictionary
        globals.materials[self.material_name_entry.get()] = info

        #Sort the materials dictionary after the "layer" value
        globals.app.sort_dictionary()
        # globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["layer"]))
       

    # """
    # -Deletes all widgets from material_adjustment_panel, material_control_panel and canvas_control_panel
    # -Renders materials along with a 'select' button on the side
    # -Renders a 'cancel edit' button
    # """
    # def choose_material(self):
        # # print("CHOOSE_MATERIAL()")

        # #Delete all the widgets in the "material_adjustment_panel"
        # for widget in globals.material_adjustment_panel.material_adjustment_panel_frame.winfo_children():
        #     widget.destroy()
        
        # #Delete all the widgets in the "canvas_control_panel"
        # for widget in globals.canvas_control_panel.canvas_control_panel_frame.winfo_children():
        #     widget.destroy()

        # #Delete all the widgets in the "material_control_panel"
        # for widget in globals.material_control_panel.material_control_panel_frame.winfo_children():
        #     widget.destroy()   


        # #Render all materials with a checkbox on the left side
        # row_counter = 0
        # for material in globals.materials:
        #     if(material.lower() != "substrate"):
        #         #Create a "choose material" button and place it
        #         choose_button = customtkinter.CTkButton(
        #             master=globals.material_adjustment_panel.material_adjustment_panel_frame, 
        #             text="Select", 
        #             width=90,
        #             height=10,
        #             hover_color=globals.materials[material]["Color"],
        #             command=lambda chosen_material=material: self.move_material(chosen_material)
        #         )
        #         choose_button.grid(
        #             row=row_counter,
        #             column=0,
        #             sticky="",
        #             padx=(0,0),
        #             pady=(0,0)
        #         )

        #     #Create a "layer" label for current material
        #     layer_label = customtkinter.CTkLabel(
        #         master=globals.material_adjustment_panel.material_adjustment_panel_frame,
        #         text=globals.materials[material]["Layer"]
        #     )
        #     layer_label.grid(
        #         row=row_counter,
        #         column=1,
        #         sticky="",
        #         padx=(10,0),
        #         pady=(0,0)
        #     )

        #     #Create a label for current material
        #     material_label = customtkinter.CTkLabel(
        #         master=globals.material_adjustment_panel.material_adjustment_panel_frame,
        #         text=material,
        #     )
        #     material_label.grid(
        #         row=row_counter,
        #         column=2,
        #         sticky="",
        #         padx=(10,0),
        #         pady=(0,0)
        #     )

        #     row_counter += 1

        # #Render an explanation on how the editing works
        # explanation_label = customtkinter.CTkLabel(
        #     master=globals.material_adjustment_panel.material_adjustment_panel_frame,
        #     text="Please select the material \nyou want to move",
        #     fg_color="#36556c"
        # )
        # explanation_label.grid(
        #     row=0,
        #     column=4,
        #     sticky="e",
        #     padx=(20,0),
        #     pady=(0,0)
        # )


        # #Render a "cancel edit mode" button, and place it
        # cancel_edit_mode_button = customtkinter.CTkButton(
        #     master=globals.material_control_panel.material_control_panel_frame, 
        #     text="Done editing", 
        #     width=70,
        #     height=10,
        #     command=self.finish_edit
        # )
        # cancel_edit_mode_button.grid(
        #     row=0,
        #     column=0,
        #     sticky="",
        #     padx=(140,0),
        #     pady=(25,0)
        # )

        # # #Render a "done" button and place it
        # # finish_edit_button = customtkinter.CTkButton(
        # #     master=globals.material_control_panel.material_control_panel_frame, 
        # #     text="Confirm", 
        # #     width=70,
        # #     height=10,
        # #     command=self.finish_edit
        # # )
        # # finish_edit_button.grid(
        # #     row=0,
        # #     column=1,
        # #     sticky="",
        # #     padx=(5,0),
        # #     pady=(5,0)
        # # )


    # """
    # -Deletes all widgets in material_adjustment_panel
    # -Renders all materials along with a 'move_here' button
    # """
    # def move_material(self, chosen_material):
        # # print("MOVE_MATERIAL()")
        
        # #Delete all the widgets in the "material_adjustment_panel"
        # for widget in globals.material_adjustment_panel.material_adjustment_panel_frame.winfo_children():
        #     widget.destroy()

        # #Render all materials with a button on the left side
        # row_counter = 0
        # for material in globals.materials:

        #     #Render "deselect" button for chosen_material
        #     if(material == chosen_material):
        #         deselect_button = customtkinter.CTkButton(
        #             master=globals.material_adjustment_panel.material_adjustment_panel_frame, 
        #             text="Deselect", 
        #             width=70,
        #             height=10,
        #             fg_color="#d80000",
        #             hover_color="#ff0000",
        #             # command=lambda selected_layer=material, chosen_material=chosen_material: self.edit_layers(chosen_material, selected_layer)
        #             command=self.choose_material
        #         )
        #         deselect_button.grid(
        #             row=row_counter,
        #             column=0,
        #             sticky="",
        #             padx=(0,0),
        #             pady=(0,0)
        #         )
        #     #Render "choose material" button for the other materials
        #     else:
        #         #Create a "choose material" button and place it, but skip "substrate"
        #         if(material.lower() != "substrate"):
        #             move_here_button = customtkinter.CTkButton(
        #                 master=globals.material_adjustment_panel.material_adjustment_panel_frame, 
        #                 text=f"Place in row: ",#{globals.materials[material]['layer']}", 
        #                 width=70,
        #                 height=10,
        #                 hover_color=globals.materials[material]["Color"],# "#26aa00",
        #                 command=lambda selected_layer=material, chosen_material=chosen_material: self.edit_layers(chosen_material, selected_layer)
        #             )
        #             move_here_button.grid(
        #                 row=row_counter,
        #                 column=0,
        #                 sticky="",
        #                 padx=(0,0),
        #                 pady=(0,0)
        #             )

        #     #Create a "layer" label for current material
        #     layer_label = customtkinter.CTkLabel(
        #         master=globals.material_adjustment_panel.material_adjustment_panel_frame,
        #         text=globals.materials[material]["Layer"],
        #     )
        #     layer_label.grid(
        #         row=row_counter,
        #         column=1,
        #         sticky="w",
        #         padx=(10,0),
        #         pady=(0,0)
        #     )

        #     #Create a label for current material
        #     material_label = customtkinter.CTkLabel(
        #         master=globals.material_adjustment_panel.material_adjustment_panel_frame,
        #         text=material,
        #     )
        #     material_label.grid(
        #         row=row_counter,
        #         column=2,
        #         sticky="",
        #         padx=(10,0),
        #         pady=(0,0)
        #     )

        #     row_counter += 1
        
        # #Render an explanation on how the editing works
        # explanation_label = customtkinter.CTkLabel(
        #     master=globals.material_adjustment_panel.material_adjustment_panel_frame,
        #     text="Please select the row\nto place it in",
        #     fg_color="#36556c"
        # )
        # explanation_label.grid(
        #     row=0,
        #     column=4,
        #     sticky="e",
        #     padx=(30,0),
        #     pady=(0,0)
        # )


    # """
    # -Organizes materials{} so that the order of "layers" is consistent
    # -Redraws the material stack
    # -Renders the 'choose_material' version of the material_adjustment_frame again
    # """
    # def edit_layers(self, first_material, second_material):
        # # print("EDIT_LAYERS()")

        # #save first material original "layer" value
        # first_material_orig_layer = globals.materials[first_material]["Layer"] 

        # #Save second_material original "layer" value
        # second_material_orig_layer = globals.materials[second_material]["Layer"] 

        # if(first_material_orig_layer > second_material_orig_layer):
        #     #Change the layer value in chosen material to the selected layer
        #     globals.materials[first_material]["Layer"] = globals.materials[second_material]["Layer"]

        #     #For everything that is lower than first material layer, excluding the first_material
        #     for material in globals.materials:
        #         if(material != first_material):
        #             if(globals.materials[material]["Layer"] < first_material_orig_layer):
        #                 if(globals.materials[material]["Layer"] >= second_material_orig_layer):
        #                     globals.materials[material]["Layer"] += 1
        
        # #first_material layer is less than second_material layer
        # else:
        #     #Change the layer value in chosen material to the selected layer
        #     globals.materials[first_material]["Layer"] = globals.materials[second_material]["Layer"]

        #     #For everything that is higher than first material layer, excluding the first_material
        #     for material in globals.materials:
        #         if(material != first_material):
        #             if(globals.materials[material]["Layer"] > first_material_orig_layer):
        #                 if(globals.materials[material]["Layer"] <= second_material_orig_layer):
        #                     globals.materials[material]["Layer"] -= 1


        # #Order globals.materials{} in order of "layer"
        # globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["Layer"]))

        # #Redraw the material stack
        # globals.layer_stack_canvas.draw_material_stack()

        # #Render the first "select material" edit mode version
        # self.choose_material()


    # """
    # -Deletes all widgets from material_adjustment_panel, material_control_panel and canvas_control_panel
    # -Rebuilds the original verions of material_adjustment_panel, material_control_panel and canvas_control_panel
    # """
    # def finish_edit(self):
        # # print("FINISH_EDIT()")
        
        # #Delete widgets in material_adjustment_panel_frame
        # for widget in globals.material_adjustment_panel.material_adjustment_panel_frame.winfo_children():
        #     widget.destroy()  

        # #Delete widgets in material_control_panel_frame
        # for widget in globals.material_control_panel.material_control_panel_frame.winfo_children():
        #     widget.destroy()

        # #Delete widgets in canvas_control_panel_frame
        # for widget in globals.canvas_control_panel.canvas_control_panel_frame.winfo_children():
        #     widget.destroy()

        # #Restore the material_adjustment_panel
        # globals.material_adjustment_panel.create_material_adjustment_panel()

        # #Restore the material_control_panel
        # globals.material_control_panel_frame = globals.material_control_panel.create_material_control_panel()

        # #Restore the canvas_control_panel
        # globals.canvas_control_panel.create_canvas_control_panel()


    """Creates a new 'modify_material' window where the user can change the attributes of each material"""
    def modify_material(self):
        # print("MODIFY_MATERIAL()")

        #Create dictionary to contain ALL entries
        self.entry_dictionary = {}

        #Open up new program window
        self.modify_material_window = tkinter.Toplevel(self.window)
        self.modify_material_window.title("Modify material")
        self.modify_material_window.geometry(f"{settings.modify_material_window_width}x{settings.modify_material_window_height}")
        self.modify_material_window.configure(bg=settings.modify_material_window_background_color)

        headline_label = customtkinter.CTkLabel(
            master=self.modify_material_window,
            text="      Material          Thickness      Unit      Indent[nm]         Color          Modulus [GPa]      CTE [ppm/deg]    Density [kg/m3]    Stress_x [MPa]         Poisson",
            font=(settings.modify_material_window_text_font, settings.modify_material_window_text_size, "bold"),
            text_color="white",
            fg_color=settings.modify_material_window_background_color
        )
        headline_label.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=(5,0),
            pady=(0,0)
        )

        #Create a scrollable frame for entries to each material
        scrollable_frame = customtkinter.CTkScrollableFrame(
            master=self.modify_material_window,
            width=settings.modify_material_window_scrollable_frame_width,
            height=settings.modify_material_window_scrollable_frame_height,
            # label_text = "   Material     Thickness         Unit        Indent[nm]       Color     Modulus [GPa]        CTE [ppm/deg]      Density [kg/m3]         Stress_x [MPa]       Poisson",
            # label_fg_color = settings.modify_material_window_background_color,
            # label_font=(settings.modify_material_window_text_font, settings.modify_material_window_text_size, "bold"),
            # label_anchor="w"
        )
        scrollable_frame.grid(
            row=1,
            column=0,
            sticky="nw",
            padx=(0,0),
            pady=(0,0)
        )

        #Loop through all materials
        row_counter = 0
        for material in globals.materials:
            inner_dictionary = {}

            #Create entries for each category in materials

            #MATERIAL NAME
            material_name_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Name"])),
                width=100, #settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            material_name_entry.grid(
                row=row_counter,
                column=0,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )
            #Add entry to dictionary
            inner_dictionary["Name_entry"] = material_name_entry

            #THICKNESS
            thickness_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Thickness"])),
                width=100, #settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            thickness_entry.grid(
                row=row_counter,
                column=1,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["Thickness_entry"] = thickness_entry

            
            #UNIT
            unit_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Unit"])),
                width=40,#settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            unit_entry.grid(
                row=row_counter,
                column=2,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["Unit_entry"] = unit_entry

            
            #INDENT [NM]
            indent_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Indent [nm]"])),
                width=100, #settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            indent_entry.grid(
                row=row_counter,
                column=3,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["Indent_entry"] = indent_entry

            
            #COLOR
            color_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Color"])),
                width=settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            color_entry.grid(
                row=row_counter,
                column=4,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["Color_entry"] = color_entry

            
            #MODULUS [GPa]
            modulus_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Modulus [GPa]"])),
                width=120, #settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            modulus_entry.grid(
                row=row_counter,
                column=5,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["Modulus_entry"] = modulus_entry

            
            #CTE [ppm/deg]
            CTE_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["CTE [ppm/deg]"])),
                width=120, #settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            CTE_entry.grid(
                row=row_counter,
                column=6,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["CTE_entry"] = CTE_entry

            
            #DENSITY [kg/m3]
            density_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Density [kg/m3]"])),
                width=120, #settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            density_entry.grid(
                row=row_counter,
                column=7,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["Density_entry"] = density_entry

            
            #STRESS_X [MPa]
            stress_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Stress_x [MPa]"])),
                width=120, #settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            stress_entry.grid(
                row=row_counter,
                column=8,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["Stress_entry"] = stress_entry

            #POISSON
            poisson_entry = customtkinter.CTkEntry(
                master=scrollable_frame,
                textvariable=StringVar(value=str(globals.materials[material]["Poisson"])),
                width=120, #settings.modify_material_window_entry_width,
                height=10,
                fg_color="white",
                text_color="black",
                justify="center"
            )
            poisson_entry.grid(
                row=row_counter,
                column=9,
                sticky="",
                padx=(3,0),
                pady=(0,0)
            )
            inner_dictionary["Poisson_entry"] = poisson_entry

            self.entry_dictionary[material] = inner_dictionary

            row_counter += 1
        
        confirm_button = customtkinter.CTkButton(
            master=self.modify_material_window,
            text="Confirm changes",
            command=self.validate_modify_material_inputs
        )
        confirm_button.grid(
            row=2,
            column=0,
            sticky="",
            padx=(0,0),
            pady=(0,0)
        )


    """Goes through all entries in self.entry_dictionary and validates all entries"""
    def validate_modify_material_inputs(self):
        for material in self.entry_dictionary:
            
            #NAME
            try:
                name = str(self.entry_dictionary[material]["Name_entry"].get())
                if(name == ""):
                    messagebox.showerror("ERROR", "'Material Name' can not be empty", parent=self.modify_material_window)
                    self.modify_material_window.lift()
                    return

            except ValueError:
                print("Material Name must be of type 'string'")
                return

            #THICKNESS
            try:
                thickness = int(self.entry_dictionary[material]["Thickness_entry"].get())

            except ValueError:
                messagebox.showerror("ERROR", "'Thickness' must be a 'digit'", parent=self.modify_material_window)
                return
        
            #UNIT
            try:
                unit = str(self.entry_dictionary[material]["Unit_entry"].get())
                if(unit == ""):
                    messagebox.showerror("ERROR", "'Unit' can not be empty", parent=self.modify_material_window)
                    self.modify_material_window.lift()
                    return

            except ValueError:
                messagebox.showerror("ERROR", "'Unit' must be of type 'string'", parent=self.modify_material_window)
                return 
        
            #INDENT [NM]
            try:
                indent = int(self.entry_dictionary[material]["Indent_entry"].get())

            except ValueError:
                messagebox.showerror("ERROR", "'Indent' must be a 'digit'", parent=self.modify_material_window)
                return
        
            #COLOR
            #Check if input color is valid
            if(self.is_valid_color(self.entry_dictionary[material]["Color_entry"].get()) == False):
                messagebox.showerror("ERROR", "Given 'Color' is not valid.\nValue must be valid string or hex-value ('#123456)", parent=self.modify_material_window)
                self.modify_material_window.lift()
                return
            try:
                color = str(self.entry_dictionary[material]["Color_entry"].get())
                if(color == ""):
                    messagebox.showerror("ERROR", "'Color' can not be empty", parent=self.modify_material_window)
                    self.modify_material_window.lift()
                    return

            except ValueError:
                print("'Color' must be of type 'string'")
                return


            #MODULUS [GPa]
            try:
                modulus = int(self.entry_dictionary[material]["Modulus_entry"].get())

            except ValueError:
                messagebox.showerror("ERROR", "'Modulus [GPa]' must be a 'digit'", parent=self.modify_material_window)
                return  
        
            #CTE [ppm/deg]
            try:
                CTE = int(self.entry_dictionary[material]["CTE_entry"].get())

            except ValueError:
                messagebox.showerror("ERROR", "'CTE [ppm/deg]' must be a 'digit'", parent=self.modify_material_window)
                return

            
            #DENSITY [kg/m3]
            try:
                density = int(self.entry_dictionary[material]["Density_entry"].get())

            except ValueError:
                messagebox.showerror("ERROR", "'Density [kg/m3]' must be a 'digit'", parent=self.modify_material_window)
                return

        
            #STRESS_X [MPa]
            try:
                stress = int(self.entry_dictionary[material]["Stress_entry"].get())

            except ValueError:
                messagebox.showerror("ERROR", "'Stress_x [MPa]' must be a 'digit'", parent=self.modify_material_window)
                return
        
            #POISSON
            try:
                poisson = int(self.entry_dictionary[material]["Poisson_entry"].get())

            except ValueError:
                messagebox.showerror("ERROR", "'Poisson' must be a 'digit'", parent=self.modify_material_window)
                return

        self.confirm_material_changes()

    
    """
    -Makes changes to the materials{} dictionary based on the values given by user
    -If the user modified the 'material_name' then the main key in materials{} is changed to the new name 
    """
    def confirm_material_changes(self):
        # print("CONFIRM_MATERIAL_CHANGES()")

        for material in self.entry_dictionary:
            #Change the main key in materials{} dictionary
            new_key = self.entry_dictionary[material]["Name_entry"].get()
            globals.materials[new_key] = globals.materials.pop(material)   

            #Replace values in dictionary 
            globals.materials[new_key]["Name"] = self.entry_dictionary[material]["Name_entry"].get()
            globals.materials[new_key]["Thickness"] = int(self.entry_dictionary[material]["Thickness_entry"].get())  
            globals.materials[new_key]["Unit"] = self.entry_dictionary[material]["Unit_entry"].get()  
            globals.materials[new_key]["Indent [nm]"] = int(self.entry_dictionary[material]["Indent_entry"].get()) 
            globals.materials[new_key]["Color"] = self.entry_dictionary[material]["Color_entry"].get()  
            globals.materials[new_key]["Modulus [GPa]"] = int(self.entry_dictionary[material]["Modulus_entry"].get())  
            globals.materials[new_key]["CTE [ppm/deg]"] = int(self.entry_dictionary[material]["CTE_entry"].get())
            globals.materials[new_key]["Density [kg/m3]"] = int(self.entry_dictionary[material]["Density_entry"].get())
            globals.materials[new_key]["Stress_x [MPa]"] = int(self.entry_dictionary[material]["Stress_entry"].get())
            globals.materials[new_key]["Poisson"] = int(self.entry_dictionary[material]["Poisson_entry"].get())

        #Sort materials dictionary
        globals.app.sort_dictionary()

        #Re-create the material_adjustment_panel
        globals.material_adjustment_panel.create_material_adjustment_panel() 

        #Redraw the material stack
        globals.layer_stack_canvas.draw_material_stack()

        #Destroy modify_material_window
        self.modify_material_window.destroy()


    """Saves the values from materials{} to an excel file and places a screenshot of the current stack in the excel file"""
    def export_to_excel(self):
        # print("EXPORT_TO_EXCEL()")

        #Create an filename and a workbook to contain data
        filename = "exported_materials.xlsx"

        #Create main folder if it does not already exist
        main_folder = "exports"
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        #Create sub_folder if it does not already exist
        sub_folder = "excel"
        if not os.path.exists(f"{main_folder}/{sub_folder}"):
            os.makedirs(f"{main_folder}/{sub_folder}")
        

        #Create path for file to be saved in
        file_path = os.path.join(f"{main_folder}/{sub_folder}/{filename}")

        workbook = Workbook()

        # Optionally, rename the default sheet
        sheet = workbook.active
        # sheet.title = ""

        #Create header cells
        sheet["A1"] = "Material"          # Add a new header in column A row 1
        sheet["B1"] = "Thickness"
        sheet["C1"] = "Unit"
        sheet["D1"] = "Indent [nm]"
        sheet["E1"] = "Color"
        sheet["F1"] = "Modulus [GPa]"
        sheet["G1"] = "CTE [ppm/deg]"
        sheet["H1"] = "Density [kg/m3]"
        sheet["I1"] = "Stress_x [MPa]"
        sheet["J1"] = "Poisson"

        #Define a fill_color for cells
        fill_color = PatternFill(start_color="85c4f3", end_color="85c4f3", fill_type="solid")

        #Loop through the desired range of columns and rows to apply the fill_color and set a bold font
        for row in sheet.iter_rows(min_row=1, max_row=1, min_col=1, max_col=10):  # Adjust row/column range as needed
            for cell in row:
                cell.font = Font(bold=True)
                cell.fill = fill_color


        #Define a border style (thin lines for grid)
        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin")
        )

        #Apply the border to a range of cells and center the text in each cell
        for row in sheet.iter_rows(min_row=1, max_row=len(globals.materials)+1, min_col=1, max_col=10):  # Adjust range as needed
            for cell in row:
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="center", vertical="center")

        #Set the height and width values of cells in the excel file
        sheet.column_dimensions['A'].width = 13  #Width of column A
        sheet.column_dimensions['B'].width = 10  
        sheet.column_dimensions['C'].width = 6  
        sheet.column_dimensions['D'].width = 13  
        sheet.column_dimensions['E'].width = 10  
        sheet.column_dimensions['F'].width = 15  
        sheet.column_dimensions['G'].width = 15  
        sheet.column_dimensions['H'].width = 15
        sheet.column_dimensions['I'].width = 15  
        sheet.column_dimensions['J'].width = 10

        # Set row height
        # sheet.row_dimensions[1].height = 20  # Height of row 1 set to 30


        #Loop through materials{} and place values in excel file
        row_counter = 2

        for material in globals.materials:
            sheet.cell(row=row_counter, column=1, value=globals.materials[material]["Name"])
            sheet.cell(row=row_counter, column=2, value=globals.materials[material]["Thickness"])
            sheet.cell(row=row_counter, column=3, value=globals.materials[material]["Unit"])
            sheet.cell(row=row_counter, column=4, value=globals.materials[material]["Indent [nm]"])
            sheet.cell(row=row_counter, column=5, value=globals.materials[material]["Color"])
            sheet.cell(row=row_counter, column=6, value=globals.materials[material]["Modulus [GPa]"])
            sheet.cell(row=row_counter, column=7, value=globals.materials[material]["CTE [ppm/deg]"])
            sheet.cell(row=row_counter, column=8, value=globals.materials[material]["Density [kg/m3]"])
            sheet.cell(row=row_counter, column=9, value=globals.materials[material]["Stress_x [MPa]"])
            sheet.cell(row=row_counter, column=10, value=globals.materials[material]["Poisson"])

            #increment row_counter
            row_counter += 1


        #Find coordinates of canvas on the screen
        canvas_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_rootx()
        canvas_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_rooty()
        canvas_x2 = canvas_x1 + globals.layer_stack_canvas.layer_stack_canvas.winfo_width()
        canvas_y2 = canvas_y1 + globals.layer_stack_canvas.layer_stack_canvas.winfo_height()

        bbox = (canvas_x1, canvas_y1, canvas_x2, canvas_y2)

        #Take a screenshot of the screen where canvas is
        screenshot = ImageGrab.grab(bbox=bbox)
        screenshot.save(f"{main_folder}/{sub_folder}/canvas_screenshot.png", "PNG")

        #Load the image with openpyxl
        canvas_screenshot = Image(f"{main_folder}/{sub_folder}/canvas_screenshot.png")

        #Set the width and height of image placed in excel file
        match globals.option_menu:
            case "Stacked" | "Realistic" | "Stepped":
                canvas_screenshot.width = 750
                canvas_screenshot.height = 350
            case "Stress":
                canvas_screenshot.width = 350
                canvas_screenshot.height = 350

        #Add the image to the excel file
        sheet.add_image(canvas_screenshot, "L1")

        #Save the workbook as excel file
        workbook.save(f"{main_folder}/{sub_folder}/{filename}")