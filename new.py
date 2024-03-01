import customtkinter
import tkinter
import pyautogui
from tkinter import messagebox, Frame, Label, Entry, StringVar, Scale, Canvas
from settings import Settings
import pandas   #Excel-file reading
import openpyxl #Excel-file reading


class Material_stack_visualizer_app:
    def __init__(self):
        print("INIT()")
        #Create a dictionary to hold ALL the information about a material
        self.materials = {}
        #Read the given excel-file and populate the materials dictionary
        self.load_materials_from_excel(Settings.EXCEL_FILE)

        #Create a user interface
        self.user_interface_frame = self.create_user_interface()

        #Create canvas
        self.canvas = self.create_canvas()
    
    """Reads the given excel-file and populates the self.materials dictionary with info about each material"""
    def load_materials_from_excel(self, excel_file):
        print("LOAD_MATERIALS_FROM_EXCEL()")
        
        try:
            #Read given excel file into Pandas dataframe
            excel_data = pandas.read_excel(excel_file)

            #Open excel-file to read background colors of each cell
            work_book = openpyxl.load_workbook(excel_file, data_only=True)
            fs = work_book.active

            #Loop through the rows in excel_file
            i = 2
            for column, row in excel_data.iterrows():
                #Check the background color of the cell
                background_color = fs.cell(column=2, row=i).fill.bgColor.index
                if(background_color == "FFFFFF00"):
                    status = "disabled"
                else:
                    status = "active"
                #Increment "i" to go to the next row
                i+=1

                #Create an "info" dictionary to contain all info from excel-file
                info = {
                    "name": row["Material"],
                    "layer": row["Layer"],
                    "thickness": row["Thickness"],
                    "unit": row["Unit"],
                    "indent": row["Indent"],
                    "color": row["Color"],
                    "status": status,
                    "rectangle_id": None,
                    "text_id": None,
                    "text_bbox_id" : None,
                    "line_id": None,
                    "entry_id": None,
                    "slider_id": None,
                    "indent_text_id": None,
                    "indent_arrow_id": None
                }

                #Put "info" dictionary into self.materials dictionary
                self.materials[row["Material"]] = info

        except Exception as error:
            messagebox.showerror("Error", "Could not load materials from Excel-file")
            window.destroy()

    """Creates a Frame with sliders, entries and buttons"""
    def create_user_interface(self):
        print("CREATE_USER_INTERFACE()")
        
        #Create Frame and place it
        user_interface_frame = customtkinter.CTkScrollableFrame(
            master=window, 
            width=Settings.UI_FRAME_WIDTH, 
            height=Settings.UI_FRAME_HEIGHT,
            fg_color=Settings.UI_FRAME_BACKGROUND_COLOR
        )
        user_interface_frame.grid(
            row=0, 
            column=0, 
            padx=(0,0), 
            pady=(5,0),
            sticky="n"
        )

        #Create sliders, buttons etc for each material
        row_counter = 0
        for material in dict(reversed(self.materials.items())):
            #Create label and place it
            label = tkinter.Label(
                user_interface_frame, 
                text=material, 
                bg=Settings.UI_LABEL_BACKGROUND_COLOR,
                fg=Settings.UI_FRAME_TEXT_COLOR
            )
            label.grid(row=row_counter, column=0, sticky="nw", padx=(0,0))

            #Create Entry, customize it and add it to dictionary
            entry = customtkinter.CTkEntry(
                master=user_interface_frame,
                textvariable=StringVar(value=str(self.materials[material]["thickness"])),
                fg_color = Settings.UI_ENTRY_BACKGROUND_COLOR,
                text_color="black",
                width=70,
                justify="center"
            )
            entry.grid(
                row=row_counter, 
                column=1,
                sticky="e",
                pady=(0,0),
                padx=(0,0)
            )
            entry.bind("<Return>", lambda event, e=entry: self.material_entry_updated(e))
            self.materials[material]["entry_id"] = entry

            #Create Slider, customize it and add it to dictionary
            slider = customtkinter.CTkSlider(
                master=user_interface_frame, 
                from_=Settings.SLIDER_RANGE_MIN, 
                to=Settings.SLIDER_RANGE_MAX,
                progress_color=self.materials[material]["color"],
                command=lambda value, identifier=material:self.material_slider_updated(round(value), identifier)
            )
            slider.grid(
                row=row_counter, 
                column=2,
                sticky="e",
                pady=(0,0),
                padx=(0,0)
            )
            slider.set(self.materials[material]["thickness"])
            self.materials[material]["slider_id"] = slider 
            #Disable slider and Entry if specified by the excel-file
            if(self.materials[material]["status"] == "disabled"):
                self.materials[material]["slider_id"].configure(state="disabled") #Disable slider
                self.materials[material]["entry_id"].delete(0, tkinter.END)     #Disable Entry
                self.materials[material]["entry_id"].insert(0, "Disabled")      #Disable Entry
                self.materials[material]["entry_id"].configure(state="disabled")#Disable Entry
            self.materials[material]["slider_id"] = slider 

            #Increment row_counter
            row_counter+=1

        #Reset canvas button
        reset_canvas_button = customtkinter.CTkButton(
            master=window, 
            text="Reset canvas", 
            fg_color=Settings.BUTTON_FG_COLOR, 
            hover_color=Settings.BUTTON_HOVER_COLOR, 
            text_color=Settings.UI_FRAME_TEXT_COLOR,
            width=15,
            command=self.reset_canvas)
        reset_canvas_button.grid(row=1, column=1, sticky="nw", padx=(0, 0))

        #Reset values button
        reset_values_button = customtkinter.CTkButton(
            master=window,
            text="Reset values",
            fg_color=Settings.BUTTON_FG_COLOR, 
            hover_color=Settings.BUTTON_HOVER_COLOR, 
            text_color=Settings.UI_FRAME_TEXT_COLOR,
            width=15,
            command=self.reset_values
        )
        reset_values_button.grid(row=2, column=1, sticky="nw", padx=(0, 0), pady=(0,0))

        #Export stack button
        export_stack_button = customtkinter.CTkButton(
            master=window,
            text="Export stack",
            fg_color=Settings.BUTTON_FG_COLOR, 
            hover_color=Settings.BUTTON_HOVER_COLOR, 
            text_color=Settings.UI_FRAME_TEXT_COLOR,
            width=15,
            command=self.export_stack_as_svg
        )
        export_stack_button.grid(row=1, column=1, sticky="n", padx=(0, 0), pady=(0,0))
        
        #Export layers button
        export_layers_button = customtkinter.CTkButton(
            master=window,
            text="Export layers",
            fg_color=Settings.BUTTON_FG_COLOR, 
            hover_color=Settings.BUTTON_HOVER_COLOR, 
            text_color=Settings.UI_FRAME_TEXT_COLOR,
            width=15,
            command=self.export_layers_as_svg
        )
        export_layers_button.grid(row=2, column=1, sticky="n", padx=(0, 0), pady=(5,0))

        #Switch layout ComboBox
        self.option_menu = customtkinter.CTkOptionMenu(
            master=window, 
            values=["Stacked", "Realistic", "Stepped"],
            command=self.switch_layout
        )
        self.option_menu.grid(row=1, column=1, sticky="ne", padx=(0, 0), pady=(0,0))
        
        return user_interface_frame
    
    """Returns a canvas created in the program window"""
    def create_canvas(self):
        print("CREATE_CANVAS()")
        
        #Create canvas and place it
        canvas = Canvas(
            master=window, 
            height=Settings.CANVAS_HEIGHT, 
            width=Settings.CANVAS_WIDTH, # self.program_window_width-self.user_interface_frame.winfo_width(), 
            bg=Settings.CANVAS_BACKGROUND_COLOR,
            highlightbackground="black", 
            highlightthickness=1
            )
        canvas.grid(
            row=0, 
            column=1, 
            sticky="s", 
            padx=(3,3), 
            pady=(5,0)
        )

        #Set canvas_bbox coordniates for later use
        self.visible_canvas_bbox_x0 = 2
        self.visible_canvas_bbox_y0 = 2
        self.visible_canvas_bbox_x1 = canvas.winfo_reqwidth() - 3 
        self.visible_canvas_bbox_y1 = canvas.winfo_reqheight() - 3
        self.canvas_height = self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0
        self.canvas_width = self.visible_canvas_bbox_x1 - self.visible_canvas_bbox_x0

        #Draw bounding box around canvas
        canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline="black")

        #Listen to mouse: buttonpress, motion and zoom events
        canvas.bind("<ButtonPress-1>", lambda event, canvas=canvas: self.click_on_canvas(event, canvas))
        canvas.bind("<B1-Motion>", lambda event, canvas=canvas: self.canvas_drag(event, canvas))
        canvas.bind("<MouseWheel>", lambda event, canvas=canvas: self.canvas_zoom(event, canvas))

        return canvas

    """Updates the thickness value in self.materials with the slider value and updates corresponding entry-widget"""
    def material_slider_updated(self, value, identifier): 
        print("MATERIAL_SLIDER_UPDATED()")
        
        #Update the thickness value in self.materials
        self.materials[identifier]["thickness"] = value

        #Update the entry corresponding to key
        self.materials[identifier]["entry_id"].delete(0, tkinter.END)
        self.materials[identifier]["entry_id"].insert(0, value)

    """Updates the thickness value in self.materials with the entered value and updates corresponding slider-widget"""
    def material_entry_updated(self, entry):
        print("MATERIAL_ENTRY_UPDATED()")
        
        #Find material that corresponds to "entry"
        for material in self.materials:
            if(self.materials[material]["entry_id"] == entry):
                #Find entered value
                entered_value = int(entry.get())
                #Update the thickness value in self.materials
                self.materials[material]["thickness"] = entered_value

                #Update the slider corresponding to the key
                self.materials[material]["slider_id"].set(entered_value)
    
    """Deletes the current canvas and creates a new one in its original place"""
    def reset_canvas(self, *args):
        print("RESET_CANVAS")

        #Delete canvas from program window
        self.canvas.destroy()

        #Create new canvas in its original position
        self.canvas = self.create_canvas()

    """Reads the excel file again and repopulated the "thickness" in self.materials. Updates sliders and entries with new values"""
    def reset_values(self):
        print("RESET_VALUES")

        #Reload initial values from given excel file
        try:
            #Read given excel file into Pandas dataframe
            excel_data = pandas.read_excel(Settings.EXCEL_FILE)

            #Loop through the rows in excel_file and populate "self.materials"
            for index, row in excel_data.iterrows():
                material_name = row["Material"]
                material_thickness = row["Thickness"]
                
                #Populate material dictionary
                self.materials[material_name]["thickness"] = material_thickness
                
                #Update sliders and Entries
                self.materials[material_name]["slider_id"].set(material_thickness)
                self.materials[material_name]["entry_id"].delete(0, tkinter.END)
                self.materials[material_name]["entry_id"].insert(0, material_thickness)
            
            # #Reset text_size
            # self.current_text_size = self.original_text_size
            
            # #Draw rectangle stack with original values
            # self.draw_material_stack()
        
        #Handle errors
        except Exception as error:
            messagebox.showerror("Error", "Could not reset values\nMay be a issue with reading from excel-file")
        
    """Remembers the initial mouse click-position on the canvas"""
    def click_on_canvas(self, event, canvas):
        print("CLICK_ON_CANVAS()")
        
        canvas.scan_mark(event.x, event.y)
    
    """Moves the position of the canvas"""
    def canvas_drag(self, event, canvas):
        print("CANVAS_DRAG()")
        
        canvas.scan_dragto(event.x, event.y, gain=1)

    """Scales all the elements on the canvas up or down"""
    def canvas_zoom(self, event, canvas):
        print("CANVAS_ZOOM()")
        
        zoom_factor = 1.05

        #Zoom in: Scale all items on the canvas around the mouse cursor
        if event.delta > 0:
            canvas.scale("all", event.x, event.y, zoom_factor, zoom_factor)
            # self.current_text_size *= zoom_factor
            # self.current_text_size = math.ceil(self.current_text_size)

        #Zoom out: Scale all items on the canvas around the mouse cursor
        elif event.delta < 0:
            canvas.scale("all", event.x, event.y, 1.0/zoom_factor, 1.0/zoom_factor)
            # self.current_text_size /= zoom_factor
            # self.current_text_size = math.floor(self.current_text_size)

        #Redraw text on stack
        # if(self.switch_layout_counter % 3 == 0):
        #     self.write_text_on_stack(self.current_text_size)
        # elif(self.switch_layout_counter % 3 == 1):
        #     self.write_text_on_stack(self.current_text_size)
        # else:
        #     self.write_text_on_stepped_stack(self.current_text_size)

    def program_window_resized(self):
        print("PROGRAM_WINDOW_RESIZED() - NOT IMPLEMENTED")

    def switch_layout(self, event):
        print("SWITCH LAYOUT")
        value = self.option_menu.get()
        if(value == "Stacked"):
            print("STAAAAACKED")
        if(value == "Realistic"):
            print("REALIIIISTIIIC")
        if(value == "Stepped"):
            print("STEEEEPPED")


    def export_stack_as_svg(self):
        print("EXPORT_STACK_AS_SVG")
    
    def export_layers_as_svg(self):
        print("EXPORT_LAYERS_AS_SVG")



    

#Main starting point of program
if __name__ == "__main__":
    #Create a host tkinter program window
    window = tkinter.Tk()

    #Set program window title, dimensions and color
    window.title(Settings.PROGRAM_TITLE)
    window.geometry(f"{Settings.PROGRAM_WINDOW_WIDTH}x{Settings.PROGRAM_WINDOW_HEIGHT}")
    window.configure(bg=Settings.PROGRAM_BACKGROUND_COLOR)

    #Create keyboard shortcuts for program window
    window.bind("<Escape>", lambda event: window.destroy())

    #Create instance of Layer_stack_vizualiser class and run it
    material_stack_visualizer_app = Material_stack_visualizer_app()

    #Start the main loop of the program
    window.mainloop()