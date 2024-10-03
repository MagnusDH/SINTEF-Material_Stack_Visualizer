#PROGRAM WINDOW
program_window_title = "Layer stack visualizer"
program_window_width = 1550
program_window_height = 650
program_window_background_color = "#4c4c4c"
text_size = 10
text_font = "Arial"
text_color = "black"
widget_scaling = 1.0            #Option to scale widgets up or down (1.0 is no scaling)
program_window_scaling = 1.0    #Option to scale the program_window up or down (1.0 is no scaling)


#BACKGROUND CANVAS
background_canvas_background_color = "white"


#CANVAS SCROLLBARS
scrollbar_width = 15
scrollbar_border_spacing = 3
scrollbar_background_color = "#4c4c4c"


#MAIN FRAME
main_frame_width = program_window_width * 0.8      #Scaling for widgets is different, and is around 75% of the main program_window
main_frame_height = program_window_height * 0.75    #Scaling for widgets is different, and is around 75% of the main program_window
main_frame_background_color = "#00192c"


#MATERIAL CONTROL PANEL
material_control_panel_width = 340
material_control_panel_height = 340
material_control_panel_padding_top = 5
material_control_panel_padding_bottom = 0
material_control_panel_padding_right = 0
material_control_panel_padding_left = 5
material_control_panel_background_color = "#284154"
material_control_panel_text_color = "white"
material_control_panel_entry_background_color = "white"
material_control_panel_entry_width = 60
material_control_panel_entry_height = 10
material_control_panel_slider_width = 130
material_control_panel_slider_height = 17
material_control_panel_slider_range_min = 0
material_control_panel_slider_range_max = 6000
material_control_panel_slider_color = "#00192c"
material_control_panel_slider_hover_color = "#009ffb"
material_control_panel_button_color = "#0080ca"
material_control_panel_button_hover_color = "#009ffb"


#POP UP WINDOW FOR ADDING MATERIAL
add_material_window_width = 300
add_material_window_height = 200
add_material_window_background_color = "#284154"
add_material_window_text_color = "white"
add_material_window_button_color = "#0080ca"
add_material_window_button_hover_color = "#009ffb"


#LAYER STACK CANVAS
layer_stack_canvas_width = 500
layer_stack_canvas_height = 440
layer_stack_canvas_padding_top = 5
layer_stack_canvas_padding_bottom = 0
layer_stack_canvas_padding_left = 5
layer_stack_canvas_padding_right = 0
layer_stack_canvas_background_color = "#a1e9ff"
layer_stack_canvas_outline_color = "#666666"
layer_stack_canvas_text_indent = 150
layer_stack_canvas_rectangle_outline_color = "black"
layer_stack_canvas_indent_right_side = 100
layer_stack_canvas_indent_left_side = 150
# layer_stack_canvas_indent_top = 0
layer_stack_canvas_stepped_indent_top = 0


#LAYER STACK CANVAS CONTROL PANEL
layer_stack_canvas_control_panel_width = 400
layer_stack_canvas_control_panel_height = 100
layer_stack_canvas_control_panel_padding_top = 5
layer_stack_canvas_control_panel_padding_bottom = 0
layer_stack_canvas_control_panel_padding_right = 0
layer_stack_canvas_control_panel_padding_left = 5
layer_stack_canvas_control_panel_background_color = "#284154"
layer_stack_canvas_control_panel_text_color = "white"
layer_stack_canvas_control_panel_button_color = "#0080ca"
layer_stack_canvas_control_panel_button_hover_color = "#009ffb"


#GRAPH FRAME
graph_frame_width = 400
graph_frame_height = 352
graph_frame_background_color = material_control_panel_background_color
graph_frame_padding_top = 5
graph_frame_padding_bottom = 0
graph_frame_padding_left = 5
graph_frame_padding_right = 0


#GRAPH
graph_width = 580
graph_height = 470
graph_dpi = 75                  #resolution (100 = 100% original size)
graph_x_axis_range_min = -100
graph_x_axis_range_max = 100
graph_y_axis_range_min = -100
graph_y_axis_range_max = 100


#GRAPH CONTROL PANEL
graph_control_panel_width = 400
graph_control_panel_height = 100
graph_control_panel_background_color = material_control_panel_background_color
graph_control_panel_padding_top = 5
graph_control_panel_padding_bottom = 0
graph_control_panel_padding_left = 5
graph_control_panel_padding_right = 0
graph_control_panel_slider_width = 300
graph_control_panel_slider_height = 20
graph_control_panel_slider_range_min = graph_x_axis_range_min
graph_control_panel_slider_range_max = graph_x_axis_range_max
graph_control_panel_slider_background_color = main_frame_background_color
graph_control_panel_slider_progress_color = main_frame_background_color
graph_control_panel_slider_button_color = material_control_panel_button_color
graph_control_panel_slider_hover_color = material_control_panel_button_hover_color


#SVG
svg_text_size = 14