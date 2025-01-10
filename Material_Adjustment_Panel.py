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

        #if material_adjustment_frame has NOT been created before, create it
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

        #Create a different layout based on the "view"
        match globals.option_menu:
            case "Stacked" | "Realistic":
                #Create label headline for "material"
                material_headline = customtkinter.CTkLabel(
                    master=self.material_adjustment_panel_frame, 
                    text="Material", 
                    fg_color=settings.material_adjustment_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 18, "bold")
                )
                material_headline.grid(
                    row=self.row_counter,
                    column=1,
                    sticky="n",
                    padx=(0,0),
                    pady=(0,0)
                )

                #Create label to display slider functionality and place it
                self.slider_label = customtkinter.CTkLabel(
                    master=self.material_adjustment_panel_frame, 
                    text="Thickness [nm]", 
                    fg_color=settings.material_adjustment_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 18, "bold")
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

                    for material in globals.materials: 
                        #Button to delete material
                        delete_material_button = customtkinter.CTkButton(
                            master=self.material_adjustment_panel_frame, 
                            width=1,
                            height=1,
                            text="✕", #✕ 🗑
                            font=(settings.text_font, -15, "bold"),
                            fg_color="#820000",
                            hover_color="#da0000", #settings.material_control_panel_button_hover_color, 
                            text_color=settings.material_control_panel_text_color,
                            command=lambda button_layer=self.row_counter: self.delete_material(button_layer)
                        )
                        delete_material_button.grid(
                            row=self.row_counter,
                            column=0,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
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
                        #Add label to dictionary
                        globals.materials[material]["Label_name_id"] = label


                        #Create Entry, customize it and add it to dictionary
                        entry = customtkinter.CTkEntry(
                            master=self.material_adjustment_panel_frame,
                            # textvariable=StringVar(value=str(globals.materials[material]["thickness"])),
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
                        globals.materials[material]["Entry_id"] = entry

                        #Create Slider, customize it and add it to dictionary
                        slider = customtkinter.CTkSlider(
                            master=self.material_adjustment_panel_frame, 
                            width=settings.material_adjustment_panel_slider_width,
                            height=settings.material_adjustment_panel_slider_height,
                            from_=settings.material_adjustment_panel_slider_range_min, 
                            to=settings.material_adjustment_panel_slider_range_max,
                            progress_color=globals.materials[material]["Color"],
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
                        globals.materials[material]["Slider_id"] = slider 

                        #Set slider and entry values
                        entry.configure(textvariable=StringVar(value=str(globals.materials[material]["Thickness"])))
                        slider.set(globals.materials[material]["Thickness"])
                            
                        globals.materials[material]["Slider_id"] = slider 

                        #Create buttons to move layer up or down
                        if(len(globals.materials) > 1):
                            if(material.lower() != "substrate"):
                                move_down_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    width=20,
                                    height=1,
                                    text="⬇", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, -15),
                                    fg_color="white", #settings.material_adjustment_panel_button_color,
                                    hover_color=settings.material_adjustment_panel_button_hover_color, 
                                    text_color="blue", #settings.material_adjustment_panel_text_color,
                                    command=lambda material=material, up_or_down="down", button_layer=self.row_counter: self.move_material(material, up_or_down, button_layer)
                                )
                                move_down_button.grid(
                                    row=self.row_counter,
                                    column=4,
                                    sticky="",
                                    padx=(5,0),
                                    pady=(0,0)
                                )

                                move_up_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    width=20,
                                    height=1,
                                    text="⬆", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, -15),
                                    fg_color="white", #settings.material_adjustment_panel_button_color,
                                    hover_color=settings.material_adjustment_panel_button_hover_color, 
                                    text_color="blue",#settings.material_adjustment_panel_text_color,
                                    command=lambda material=material, up_or_down="up", button_layer=self.row_counter: self.move_material(material, up_or_down, button_layer)
                                )
                                move_up_button.grid(
                                    row=self.row_counter,
                                    column=5,
                                    sticky="",
                                    padx=(7,0),
                                    pady=(0,0)
                                )

                        #Increment row_counter
                        self.row_counter+=1

            case "Stepped":
                #Create label headline for "material"
                material_headline = customtkinter.CTkLabel(
                    master=self.material_adjustment_panel_frame, 
                    text="Material", 
                    fg_color=settings.material_adjustment_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 18, "bold")
                )
                material_headline.grid(
                    row=self.row_counter,
                    column=1,
                    sticky="n",
                    padx=(0,0),
                    pady=(0,0)
                )

                #Create label to display slider functionality and place it
                self.slider_label = customtkinter.CTkLabel(
                    master=self.material_adjustment_panel_frame, 
                    text="Indent [nm]", 
                    fg_color=settings.material_adjustment_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 18, "bold")
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

                    for material in globals.materials: 
                        #Button to delete material
                        delete_material_button = customtkinter.CTkButton(
                            master=self.material_adjustment_panel_frame, 
                            width=1,
                            height=1,
                            text="✕", #✕ 🗑
                            font=(settings.text_font, -15, "bold"),
                            fg_color="#820000",
                            hover_color="#da0000", #settings.material_control_panel_button_hover_color, 
                            text_color=settings.material_control_panel_text_color,
                            command=lambda button_layer=self.row_counter: self.delete_material(button_layer)
                        )
                        delete_material_button.grid(
                            row=self.row_counter,
                            column=0,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
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
                        #Add label to dictionary
                        globals.materials[material]["Label_name_id"] = label


                        #Create Entry, customize it and add it to dictionary
                        entry = customtkinter.CTkEntry(
                            master=self.material_adjustment_panel_frame,
                            # textvariable=StringVar(value=str(globals.materials[material]["thickness"])),
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
                        globals.materials[material]["Entry_id"] = entry

                        #Create Slider, customize it and add it to dictionary
                        slider = customtkinter.CTkSlider(
                            master=self.material_adjustment_panel_frame, 
                            width=settings.material_adjustment_panel_slider_width,
                            height=settings.material_adjustment_panel_slider_height,
                            from_=settings.material_adjustment_panel_slider_range_min, 
                            to=settings.material_adjustment_panel_slider_range_max,
                            progress_color=globals.materials[material]["Color"],
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
                        globals.materials[material]["Slider_id"] = slider 

                        #Set slider and entry values
                        entry.configure(textvariable=StringVar(value=str(globals.materials[material]["Indent [nm]"])))
                        slider.set(globals.materials[material]["Indent [nm]"])

                        #Add slider to globals.materials
                        globals.materials[material]["Slider_id"] = slider 

                        #Create buttons to move layer up or down
                        if(len(globals.materials) > 1):
                            if(material.lower() != "substrate"):
                                move_down_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    width=20,
                                    height=1,
                                    text="⬇", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, -15),
                                    fg_color="white", #settings.material_adjustment_panel_button_color,
                                    hover_color=settings.material_adjustment_panel_button_hover_color, 
                                    text_color="blue", #settings.material_adjustment_panel_text_color,
                                    command=lambda material=material, up_or_down="down", button_layer=self.row_counter: self.move_material(material, up_or_down, button_layer)
                                )
                                move_down_button.grid(
                                    row=self.row_counter,
                                    column=4,
                                    sticky="",
                                    padx=(5,0),
                                    pady=(0,0)
                                )

                                move_up_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    width=20,
                                    height=1,
                                    text="⬆", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, -15),
                                    fg_color="white", #settings.material_adjustment_panel_button_color,
                                    hover_color=settings.material_adjustment_panel_button_hover_color, 
                                    text_color="blue",#settings.material_adjustment_panel_text_color,
                                    command=lambda material=material, up_or_down="up", button_layer=self.row_counter: self.move_material(material, up_or_down, button_layer)
                                )
                                move_up_button.grid(
                                    row=self.row_counter,
                                    column=5,
                                    sticky="",
                                    padx=(7,0),
                                    pady=(0,0)
                                )

                        #Increment row_counter
                        self.row_counter+=1
            
            case "Stoney":
                
                #Create label headline for "material"
                material_headline = customtkinter.CTkLabel(
                    master=self.material_adjustment_panel_frame, 
                    text="Material", 
                    fg_color=settings.material_adjustment_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 18, "bold")
                )
                material_headline.grid(
                    row=self.row_counter,
                    column=1,
                    sticky="n",
                    padx=(0,0),
                    pady=(0,0)
                )

                #Create label to display slider functionality and place it
                self.slider_label = customtkinter.CTkLabel(
                    master=self.material_adjustment_panel_frame, 
                    text="Thickness [nm]", 
                    fg_color=settings.material_adjustment_panel_background_color,
                    text_color="#55b6ff",
                    font=(settings.text_font, 18, "bold")
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

                    for material in globals.materials: 
                        #Checkbox to select or deselect material
                        checkbox_value = customtkinter.StringVar(value="off")
                        checkbox = customtkinter.CTkCheckBox(
                            master=self.material_adjustment_panel_frame,
                            width=0,
                            text="",
                            command=lambda material=material, checkbox=checkbox_value: self.checkbox_event(material),
                            variable=checkbox_value,
                            onvalue="on",
                            offvalue="off"
                        )
                        checkbox.grid(
                            row=self.row_counter,
                            column=0,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )
                        globals.materials[material]["Checkbox_id"] = checkbox

                        #if material is substrate, then the checkbox must be "on"
                        if(material.lower() == "substrate"):
                            globals.materials[material]["Checkbox_id"].select()


                        #Material name label
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
                        #Add label to dictionary
                        globals.materials[material]["Label_name_id"] = label


                        #Create Entry, customize it and add it to dictionary
                        entry = customtkinter.CTkEntry(
                            master=self.material_adjustment_panel_frame,
                            # textvariable=StringVar(value=str(globals.materials[material]["thickness"])),
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
                        globals.materials[material]["Entry_id"] = entry

                        #Create Slider, customize it and add it to dictionary
                        slider = customtkinter.CTkSlider(
                            master=self.material_adjustment_panel_frame, 
                            width=settings.material_adjustment_panel_slider_width,
                            height=settings.material_adjustment_panel_slider_height,
                            from_=settings.material_adjustment_panel_slider_range_min, 
                            to=settings.material_adjustment_panel_slider_range_max,
                            progress_color=globals.materials[material]["Color"],
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
                        globals.materials[material]["Slider_id"] = slider 

                        #Set slider and entry values
                        entry.configure(textvariable=StringVar(value=str(globals.materials[material]["Thickness"])))
                        slider.set(globals.materials[material]["Thickness"])

                        #Add slider to globals.materials                            
                        globals.materials[material]["Slider_id"] = slider 


                        #Create buttons to move layer up or down
                        if(len(globals.materials) > 1):
                            if(material.lower() != "substrate"):
                                move_down_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    width=20,
                                    height=1,
                                    text="⬇", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, -15),
                                    fg_color="white", #settings.material_adjustment_panel_button_color,
                                    hover_color=settings.material_adjustment_panel_button_hover_color, 
                                    text_color="blue", #settings.material_adjustment_panel_text_color,
                                    command=lambda material=material, up_or_down="down", button_layer=self.row_counter: self.move_material(material, up_or_down, button_layer)
                                )
                                move_down_button.grid(
                                    row=self.row_counter,
                                    column=4,
                                    sticky="",
                                    padx=(5,0),
                                    pady=(0,0)
                                )

                                move_up_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    width=20,
                                    height=1,
                                    text="⬆", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, -15),
                                    fg_color="white", #settings.material_adjustment_panel_button_color,
                                    hover_color=settings.material_adjustment_panel_button_hover_color, 
                                    text_color="blue",#settings.material_adjustment_panel_text_color,
                                    command=lambda material=material, up_or_down="up", button_layer=self.row_counter: self.move_material(material, up_or_down, button_layer)
                                )
                                move_up_button.grid(
                                    row=self.row_counter,
                                    column=5,
                                    sticky="",
                                    padx=(7,0),
                                    pady=(0,0)
                                )

                        #Increment row_counter
                        self.row_counter+=1


    def checkbox_event(self, chosen_material):
        # print("CHECKBOX_EVENT()")

        #Turn off all materials->checkboxes and mark them as "inactive"
        for material in globals.materials:
            #Mark the chosen material and "substrate" as "active" and turn on their checkboxes
            if((material.lower() == "substrate") or material == chosen_material):
                globals.materials[material]["Checkbox_id"].select()
                globals.materials[material]["Status"] = "active"
            #for every other material: Turn off checkboxes and mark them as "inactive"
            else:
                globals.materials[material]["Checkbox_id"].deselect()
                globals.materials[material]["Status"] = "inactive"
            
        #Redraw the material stack in a limited version
        globals.layer_stack_canvas.draw_material_stack()

        #Create graph with the two given materials
        globals.graph.draw_graph()
            
    
    """Updates the thickness value in globals.materials with the entered value and updates corresponding slider-widget"""
    def material_entry_updated(self, entry):
        # print("MATERIAL_ENTRY_UPDATED()")
    
        # Update different values in self.materials based on option menu value
        match globals.option_menu:
            case "Stacked" | "Realistic":
                #Find material that corresponds to "entry"
                for material in globals.materials:
                    if(globals.materials[material]["Entry_id"] == entry):
                        #Find entered value
                        entered_value = int(entry.get())
                        #Update the thickness value in self.materials
                        globals.materials[material]["Thickness"] = entered_value

                        #Update the slider corresponding to the key
                        globals.materials[material]["Slider_id"].set(entered_value)

            case "Stepped":
                #Find material that corresponds to "entry"
                for material in globals.materials:
                    if(globals.materials[material]["Entry_id"] == entry):
                        #Find entered value
                        entered_value = int(entry.get())
                        #Update the thickness value in self.materials
                        globals.materials[material]["Indent [nm]"] = entered_value

                        #Update the slider corresponding to the key
                        globals.materials[material]["Slider_id"].set(entered_value)

            case "Stoney":
                #Find material that corresponds to "entry"
                for material in globals.materials:
                    if(globals.materials[material]["Entry_id"] == entry):
                        #Find entered value
                        entered_value = int(entry.get())
                        #Update the thickness value in self.materials
                        globals.materials[material]["Thickness"] = entered_value

                        #Update the slider corresponding to the key
                        globals.materials[material]["Slider_id"].set(entered_value)
                
                #Redraw the graph
                globals.graph.draw_graph()
        
        #Redraw material stack
        globals.layer_stack_canvas.draw_material_stack()


    """Updates the thickness value in self.materials with the slider value and updates corresponding entry-widget"""
    def material_slider_updated(self, value, identifier): 
        # print("MATERIAL_SLIDER_UPDATED()")
      
        #Update different values in self.materials based on option value
        match globals.canvas_control_panel.option_menu.get():
            case "Stacked"|"Realistic":
                #Update the thickness value in self.materials
                globals.materials[identifier]["Thickness"] = value

                #Update the entry corresponding to key
                globals.materials[identifier]["Entry_id"].delete(0, tkinter.END)
                globals.materials[identifier]["Entry_id"].insert(0, value)
            
            case "Stepped":
                #Update the "indent" value in self.materials
                globals.materials[identifier]["Indent [nm]"] = value

                #Update the entry corresponding to key
                globals.materials[identifier]["Entry_id"].delete(0, tkinter.END)
                globals.materials[identifier]["Entry_id"].insert(0, value)
            
            case "Stoney":
                #Update the thickness value in self.materials
                globals.materials[identifier]["Thickness"] = value

                #Update the entry corresponding to key
                globals.materials[identifier]["Entry_id"].delete(0, tkinter.END)
                globals.materials[identifier]["Entry_id"].insert(0, value)

                #Redraw the graph
                globals.graph.draw_graph()

        #Redraw material stack
        globals.layer_stack_canvas.draw_material_stack()


    """
    -Deletes the material that has the same layer value as 'button_layer' from the materials{} dictionary
    -Decrements the materials with a layer value above 'button_layer'
    -Reorders the materials{} dictionary
    -Re-renders the material adjustment panel
    -Redraws the material_stack
    """
    def delete_material(self, button_layer):
        #print("DELETE_MATERIAL()")

        #Go through all materials
        for material in globals.materials:
            #Delete the material at the same row as button layer
            if(globals.materials[material]["Layer"] == button_layer):
                delete_material = material

            #Decrement the layer value of materials above button_layer/deleted material
            if(globals.materials[material]["Layer"] > button_layer):
                globals.materials[material]["Layer"] -= 1

        del globals.materials[delete_material]

        #Sort the materials{} dictionary
        globals.app.sort_dictionary()
        
        #Update the material_adjustment_panel
        self.create_material_adjustment_panel()

        #Re-draw the material stack
        globals.layer_stack_canvas.draw_material_stack()
        

        

        # #check if given material key is in dictionary
        # if chosen_material in globals.materials:
        #     #The materials with a "layer" value less than chosen material must be decremented to keep materials{} organized by "layer"
        #     for material in globals.materials:
        #         if(globals.materials[material]["Layer"] > globals.materials[chosen_material]["Layer"]):
        #             globals.materials[material]["Layer"] -= 1
            
        #     #Delete the key
        #     del globals.materials[chosen_material]

        #     #Update the material_adjustment_panel
        #     self.create_material_adjustment_panel()

        #     #Re-draw the material stack
        #     globals.layer_stack_canvas.draw_material_stack()
        
        # else:
        #     messagebox.showerror("ERROR", "Could not find material-key in globals.materials")


    """
    -Switches the places between chosen material and whatever material is over or under it
    -Organizes materials{} so that the order of "layers" is consistent
    -Redraws the material stack
    -Switches the grid places of the modified materials Label_name:id, Entry_id and Slider_id in the material_adjustment_panel
    """
    def move_material(self, chosen_material, up_or_down, button_layer):
        # print("MOVE_MATERIAL()")

        #Find the needed material names
        chosen_material = None
        above_material = None
        below_material = None
        for material in globals.materials:
            if(globals.materials[material]["Layer"] == button_layer):
                chosen_material = material

            if(globals.materials[material]["Layer"] == button_layer-1):
                above_material = material
            
            if(globals.materials[material]["Layer"] == button_layer+1):
                below_material = material

        #Move chosen_material up one layer and above_material down one layer 
        if(up_or_down == "up"):
            #Skip this function if the user tries to move the material to row zero, which does not exist
            if(button_layer == 1):
                return

            #Switch places of the chosen material and the material above chosen material
            tmp_layer = globals.materials[chosen_material]["Layer"]
            globals.materials[chosen_material]["Layer"] = globals.materials[above_material]["Layer"]
            globals.materials[above_material]["Layer"] = tmp_layer

            #Sort the dictionary
            globals.app.sort_dictionary()

            #Redraw the material stack
            globals.layer_stack_canvas.draw_material_stack()
                    
            #Move the chosen_material label, entry_id and slider_id
            globals.materials[chosen_material]["Slider_id"].grid(row=globals.materials[chosen_material]["Layer"])
            globals.materials[chosen_material]["Entry_id"].grid(row=globals.materials[chosen_material]["Layer"])
            globals.materials[chosen_material]["Label_name_id"].grid(row=globals.materials[chosen_material]["Layer"])

            #Move the replaced materials label, entry_id and slider_id
            globals.materials[above_material]["Slider_id"].grid(row=globals.materials[above_material]["Layer"])
            globals.materials[above_material]["Entry_id"].grid(row=globals.materials[above_material]["Layer"])
            globals.materials[above_material]["Label_name_id"].grid(row=globals.materials[above_material]["Layer"])


        #Move chosen_material down one layer and below_material up one layer 
        else:
            #Switch places of the chosen material and the material above chosen material
            tmp_layer = globals.materials[chosen_material]["Layer"]
            globals.materials[chosen_material]["Layer"] = globals.materials[below_material]["Layer"]
            globals.materials[below_material]["Layer"] = tmp_layer

            #Sort the dictionary
            globals.app.sort_dictionary()

            #Redraw the material stack
            globals.layer_stack_canvas.draw_material_stack()
                    
            #Move the chosen_material label, entry_id and slider_id to its new place in the material_adjustment_panel
            globals.materials[chosen_material]["Slider_id"].grid(row=globals.materials[chosen_material]["Layer"])
            globals.materials[chosen_material]["Entry_id"].grid(row=globals.materials[chosen_material]["Layer"])
            globals.materials[chosen_material]["Label_name_id"].grid(row=globals.materials[chosen_material]["Layer"])

            #Move the below_materials label, entry_id and slider_id to its new place in the material_adjustment_panel
            globals.materials[below_material]["Slider_id"].grid(row=globals.materials[below_material]["Layer"])
            globals.materials[below_material]["Entry_id"].grid(row=globals.materials[below_material]["Layer"])
            globals.materials[below_material]["Label_name_id"].grid(row=globals.materials[below_material]["Layer"])



































