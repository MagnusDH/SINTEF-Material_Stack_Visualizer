# GUI program for visualizing thickness of materials in Python

    *How to run program:
        1. Open a terminal in the folder containing the "program.py" file
        2. Run one of the following commands:
            "python program.py"
            "python3 program.py"


    *Required libraries:
        1. Pandas: 
            -to read from .excel file
            -" pip install pandas "

        2. openpyxl:
            -required to read from excel files.
            -" pip install openpyxl "
    
        3. pyautogui
            -For taking correct screenshot of rectangle stack
            -" pip install pyautogui "


    FUNCTIONS OF PROGRAM:
        -Adjust the thickness of each layer by using the sliders or entry-boxes
        -Rectangle stack gets redrawn acording to the size of the app-window
        -Close program by pressing "esc" or closing app-window manually
        -"export_recStack_as_jpg" takes a screenshot of the entire rectangle stack
        -"export_all_as_jpg" takes incrementing screenshots of all the materials/layers in the rectangle stack

    BUGS:
        -There is a small delay when the sliders are adjusted. Rectangle stack does not get drawn imidietly when the slider is adjusted, so for now you need to hover the mouse over the slider after releasing it to draw the rectangle stack.
        
        -If you maximise all the thicknesses, then the last rectangle is drawn slightly outside the canvas