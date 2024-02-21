class Settings:
    #Program settings
    PROGRAM_TITLE = "Layer stack visualizer"    #Title to be displayed on the program window
    PROGRAM_WINDOW_WIDTH = 1000                 #Initial width of program window
    PROGRAM_WINDOW_HEIGHT = 850                 #Initial height of program window
    EXCEL_FILE = "Materials.xlsx"               #Excel-file to load materials from
    
    #User interface settings
    SLIDER_RANGE_MIN = None
    SLIDER_RANGE_MAX = None 
    
    #Stack settings
    TEXT_SIZE = 10                              #Text size on the canvas
    TEXT_FONT = "Arial"                         
    STACK_TEXT_INDENT = 150                     #How much the stack is minimized to leave space for text on the side
    INDENT_RANGE = 70000                        #How much the indent will be between layers in the "stepped stack" 

    #Color settings
    PROGRAM_BACKGROUND_COLOR = None
    CANVAS_BACKGROUND_COLOR = None
    FRAME_BACKGROUND_COLOR = None
    SLIDER_BACKGROUND_COLOR = None

    #SVG-export settings
    SVG_TEXT_SIZE = 14