class Settings:
    #Program settings
    PROGRAM_TITLE = "Layer stack visualizer"    #Title to be displayed on the program window
    PROGRAM_WINDOW_WIDTH = 1000                 #Initial width of program window
    PROGRAM_WINDOW_HEIGHT = 500                 #Initial height of program window
    PROGRAM_BACKGROUND_COLOR = "#434343"
    EXCEL_FILE = "Materials.xlsx"               #Excel-file to load materials from
    
    #User interface settings
    UI_FRAME_HEIGHT = 300
    UI_FRAME_WIDTH = 350
    UI_FRAME_BACKGROUND_COLOR = "#212B33"
    UI_FRAME_TEXT_COLOR = "white"
    UI_LABEL_BACKGROUND_COLOR = "#434343"
    UI_ENTRY_BACKGROUND_COLOR = "lightgrey"#"#434343"
    SLIDER_RANGE_MIN = 1
    SLIDER_RANGE_MAX = 1000
    BUTTON_FG_COLOR = "#0085d2"
    BUTTON_HOVER_COLOR = "#009ffb"
    
    #Canvas settings
    CANVAS_HEIGHT = 400
    CANVAS_WIDTH = 500
    CANVAS_PROGRAM_BORDER_WIDTH = 30             #How big the gap between the canvas border and the program-window edge width is
    CANVAS_PROGRAM_BORDER_HEIGHT = 0            #How big the gap between the canvas border and the program-window edge height is
    CANVAS_BACKGROUND_COLOR = None
    TEXT_SIZE = 10                              #Text size on the canvas
    TEXT_FONT = "Arial"                         
    STACK_TEXT_INDENT = 150                     #How much the stack is minimized to leave space for text on the side
    INDENT_RANGE = 70000                        #How much the indent will be between layers in the "stepped stack" 

    #SVG-export settings
    SVG_TEXT_SIZE = 14