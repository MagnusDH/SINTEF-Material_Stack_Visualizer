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
        
        5. Pillow
            -For taking screenshot of the canvas
            -"pip install pillow"
        
        6. matplotlib
            -For creating graphs
            -"pip install matplotlib"

    

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
    
    *Layer Stack Canvas ITEM TAGS
        -"layer_stack_canvas_bounding_rectangle"                    == a rectangle representing the canvas boundaries 
        -"material_rectangle"                                       == a rectangle representing the material in the stack
        -"text"                                                     == a plain text
        -"text_bbox"                                                == a rectangle representing the bounding box around a text
        -"line"                                                     == a plain line
        -"dotted_line"                                              == a dotted line
        -"arrow_line"                                               == a line with an arrowhead at the end of the line
        -"arrow_line_both"                                          == a line with two arrowheads pointing in both directions


    *Class Organization and inheritance
        -The main class "App" creates ONE instance of each class which is stored in the "globals.py" file
        -From this "globals.py" file you can access the attributes and methods of each class


    #HOW TO CREATE AN EXECUTABLE FILE:
        -Navigate to the folder containing the python program
        -Run the following command: "python -m PyInstaller --onefile program_name.py"





    BUGS:
        -If the program window is in full-screen mode and you then change the view to "stoney", the graph does not render itself properly. 
        
        -I "draw_indent_on_stepped_stack" så kan indent bokser tegnes over canvas og overlappe hverandre fra toppen av stacken og nedover. For å finne en løsning på dette må man loope gjennom material{} og samtidig finne rektangel koordinatene til det neste materialet i materials{} og dette har jeg ikke funnet en løsning på. 

    TO DO         
        -Fjern all funksjon som gjør at "substrate" blir lagt nederst
        -Fix slik at "visible canvas" variabler alltid starter fra nedre venstre hjørne
        -Regn ut og sjekk nye ligninger fra Runar
        -Legg til to grafer i "multi" view
            -Top graf i multi view skal ha (0,0) nede i venstre hjørne (blå halvsirkel skal ikke være der)
        -Lag grid-layout for "add material window"
        

    QUESTIONS:
        -The svg exports of the stack (both full stack and layers) have different SVG sizes if the export was made when the program window was big or small. Is it necessary that they are the same size?
    

    POTENTIAL FIXES:
        -The entire program is set up as if "substrate" is the layer with the highest number. Change this so "substrate" is the lowest layer number and the rest follows

        -Check the width of a materials name. If the name is really long then the text is overlapping the rectangle on the layer stack canvas

        -Add a "scrollable frame" in "add material" window

        -If "materials.xlsx" exists, give the user the option to load this file or start an empty project?

        -I write_text_on_stack: hvis et rectangel er for kort i vidden, så blir teksten skrevet utfor rektanglet på begge sider. Lag en tekst box heller på siden?

        -Fjerne "reset values" knappen? hvis nye materialer er lagt til eller navnet på et materiale er endret så vil ikke dette materialet resettes
        -When the "reset values" button is pressed, then the integer values are converted to "str" which causes bugs when you try to "modify material". Check the reset_values function

        -I "stoney" view: Materialer der tickbox value="off" kan være grå farge, materialer der tickbox value="on" kan være deres egen farge

        -Istedetfor å sjekke om en widget eller noe i materials{} er "None" før du lager det, kan du heller sjekke om "key'en" finnes, slik at du slipper å legge til alle variabler i materials{} når du start programmet eller legger til nye materialer

        -Make a button that gives the user the option to load an excel file

