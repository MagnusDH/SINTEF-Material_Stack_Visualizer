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
        
        #Remove all widgets from material_adjustment_panel_frame
        for widget in self.material_adjustment_panel_frame.winfo_children():
            widget.grid_remove()


        #Reset the grid in material_adjustment_panel_frame
        num_columns = self.material_adjustment_panel_frame.grid_size()[0]
        num_rows = self.material_adjustment_panel_frame.grid_size()[1]
        for i in range(num_columns):
            self.material_adjustment_panel_frame.columnconfigure(i, weight=0, minsize=0, uniform="reset")
        for i in range(num_rows):
            self.material_adjustment_panel_frame.rowconfigure(i, weight=0, minsize=0, uniform="reset")


        #Create a different layout based on the "view"
        row_counter = 1
        match globals.current_view.get():
            case "Stacked" | "Realistic":
                #Define the row&column layout of the program window
                self.material_adjustment_panel_frame.columnconfigure(0, weight=5, uniform="group1")    #Delete Button
                self.material_adjustment_panel_frame.columnconfigure(1, weight=20, uniform="group1")    #Material name
                self.material_adjustment_panel_frame.columnconfigure(2, weight=20, uniform="group1")     #Entry
                self.material_adjustment_panel_frame.columnconfigure(3, weight=35, uniform="group1")    #Slider
                self.material_adjustment_panel_frame.columnconfigure(4, weight=6, uniform="group1")    #Down Button
                self.material_adjustment_panel_frame.columnconfigure(5, weight=6, uniform="group1")    #Up Button

                self.material_adjustment_panel_frame.rowconfigure((0,1), weight=4, uniform="group1")  

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
                #Adjust existing material_headline
                else:
                    self.material_headline.configure(text="Material")
                #Place headline on the grid
                self.material_headline.grid(
                    row=0,
                    column=1,
                    sticky="n",
                    padx=(0,0),
                    pady=(0,0),
                )
                

                #CREATE SLIDER LABEL
                if not hasattr(self, 'slider_headline'):
                    self.slider_headline = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Thickness [nm]", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color=settings.material_adjustment_panel_text_color,
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, "bold")
                    )                    
                #Adjust existing slider_headline
                else:
                    self.slider_headline.configure(text="Thickness [nm]")
                #Place slider_headline on the grid
                self.slider_headline.grid(
                        row=0,
                        column=3,
                        columnspan=2,
                        sticky="nsew",
                        padx=(0,0),
                        pady=(0,0)
                    )

                
                #If materials dictionary is not empty, go through it and add label, entry and slider for each material in it
                if(len(globals.materials) > 0):
                    for material in dict(reversed(globals.materials.items())): 
                        
                        #DELETE BUTTON
                        if("Delete_material_button_id" not in globals.materials[material]):                  
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
                            #Add button to dictionary
                            globals.materials[material]["Delete_material_button_id"] = delete_material_button
                        #Adjust existing delete_button
                        else:
                            globals.materials[material]["Delete_material_button_id"].configure(
                                command=lambda identifier=material: self.delete_material(identifier),
                                hover_color=settings.material_adjustment_panel_delete_button_hover_color
                            )
                        #Place delete button on grid
                        globals.materials[material]["Delete_material_button_id"].grid(
                            row=row_counter,
                            column=0,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #MATERIAL NAME LABEL
                        if("Label_name_id" not in globals.materials[material]):                  

                            label = customtkinter.CTkLabel(
                                master=self.material_adjustment_panel_frame, 
                                textvariable=globals.materials[material]["Name"], 
                                fg_color=settings.material_adjustment_panel_background_color,
                                text_color=globals.materials[material]["Color"].get()
                            )
                            #Add label to dictionary
                            globals.materials[material]["Label_name_id"] = label
                        #Adjust existing material name label
                        else:
                            globals.materials[material]["Label_name_id"].configure(
                                textvariable=globals.materials[material]["Name"],
                                text_color=globals.materials[material]["Color"].get()
                            )
                        #place material name label on the grid
                        globals.materials[material]["Label_name_id"].grid(
                            row=row_counter, 
                            column=1, 
                            sticky="", 
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #THICNKESS ENTRY
                        if("Entry_id" not in globals.materials[material]):                  
                            entry = customtkinter.CTkEntry(
                                master=self.material_adjustment_panel_frame,
                                textvariable=globals.materials[material]["Thickness [nm]"],
                                fg_color = settings.material_adjustment_panel_entry_background_color,
                                border_color=settings.material_adjustment_panel_entry_border_color,
                                border_width=1,
                                text_color=settings.material_adjustment_panel_entry_text_color,
                                justify="center"
                            )
                            #Add entry to dictionary
                            globals.materials[material]["Entry_id"] = entry
                        #Adjust existing Entry
                        else:
                            globals.materials[material]["Entry_id"].configure(
                                textvariable=globals.materials[material]["Thickness [nm]"]
                            )
                        globals.materials[material]["Entry_id"].grid(
                            row=row_counter, 
                            column=2,
                            sticky="e",
                            padx=(0,0),
                            pady=(0,1)
                        )


                        #THICKNESS SLIDER
                        if("Slider_id" not in globals.materials[material]):                  
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
                            )
                            #Add slider to dictionary
                            globals.materials[material]["Slider_id"] = slider 
                        #Adjust existing slider
                        else:
                            globals.materials[material]["Slider_id"].configure(
                                variable=globals.materials[material]["Thickness [nm]"],
                                progress_color=globals.materials[material]["Color"].get()
                            )
                        #Place slider on the grid
                        globals.materials[material]["Slider_id"].grid(
                            row=row_counter, 
                            column=3,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #MOVE DOWN BUTTON
                        if("Move_down_button_id" not in globals.materials[material]):                  
                            move_down_button = customtkinter.CTkButton(
                                master=self.material_adjustment_panel_frame, 
                                text="⬇", #⬆ ⬇ 🔼 🔽
                                font=(settings.text_font, 15),
                                fg_color=settings.material_adjustment_panel_button_color,
                                hover_color=globals.materials[material]["Color"].get(), 
                                text_color=settings.material_adjustment_panel_button_text_color,
                                command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down)
                            )
                            #Add button to dictionary
                            globals.materials[material]["Move_down_button_id"] = move_down_button
                        #Adjust existing move_down_button
                        else:
                            globals.materials[material]["Move_down_button_id"].configure(
                                command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down),
                                hover_color=globals.materials[material]["Color"].get()
                            )
                        #Place button on grid
                        globals.materials[material]["Move_down_button_id"].grid(
                            row=row_counter,
                            column=4,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #MOVE UP BUTTON
                        if("Move_up_button_id" not in globals.materials[material]):                  
                            move_up_button = customtkinter.CTkButton(
                                master=self.material_adjustment_panel_frame, 
                                text="⬆", #⬆ ⬇ 🔼 🔽
                                font=(settings.text_font, 15),
                                fg_color=settings.material_adjustment_panel_button_color,
                                hover_color=globals.materials[material]["Color"].get(), 
                                text_color=settings.material_adjustment_panel_button_text_color,
                                command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down)
                            )
                            #Add button do dictionary
                            globals.materials[material]["Move_up_button_id"] = move_up_button
                        #Adjust existing move_down_button
                        else:
                            globals.materials[material]["Move_up_button_id"].configure(
                                command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down),
                                hover_color=globals.materials[material]["Color"].get()
                            )
                        #Place button on grid
                        globals.materials[material]["Move_up_button_id"].grid(
                            row=row_counter,
                            column=5,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )

                        #Increment row_counter
                        row_counter+=1

            case "Stepped":
                #Define the row&column layout of the program window
                self.material_adjustment_panel_frame.columnconfigure(0, weight=5, uniform="group1")    #Delete Button
                self.material_adjustment_panel_frame.columnconfigure(1, weight=20, uniform="group1")    #Material name
                self.material_adjustment_panel_frame.columnconfigure(2, weight=20, uniform="group1")     #Entry
                self.material_adjustment_panel_frame.columnconfigure(3, weight=35, uniform="group1")    #Slider
                self.material_adjustment_panel_frame.columnconfigure(4, weight=6, uniform="group1")    #Down Button
                self.material_adjustment_panel_frame.columnconfigure(5, weight=6, uniform="group1")    #Up Button

                self.material_adjustment_panel_frame.rowconfigure((0,1), weight=4, uniform="group1")  

                #MATERIAL HEADLINE
                if not hasattr(self, 'material_headline'):
                    #Create label headline for "material"
                    self.material_headline = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Material", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color="#55b6ff",
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, "bold")
                    )
                #Adjust existing material_headline
                else:
                    self.material_headline.configure(text="Material")
                #Place headline on grid
                self.material_headline.grid(
                    row=0,
                    column=1,
                    sticky="n",
                    padx=(0,0),
                    pady=(0,0)
                )
                    

                #SLIDER HEADLINE
                if not hasattr(self, 'slider_headline'):
                    self.slider_headline = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Indent [nm]", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color="#55b6ff",
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, "bold")
                    )                    
                #Adjust existing slider_headline
                else:
                    self.slider_headline.configure(text="Indent [nm]")
                #Place slider headline on grid
                self.slider_headline.grid(
                    row=0,
                    column=2,
                    columnspan=2,
                    sticky="nsew",
                    padx=(0,0),
                    pady=(0,0)
                )


                #If materials dictionary is not empty, go through it and add label, entry and slider for each material in it
                if(len(globals.materials) > 0):
                    for material in dict(reversed(globals.materials.items())): 
                        #DELETE MATERIAL BUTTON
                        if("Delete_material_button_id" not in globals.materials[material]):                  
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
                            #Add button to dictionary
                            globals.materials[material]["Delete_material_button_id"] = delete_material_button
                        #Adjust existing delete_button
                        else:
                            globals.materials[material]["Delete_material_button_id"].configure(
                                command=lambda identifier=material: self.delete_material(identifier)
                            )
                        #Place button on grid
                        globals.materials[material]["Delete_material_button_id"].grid(
                            row=row_counter,
                            column=0,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #MATERIAL NAME LABEL
                        if("Label_name_id" not in globals.materials[material]):                  
                            label = customtkinter.CTkLabel(
                                master=self.material_adjustment_panel_frame, 
                                textvariable=globals.materials[material]["Name"], 
                                fg_color=settings.material_adjustment_panel_background_color,
                                text_color=globals.materials[material]["Color"].get(),
                            )
                            #Add label to dictionary
                            globals.materials[material]["Label_name_id"] = label
                        #Adjust existing material name label
                        else:
                            globals.materials[material]["Label_name_id"].configure(
                                textvariable=globals.materials[material]["Name"],
                                text_color=globals.materials[material]["Color"].get()
                            )
                        #Place label on grid
                        globals.materials[material]["Label_name_id"].grid(
                            row=row_counter, 
                            column=1, 
                            sticky="", 
                            padx=(0,0),
                            pady=(0,0)
                        )

                        
                        #THCIKNESS ENTRY
                        if("Entry_id" not in globals.materials[material]):                  
                            entry=customtkinter.CTkEntry(
                                master=self.material_adjustment_panel_frame,
                                textvariable=globals.materials[material]["Indent [nm]"],
                                fg_color = settings.material_adjustment_panel_entry_background_color,
                                border_color=settings.material_adjustment_panel_entry_border_color,
                                border_width=1,
                                text_color=settings.material_adjustment_panel_entry_text_color,
                                justify="center"
                            )
                            
                            globals.materials[material]["Entry_id"] = entry
                        #Adjust existing Entry
                        else:
                            globals.materials[material]["Entry_id"].configure(
                                textvariable=globals.materials[material]["Indent [nm]"]
                            )
                        #Place entry oin grid
                        globals.materials[material]["Entry_id"].grid(
                            row=row_counter, 
                            column=2,
                            sticky="e",
                            padx=(0,0),
                            pady=(0,1)
                        )


                        #THICKNESS SLIDER
                        if("Slider_id" not in globals.materials[material]):                  
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
                            )
                            #Add slider to dictionary
                            globals.materials[material]["Slider_id"] = slider 
                        #Adjust existing slider
                        else:
                            globals.materials[material]["Slider_id"].configure(
                                variable=globals.materials[material]["Indent [nm]"],
                                progress_color=globals.materials[material]["Color"].get()
                            )
                        #Place slider on grid
                        globals.materials[material]["Slider_id"].grid(
                            row=row_counter, 
                            column=3,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )

                        
                        #Move up and down buttons
                        if(len(globals.materials) > 1):

                            #DOWN BUTTON
                            if("Move_down_button_id" not in globals.materials[material]):                  
                                move_down_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    text="⬇", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, 15),
                                    fg_color=settings.material_adjustment_panel_button_color,
                                    hover_color=globals.materials[material]["Color"].get(),
                                    text_color=settings.material_adjustment_panel_button_text_color,
                                    command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down)
                                )
                                #Add button to dictionary
                                globals.materials[material]["Move_down_button_id"] = move_down_button
                            #Adjust existing move_down_button
                            else:
                                globals.materials[material]["Move_down_button_id"].configure(
                                    command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down),
                                    hover_color=globals.materials[material]["Color"].get()
                                )
                            #Place button on grid
                            globals.materials[material]["Move_down_button_id"].grid(
                                row=row_counter,
                                column=4,
                                sticky="",
                                padx=(0,0),
                                pady=(0,0)
                            )


                            #UP BUTTON
                            if("Move_up_button_id" not in globals.materials[material]):                  
                                move_up_button = customtkinter.CTkButton(
                                    master=self.material_adjustment_panel_frame, 
                                    text="⬆", #⬆ ⬇ 🔼 🔽
                                    font=(settings.text_font, 15),
                                    fg_color=settings.material_adjustment_panel_button_color,
                                    hover_color=globals.materials[material]["Color"].get(), 
                                    text_color=settings.material_adjustment_panel_button_text_color,
                                    command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down)
                                )
                                #Add button to dictionary
                                globals.materials[material]["Move_up_button_id"] = move_up_button
                            #Adjust existing move_down_button
                            else:
                                globals.materials[material]["Move_up_button_id"].configure(
                                    command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down),
                                    hover_color=globals.materials[material]["Color"].get()
                                )
                            #Place button on grid
                            globals.materials[material]["Move_up_button_id"].grid(
                                row=row_counter,
                                column=5,
                                sticky="",
                                padx=(0,0),
                                pady=(0,0)
                            )

                        #Increment row_counter
                        row_counter+=1

            case "Multi":
                #Define the row&column layout of the program window
                self.material_adjustment_panel_frame.columnconfigure(0, weight=5, uniform="group1")    #Delete Button
                self.material_adjustment_panel_frame.columnconfigure(1, weight=20, uniform="group1")    #Material name
                self.material_adjustment_panel_frame.columnconfigure(2, weight=15, uniform="group1")     #Piezo checkbox
                self.material_adjustment_panel_frame.columnconfigure(3, weight=20, uniform="group1")     #Entry
                self.material_adjustment_panel_frame.columnconfigure(4, weight=30, uniform="group1")    #Slider
                self.material_adjustment_panel_frame.columnconfigure(5, weight=6, uniform="group1")    #Down Button
                self.material_adjustment_panel_frame.columnconfigure(6, weight=6, uniform="group1")    #Up Button

                self.material_adjustment_panel_frame.rowconfigure((0,1), weight=4, uniform="group1")  


                #MATERIAL HEADLINE
                if not hasattr(self, 'material_headline'):
                    #Create label headline for "material"
                    self.material_headline = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Material", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color=settings.material_adjustment_panel_text_color,
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, settings.material_adjustment_panel_label_weight)
                    )
                #Adjust existing material_headline
                else:
                    self.material_headline.configure(text="Material")
                #Place headline on the grid
                self.material_headline.grid(
                    row=0,
                    column=1,
                    sticky="n",
                    padx=(0,0),
                    pady=(0,0),
                )


                #PIEZO HEADLINE
                if not hasattr(self, 'piezo_headline'):
                    #Create label headline for "material"
                    self.piezo_headline = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Piezo?", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color=settings.material_adjustment_panel_text_color,
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, settings.material_adjustment_panel_label_weight)
                    )
                #Adjust existing material_headline
                # else:
                    # self.piezo_headline.configure(text="Piezo?")
                #Place headline on the grid
                self.piezo_headline.grid(
                    row=0,
                    column=2,
                    sticky="n",
                    padx=(0,0),
                    pady=(0,0),
                )
                

                #SLIDER HEADLINE
                if not hasattr(self, 'slider_headline'):
                    self.slider_headline = customtkinter.CTkLabel(
                        master=self.material_adjustment_panel_frame, 
                        text="Thickness [nm]", 
                        fg_color=settings.material_adjustment_panel_background_color,
                        text_color=settings.material_adjustment_panel_text_color,
                        font=(settings.text_font, settings.material_adjustment_panel_label_size, settings.material_adjustment_panel_label_weight)
                    )                    
                #Adjust existing slider_headline
                else:
                    self.slider_headline.configure(text="Thickness [nm]")
                #Place slider_headline on the grid
                self.slider_headline.grid(
                        row=0,
                        column=3,
                        columnspan=2,
                        sticky="nsew",
                        padx=(0,0),
                        pady=(0,0)
                    )

                
                #If materials dictionary is not empty, go through it and add label, entry and slider for each material in it
                if(len(globals.materials) > 0):
                    for material in dict(reversed(globals.materials.items())): 
                        
                        #DELETE BUTTON                        
                        if("Delete_material_button_id" not in globals.materials[material]):                  
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
                            #Add button to dictionary
                            globals.materials[material]["Delete_material_button_id"] = delete_material_button
                        #Adjust existing delete_button
                        else:
                            globals.materials[material]["Delete_material_button_id"].configure(
                                command=lambda identifier=material: self.delete_material(identifier),
                                hover_color=settings.material_adjustment_panel_delete_button_hover_color
                            )
                        #Place delete button on grid
                        globals.materials[material]["Delete_material_button_id"].grid(
                            row=row_counter,
                            column=0,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #MATERIAL NAME LABEL
                        if("Label_name_id" not in globals.materials[material]):                  
                            label = customtkinter.CTkLabel(
                                master=self.material_adjustment_panel_frame, 
                                textvariable=globals.materials[material]["Name"], 
                                fg_color=settings.material_adjustment_panel_background_color,
                                text_color=globals.materials[material]["Color"].get()
                            )
                            #Add label to dictionary
                            globals.materials[material]["Label_name_id"] = label
                        #Adjust existing material name label
                        else:
                            globals.materials[material]["Label_name_id"].configure(
                                textvariable=globals.materials[material]["Name"],
                                text_color=globals.materials[material]["Color"].get()
                            )
                        #place material name label on the grid
                        globals.materials[material]["Label_name_id"].grid(
                            row=row_counter, 
                            column=1, 
                            sticky="", 
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #CREATE PIEZO CHECKBOX
                        if("Piezo_checkbox_id" not in globals.materials[material]):                  
                            piezo_checkbox = customtkinter.CTkCheckBox(
                                master=self.material_adjustment_panel_frame,
                                text="",
                                onvalue="on",
                                offvalue="off",
                                fg_color = settings.material_adjustment_panel_entry_background_color,
                                border_color=settings.material_adjustment_panel_entry_border_color,
                                border_width=1,
                                text_color=settings.material_adjustment_panel_entry_text_color,
                                command=lambda identifier="piezo_material_updated": globals.app.update_widgets(identifier)
                            )
                            #Add checkbox to dictionary                            
                            globals.materials[material]["Piezo_checkbox_id"] = piezo_checkbox
                        #Adjust existing piezo_checkbox
                        else:
                            pass
                        #Place checkbox on grid
                        globals.materials[material]["Piezo_checkbox_id"].grid(
                            row=row_counter, 
                            column=2,
                            sticky="nsew",
                            padx=(15,0),
                            pady=(0,1)
                        )


                        #THICNKESS ENTRY
                        if("Entry_id" not in globals.materials[material]):                  
                            entry = customtkinter.CTkEntry(
                                master=self.material_adjustment_panel_frame,
                                textvariable=globals.materials[material]["Thickness [nm]"],
                                fg_color = settings.material_adjustment_panel_entry_background_color,
                                border_color=settings.material_adjustment_panel_entry_border_color,
                                border_width=1,
                                text_color=settings.material_adjustment_panel_entry_text_color,
                                justify="center"
                            )
                            #Add entry to dictionary
                            globals.materials[material]["Entry_id"] = entry
                        #Adjust existing Entry
                        else:
                            globals.materials[material]["Entry_id"].configure(
                                textvariable=globals.materials[material]["Thickness [nm]"]
                            )
                        globals.materials[material]["Entry_id"].grid(
                            row=row_counter, 
                            column=3,
                            sticky="e",
                            padx=(0,0),
                            pady=(0,1)
                        )


                        #THICKNESS SLIDER
                        if("Slider_id" not in globals.materials[material]):                  
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
                            )
                            #Add slider to dictionary
                            globals.materials[material]["Slider_id"] = slider 
                        #Adjust existing slider
                        else:
                            globals.materials[material]["Slider_id"].configure(
                                variable=globals.materials[material]["Thickness [nm]"],
                                progress_color=globals.materials[material]["Color"].get()
                            )
                        #Place slider on the grid
                        globals.materials[material]["Slider_id"].grid(
                            row=row_counter, 
                            column=4,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #MOVE DOWN BUTTON
                        if("Move_down_button_id" not in globals.materials[material]):                  
                            move_down_button = customtkinter.CTkButton(
                                master=self.material_adjustment_panel_frame, 
                                text="⬇", #⬆ ⬇ 🔼 🔽
                                font=(settings.text_font, 15),
                                fg_color=settings.material_adjustment_panel_button_color,
                                hover_color=globals.materials[material]["Color"].get(), 
                                text_color=settings.material_adjustment_panel_button_text_color,
                                command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down)
                            )
                            #Add button to dictionary
                            globals.materials[material]["Move_down_button_id"] = move_down_button
                        #Adjust existing move_down_button
                        else:
                            globals.materials[material]["Move_down_button_id"].configure(
                                command=lambda chosen_material=material, up_or_down="down": self.move_material(chosen_material, up_or_down),
                                hover_color=globals.materials[material]["Color"].get()
                            )
                        #Place button on grid
                        globals.materials[material]["Move_down_button_id"].grid(
                            row=row_counter,
                            column=5,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )


                        #MOVE UP BUTTON
                        if("Move_up_button_id" not in globals.materials[material]):                  
                            move_up_button = customtkinter.CTkButton(
                                master=self.material_adjustment_panel_frame, 
                                text="⬆", #⬆ ⬇ 🔼 🔽
                                font=(settings.text_font, 15),
                                fg_color=settings.material_adjustment_panel_button_color,
                                hover_color=globals.materials[material]["Color"].get(), 
                                text_color=settings.material_adjustment_panel_button_text_color,
                                command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down)
                            )
                            #Add button do dictionary
                            globals.materials[material]["Move_up_button_id"] = move_up_button
                        #Adjust existing move_down_button
                        else:
                            globals.materials[material]["Move_up_button_id"].configure(
                                command=lambda chosen_material=material, up_or_down="up": self.move_material(chosen_material, up_or_down),
                                hover_color=globals.materials[material]["Color"].get()
                            )
                        #Place button on grid
                        globals.materials[material]["Move_up_button_id"].grid(
                            row=row_counter,
                            column=6,
                            sticky="",
                            padx=(0,0),
                            pady=(0,0)
                        )

                        #Increment row_counter
                        row_counter+=1
                        

        return self.material_adjustment_panel_frame
          
    
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
        if("Label_name_id" in globals.materials[material]):                          
            globals.materials[material]["Label_name_id"].destroy()

        if("Delete_material_button_id" in globals.materials[material]):                  
            globals.materials[material]["Delete_material_button_id"].destroy()
        
        if("Piezo_checkbox_id" in globals.materials[material]):                  
            globals.materials[material]["Piezo_checkbox_id"].destroy()

        if("Move_down_button_id" in globals.materials[material]):                          
            globals.materials[material]["Move_down_button_id"].destroy()
        
        if("Move_up_button_id" in globals.materials[material]):                          
            globals.materials[material]["Move_up_button_id"].destroy()

        if("Entry_id" in globals.materials[material]):                          
            globals.materials[material]["Entry_id"].destroy()

        if("Slider_id" in globals.materials[material]):                                      
            globals.materials[material]["Slider_id"].destroy()

        if("Checkbox_id" in globals.materials[material]):                                                  
            globals.materials[material]["Checkbox_id"].destroy()

        if("Results_panel_Mp_material_name_label_id" in globals.materials[material]):                                                  
            globals.materials[material]["Results_panel_Mp_material_name_label_id"].destroy()
        
        if("Results_panel_Mp_value_label_id" in globals.materials[material]):                                                  
            globals.materials[material]["Results_panel_Mp_value_label_id"].destroy()
        
        if("Results_panel_blocking_force_material_name_label_id" in globals.materials[material]):                                                  
            globals.materials[material]["Results_panel_blocking_force_material_name_label_id"].destroy()
        
        if("Results_panel_blocking_force_value_label_id" in globals.materials[material]):                                                  
            globals.materials[material]["Results_panel_blocking_force_value_label_id"].destroy()


        #delete material from dictionary
        del globals.materials[material]

        #Sort the materials{} dictionary
        globals.app.sort_dictionary()
        
        globals.app.update_widgets("material_deleted")
        

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

        globals.app.update_widgets("material_moved")
