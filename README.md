# Python Graphical User Interface program for visualizing thickness of materials and their behaviours

# How to run program
    1. Open a terminal in the folder containing the "app.py" file
    2. Run one of the following commands:
        "python app.py"
        "python3 app.py"


# Required libraries:
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
        
    5. Pillow
        -For taking screenshot of the canvas
        -"pip install pillow"
        
    6. matplotlib
        -For creating graphs
        -"pip install matplotlib"

    

# Main materials dictionary:
    *The dictionary is always organized so that the first material layer in the stack is the first element in the dictionary. If a material is at layer 5 the it will be the 5th element in the dictionary
    
    materials = {

        "material_name" = {

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
    }
    
    

# Class Organization and inheritance
    *The main class "App" creates ONE instance of each class which is stored in the "globals.py" file and is easily accessed via "globals.class_name.function_name()"

# Layer Stack Canvas 
    *ITEM TAGS
        -"layer_stack_canvas_bounding_rectangle"                    == a rectangle representing the canvas boundaries 
        -"material_rectangle"                                       == a rectangle representing the material in the stack
        -"text"                                                     == a plain text
        -"text_bbox"                                                == a rectangle representing the bounding box around a text
        -"line"                                                     == a plain line
        -"dotted_line"                                              == a dotted line
        -"arrow_line"                                               == a line with an arrowhead at the end of the line
        -"arrow_line_both"                                          == a line with two arrowheads pointing in both directions

    *All rectangles on the canvas is drawn from the bottom left corner to top right corner. x0/y0 = bottom left corner, x1/y1 = top right corner


# HOW TO CREATE AN EXECUTABLE FILE:
    -Navigate to the folder containing the python program
    -Run the following command: "python -m PyInstaller --onefile program_name.py"


# TO DO         
    -Finne ut av hvordan "stepped" stack og dens indent'er egentlig skal regnes ut. slik det er nå gir ikke så mye mening
    -Finne ut hvordan verdien på slidere skal fungere, hva skal de gå til?
    -Lag grid-layout for "add material window"
    -Regn ut og sjekk nye ligninger fra Runar
    -Legg til to grafer i "multi" view
        -Top graf i multi view skal ha (0,0) nede i venstre hjørne (blå halvsirkel skal ikke være der)
    -ZN blir regnet ut feil ifølge Runar, snakk om dette
    -Sette alle dictionary variabler til "None" i draw_material_stack, og ikke i alle separate funksjoner?
    -Sjekk "TODO" i starten av "write_indent_on_stepped_stack" funksjonen. den er ikke helt ferdig implementert

    -Check the width of a materials->name. If the name is really long then the text is overlapping the rectangle on the layer stack canvas

    -Add a "scrollable frame" in "add material" window

    -I write_text_on_stack: hvis et rectangel er for kort i vidden, så blir teksten skrevet utfor rektanglet på begge sider. Lag en tekst box heller på siden?

    -Fjerne eller forbedre "reset values" knappen??????? (hvis nye materialer er lagt til eller navnet på et materiale er endret så vil ikke dette materialet resettes)

    -Istedetfor å sjekke om en widget eller noe i materials{} er "None" før du lager det, kan du heller sjekke om "key'en" finnes, slik at du slipper å legge til alle variabler i materials{} når du start programmet eller legger til nye materialer

    -Make a button that gives the user the option to load an excel file

# QUESTIONS:
    -The svg exports of the stack (both full stack and layers) have different SVG sizes if the export was made when the program window was big or small. Is it necessary that they are the same size?
    
# BUGS:
    -I "draw_indent_on_stepped_stack" så kan indent bokser tegnes over canvas og overlappe hverandre fra toppen av stacken og nedover. For å finne en løsning på dette må man loope gjennom material{} og samtidig finne rektangel koordinatene til det neste materialet i materials{} og dette har jeg ikke funnet en løsning på. 
