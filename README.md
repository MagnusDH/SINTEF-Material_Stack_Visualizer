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
        -Det er noen få variabler som jeg har måtte legge inn manuelt fordi ting ikke passer på canvas. F.eks i draw_rectangle_stack() så må x0 og yo starte på 2
        -På min PC kan man kun ha 11 materialer før sliders blir for lang og sliders passer ikke inn i applikasjonen. Må dette endres?

    NOTES:
        -The export_as_svg functions are heavily based on and taken from chatGPT