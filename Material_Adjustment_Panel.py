import tkinter
from tkinter import StringVar
import customtkinter
import settings #File containing settings
import globals  #File containing global variables
import helper_functions


#This class handles the modification of the materials properties
class Material_Adjustment_Panel:
    def __init__(self, window, row_placement:int, column_placement:int):
        # print("CLASS MATERIAL_ADJUSTMENT_PANEL INIT()")

        #Window where everything is placed
        self.program_window = window

        #Row/column placement in main program window
        self.row_placement = row_placement
        self.column_placement = column_placement
        
        self.material_adjustment_panel_frame = self.create_material_adjustment_panel()

        
    def create_material_adjustment_panel(self):
        """
        -Creates a Frame and material_adjustment_panel in the given window if it does not already exist\n
        -If the Frame exists, then the material_adjustment_panel is simply updated corresponding with the materials in globals.materials{} 
        """
        # print("CREATE_MATERIAL_ADJUSTMENT_PANEL()")

        #if material_adjustment_frame has NOT been created before, create it
        if not hasattr(self, 'material_adjustment_panel_frame'):
            #Create Frame from the control panel and place it within given window
            self.material_adjustment_panel_frame = customtkinter.CTkScrollableFrame(
                master=self.program_window,
                fg_color=settings.material_adjustment_panel_background_color
            )
            self.material_adjustment_panel_frame.grid(
                row=self.row_placement,
                column=self.column_placement,
                padx=(settings.material_adjustment_panel_padding_left, settings.material_adjustment_panel_padding_right),
                pady=(settings.material_adjustment_panel_padding_top, settings.material_adjustment_panel_padding_bottom),
                sticky="nswe"
            )

            #Define the row&column layout of the program window
            self.material_adjustment_panel_frame.columnconfigure(0, weight=8, uniform="group1")    #Delete Button
            self.material_adjustment_panel_frame.columnconfigure(1, weight=30, uniform="group1")    #Material name
            self.material_adjustment_panel_frame.columnconfigure(2, weight=17, uniform="group1")     #Entry
            self.material_adjustment_panel_frame.columnconfigure(3, weight=35, uniform="group1")    #Slider
            self.material_adjustment_panel_frame.columnconfigure(4, weight=6, uniform="group1")    #Down Button
            self.material_adjustment_panel_frame.columnconfigure(5, weight=6, uniform="group1")    #Up Button

            self.material_adjustment_panel_frame.rowconfigure((0,1), weight=4, uniform="group1")    

        row_counter = 1
        #Create a different layout based on the "view"
        match globals.current_view:
            case "Stacked" | "Realistic" | "Multi":
                #If checkboxes has been made, disable it
                for material in globals.materials:
                    if(globals.materials[material]["Checkbox_id"] != None):
                        globals.materials[material]["Checkbox_id"].grid_forget()

                #Create label headline for "material"
                if not hasattr(self, 'material_headline'):
                    #Create label headline for "material"
                    self.material_headline = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Material", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color=settings.material_adjustment_panel_text_color,
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, settings.material_adjustment_panel_label_weight)
                    )
                    self.material_headline.grid(
                        row=0,
                        column=1,
                        sticky="n",
                        padx=(0,0),
                        pady=(0,0)
                    )
                #Adjust existing material_headline
                else:
                    self.material_headline.configure(text="Material")
                

                #Create label to display slider functionality and place it
                if not hasattr(self, 'slider_label'):
                    self.slider_label = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Thickness [nm]", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color=settings.material_adjustment_panel_text_color,
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, "bold")
                    )                    
                    self.slider_label.grid(
                        row=0,
                        column=2,
                        columnspan=2,
                        sticky="nsew",
                        padx=(0,0),
                        pady=(0,0)
                    )
                #Adjust existing slider_label
                else:
                    self.slider_label.configure(text="Thickness [nm]")

                
                #If materials dictionary is not empty, go through it and add label, entry and slider for each material in it
                if(len(globals.materials) > 0):
                    
                    for material in dict(reversed(globals.materials.items())): 
                        #Create button to delete material
                        if(globals.materials[material]["Delete_material_button_id"] == None):
                            delete_material_button = customtkinter.CTkButton(
                                master=self.material_adjustment_panel_frame, 
                                width=1,
                                height=1,
                                text="✕", #✕ 🗑
                                font=(settings.text_font, 10, "bold"),
                                fg_color=settings.material_adjustment_panel_delete_button_color,
                                hover_color=settings.material_adjustment_panel_delete_button_hover_color, 
                                text_color="black",
                                command=lambda identifier=material: self.delete_material(identifier)
                            )
                            delete_material_button.grid(
                                row=row_counter,
                                column=0,
                                sticky="",
                                padx=(0,0),
                                pady=(0,0)
                            )
                            globals.materials[material]["Delete_material_button_id"] = delete_material_button
                        #Adjust existing delete_button
                        else:
                            globals.materials[material]["Delete_material_button_id"].configure(
                                command=lambda identifier=material: self.delete_material(identifier),
                                hover_color=settings.material_adjustment_panel_delete_button_hover_color
                            )
                            globals.materials[material]["Delete_material_button_id"].grid(
                                row=row_counter,
                                column=0
                            )

                        #Create label to display material name
                        if(globals.materials[material]["Label_name_id"] == None):
                            label = customtkinter.CTkLabel(
                                master=self.material_adjustment_panel_frame, 
                                textvariable=globals.materials[material]["Name"], 
                                fg_color=settings.material_adjustment_panel_background_color,
                                text_color=globals.materials[material]["Color"].get()
                            )
                            label.grid(
                                row=row_counter, 
                                column=1, 
                                sticky="", 
                                padx=(0,0),
                                pady=(0,0)
                            )
                            #Add label to dictionary
                            globals.materials[material]["Label_name_id"] = label
                        #Adjust existing material name label
                        else:
                            globals.materials[material]["Label_name_id"].configure(
                                textvariable=globals.materials[material]["Name"],
                                text_color=globals.materials[material]["Color"].get()
                            )
                            globals.materials[material]["Label_name_id"].grid(
                                row=row_counter,
                                column=1
                            )

                        #Create Entry
                        if(globals.materials[material]["Entry_id"] == None):
                            entry = customtkinter.CTkEntry(
                                master=self.material_adjustment_panel_frame,
                                textvariable=globals.materials[material]["Thickness [nm]"],
                                fg_color = settings.material_adjustment_panel_entry_background_color,
                                border_color=settings.material_adjustment_panel_entry_border_color,
                                border_width=0.4,
                                text_color=settings.material_adjustment_panel_entry_text_color,
                                justify="center"
                            )
                            entry.grid(
                                row=row_counter, 
                                column=2,
                                sticky="e",
                                padx=(0,0),
                                pady=(0,0)
                            )
                            # entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))
                            globals.materials[material]["Entry_id"] = entry
                        #Adjust existing Entry
                        else:
                            globals.materials[material]["Entry_id"].configure(
                                textvariable=globals.materials[material]["Thickness [nm]"]
                            )
                            globals.materials[material]["Entry_id"].grid(
                                row=row_counter,
                                column=2
                            )


                        #Create Slider
                        if(globals.materials[material]["Slider_id"] == None):
                            slider = customtkinter.CTkSlider(
                                master=self.material_adjustment_panel_frame, 
                                from_=settings.material_adjustment_panel_slider_range_min, 
                                to=settings.material_adjustment_panel_slider_range_max,
                                variable=globals.materials[material]["Thickness [nm]"],
                                number_of_steps=1000,
                                fg_color=settings.material_adjustment_panel_slider_background_color,
                                button_color=settings.material_adjustment_panel_slider_button_color,
                                progress_color=globals.materials[material]["Color"].get(),#settings.material_adjustment_panel_slider_progress_color,
                                button_hover_color=settings.material_adjustment_panel_slider_hover_color,
                                # command=lambda value, identifier=material:self.material_slider_updated(round(value), identifier)
                            )
                            slider.grid(
                                row=row_counter, 
                                column=3,
                                sticky="",
                                padx=(0,0),
                                pady=(0,0)
                            )
                            globals.materials[material]["Slider_id"] = slider 
                            # slider.set(globals.materials[material]["Thickness [nm]"].get())
                        #Adjust existing slider
                        else:
                            globals.materials[material]["Slider_id"].configure(
                                variable=globals.materials[material]["Thickness [nm]"],
                                progress_color=globals.materials[material]["Color"].get()
                                # command=lambda value, identifier=material:self.material_slider_updated(round(value), identifier),
                            )

                            globals.materials[material]["Slider_id"].grid(
                                row=row_counter,
                                column=3
                            )
                            # globals.materials[material]["Slider_id"].set(globals.materials[material]["Thickness [nm]"])


                        #Create move down_button
                        if(globals.materials[material]["Move_down_button_id"] == None):
                            move_down_button = customtkinter.CTkButton(
                                master=self.material_adjustment_panel_frame, 
                                text="⬇", #⬆ ⬇ 🔼 🔽
                                font=(settings.text_font, 15),
                                fg_color=settings.material_adjustment_panel_button_color,
                                hover_color=globals.materials[material]["Color"].get(), 
                                text_color=settings.material_adjustment_panel_button_text_color,
                                command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down)
                            )
                            move_down_button.grid(
                                row=row_counter,
                                column=4,
                                sticky="",
                                padx=(0,0),
                                pady=(0,0)
                            )
                            globals.materials[material]["Move_down_button_id"] = move_down_button
                        #Adjust existing move_down_button
                        else:
                            globals.materials[material]["Move_down_button_id"].configure(
                                command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down),
                                hover_color=globals.materials[material]["Color"].get()
                            )
                            globals.materials[material]["Move_down_button_id"].grid(
                                row=row_counter,
                                column=4
                            )

                        #Create move up_button
                        if(globals.materials[material]["Move_up_button_id"] == None):
                            move_up_button = customtkinter.CTkButton(
                                master=self.material_adjustment_panel_frame, 
                                text="⬆", #⬆ ⬇ 🔼 🔽
                                font=(settings.text_font, 15),
                                fg_color=settings.material_adjustment_panel_button_color,
                                hover_color=globals.materials[material]["Color"].get(), 
                                text_color=settings.material_adjustment_panel_button_text_color,
                                command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down)
                            )
                            move_up_button.grid(
                                row=row_counter,
                                column=5,
                                sticky="",
                                padx=(0,0),
                                pady=(0,0)
                            )
                            globals.materials[material]["Move_up_button_id"] = move_up_button
                        #Adjust existing move_down_button
                        else:
                            globals.materials[material]["Move_up_button_id"].configure(
                                command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down),
                                hover_color=globals.materials[material]["Color"].get()
                            )
                            globals.materials[material]["Move_up_button_id"].grid(
                                row=row_counter,
                                column=5
                            )

                        #Increment row_counter
                        row_counter+=1

            case "Stepped":
                #If checkboxes has been made, disable it
                for material in globals.materials:
                    if(globals.materials[material]["Checkbox_id"] != None):
                        globals.materials[material]["Checkbox_id"].grid_forget()

                #Create label headline for "material"
                if not hasattr(self, 'material_headline'):
                    #Create label headline for "material"
                    self.material_headline = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Material", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color="#55b6ff",
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, "bold")
                    )
                    self.material_headline.grid(
                        row=0,
                        column=1,
                        sticky="n",
                        padx=(0,0),
                        pady=(0,0)
                    )
                #Adjust existing material_headline
                else:
                    self.material_headline.configure(text="Material")
                    

                #Create label to display slider functionality and place it
                if not hasattr(self, 'slider_label'):
                    self.slider_label = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Indent [nm]", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color="#55b6ff",
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, "bold")
                    )                    
                    self.slider_label.grid(
                        row=0,
                        column=2,
                        columnspan=2,
                        sticky="nsew",
                        padx=(0,0),
                        pady=(0,0)
                    )
                #Adjust existing slider_label
                else:
                    self.slider_label.configure(text="Indent [nm]")

                #If materials dictionary is not empty, go through it and add label, entry and slider for each material in it
                if(len(globals.materials) > 0):
                    for material in dict(reversed(globals.materials.items())): 
                        #Create button to delete material
                        if(globals.materials[material]["Delete_material_button_id"] == None):
                            delete_material_button = customtkinter.CTkButton(
                                master=self.material_adjustment_panel_frame, 
                                width=1,
                                height=1,
                                text="✕", #✕ 🗑
                                font=(settings.text_font, 10, "bold"),
                                fg_color=settings.material_adjustment_panel_delete_button_color,
                                hover_color=settings.material_adjustment_panel_delete_button_hover_color, 
                                text_color="black",
                                command=lambda identifier=material: self.delete_material(identifier)
                            )
                            delete_material_button.grid(
                                row=row_counter,
                                column=0,
                                sticky="",
                                padx=(0,0),
                                pady=(0,0)
                            )
                            globals.materials[material]["Delete_material_button_id"] = delete_material_button
                        #Adjust existing delete_button
                        else:
                            globals.materials[material]["Delete_material_button_id"].configure(
                                command=lambda identifier=material: self.delete_material(identifier)
                            )
                            globals.materials[material]["Delete_material_button_id"].grid(
                                row=row_counter,
                                column=0
                            )

                        #Create label to display material name
                        if(globals.materials[material]["Label_name_id"] == None):
                            label = customtkinter.CTkLabel(
                                master=self.material_adjustment_panel_frame, 
                                textvariable=globals.materials[material]["Name"], 
                                fg_color=settings.material_adjustment_panel_background_color,
                                text_color=globals.materials[material]["Color"].get(),
                            )
                            label.grid(
                                row=row_counter, 
                                column=1, 
                                sticky="", 
                                padx=(0,0),
                                pady=(0,0)
                            )
                            #Add label to dictionary
                            globals.materials[material]["Label_name_id"] = label
                        #Adjust existing material name label
                        else:
                            globals.materials[material]["Label_name_id"].configure(
                                textvariable=globals.materials[material]["Name"],
                                text_color=globals.materials[material]["Color"].get()
                            )
                            globals.materials[material]["Label_name_id"].grid(
                                row=row_counter,
                                column=1
                            )

                        #Create Entry
                        if(globals.materials[material]["Entry_id"] == None):
                            entry=customtkinter.CTkEntry(
                                master=self.material_adjustment_panel_frame,
                                textvariable=globals.materials[material]["Indent [nm]"],
                                fg_color = settings.material_adjustment_panel_entry_background_color,
                                border_color=settings.material_adjustment_panel_entry_border_color,
                                border_width=0.4,
                                text_color=settings.material_adjustment_panel_entry_text_color,
                                justify="center"
                            )
                            entry.grid(
                                row=row_counter, 
                                column=2,
                                sticky="e",
                                padx=(0,0),
                                pady=(0,0)
                            )
                            # entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))
                            globals.materials[material]["Entry_id"] = entry
                        #Adjust existing Entry
                        else:
                            globals.materials[material]["Entry_id"].configure(
                                textvariable=globals.materials[material]["Indent [nm]"]
                            )
                            globals.materials[material]["Entry_id"].grid(
                                row=row_counter,
                                column=2
                            )


                        #Create Slider
                        if(globals.materials[material]["Slider_id"] == None):
                            slider = customtkinter.CTkSlider(
                                master=self.material_adjustment_panel_frame, 
                                from_=settings.material_adjustment_panel_slider_range_min, 
                                to=settings.material_adjustment_panel_slider_range_max,
                                variable=globals.materials[material]["Indent [nm]"],
                                number_of_steps=1000,
                                fg_color=settings.material_adjustment_panel_slider_background_color,
                                button_color=settings.material_adjustment_panel_slider_button_color,
                                progress_color=globals.materials[material]["Color"].get(),
                                button_hover_color=settings.material_adjustment_panel_slider_hover_color,
                                # command=lambda value, identifier=material:self.material_slider_updated(round(value), identifier)
                            )
                            slider.grid(
                                row=row_counter, 
                                column=3,
                                sticky="",
                                padx=(0,0),
                                pady=(0,0)
                            )
                            globals.materials[material]["Slider_id"] = slider 
                            # slider.set(globals.materials[material]["Indent [nm]"])
                        #Adjust existing slider
                        else:
                            globals.materials[material]["Slider_id"].configure(
                                # command=lambda value, identifier=material:self.material_slider_updated(round(value), identifier),
                                variable=globals.materials[material]["Indent [nm]"],
                                progress_color=globals.materials[material]["Color"].get()
                            )
                            globals.materials[material]["Slider_id"].grid(
                                row=row_counter,
                                column=3
                            )
                            # globals.materials[material]["Slider_id"].set(globals.materials[material]["Indent [nm]"])

                        
                        #Create buttons to move layer up or down
                        if(len(globals.materials) > 1):
                            #Create down_button
                            if(globals.materials[material]["Move_down_button_id"] == None):
                                move_down_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    text="⬇", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, 15),
                                    fg_color=settings.material_adjustment_panel_button_color,
                                    hover_color=globals.materials[material]["Color"].get(),
                                    text_color=settings.material_adjustment_panel_button_text_color,
                                    command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down)
                                )
                                move_down_button.grid(
                                    row=row_counter,
                                    column=4,
                                    sticky="",
                                    padx=(0,0),
                                    pady=(0,0)
                                )
                                globals.materials[material]["Move_down_button_id"] = move_down_button
                            #Adjust existing move_down_button
                            else:
                                globals.materials[material]["Move_down_button_id"].configure(
                                    command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down),
                                    hover_color=globals.materials[material]["Color"].get()
                                )
                                globals.materials[material]["Move_down_button_id"].grid(
                                    row=row_counter,
                                    column=4
                                )

                            #Create up_button
                            if(globals.materials[material]["Move_up_button_id"] == None):
                                move_up_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    text="⬆", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, 15),
                                    fg_color=settings.material_adjustment_panel_button_color,
                                    hover_color=globals.materials[material]["Color"].get(), 
                                    text_color=settings.material_adjustment_panel_button_text_color,
                                    command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down)
                                )
                                move_up_button.grid(
                                    row=row_counter,
                                    column=5,
                                    sticky="",
                                    padx=(0,0),
                                    pady=(0,0)
                                )
                                globals.materials[material]["Move_up_button_id"] = move_up_button
                            #Adjust existing move_down_button
                            else:
                                globals.materials[material]["Move_up_button_id"].configure(
                                    command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down),
                                    hover_color=globals.materials[material]["Color"].get()
                                )
                                globals.materials[material]["Move_up_button_id"].grid(
                                    row=row_counter,
                                    column=5
                                )

                        #Increment row_counter
                        row_counter+=1


        return self.material_adjustment_panel_frame
          
    
    # def material_entry_updated(self, entry):
    #     """
    #     -Depending on the current view: different material values are changed and the stack and graphs are redrawn
    #     """

    #     print("MATERIAL_ENTRY_UPDATED()")

        #Update different values in self.materials based on option menu value
        # match globals.current_view:
        #     case "Stacked" | "Realistic":
        #         #Find material that corresponds to "entry"
        #         for material in globals.materials:
        #             if(globals.materials[material]["Entry_id"] == entry):
                        # #Find entered value
                        # entered_value = helper_functions.convert_decimal_string_to_float(entry.get())
                        # #Update the thickness value in self.materials
                        # globals.materials[material]["Thickness [nm]"] = entered_value

                        #Update the slider corresponding to the key
                        # globals.materials[material]["Slider_id"].set(entered_value)

            # case "Stepped":
            #     #Find material that corresponds to "entry"
            #     for material in globals.materials:
            #         if(globals.materials[material]["Entry_id"] == entry):
            #             #Find entered value
            #             entered_value = helper_functions.convert_decimal_string_to_float(entry.get())

            #             #Update the thickness value in self.materials
            #             globals.materials[material]["Indent [nm]"] = entered_value

            #             #Update the slider corresponding to the key
            #             globals.materials[material]["Slider_id"].set(entered_value)


            # case "Multi":
            #     #Find material that corresponds to "entry"
            #     for material in globals.materials:
            #         if(globals.materials[material]["Entry_id"] == entry):
            #             #Find entered value
            #             entered_value = helper_functions.convert_decimal_string_to_float(entry.get())

            #             #Update the thickness value in self.materials
            #             globals.materials[material]["Thickness [nm]"] = entered_value

            #             #Update the slider corresponding to the key
            #             globals.materials[material]["Slider_id"].set(entered_value)  

            #             #Re-draw the "z_tip_is" graph
            #             globals.graph_canvas.draw_z_tip_is_graph() 

            #             #Re-draw the "stoney" graph
            #             globals.graph_canvas.draw_stoney_graph()


        #Redraw material stack
        # globals.layer_stack_canvas.draw_material_stack()


    # def material_slider_updated(self, value, identifier): 
    #     """
    #     -Depending on the current view: different material values are changed and the stack and graphs are redrawn
    #     """
      
    #     print("MATERIAL_SLIDER_UPDATED()")

        ################################################################################################
        #Calculate slider range value
        # slider_max_value = 0
        # for material in globals.materials:
        #     #Do not include the first layer
        #     if(globals.materials[material]["Layer"].get() == 1):
        #         continue
        #     slider_max_value += globals.materials[material]["Thickness [nm]"]

        # for material in globals.materials:
        #     globals.materials[material]["Slider_id"].configure(
        #         to=slider_max_value)

        #     globals.materials[material]["Slider_id"].set(globals.materials[material]["Thickness [nm]"])
        ################################################################################################
            
        #Update different values in self.materials based on option value
        # match globals.current_view:
        #     case "Stacked"|"Realistic":
        #         #Update the thickness value in self.materials
        #         globals.materials[identifier]["Thickness [nm]"] = value

        #         #Update the entry corresponding to key
        #         globals.materials[identifier]["Entry_id"].delete(0, tkinter.END)
        #         globals.materials[identifier]["Entry_id"].insert(0, value)
            
        #     case "Stepped":
        #         #Update the "indent" value in self.materials
        #         globals.materials[identifier]["Indent [nm]"] = value

        #         #Update the entry corresponding to key
        #         globals.materials[identifier]["Entry_id"].delete(0, tkinter.END)
        #         globals.materials[identifier]["Entry_id"].insert(0, value)
            
        #     case "Multi":
        #         #Update the thickness value in self.materials
        #         globals.materials[identifier]["Thickness [nm]"] = value

        #         #Update the entry corresponding to key
        #         globals.materials[identifier]["Entry_id"].delete(0, tkinter.END)
        #         globals.materials[identifier]["Entry_id"].insert(0, value)
                
        #         #Re-draw the "z_tip_is" graph
        #         globals.graph_canvas.draw_z_tip_is_graph() 

        #         #Re-draw the "stoney" graph
        #         globals.graph_canvas.draw_stoney_graph()

        # #Redraw material stack
        # globals.layer_stack_canvas.draw_material_stack()


    def delete_material(self, material):
        """
        -Deletes the material given material from globals.materials{}\n
        -Deletes all widgets related to the given material\n
        -Sorts globals.materials{} making the "layer" values correct\n
        -Updates the widgets in material_adjustment_panel_frame\n
        -Redraws the material_stack
        """
        # print("DELETE_MATERIAL()")

        #Destroy all widgets related to material
        if(globals.materials[material]["Label_name_id"] != None):
            globals.materials[material]["Label_name_id"].destroy()
        if(globals.materials[material]["Delete_material_button_id"] != None):
            globals.materials[material]["Delete_material_button_id"].destroy()
        if(globals.materials[material]["Move_down_button_id"] != None):
            globals.materials[material]["Move_down_button_id"].destroy()
        if(globals.materials[material]["Move_up_button_id"] != None):
            globals.materials[material]["Move_up_button_id"].destroy()
        if(globals.materials[material]["Entry_id"] != None):
            globals.materials[material]["Entry_id"].destroy()
        if(globals.materials[material]["Slider_id"] != None):
            globals.materials[material]["Slider_id"].destroy()
        if(globals.materials[material]["Checkbox_id"] != None):
            globals.materials[material]["Checkbox_id"].destroy()

        # if(globals.materials[material]["Rectangle_id"] != None):
        #     globals.materials[material]["Rectangle_id"].destroy()
        # if(globals.materials[material]["Text_id"] != None):
        #     globals.materials[material]["Text_id"].destroy()
        # if(globals.materials[material]["Text_bbox_id"] != None):
        #     globals.materials[material]["Text_bbox_id"].destroy()
        # if(globals.materials[material]["Line_id"] != None):
        #     globals.materials[material]["Line_id"].destroy()
        # if(globals.materials[material]["Indent_text_id"] != None):
        #     globals.materials[material]["Indent_text_id"].destroy()
        # if(globals.materials[material]["Indent_text_bbox_id"] != None):
        #     globals.materials[material]["Indent_text_bbox_id"].destroy()
        # if(globals.materials[material]["Indent_line_id"] != None):
        #     globals.materials[material]["Indent_line_id"].destroy()
        # if(globals.materials[material]["Indent_arrow_pointer_id"] != None):
        #     globals.materials[material]["Indent_arrow_pointer_id"].destroy()

        #delete material from dictionary
        del globals.materials[material]

        #Sort the materials{} dictionary
        globals.app.sort_dictionary()
        
        #Update the material_adjustment_panel
        self.create_material_adjustment_panel()

        #Redraw the material stack
        globals.layer_stack_canvas.draw_material_stack()

        #If graphs has been created, redraw them
        if(globals.graph_canvas != None):
            globals.graph_canvas.draw_z_tip_is_graph()
            globals.graph_canvas.draw_stoney_graph()
        

    def move_material(self, chosen_material, up_or_down):
        """
        -Switches the places between chosen material and the material that is over or under it\n
        -Organizes globals.materials{} so that the order of "layers" is consistent\n
        -Redraws the material stack\n
        -Updates the widgets in material_adjustment_panel_frame
        """
        # print("MOVE_MATERIAL()")

        #Find the needed material names
        above_material = None
        below_material = None
        for material in globals.materials:
            if(globals.materials[material]["Layer"].get() == globals.materials[chosen_material]["Layer"].get() - 1):
                below_material = material

            if(globals.materials[material]["Layer"].get() == globals.materials[chosen_material]["Layer"].get() + 1):
                above_material = material

        
        #Move chosen_material down one layer and below_material up one layer 
        if(up_or_down == "down"):
            if(below_material != None):
                tmp_layer = globals.materials[chosen_material]["Layer"]
                globals.materials[chosen_material]["Layer"] = globals.materials[below_material]["Layer"]
                globals.materials[below_material]["Layer"] = tmp_layer

        #Move chosen_material up one layer and above_material down one layer 
        else:
            if(above_material != None):
                tmp_layer = globals.materials[chosen_material]["Layer"]
                globals.materials[chosen_material]["Layer"] = globals.materials[above_material]["Layer"]
                globals.materials[above_material]["Layer"] = tmp_layer

        #Sort the keys in globals.materials after the "layer" value of each material
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["Layer"].get()))

        #Adjust the widgets in material_adjustment_panel_frame
        self.create_material_adjustment_panel()

        #Redraw the material stack
        globals.layer_stack_canvas.draw_material_stack()

        #If graphs has been created, redraw them
        if(globals.graph_canvas != None):
            globals.graph_canvas.draw_z_tip_is_graph()
            globals.graph_canvas.draw_stoney_graph()
