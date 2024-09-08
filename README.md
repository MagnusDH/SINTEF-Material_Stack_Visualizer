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
                {"layer" : value},
                {"name"} : "value"},
                {"thickness": value},
                {"unit" : "value"},
                {"indent" : value},
                {"color" : "value"},
                {"status" : "value"},
                {"rectangle_id": value},
                {"text_id": value},
                {"text_bbox_id" : value},
                {"line_id": value},
                {"entry_id": value},
                {"slider_id": value},
                {"indent_text_id": value},
                {"indent_arrow_id": value}
        }
        self.materials[material_name] = {"layer": 0, "name": "gull", "thickness":30, "unit":"nm", "indent": 69, "color": "blue", "rectangle_id": None, "text_id": None, "line_id": None, "entry_id": None, "slider_id": None, "indent_text_id": None, "indent_arrow_id": None}


    *Class Organization and inheritance
        -The main class "Layer_Stack_Visualizer" creates ONE instance of each class which is stored in the "globals.py" file
        -From this "globals.py" file you can access the attributes and methods of each class


    *Window/Frame hierarchy of the application:
        #To be able to have scrolling functionality in the application I had to have this hierarchy of windows and frames:
            1. "Main_window": The main program window hosting the entire application
            2. "self.background_canvas": a canvas needed for horizontal scrolling
            3. "self.main_frame": a frame that lays on top of the background_canvas. This frame is the main frame for all other widgets in the application



    BUGS:
        -If you delete a material then you can not "reset values". Must be fixed
        -When you "add material" you have to check if the "color" value is valid. This currently gives an error, must be fixed
        -If the text for the lowest material must be drawn in a text box, it might be pushed under the canvas if there are other text boxes over it
        -If the UI_FRAME_WIDTH is changed, then the CANVAS_PROGRAM_BORDER_WIDTH must also be changed so that it fits the program window correctly

    #HOW TO CREATE AN EXECUTABLE FILE:
        -Navigate to the folder containing the python program
        -Run the following command: "python -m PyInstaller --onefile program_name.py"