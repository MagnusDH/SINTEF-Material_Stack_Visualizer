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

    

    *materials dictionary layout:

        materials = {
            "material_name":
                {"layer" : int(value)},
                {"name"} : str(value)},
                {"thickness": int(value)},
                {"unit" : str(value)},
                {"indent" : int(value)},
                {"color" : str(value)},
                {"status" : str(value)},
                {"E": int(value)},
                {"rho": int(value)},
                {"sigma": int(value)},
                {"nu": int(value),
                {"entry_id": tkinter(value)},
                {"slider_id": tkinter(value)},
                {"rectangle_id": tkinter(value)},
                {"text_id": tkinter(value)},
                {"text_bbox_id" : tkinter(value)},
                {"line_id": tkinter(value)},
                {"indent_text_id": tkinter(value)},
                {"indent_text_bbox_id": tkinter(value)},
                {"indent_line_id": tkinter(value)},
                {"indent_arrow_pointer_id": tkinter(value)}
        }


        self.materials[material_name] = {"layer": 0, "name": "gull", "thickness":30, "unit":"nm", "indent": 69, "color": "blue", "status": "active/disabled", "rectangle_id": None, "text_id": None, "text_bbox_id": None, line_id": None, "entry_id": None, "slider_id": None, "indent_text_id": None, "indent_arrow_id": None}


    *Class Organization and inheritance
        -The main class "App" creates ONE instance of each class which is stored in the "globals.py" file
        -From this "globals.py" file you can access the attributes and methods of each class


    *Window/Frame hierarchy of the application:
        #To be able to have scrolling functionality in the application I had to have this hierarchy of windows and frames:
            1. "Main_window": The main program window hosting the entire application
            2. "self.background_canvas": a canvas needed for horizontal scrolling
            3. "self.main_frame": a frame that lays on top of the background_canvas. This frame is the main frame for all other widgets in the application



    BUGS:
        -write indent on stepped stack
            #Sjekk at indent text bokser ikke tegnes utenfor canvas når materialer blir for tynn eller tykk
            #I write_text_on_stack: hvis et rectangel er for kort i vidden, så blir teksten skrevet utfor rektanglet på begge sider. Lag en tekst box heller på siden?
        -If the text for the lowest material must be drawn in a text box, it might be pushed under the canvas if there are other text boxes over it
            

    #HOW TO CREATE AN EXECUTABLE FILE:
        -Navigate to the folder containing the python program
        -Run the following command: "python -m PyInstaller --onefile program_name.py"

    TO DO
        -Create a functionality to move each layer up and down in the stack

        -Create a new View, "Stress":
            -Shows the "stacked" stack and curve side by side
            -Show the value for R explicitly in the graph (ex. In upper right corner)
            -Change the color of the graph when curving up vs down
            -All the other Views should only be the stack in different modes
        
        -Create an "export as excel" button that:
            -creates an excel sheet of all the current values in the material{} dictionary
                -this should overwrite the current excel sheet in the folder (if it exists) so that it is imported the next time
            -Import/glue a picture/svg of the stack into the excel sheet