# def create_material_adjustment_panel(self):
#         # print("CREATE_MATERIAL_ADJUSTMENT_PANEL()")

#         #if material_adjustment_frame has NOT been created before, create it
#         if not hasattr(self, 'material_adjustment_panel_frame'):
#             #Create Frame from the control panel and place it within given window
#             self.material_adjustment_panel_frame = customtkinter.CTkScrollableFrame(
#                 master=self.window,
#                 width=settings.material_adjustment_panel_width,
#                 height=settings.material_adjustment_panel_height,
#                 fg_color=settings.material_adjustment_panel_background_color
#             )
#             self.material_adjustment_panel_frame.grid(
#                 row=0,
#                 column=0,
#                 padx=(settings.material_adjustment_panel_padding_left, settings.material_adjustment_panel_padding_right),
#                 pady=(settings.material_adjustment_panel_padding_top, settings.material_adjustment_panel_padding_bottom),
#                 sticky="nw"
#             )
        
#         #delete all widgets in frame
#         for widget in self.material_adjustment_panel_frame.winfo_children():
#             widget.destroy()
#             self.row_counter = 0

#         #Create label headline for "material"
#         material_headline = customtkinter.CTkLabel(
#             master=self.material_adjustment_panel_frame, 
#             text="Material", 
#             fg_color=settings.material_adjustment_panel_background_color,
#             text_color="#55b6ff",
#             font=(settings.text_font, 20, "bold")
#         )
#         material_headline.grid(
#             row=self.row_counter,
#             column=1,
#             sticky="n",
#             padx=(0,0),
#             pady=(0,0)
#         )

