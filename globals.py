import tkinter

#The main dictionary where ALL materials and info about each material is stored
materials = {}

#Instance of classes
app = None
material_adjustment_panel = None
material_control_panel = None
new_panel = None
layer_stack_canvas = None
canvas_control_panel = None
graph = None
graph_control_panel = None
equations = None

#The start view for the program
current_view = "Multi"

#Reference to current sizes of program window
current_program_window_height = None
current_program_window_width = None