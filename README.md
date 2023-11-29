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
        -Fjernet self.sliders[] listen. Rectangle stack blir nå tegnet basert på tykkelsene i self.materials
        -La til funksjon som lukker programmet når "esc" blir trykket

    BUGS:
        -Det er et delay i sliders når de blir justert. Rectangle stack blir ikke tegnet helt nøyaktig og musen må dras over slideren for at rectangle stack skal bli tegnet HELT korrekt 
        -For at ikke rectangle stack skal bli tegnet utenfor vinduet blir den totale høyden på programmet delt på antall materialer. Dermed kan det bli uoversiktlig hvis du har for mange materialer