#         #Create label to display slider functionality and place it
#         match globals.option_menu:
#             case "Stacked" | "Realistic" | "Stoney":
#                 self.slider_label = customtkinter.CTkLabel(
#                     master=self.material_adjustment_panel_frame, 
#                     text="Thickness [nm]", 
#                     fg_color=settings.material_adjustment_panel_background_color,
#                     text_color="#55b6ff",
#                     font=(settings.text_font, 20, "bold")
#                 )
            
#             case "Stepped":
#                 self.slider_label = customtkinter.CTkLabel(
#                     master=self.material_adjustment_panel_frame, 
#                     text="Indent [nm]", 
#                     fg_color=settings.material_adjustment_panel_background_color,
#                     text_color="#55b6ff",
#                     font=(settings.text_font, 20, "bold")
#                 )
            
#         self.slider_label.grid(
#             row=self.row_counter,
#             column=3,
#             sticky="n",
#             padx=(0,0),
#             pady=(0,0)
#         )

#         self.row_counter += 1
        
#         #If materials dictionary is not empty, go through it and add label, entry and slider for each material in it
#         if(len(globals.materials) > 0):

#             for material in globals.materials: 
#                 #Button to delete material
#                 delete_material_button = customtkinter.CTkButton(
#                     master=self.material_adjustment_panel_frame, 
#                     width=1,
#                     height=1,
#                     text="✕", #✕ 🗑
#                     font=(settings.text_font, -15, "bold"),
#                     fg_color="#820000",
#                     hover_color="#da0000", #settings.material_control_panel_button_hover_color, 
#                     text_color=settings.material_control_panel_text_color,
#                     command=lambda button_layer=self.row_counter: self.delete_material(button_layer)
#                 )
#                 delete_material_button.grid(
#                     row=self.row_counter,
#                     column=0,
#                     sticky="",
#                     padx=(0,0),
#                     pady=(0,0)
#                 )

