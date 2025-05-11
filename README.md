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
    
    materials = 
        {
            ["material_name"] : str(value) = 
                {
                    ["Name"] : tkinter.StringVar,
                    ["Layer"] : tkinter.IntVar,
                    ["Thickness [nm]"] : tkinter.DoubleVar,
                    ["Unit"] : tkinter.StringVar,
                    ["Indent [nm]"] : tkinter.DoubleVar,
                    ["Color"] : tkinter.StringVar,
                    ["Status"] : tkinter.StringVar,                          == "active" or "inactive"                             
                    ["Modulus [GPa]"] : tkinter.DoubleVar,                   == E
                    ["CTE [ppm/deg]"] : tkinter.DoubleVar,
                    ["Density [kg/m3]"] : tkinter.DoubleVar,                 == rho
                    ["Stress_x [MPa]"] : tkinter.DoubleVar,                  == sigma
                    ["Poisson"] : tkinter.DoubleVar,                         == nu
                    ["R0"] : tkinter.DoubleVar,
                    ["R"] : tkinter.DoubleVar
                    ["Label_name_id]" : tkinter(value),                      == ID of the label in material_adjustment_panel
                    ["Delete_material_button_id"] : tkinter(value),
                    ["Move_down_button_id"] : tkinter(value),
                    ["Move_up_button_id"] : tkinter(value),
                    ["Entry_id"] : tkinter(value),
                    ["Slider_id"] : tkinter(value),
                    ["Checkbox_id"] : tkinter(value),
                    ["Rectangle_id"] : tkinter(value),
                    ["Text_id"] : tkinter(value),
                    ["Text_bbox_id"] : tkinter(value),
                    ["Line_id"] : tkinter(value),
                    ["Indent_text_id"] : tkinter(value),
                    ["Indent_text_bbox_id"] : tkinter(value),
                    ["Indent_line_id"] : tkinter(value),
                    ["Indent_arrow_pointer_id"] : tkinter(value)
                }
        }
    
    

# Program layout
    -The main class "App" creates ONE instance of each class which is stored in the "globals.py" file and is easily accessed via "globals.class_name.function_name()"
    -All variables are tkinter variables (StringVar, IntVar, DoubleVar etc...) and have traces which detects changes on the variable and updates other widgets accordingly

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


# Equation units:
    -Modulus values are entered as Giga Pascal (GPa). To convert these values to "Pascal", multiply it with 1e9 
    -Thickness values are entered in nanometers (nm). To convert these to meters, divide them by 1e9
    -"Nu" or "Poisson" values are unitless and does not need to be converted
    -Stress_x values are entered as Mega Pascal (MPa). To convert these to Pascal, multiply it with 1e6
    -Zn: to convert Zn to nanometers, multiply it with 1e9
    -Zp: to convert Zp to nanometers, multiply it with 1e9
    -W are entered in micrometers (μm). To convert to meters, divide it by 1e6
    -L are enterd in micrometers (μm). To convert to meters, divide it by 1e6
    -M_is is a value in newton meters and needs no conversion
    -M_p is a value in newton meters and needs no conversion
    -M_tot is a value in newton meters and needs no conversion
    -EI is a value in newton meter**2 and needs no conversion
    -curv_is is a value in "1/meters" and needs no conversion
    -V_p is a value in "volt" and needs no conversion
    -e_31_f is a value in "c/m2" and needs no conversion



# HOW TO CREATE AN EXECUTABLE FILE:
    -Navigate to the folder containing the python program
    -Run the following command: "python -m PyInstaller --onefile program_name.py"


# TO DO
    -i piezoelectric_bending_moment_label skal verdien "M_p" legges inn
    -i stress_neutral_SiO2_thickness_label skal verdien fra globals.equations.find_t_solution() legges inn

    -Modify_materials() er full av bugs

    -Find a smart way to render parameters_panel equation labels

    -Fiks størrelse på svg exports
    
    -export stack and graph in one button   

    -Sette alle dictionary variabler til "None" i draw_material_stack, og ikke i alle separate funksjoner?
    -Sjekk "TODO" i starten av "write_indent_on_stepped_stack" funksjonen. den er ikke helt ferdig implementert
    -Check the width of a materials->name. If the name is really long then the text is overlapping the rectangle on the layer stack canvas
    -Add a "scrollable frame" in "add material" window
    -I write_text_on_stack: hvis et rectangel er for kort i vidden, så blir teksten skrevet utfor rektanglet på begge sider. Lag en tekst box heller på siden?
    -Fjerne eller forbedre "reset values" knappen??????? (hvis nye materialer er lagt til eller navnet på et materiale er endret så vil ikke dette materialet resettes)
    -Istedetfor å sjekke om en widget eller noe i materials{} er "None" før du lager det, kan du heller sjekke om "key'en" finnes, slik at du slipper å legge til alle variabler i materials{} når du start programmet eller legger til nye materialer
    -ikke vis error box, men heller rød markør rundt feil

# QUESTIONS:
    -Ta bort "unit" i excel ark? det gir ikke mening å ha lengre

    
# BUGS:
    -I "draw_indent_on_stepped_stack" så kan indent bokser tegnes over canvas og overlappe hverandre fra toppen av stacken og nedover. For å finne en løsning på dette må man loope gjennom material{} og samtidig finne rektangel koordinatene til det neste materialet i materials{} og dette har jeg ikke funnet en løsning på. 











V = helper_functions.convert_decimal_string_to_float(self.volt_entry.get())
V = 100
e_31_f = helper_functions.convert_decimal_string_to_float(self.e_31_f_entry.get())
h_Piezo = helper_functions.convert_decimal_string_to_float(self.piezo_material_entry.get())
h_Si = list(globals.materials)[0]
w = 160/1e6
L = helper_functions.convert_decimal_string_to_float(self.L_entry.get())
E = []
t = []
for material in globals.materials:
    E.append(globals.materials[material]["Modulus [GPa]"].get() * 1e9)
    t.append(float(globals.materials[material]["Thickness [nm]"].get()) / 1e9)

blocking_force_value = globals.equations.calculate_blocking_force(E, t, V, e_31_f, h_Piezo, h_Si, w, L)




