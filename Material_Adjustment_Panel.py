import tkinter
from tkinter import StringVar, messagebox
import customtkinter
import settings #File containing settings
import globals  #File containing global variables


#This class handles the modification of the materials properties
class Material_Adjustment_Panel:
    def __init__(self, window):
        # print("CLASS MATERIAL_ADJUSTMENT_PANEL INIT()")

        #Window where everything is placed
        self.window = window

        #Keeps track of how many rows with widgets has been created in the control panel frame 
        self.row_counter = 0

        self.create_material_adjustment_panel()
        
    """
    -Creates a Frame and material_adjustment_panel in the given window if it does not already exist.
    -If the Frame exists, then the material_adjustment_panel is simply updated corresponding with the materials in globals.materials{} 
    """
    def create_material_adjustment_panel(self):
        # print("CREATE_MATERIAL_ADJUSTMENT_PANEL()")

        #if material_control_frame has NOT been created before, create it
        if not hasattr(self, 'material_adjustment_panel_frame'):
            #Create Frame from the control panel and place it within given window
            self.material_adjustment_panel_frame = customtkinter.CTkScrollableFrame(
                master=self.window,
                width=settings.material_adjustment_panel_width,
                height=settings.material_adjustment_panel_height,
                fg_color=settings.material_adjustment_panel_background_color
            )
            self.material_adjustment_panel_frame.grid(
                row=0,
                column=0,
                padx=(settings.material_adjustment_panel_padding_left, settings.material_adjustment_panel_padding_right),
                pady=(settings.material_adjustment_panel_padding_top, settings.material_adjustment_panel_padding_bottom),
                sticky="nw"
            )
        
        #delete all widgets in frame
        for widget in self.material_adjustment_panel_frame.winfo_children():
            widget.destroy()
            self.row_counter = 0

        #Labels for "material", "thickness"/"Indent" and "add material" button
        material_label = customtkinter.CTkLabel(
            master=self.material_adjustment_panel_frame, 
            text="Material", 
            fg_color=settings.material_adjustment_panel_background_color,
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
            case "Stacked" | "Realistic" | "Stress":
                self.slider_label = customtkinter.CTkLabel(
                    master=self.material_adjustment_panel_frame, 
                    text="Thickness [nm]", 
                    fg_color=settings.material_adjustment_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 20, "bold")
                )
            
            case "Stepped":
                self.slider_label = customtkinter.CTkLabel(
                    master=self.material_adjustment_panel_frame, 
                    text="Indent [nm]", 
                    fg_color=settings.material_adjustment_panel_background_color,
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

        self.row_counter += 1
        
        #If materials dictionary is not empty, go through it and add label, entry and slider for each material in it
        if(len(globals.materials) > 0):

            for material in dict(reversed(globals.materials.items())):
                delete_material_button = customtkinter.CTkButton(
                    master = self.material_adjustment_panel_frame,
                    text="del",
                    fg_color=settings.material_adjustment_panel_button_color,
                    hover_color=settings.material_adjustment_panel_button_hover_color,
                    text_color=settings.material_adjustment_panel_text_color,
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
                    master=self.material_adjustment_panel_frame, 
                    text=material, 
                    fg_color=settings.material_adjustment_panel_background_color,
                    text_color=settings.material_adjustment_panel_text_color
                )
                label.grid(
                    row=self.row_counter, 
                    column=1, 
                    sticky="", 
                    padx=(0,0),
                    pady=(0,0)
                )

                #Bind the label to check for mouse clicks on it
                label.bind("<Button-1>", lambda event, row=self.row_counter, column=1: self.label_click(event, row, column))


                #Create Entry, customize it and add it to dictionary
                entry = customtkinter.CTkEntry(
                    master=self.material_adjustment_panel_frame,
                    textvariable=StringVar(value=str(globals.materials[material]["thickness"])),
                    fg_color = settings.material_adjustment_panel_entry_background_color,
                    text_color="black",
                    width=settings.material_adjustment_panel_entry_width,
                    height=settings.material_adjustment_panel_entry_height,
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
                    master=self.material_adjustment_panel_frame, 
                    width=settings.material_adjustment_panel_slider_width,
                    height=settings.material_adjustment_panel_slider_height,
                    from_=settings.material_adjustment_panel_slider_range_min, 
                    to=settings.material_adjustment_panel_slider_range_max,
                    progress_color=globals.materials[material]["color"],
                    fg_color=settings.material_adjustment_panel_slider_color,
                    button_hover_color=settings.material_adjustment_panel_slider_hover_color,
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
            case "Stacked" | "Realistic" | "Stress":
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
            case "Stacked"|"Realistic" | "Stress":
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


    """Deletes a material from the materials{} dictionary and updates the material_adjustment_panel"""
    def delete_material(self, material):
        #print("DELETE_MATERIAL()")
        
        #check if given material key is in dictionary
        if material in globals.materials:
            #Delete the key
            del globals.materials[material]

            #You might have to Update the "layer" values in globals.materials{}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            #Update the material_adjustment_panel
            self.create_material_adjustment_panel()

            #Re-draw the material stack
            globals.layer_stack_canvas.draw_material_stack()

        
        else:
            messagebox.showerror("ERROR", "Could not find material-key in globals.materials")

            
    
    def label_click(self, event, row, column):
        print("LABEL_CLICK()")

        label = event.widget

        label_name = label.cget("text")

        print(f"{label_name} clicked at row {row}, column {column}")

        #Create text to show user that he can now click another label to move current label to its place
        edit_mode_text = customtkinter.CTkLabel(
            master=globals.main_frame,
            text=f"Click another material\nto place '{label_name}' there",
            text_color="green"
        )
        edit_mode_text.grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0,0),
            pady=(0,0) 
        )

        cancel_button = customtkinter.CTkButton(
            master=globals.main_frame,
            text="Cancel",
            fg_color="white",
            text_color="black",
            hover_color="red"
        )
        cancel_button.grid(
            row=1,
            column=0,
            sticky="e",
            padx=(0,0),
            pady=(0,0)
        )