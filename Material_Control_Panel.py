import tkinter
from tkinter import messagebox
import customtkinter
import settings #File containing settings
import globals  #File containing global variables


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
            width=100,
            height=25,
            text="Add material", 
            fg_color=settings.material_control_panel_button_color,
            hover_color=settings.material_control_panel_button_hover_color,
            text_color=settings.material_control_panel_text_color,
            command=self.add_material
        )
        add_material_button.grid(
            row=0,
            column=0,
            sticky="",
            padx=(5,0),
            pady=(5,0)
        )

        #Create button to "delete material" and place it
        delete_material_button = customtkinter.CTkButton(
            master=self.material_control_panel_frame, 
            width=100,
            height=25,
            text="Delete material", 
            fg_color=settings.material_control_panel_button_color,
            hover_color=settings.material_control_panel_button_hover_color,
            text_color=settings.material_control_panel_text_color,
            command=self.delete_material

        )
        delete_material_button.grid(
            row=1,
            column=0,
            sticky="",
            padx=(5,0),
            pady=(5,0)
        )

        #Create button to modify the order of materials, and place the button
        modify_order_button = customtkinter.CTkButton(
            master=self.material_control_panel_frame, 
            width=100,
            height=25,
            text="Modify order", 
            fg_color=settings.material_control_panel_button_color,
            hover_color=settings.material_control_panel_button_hover_color,
            text_color=settings.material_control_panel_text_color,
            command=self.choose_material
        )
        modify_order_button.grid(
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
            text="export to excel", 
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


        #E value
        self.E_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="E: Youngs Modulus [GPa]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.E_value_label.grid(
            row=5, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.E_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.E_value_entry.grid(
            row=5, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )


        #"rho" value
        self.rho_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Rho: density [kg/m3]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.rho_value_label.grid(
            row=6, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.rho_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.rho_value_entry.grid(
            row=6, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )

        
        #"sigma" value
        self.sigma_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Sigma: in-plane stress [MPa]", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.sigma_value_label.grid(
            row=7, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.sigma_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.sigma_value_entry.grid(
            row=7, 
            column=1,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )
            

        #'nu' value
        self.nu_value_label = customtkinter.CTkLabel(
            master=self.add_material_window, 
            text="Nu: Poisson", 
            text_color=settings.add_material_window_text_color,
            fg_color=settings.add_material_window_background_color,
        )
        self.nu_value_label.grid(
            row=8, 
            column=0, 
            sticky="e", 
            padx=(0,0),
            pady=(0,0)
        )

        self.nu_value_entry = customtkinter.CTkEntry(
            master=self.add_material_window,
            fg_color = "white",
            text_color="black",
            width=70,
            justify="center"
        )
        self.nu_value_entry.grid(
            row=8, 
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
            command=self.validate_inputs
        )
        confirm_button.grid(
            row=9,
            column=2,
            sticky="n",
            padx=(0,0),
            pady=(0,0)
        )


    """
    Checks if the inputs from the entries are valid.
    Calls 'add_material_to_dictionary' if inputs are valid
    """
    def validate_inputs(self):
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
        if(self.E_value_entry.get() != ""):
            try:
                E_value = self.E_value_entry.get() 
                E_value = int(E_value)
            except ValueError:
                messagebox.showerror("ERROR", "'E' value has to be an integer", parent=self.add_material_window)
                return
        

        #If "rho" value is entered, check if it is integer
        if(self.rho_value_entry.get() != ""):
            try:
                rho_value = self.rho_value_entry.get() 
                rho_value = int(rho_value)
            except ValueError:
                messagebox.showerror("ERROR", "'rho' value has to be an integer", parent=self.add_material_window)
                return


        #If 'sigma' value is entered, check if it is integer 
        if(self.sigma_value_entry.get() != ""):
            try:
                sigma_value = self.sigma_value_entry.get() 
                sigma_value = int(sigma_value)
            except ValueError:
                messagebox.showerror("ERROR", "'sigma' value has to be an integer", parent=self.add_material_window)
                return


        #If 'nu' value is entered, check if it is integer
        if(self.nu_value_entry.get() != ""):
            try:
                nu_value = self.nu_value_entry.get() 
                nu_value = int(nu_value)
            except ValueError:
                messagebox.showerror("ERROR", "'nu' value has to be an integer", parent=self.add_material_window)
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

        #E VALUE
        if(self.E_value_entry.get() == ""):
            E_value = 0
        else:
            E_value = int(self.E_value_entry.get())

        #RHO VALUE
        if(self.rho_value_entry.get() == ""):
            rho_value = 0
        else:
            rho_value = int(self.rho_value_entry.get())
        
        #SIGMA VALUE
        if(self.sigma_value_entry.get() == ""):
            sigma_value = 0
        else:
            sigma_value = int(self.sigma_value_entry.get())
        
        #NU VALUE
        if(self.nu_value_entry.get() == ""):
            nu_value = 0
        else:
            nu_value = int(self.nu_value_entry.get())

        #Loop through all materials and increment "layer" with 1, assuring that the new material is placed on top of the stack
        for material in globals.materials:
            globals.materials[material]["layer"] += 1

        #Add values to dictionary
        info = {
            "name": str(self.material_name_entry.get()),
            "layer": 1,
            "thickness": material_thickness,
            "unit": "nm",
            "indent": material_indent,
            "color": str(self.material_color_entry.get()),
            "status": "active",
            "E": E_value,
            "rho": rho_value,
            "sigma": sigma_value,
            "nu": nu_value,
            "rectangle_id": None,
            "text_id": None,
            "text_bbox_id" : None,
            "line_id": None,
            "entry_id": None,
            "slider_id": None,
            "indent_text_id": None,
            "indent_text_bbox_id": None,
            "indent_line_id": None,
            "indent_arrow_pointer_id": None
        }
        
        #Put "info" dictionary into self.materials dictionary
        globals.materials[self.material_name_entry.get()] = info

        #Sort the materials dictionary after the "layer" value
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["layer"]))


    """
    -Deletes all widgets from material_adjustment_panel and material_control_panel
    -Renders materials along with delete buttons in material_adjustment_panel_frame
    -Renders a 'cancel_edit' button in material_control_panel_frame
    """
    def delete_material(self):
        print("DELETE_MATERIAL()")

        #Delete all the widgets in the "material_adjustment_panel"
        for widget in globals.material_adjustment_panel.material_adjustment_panel_frame.winfo_children():
            widget.destroy()
        
        #Delete all the widgets in the "material_control_panel"
        for widget in globals.material_control_panel.material_control_panel_frame.winfo_children():
            widget.destroy()
        
        #Render material labels to delete and delete buttons in material_adjustment_frame
        row_counter = 0
        for material in globals.materials:
            #Create a "choose material" button and place it, but skip "substrate"
            delete_button = customtkinter.CTkButton(
                master=globals.material_adjustment_panel.material_adjustment_panel_frame, 
                text="Delete", 
                width=50,
                height=10,
                hover_color=globals.materials[material]["color"],
                command=lambda delete_material=material: self.delete_material_from_dictionary(delete_material)
            )
            delete_button.grid(
                row=row_counter,
                column=0,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )

            #Create a "layer" label for current material
            layer_label = customtkinter.CTkLabel(
                master=globals.material_adjustment_panel.material_adjustment_panel_frame,
                text=globals.materials[material]["layer"]
            )
            layer_label.grid(
                row=row_counter,
                column=1,
                sticky="",
                padx=(10,0),
                pady=(0,0)
            )

            #Create a "layer" label for current material
            material_label = customtkinter.CTkLabel(
                master=globals.material_adjustment_panel.material_adjustment_panel_frame,
                text=material
            )
            material_label.grid(
                row=row_counter,
                column=1,
                sticky="",
                padx=(10,0),
                pady=(0,0)
            )

            row_counter += 1
        
        #Render a "cancel edit mode" button, and place it
        cancel_edit_mode_button = customtkinter.CTkButton(
            master=globals.material_control_panel.material_control_panel_frame, 
            text="Done deleting", 
            width=70,
            height=10,
            command=self.finish_edit
        )
        cancel_edit_mode_button.grid(
            row=0,
            column=0,
            sticky="",
            padx=(140,0),
            pady=(25,0)
        )
        

    """Deletes given material from the materials{} dictionary, reorders the materials{} dictionary and redraws the material_stack"""
    def delete_material_from_dictionary(self, chosen_material):
        #print("DELETE_MATERIAL_FROM_DICTIONARY()")

        #check if given material key is in dictionary
        if chosen_material in globals.materials:
            #The materials with a "layer" value less than chosen material must be decremented to keep materials{} organized by "layer"
            for material in globals.materials:
                if(globals.materials[material]["layer"] > globals.materials[chosen_material]["layer"]):
                    globals.materials[material]["layer"] -= 1
            
            #Delete the key
            del globals.materials[chosen_material]

            #Render the "delete material" frame again with less materials
            self.delete_material()

            #Update the material_adjustment_panel
            # self.create_material_adjustment_panel()

            #Re-draw the material stack
            globals.layer_stack_canvas.draw_material_stack()

        
        else:
            messagebox.showerror("ERROR", "Could not find material-key in globals.materials")


    """
    -Deletes all widgets from material_adjustment_panel, material_control_panel and canvas_control_panel
    -Renders materials along with a 'select' button on the side
    -Renders a 'cancel edit' button
    """
    def choose_material(self):
        # print("CHOOSE_MATERIAL()")

        #Delete all the widgets in the "material_adjustment_panel"
        for widget in globals.material_adjustment_panel.material_adjustment_panel_frame.winfo_children():
            widget.destroy()
        
        #Delete all the widgets in the "canvas_control_panel"
        for widget in globals.canvas_control_panel.canvas_control_panel_frame.winfo_children():
            widget.destroy()

        #Delete all the widgets in the "material_control_panel"
        for widget in globals.material_control_panel.material_control_panel_frame.winfo_children():
            widget.destroy()   


        #Render all materials with a checkbox on the left side
        row_counter = 0
        for material in globals.materials:
            #Create a "choose material" button and place it
            choose_button = customtkinter.CTkButton(
                master=globals.material_adjustment_panel.material_adjustment_panel_frame, 
                text="Select", 
                width=90,
                height=10,
                hover_color=globals.materials[material]["color"],
                command=lambda chosen_material=material: self.move_material(chosen_material)
            )
            choose_button.grid(
                row=row_counter,
                column=0,
                sticky="",
                padx=(0,0),
                pady=(0,0)
            )

            #Create a "layer" label for current material
            layer_label = customtkinter.CTkLabel(
                master=globals.material_adjustment_panel.material_adjustment_panel_frame,
                text=globals.materials[material]["layer"]
            )
            layer_label.grid(
                row=row_counter,
                column=1,
                sticky="",
                padx=(10,0),
                pady=(0,0)
            )

            #Create a label for current material
            material_label = customtkinter.CTkLabel(
                master=globals.material_adjustment_panel.material_adjustment_panel_frame,
                text=material,
            )
            material_label.grid(
                row=row_counter,
                column=2,
                sticky="",
                padx=(10,0),
                pady=(0,0)
            )

            row_counter += 1

        #Render an explanation on how the editing works
        explanation_label = customtkinter.CTkLabel(
            master=globals.material_adjustment_panel.material_adjustment_panel_frame,
            text="Please select the material \nyou want to move",
            fg_color="#36556c"
        )
        explanation_label.grid(
            row=0,
            column=4,
            sticky="e",
            padx=(30,0),
            pady=(0,0)
        )


        #Render a "cancel edit mode" button, and place it
        cancel_edit_mode_button = customtkinter.CTkButton(
            master=globals.material_control_panel.material_control_panel_frame, 
            text="Done editing", 
            width=70,
            height=10,
            command=self.finish_edit
        )
        cancel_edit_mode_button.grid(
            row=0,
            column=0,
            sticky="",
            padx=(140,0),
            pady=(25,0)
        )

        # #Render a "done" button and place it
        # finish_edit_button = customtkinter.CTkButton(
        #     master=globals.material_control_panel.material_control_panel_frame, 
        #     text="Confirm", 
        #     width=70,
        #     height=10,
        #     command=self.finish_edit
        # )
        # finish_edit_button.grid(
        #     row=0,
        #     column=1,
        #     sticky="",
        #     padx=(5,0),
        #     pady=(5,0)
        # )


    """
    -Deletes all widgets in material_adjustment_panel
    -Renders all materials along with a 'move_here' button
    """
    def move_material(self, chosen_material):
        # print("MOVE_MATERIAL()")
        
        #Delete all the widgets in the "material_adjustment_panel"
        for widget in globals.material_adjustment_panel.material_adjustment_panel_frame.winfo_children():
            widget.destroy()

        #Render all materials with a button on the left side
        row_counter = 0
        for material in globals.materials:

            #Render "deselect" button for chosen_material
            if(material == chosen_material):
                deselect_button = customtkinter.CTkButton(
                    master=globals.material_adjustment_panel.material_adjustment_panel_frame, 
                    text="Deselect", 
                    width=70,
                    height=10,
                    fg_color="#d80000",
                    hover_color="#ff0000",
                    # command=lambda selected_layer=material, chosen_material=chosen_material: self.edit_layers(chosen_material, selected_layer)
                    command=self.choose_material
                )
                deselect_button.grid(
                    row=row_counter,
                    column=0,
                    sticky="",
                    padx=(0,0),
                    pady=(0,0)
                )
            #Render "choose material" button for the other materials
            else:
                #Create a "choose material" button and place it, but skip "substrate"
                if(material.lower() != "substrate"):
                    move_here_button = customtkinter.CTkButton(
                        master=globals.material_adjustment_panel.material_adjustment_panel_frame, 
                        text=f"Place in row: ",#{globals.materials[material]['layer']}", 
                        width=70,
                        height=10,
                        hover_color="#26aa00",
                        command=lambda selected_layer=material, chosen_material=chosen_material: self.edit_layers(chosen_material, selected_layer)
                    )
                    move_here_button.grid(
                        row=row_counter,
                        column=0,
                        sticky="",
                        padx=(0,0),
                        pady=(0,0)
                    )

            #Create a "layer" label for current material
            layer_label = customtkinter.CTkLabel(
                master=globals.material_adjustment_panel.material_adjustment_panel_frame,
                text=globals.materials[material]["layer"],
            )
            layer_label.grid(
                row=row_counter,
                column=1,
                sticky="w",
                padx=(10,0),
                pady=(0,0)
            )

            #Create a label for current material
            material_label = customtkinter.CTkLabel(
                master=globals.material_adjustment_panel.material_adjustment_panel_frame,
                text=material,
            )
            material_label.grid(
                row=row_counter,
                column=2,
                sticky="",
                padx=(10,0),
                pady=(0,0)
            )

            row_counter += 1
        
        #Render an explanation on how the editing works
        explanation_label = customtkinter.CTkLabel(
            master=globals.material_adjustment_panel.material_adjustment_panel_frame,
            text="Please select the row\nto place it in",
            fg_color="#36556c"
        )
        explanation_label.grid(
            row=0,
            column=4,
            sticky="e",
            padx=(30,0),
            pady=(0,0)
        )


    """
    -Organizes materials{} so that the order of "layers" is consistent
    -Redraws the material stack
    -Renders the 'choose_material' version of the material_adjustment_frame again
    """
    def edit_layers(self, first_material, second_material):
        # print("EDIT_LAYERS()")

        #save first material original "layer" value
        first_material_orig_layer = globals.materials[first_material]["layer"] 

        #Save second_material original "layer" value
        second_material_orig_layer = globals.materials[second_material]["layer"] 

        if(first_material_orig_layer > second_material_orig_layer):
            #Change the layer value in chosen material to the selected layer
            globals.materials[first_material]["layer"] = globals.materials[second_material]["layer"]

            #For everything that is lower than first material layer, excluding the first_material
            for material in globals.materials:
                if(material != first_material):
                    if(globals.materials[material]["layer"] < first_material_orig_layer):
                        if(globals.materials[material]["layer"] >= second_material_orig_layer):
                            globals.materials[material]["layer"] += 1
        
        #first_material layer is less than second_material layer
        else:
            #Change the layer value in chosen material to the selected layer
            globals.materials[first_material]["layer"] = globals.materials[second_material]["layer"]

            #For everything that is higher than first material layer, excluding the first_material
            for material in globals.materials:
                if(material != first_material):
                    if(globals.materials[material]["layer"] > first_material_orig_layer):
                        if(globals.materials[material]["layer"] <= second_material_orig_layer):
                            globals.materials[material]["layer"] -= 1


        #Order globals.materials{} in order of "layer"
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["layer"]))

        #Redraw the material stack
        globals.layer_stack_canvas.draw_material_stack()

        #Render the first "select material" edit mode version
        self.choose_material()


    """
    -Deletes all widgets from material_adjustment_panel, material_control_panel and canvas_control_panel
    -Rebuilds the original verions of material_adjustment_panel, material_control_panel and canvas_control_panel
    """
    def finish_edit(self):
        # print("FINISH_EDIT()")
        
        #Delete widgets in material_adjustment_panel_frame
        for widget in globals.material_adjustment_panel.material_adjustment_panel_frame.winfo_children():
            widget.destroy()  

        #Delete widgets in material_control_panel_frame
        for widget in globals.material_control_panel.material_control_panel_frame.winfo_children():
            widget.destroy()

        #Delete widgets in canvas_control_panel_frame
        for widget in globals.canvas_control_panel.canvas_control_panel_frame.winfo_children():
            widget.destroy()

        #Restore the material_adjustment_panel
        globals.material_adjustment_panel.create_material_adjustment_panel()

        #Restore the material_control_panel
        globals.material_control_panel_frame = globals.material_control_panel.create_material_control_panel()

        #Restore the canvas_control_panel
        globals.canvas_control_panel.create_canvas_control_panel()


    def export_to_excel(self):
        print("EXPORT_TO_EXCEL()")

        #Create an excel file with a specific name
        #Put the following headlines in to excel file: Material 	Thickness	Unit	Indent	Color	E	rho	sigma	nu
        #For each row in the excel file, put the corresponding values from materials{} in to excel file
        #Export the current stack to svg file
        #Find a way to place the stack.svg file in to the excel file