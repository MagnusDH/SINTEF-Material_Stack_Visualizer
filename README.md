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
                {"Status" : str(value)},
                {"Modulus [GPa]": int(value)},                          == E
                {"CTE [ppm/deg]": int(value)}
                {"Density [kg/m3]": int(value)},                        == rho
                {"Stress_x [MPa]": int(value)},                         == sigma
                {"Poisson": int(value),                                 == nu
                {"R0": int(value)}
                {"R": int(value)}
                {"Label_name_id": tkinter(value)},                      == ID of the label in material_adjustment_panel 
                {"Entry_id": tkinter(value)},
                {"Slider_id": tkinter(value)},
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
        I "draw_indent_on_stepped_stack" så kan indent bokser tegnes over canvas og overlappe hverandre fra toppen av stacken og nedover. For å finne en løsning på dette må man loope gjennom material{} og samtidig finne rektangel koordinatene til det neste materialet i materials{} og dette har jeg ikke funnet en løsning på. 


    TO DO 
        -Stoney view skal ha et eget layout:
            -"tick bokser" skal vises istedetfor "delete material" knapper.
            -Kun ett materiale skal kunne markeres/vises samtidig som substratet
            -"R0" og "R" variablene skal vises sammens med slider og tykkelse bokser til hver materiale

        -Fjern "R-slider" i graph
    
    QUESTIONS:
        -

    POTENTIAL FIXES:
        -Add a "scrollable frame" in "add material" window

        -If "materials.xlsx" exists, give the user the option to load this file or start an empty project?

        -I write_text_on_stack: hvis et rectangel er for kort i vidden, så blir teksten skrevet utfor rektanglet på begge sider. Lag en tekst box heller på siden?

        -Fjerne "reset values" knappen? hvis nye materialer er lagt til eller navnet på et materiale er endret så vil ikke dette materialet resettes
        -When the "reset values" button is pressed, then the integer values are converted to "str" which causes bugs when you try to "modify material". Check the reset_values function

        -Trengs "dissabled/enabled" funksjonen enda å eksistere?