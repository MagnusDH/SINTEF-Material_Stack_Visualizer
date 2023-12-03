# GUI program for visualizing thickness of materials in Python

    *How to run program:
        1. Open a terminal in the folder containing the "program.py" file
        2. Run one of the following commands:
            "python program.py"
            "python3 program.py"


    * Required libraries:
        1. Pandas: 
            -to read from .excel file
            -" pip install pandas "

        2. openpyxl:
            -required to read from excel files.
            -" pip install openpyxl "
    
        3. pyautogui
            -For taking correct screenshot of rectangle stack
            -" pip install pyautogui "


    CHANGES MADE:
        -self.sliders[] list is removed. The stack is now being drawn based on the thicknesses in self.materials{}
        -The thickness in self.materials gets updated when the sliders or entry boxes are adjusted. 
        -New function lets you quit the program when pressing "esc" button
        -The rectangle stack gets redrawn when the size of the window is changed
        -The "scaling_factor" is now divided by the height of the canvas and the number of materials to ensure that the stack is not drawn outside the app-window

    BUGS:
        -There is a small delay when the sliders are adjusted. Rectangle stack does not get drawn imidietly when the slider is adjusted, so for now you need to hover the mouse over the slider after releasing it to draw the rectangle stack. 