#                 label = customtkinter.CTkLabel(
#                     master=self.material_adjustment_panel_frame, 
#                     text=material, 
#                     fg_color=settings.material_adjustment_panel_background_color,
#                     text_color=settings.material_adjustment_panel_text_color
#                 )
#                 label.grid(
#                     row=self.row_counter, 
#                     column=1, 
#                     sticky="", 
#                     padx=(0,0),
#                     pady=(0,0)
#                 )
#                 #Add label to dictionary
#                 globals.materials[material]["Label_name_id"] = label


#                 #Create Entry, customize it and add it to dictionary
#                 entry = customtkinter.CTkEntry(
#                     master=self.material_adjustment_panel_frame,
#                     # textvariable=StringVar(value=str(globals.materials[material]["thickness"])),
#                     fg_color = settings.material_adjustment_panel_entry_background_color,
#                     text_color="black",
#                     width=settings.material_adjustment_panel_entry_width,
#                     height=settings.material_adjustment_panel_entry_height,
#                     justify="center"
#                 )
#                 entry.grid(
#                     row=self.row_counter, 
#                     column=2,
#                     sticky="e",
#                     padx=(0,0),
#                     pady=(0,0)
#                 )
#                 entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))
#                 globals.materials[material]["Entry_id"] = entry

