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
                {"rectangle_id": tkinter(value)},
                {"text_id": tkinter(value)},
                {"text_bbox_id" : tkinter(value)},
                {"line_id": tkinter(value)},
                {"entry_id": tkinter(value)},
                {"slider_id": tkinter(value)},
                {"indent_text_id": tkinter(value)},
                {"indent_arrow_id": tkinter(value)}
        }
        self.materials[material_name] = {"layer": 0, "name": "gull", "thickness":30, "unit":"nm", "indent": 69, "color": "blue", "status": "active/disabled", "rectangle_id": None, "text_id": None, "text_bbox_id": None, line_id": None, "entry_id": None, "slider_id": None, "indent_text_id": None, "indent_arrow_id": None}


    *Class Organization and inheritance
        -The main class "Layer_Stack_Visualizer" creates ONE instance of each class which is stored in the "globals.py" file
        -From this "globals.py" file you can access the attributes and methods of each class


    *Window/Frame hierarchy of the application:
        #To be able to have scrolling functionality in the application I had to have this hierarchy of windows and frames:
            1. "Main_window": The main program window hosting the entire application
            2. "self.background_canvas": a canvas needed for horizontal scrolling
            3. "self.main_frame": a frame that lays on top of the background_canvas. This frame is the main frame for all other widgets in the application



    BUGS:
        -Materialene i Stepped_canvas går i minus og tegnes feil vei. Finn en fix på dette 
        -If you delete a material then you can not "reset values". Must be fixed
        -When  "delete_material" is called then the "material_control_panel" is not rendered correctly if the mode is in "stepped" mode
        -If the text for the lowest material must be drawn in a text box, it might be pushed under the canvas if there are other text boxes over it
        -If the UI_FRAME_WIDTH is changed, then the CANVAS_PROGRAM_BORDER_WIDTH must also be changed so that it fits the program window correctly
            

    #HOW TO CREATE AN EXECUTABLE FILE:
        -Navigate to the folder containing the python program
        -Run the following command: "python -m PyInstaller --onefile program_name.py"