import customtkinter
import tkinter
import pyautogui
from tkinter import messagebox, Frame, Label, Entry, StringVar, Scale
from settings import Settings
import pandas   #Excel-file reading
import openpyxl #Excel-file reading


class Material_stack_visualizer_app:
    def __init__(self):
        #Create a dictionary to hold ALL the information about a material
        self.materials = {}
        #Read the given excel-file and populate the materials dictionary
        self.load_materials_from_excel(Settings.EXCEL_FILE)

        #Create a user interface
        self.user_interface_frame = self.create_user_interface()
    
    """Reads the given excel-file and populates the self.materials dictionary with info about each material"""
    def load_materials_from_excel(self, excel_file):
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

    def create_user_interface(self):
        #Create Frame and place it
        user_interface_frame = customtkinter.CTkScrollableFrame(
            master=window, 
            width=Settings.UI_FRAME_WIDTH, 
            height=Settings.UI_FRAME_HEIGHT,
            fg_color=Settings.UI_FRAME_BACKGROUND_COLOR)
        user_interface_frame.grid(row=0, column=0, padx=(0,0), pady=(0,0))

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

        reset_canvas_button = customtkinter.CTkButton(
            master=window, 
            text="Reset canvas", 
            fg_color=Settings.BUTTON_FG_COLOR, hover_color=Settings.BUTTON_HOVER_COLOR, text_color="white")
        reset_canvas_button.grid(row=1, column=0, sticky="nw", padx=(0, 0))

        # button = customtkinter.CTkButton(user_interface_frame, text="BUTTON", fg_color="green", hover_color="yellow", text_color="green")
        # button.grid(row=row_counter, column=1, padx=20, pady=20)  


        return user_interface_frame
    
    """Updates the thickness value in self.materials with the slider value and updates corresponding entry-widget"""
    def material_slider_updated(self, value, identifier): 
        #Update the thickness value in self.materials
        self.materials[identifier]["thickness"] = value

        #Update the entry corresponding to key
        self.materials[identifier]["entry_id"].delete(0, tkinter.END)
        self.materials[identifier]["entry_id"].insert(0, value)

    """Updates the thickness value in self.materials with the entered value and updates corresponding slider-widget"""
    def material_entry_updated(self, entry):
        #Find material that corresponds to "entry"
        for material in self.materials:
            if(self.materials[material]["entry_id"] == entry):
                #Find entered value
                entered_value = int(entry.get())
                #Update the thickness value in self.materials
                self.materials[material]["thickness"] = entered_value

                #Update the slider corresponding to the key
                self.materials[material]["slider_id"].set(entered_value)
        
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