#                 #Create Slider, customize it and add it to dictionary
#                 slider = customtkinter.CTkSlider(
#                     master=self.material_adjustment_panel_frame, 
#                     width=settings.material_adjustment_panel_slider_width,
#                     height=settings.material_adjustment_panel_slider_height,
#                     from_=settings.material_adjustment_panel_slider_range_min, 
#                     to=settings.material_adjustment_panel_slider_range_max,
#                     progress_color=globals.materials[material]["Color"],
#                     fg_color=settings.material_adjustment_panel_slider_color,
#                     button_hover_color=settings.material_adjustment_panel_slider_hover_color,
#                     command=lambda value, identifier=material:self.material_slider_updated(round(value), identifier)
#                 )
#                 slider.grid(
#                     row=self.row_counter, 
#                     column=3,
#                     sticky="e",
#                     padx=(0,0),
#                     pady=(0,0)
#                 )
#                 globals.materials[material]["Slider_id"] = slider 

#                 #Set slider and entry values, based on the option_manu value
#                 match globals.option_menu:
#                     case "Stacked" | "Realistic" | "Stoney":
#                         entry.configure(textvariable=StringVar(value=str(globals.materials[material]["Thickness"])))
#                         slider.set(globals.materials[material]["Thickness"])
                    
#                     case "Stepped":
#                         entry.configure(textvariable=StringVar(value=str(globals.materials[material]["Indent [nm]"])))
#                         slider.set(globals.materials[material]["Indent [nm]"])


