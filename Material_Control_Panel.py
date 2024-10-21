import tkinter
from tkinter import StringVar, messagebox
import customtkinter
import settings #File containing settings
import globals  #File containing global variables


#This class handles the modification of the materials properties
class Material_Control_Panel:
    def __init__(self, window):
        # print("CLASS MATERIAL_CONTROL_PANEL INIT()")

        #Window where everything is placed
        self.window = window

        #Keeps track of how many rows with widgets has been created in the control panel frame 
        self.row_counter = 0

        self.create_material_control_panel()

    """
    -Creates a Frame and material_control_panel in the given window if it does not already exist.
    -If the Frame exists, then the material_control_panel is simply updated corresponding with the materials in globals.materials{} 
    """
    def create_material_control_panel(self):
        # print("CREATE_MATERIAL_CONTROL_PANEL()")

        #if material_control_frame has NOT been created before, create it
        if not hasattr(self, 'material_control_panel_frame'):
            #Create Frame from the control panel and place it within given window
            self.material_control_panel_frame = customtkinter.CTkScrollableFrame(
                master=self.window,
                width=settings.material_control_panel_width,
                height=settings.material_control_panel_height,
                fg_color=settings.material_control_panel_background_color
            )
            self.material_control_panel_frame.grid(
                row=0,
                column=0,
                padx=(settings.material_control_panel_padding_left, settings.material_control_panel_padding_right),
                pady=(settings.material_control_panel_padding_top, settings.material_control_panel_padding_bottom),
                sticky="nw"
            )
        
        #delete all widgets in frame
        for widget in self.material_control_panel_frame.winfo_children():
            widget.destroy()
            self.row_counter = 0

        #Labels for "material", "thickness"/"Indent" and "add material" button
        material_label = customtkinter.CTkLabel(
            master=self.material_control_panel_frame, 
            text="Material", 
            fg_color=settings.material_control_panel_background_color,
            text_color="#55b6ff",
            font=(settings.text_font, 20, "bold")
        )
        material_label.grid(
            row=self.row_counter,
            column=1,
            sticky="n",
            padx=(0,0),
            pady=(0,0)
        )

        #Create label to display slider functionality
        match globals.option_menu:
            case "Stacked" | "Realistic":
                self.slider_label = customtkinter.CTkLabel(
                    master=self.material_control_panel_frame, 
                    text="Thickness [nm]", 
                    fg_color=settings.material_control_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 20, "bold")
                )
            
            case "Stepped":
                self.slider_label = customtkinter.CTkLabel(
                    master=self.material_control_panel_frame, 
                    text="Indent [nm]", 
                    fg_color=settings.material_control_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 20, "bold")
                )
            

        self.slider_label.grid(
            row=self.row_counter,
            column=3,
            sticky="n",
            padx=(0,0),
            pady=(0,0)
        )

        #Button to add material
        add_material_button = customtkinter.CTkButton(
            master = self.window,
            width=40,
            height=40,
            text="+",
            bg_color=settings.material_control_panel_background_color,
            hover_color=settings.material_control_panel_button_hover_color,
            text_color=settings.material_control_panel_text_color,
            font=(settings.text_font, 30),
            command=self.add_material
        )

        add_material_button.grid(
            row=0,
            column=0,
            sticky="se",
            padx=(0,20),
            pady=(0,10)
        )


        self.row_counter += 1
        
        #If materials dictionary is not empty, go through it and add label, entry and slider for each material in it
        if(len(globals.materials) > 0):

            for material in dict(reversed(globals.materials.items())):
                delete_material_button = customtkinter.CTkButton(
                    master = self.material_control_panel_frame,
                    text="del",
                    fg_color=settings.material_control_panel_button_color,
                    hover_color=settings.material_control_panel_button_hover_color,
                    text_color=settings.material_control_panel_text_color,
                    width=20,
                    height=10,
                    command=lambda material=material: self.delete_material(material)
                )

                delete_material_button.grid(
                    row=self.row_counter,
                    column=0
                    # sticky="w",
                    # padx=(5,0),
                    # pady=(5,0)
                )
                label = customtkinter.CTkLabel(
                    master=self.material_control_panel_frame, 
                    text=material, 
                    fg_color=settings.material_control_panel_background_color,
                    text_color=settings.material_control_panel_text_color
                )
                label.grid(
                    row=self.row_counter, 
                    column=1, 
                    sticky="", 
                    padx=(0,0),
                    pady=(0,0)
                )

                #Create Entry, customize it and add it to dictionary
                entry = customtkinter.CTkEntry(
                    master=self.material_control_panel_frame,
                    textvariable=StringVar(value=str(globals.materials[material]["thickness"])),
                    fg_color = settings.material_control_panel_entry_background_color,
                    text_color="black",
                    width=settings.material_control_panel_entry_width,
                    height=settings.material_control_panel_entry_height,
                    justify="center"
                )
                entry.grid(
                    row=self.row_counter, 
                    column=2,
                    sticky="e",
                    padx=(0,0),
                    pady=(0,0)
                )
                entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))
                globals.materials[material]["entry_id"] = entry

                #Create Slider, customize it and add it to dictionary
                slider = customtkinter.CTkSlider(
                    master=self.material_control_panel_frame, 
                    width=settings.material_control_panel_slider_width,
                    height=settings.material_control_panel_slider_height,
                    from_=settings.material_control_panel_slider_range_min, 
                    to=settings.material_control_panel_slider_range_max,
                    progress_color=globals.materials[material]["color"],
                    fg_color=settings.material_control_panel_slider_color,
                    button_hover_color=settings.material_control_panel_slider_hover_color,
                    command=lambda value, identifier=material:self.material_slider_updated(round(value), identifier)
                )
                slider.grid(
                    row=self.row_counter, 
                    column=3,
                    sticky="e",
                    padx=(0,0),
                    pady=(0,0)
                )
                slider.set(globals.materials[material]["thickness"])
                globals.materials[material]["slider_id"] = slider 

                #Disable slider and Entry if specified by the excel-file
                if(globals.materials[material]["status"] == "disabled"):
                    globals.materials[material]["slider_id"].configure(state="disabled") #Disable slider
                    globals.materials[material]["entry_id"].delete(0, tkinter.END)     #Disable Entry
                    globals.materials[material]["entry_id"].insert(0, "Disabled")      #Disable Entry
                    globals.materials[material]["entry_id"].configure(state="disabled")#Disable Entry
                globals.materials[material]["slider_id"] = slider 

                #Increment row_counter
                self.row_counter+=1

    
    """Updates the thickness value in globals.materials with the entered value and updates corresponding slider-widget"""
    def material_entry_updated(self, entry):
        # print("MATERIAL_ENTRY_UPDATED()")
    
        # Update different values in self.materials based on option menu value
        match globals.option_menu:
            case "Stacked"|"Realistic":
                #Find material that corresponds to "entry"
                for material in globals.materials:
                    if(globals.materials[material]["entry_id"] == entry):
                        #Find entered value
                        entered_value = int(entry.get())
                        #Update the thickness value in self.materials
                        globals.materials[material]["thickness"] = entered_value

                        #Update the slider corresponding to the key
                        globals.materials[material]["slider_id"].set(entered_value)

            case "Stepped":
                #Find material that corresponds to "entry"
                for material in globals.materials:
                    if(globals.materials[material]["entry_id"] == entry):
                        #Find entered value
                        entered_value = int(entry.get())
                        #Update the thickness value in self.materials
                        globals.materials[material]["indent"] = entered_value

                        #Update the slider corresponding to the key
                        globals.materials[material]["slider_id"].set(entered_value)
        
        
        #Redraw material stack
        globals.layer_stack_canvas.draw_material_stack()


    """Updates the thickness value in self.materials with the slider value and updates corresponding entry-widget"""
    def material_slider_updated(self, value, identifier): 
        # print("MATERIAL_SLIDER_UPDATED()")
      
        #Update different values in self.materials based on option value
        match globals.canvas_control_panel.option_menu.get():
            case "Stacked"|"Realistic":
                #Update the thickness value in self.materials
                globals.materials[identifier]["thickness"] = value

                #Update the entry corresponding to key
                globals.materials[identifier]["entry_id"].delete(0, tkinter.END)
                globals.materials[identifier]["entry_id"].insert(0, value)
            
            case "Stepped":
                #Update the "indent" value in self.materials
                globals.materials[identifier]["indent"] = value

                #Update the entry corresponding to key
                globals.materials[identifier]["entry_id"].delete(0, tkinter.END)
                globals.materials[identifier]["entry_id"].insert(0, value)

        #Redraw material stack
        globals.layer_stack_canvas.draw_material_stack()


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


    """Deletes a material from the materials{} dictionary and updates the material_control_panel"""
    def delete_material(self, material):
        #print("DELETE_MATERIAL()")
        
        #check if given material key is in dictionary
        if material in globals.materials:
            #Delete the key
            del globals.materials[material]

            #You might have to Update the "layer" values in globals.materials{}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            #Update the material_control_panel
            self.create_material_control_panel()

            #Re-draw the material stack
            globals.layer_stack_canvas.draw_material_stack()

        
        else:
            messagebox.showerror("ERROR", "Could not find material-key in globals.materials")

            
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
        
        #Update material_control_panel
        self.create_material_control_panel()

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
            material_thickness = 0
        else:
            material_thickness = int(self.material_thickness_entry.get())

        #INDENT
        if(self.material_indent_entry.get() == ""):
            material_indent = 0
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


        #Add values to dictionary
        info = {
            "name": str(self.material_name_entry.get()),
            "layer": int(len(globals.materials)),
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
