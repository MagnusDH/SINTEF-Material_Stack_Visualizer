# GUI program for visualizing thickness of materials in Python

    *How to run program:
        1. Open a terminal in the folder containing the "material_stack_visualizer.py" file
        2. Run one of the following commands:
            "python material_stack_visualizer.py"
            "python3 material_stack_visualizer.py"


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

    

    self.materials layout:

        Self.materials = {
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

    BUGS:
        -If the text for the lowest material must be drawn in a text box, it might be pushed under the canvas if there are other text boxes over it
        -If the UI_FRAME_WIDTH is changed, then the CANVAS_PROGRAM_BORDER_WIDTH must also be changed so that it fits the program window correctly

    #HOW TO CREATE AN EXECUTABLE FILE:
        -Navigate to the folder containing the python program
        -Run the following command: "python -m PyInstaller --onefile program_name.py"
