# Python Graphical User Interface program for visualizing thickness of materials and their behaviours

# RUNAR
    -Alle Zp verdier blir lagret i en dictionary kalt "globals.zp".
    -Zp verdi blir kun regnet ut og lagret hvis du har markert et materiale som piezo materiale i check-boksene 


    dictionary key = "navn på materialet"
    dictionary value = Zp  

    KODE FOR Å HENTE UT ZP VERDIER:

    for key in globals.zp:
        material_name = key
        zp_value = globals.zp[key]
        print(f"Key:{material_name}, Zp value: {zp_value}")
        

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
                    ["Piezo_checkbox_id"] : tkinter(value),
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

# TO DO
    -legge til flere piezo electric bending moment labels (som runar viste på bilde)

    -Slette globals.zp liste?

    -legge til settings for størrelse på svg eksport

    -hvordan ta bort piezo material entry og fremdeles tegne graf og equation labels riktig?

    -Sjekk "TODO" i starten av "write_indent_on_stepped_stack" funksjonen. den er ikke helt ferdig implementert

# QUESTIONS:
    -Spør om design problemet er fikset hos runar nå. (har bare økt border radius til entry bokser fra 0.4 til 1)
    
    -hvordan ta bort piezo material entry og fremdeles tegne graf og equation labels riktig?
    -Be runar ta en dobbelsjekk for om at alle utregninger fremdeles er korrekt

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

