class Settings:
    #Program settings
    PROGRAM_TITLE = "Layer stack visualizer"    #Title to be displayed on the program window
    PROGRAM_WINDOW_WIDTH = 1500                 #Initial width of program window
    PROGRAM_WINDOW_HEIGHT = 600                 #Initial height of program window
    PROGRAM_BACKGROUND_COLOR = "#00192c"
    PROGRAM_BACKGROUND_PHOTO = "bg.jpg"
    EXCEL_FILE = "Materials.xlsx"               #Excel-file to load materials from
    
    #User interface settings
    UI_FRAME_HEIGHT = 350
    UI_FRAME_WIDTH = 350
    UI_FRAME_BACKGROUND_COLOR = "#284154"
    UI_FRAME_TEXT_COLOR = "white"
    UI_LABEL_BACKGROUND_COLOR = "#284154"
    UI_ENTRY_BACKGROUND_COLOR = "lightgrey"
    SLIDER_RANGE_MIN = 1
    SLIDER_RANGE_MAX = 6000
    SLIDER_LINE_COLOR = "#00192c" 
    BUTTON_FG_COLOR = "#284154"
    BUTTON_HOVER_COLOR = "#009ffb"
    
    #Canvas settings
    CANVAS_HEIGHT = 400
    CANVAS_WIDTH = 1000
    CANVAS_PROGRAM_BORDER_WIDTH = 0             #How big the gap between the canvas border and the program-window edge width is
    CANVAS_PROGRAM_BORDER_HEIGHT = 0            #How big the gap between the canvas border and the program-window edge height is
    CANVAS_BACKGROUND_COLOR = "#5692bf"
    CANVAS_OUTLINE_COLOR = "#666666"
    TEXT_SIZE = 10                              #Text size on the canvas
    TEXT_FONT = "Arial"                         
    TEXT_COLOR = "black"
    STACK_TEXT_INDENT = 150                     #How much space is left in the side of the stack for text
    RECTANGLE_OUTLINE_COLOR = "black"

    #SVG-export settings
    SVG_TEXT_SIZE = 14