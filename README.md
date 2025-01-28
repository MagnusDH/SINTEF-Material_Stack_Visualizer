# GUI program for visualizing thickness of materials in Python

    *How to run program:
        1. Open a terminal in the folder containing the "app.py" file
        2. Run one of the following commands:
            "python app.py"
            "python3 app.py"


    *Required libraries:
        1. Pandas: 
            -to read from .excel file
            -"pip install pandas"

        2. openpyxl:
            -required to read from excel files.
            -"pip install openpyxl"
    
        3. pyautogui
            -For taking correct screenshot of rectangle stack
            -"pip install pyautogui"
        
        4.CustomTkinter
            -For a more modern look of the app
            -"pip install customtkinter"
        
        5.Pillow
            -For taking screenshot of the canvas
            -"pip install pillow"

    

    *materials dictionary layout:

        materials = {
            "material_name":
                {"Name"} : str(value)},
                {"Layer"}: int(value),
                {"Thickness": int(value)},
                {"Unit" : str(value)},
                {"Indent [nm]" : int(value)},
                {"Color" : str(value)},
                {"Status" : str(value)},                                == "active" or "inactive"                             
                {"Modulus [GPa]": int(value)},                          == E
                {"CTE [ppm/deg]": int(value)}
                {"Density [kg/m3]": int(value)},                        == rho
                {"Stress_x [MPa]": int(value)},                         == sigma
                {"Poisson": int(value),                                 == nu
                {"R0": int(value)}
                {"R": int(value)}
                {"Label_name_id": tkinter(value)},                      == ID of the label in material_adjustment_panel
                {"Delete_material_button_id": tkinter(value)},
                {"Move_down_button_id": tkinter(value)},
                {"Move_up_button_id": tkinter(value)},
                {"Entry_id": tkinter(value)},
                {"Slider_id": tkinter(value)},
                {"Checkbox_id": tkinter(value)},
                {"Rectangle_id": tkinter(value)},
                {"Text_id": tkinter(value)},
                {"Text_bbox_id" : tkinter(value)},
                {"Line_id": tkinter(value)},
                {"Indent_text_id": tkinter(value)},
                {"Indent_text_bbox_id": tkinter(value)},
                {"Indent_line_id": tkinter(value)},
                {"Indent_arrow_pointer_id": tkinter(value)}
        }
            


    *Class Organization and inheritance
        -The main class "App" creates ONE instance of each class which is stored in the "globals.py" file
        -From this "globals.py" file you can access the attributes and methods of each class


    *Window/Frame hierarchy of the application:
        #To be able to have scrolling functionality in the application I had to have this hierarchy of windows and frames:
            1. "Main_window": The main program window hosting the entire application
            2. "self.background_canvas": a canvas needed for horizontal scrolling
            3. "self.main_frame": a frame that lays on top of the background_canvas. This frame is the main frame for all other widgets in the application


    #HOW TO CREATE AN EXECUTABLE FILE:
        -Navigate to the folder containing the python program
        -Run the following command: "python -m PyInstaller --onefile program_name.py"


    BUGS:
        -If you move a layer up or down in "stoney" view, then the checkbox does not follow the correct layer and messes up the graph values

        -I "draw_indent_on_stepped_stack" så kan indent bokser tegnes over canvas og overlappe hverandre fra toppen av stacken og nedover. For å finne en løsning på dette må man loope gjennom material{} og samtidig finne rektangel koordinatene til det neste materialet i materials{} og dette har jeg ikke funnet en løsning på. 

        -The svg exports of the stack (both full stack and layers) have different SVG sizes if the export was made when the program window was big or small. Is it necessary that they are the same size?


    TO DO               
        -finish write_indent_on_stepped_stack()
        -in load_materials_from_excel: if an excel headline does not exist, then it causes an error. It should be so that if a headline is not found, then a default value should be added to materials dictionary
            
    
    QUESTIONS:
        -How many decimal points does he want for sigma_R value in graph? in the calculations in his previous mail he has rounded every number up. I get 288,6 and he writes 289
        -Ligningen du har gitt meg kan noen ganger ende i at det er 0 under brøklinjen som fører til en "zero divison error". Akkurat nå får brukeren en beskjed om at verdiene som førte til dette må endre. Ønsker du at det skal håndteres på en annen måte?

    POTENTIAL FIXES:
        -Find a way to resize the scaling of the graph so that everything that is plotted inside it shows correctly?
        
        -Check the width of a materials name. If the name is really long then the text is overlapping the rectangle on the layer stack canvas

        -Add a "scrollable frame" in "add material" window

        -If "materials.xlsx" exists, give the user the option to load this file or start an empty project?

        -I write_text_on_stack: hvis et rectangel er for kort i vidden, så blir teksten skrevet utfor rektanglet på begge sider. Lag en tekst box heller på siden?

        -Fjerne "reset values" knappen? hvis nye materialer er lagt til eller navnet på et materiale er endret så vil ikke dette materialet resettes
        -When the "reset values" button is pressed, then the integer values are converted to "str" which causes bugs when you try to "modify material". Check the reset_values function

        -I "stoney" view: Materialer der tickbox value="off" kan være grå farge, materialer der tickbox value="on" kan være deres egen farge

        -Istedetfor å sjekke om en widget eller noe i materials{} er "None" før du lager det, kan du heller sjekke om "key'en" finnes, slik at du slipper å legge til alle variabler i materials{} når du start programmet eller legger til nye materialer











    #CODE FOR FINDING CORRECT SCREEN AND WINDOW SIZES!
    def get_window_sizes(program_window):
        ######################################################################
        self.program_window.update()
        self.program_window.update_idletasks()
        self.background_canvas.update_idletasks() 
        self.main_frame.update_idletasks()

        screen_width = self.program_window.winfo_screenwidth()
        screen_height = self.program_window.winfo_screenheight()
        program_window_width = self.program_window.winfo_width()
        program_window_height = self.program_window.winfo_height()
        background_canvas_width = self.background_canvas.winfo_width()
        background_canvas_height = self.background_canvas.winfo_height()
        main_frame_width = self.main_frame.winfo_width()
        main_frame_height = self.main_frame.winfo_height()    

        print("Screen Width:", screen_width, "Screen Height:", screen_height)
        print("program_window Width:", program_window_width, "program_window height:", program_window_height)
        print("BG canvas Width:", background_canvas_width, "BG canvas height:", background_canvas_height)
        print("main_frame width: ", main_frame_width, "main_frame height: ", main_frame_height)
        ########################################################################