#                 #Disable slider and Entry if specified by the excel-file
#                 if(globals.materials[material]["Status"] == "inactive"):
#                     globals.materials[material]["Slider_id"].configure(state="disabled") #Disable slider
#                     globals.materials[material]["Entry_id"].delete(0, tkinter.END)     #Disable Entry
#                     globals.materials[material]["Entry_id"].insert(0, "inactive")      #Disable Entry
#                     globals.materials[material]["Entry_id"].configure(state="disabled")#Disable Entry
#                 globals.materials[material]["Slider_id"] = slider 

#                 #Create buttons to move layer up or down
#                 if(len(globals.materials) > 1):
#                     if(material.lower() != "substrate"):
#                         move_down_button = customtkinter.CTkButton(
#                             master=self.material_adjustment_panel_frame, 
#                             width=20,
#                             height=1,
#                             text="⬇", #⬆ ⬇ 🔼 🔽
#                             font=(settings.text_font, -15),
#                             fg_color="white", #settings.material_adjustment_panel_button_color,
#                             hover_color=settings.material_adjustment_panel_button_hover_color, 
#                             text_color="blue", #settings.material_adjustment_panel_text_color,
#                             command=lambda material=material, up_or_down="down", button_layer=self.row_counter: self.move_material(material, up_or_down, button_layer)
#                         )
#                         move_down_button.grid(
#                             row=self.row_counter,
#                             column=4,
#                             sticky="",
#                             padx=(5,0),
#                             pady=(0,0)
#                         )
#                         move_up_button = customtkinter.CTkButton(
#                             master=self.material_adjustment_panel_frame, 
#                             width=20,
#                             height=1,
#                             text="⬆", #⬆ ⬇ 🔼 🔽
#                             font=(settings.text_font, -15),
#                             fg_color="white", #settings.material_adjustment_panel_button_color,
#                             hover_color=settings.material_adjustment_panel_button_hover_color, 
#                             text_color="blue",#settings.material_adjustment_panel_text_color,
#                             command=lambda material=material, up_or_down="up", button_layer=self.row_counter: self.move_material(material, up_or_down, button_layer)

#                         )
#                         move_up_button.grid(
#                             row=self.row_counter,
#                             column=5,
#                             sticky="",
#                             padx=(7,0),
#                             pady=(0,0)
#                         )


#                 #Increment row_counter
#                 self.row_counter+=1

    