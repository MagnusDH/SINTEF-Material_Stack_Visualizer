#PROGRAM WINDOW
program_window_title = "Layer stack visualizer"
program_window_width = 1300
program_window_height = int(program_window_width * 0.5625) #Same aspect as a HD and 4K screen
program_window_background_color = "black"# "#4c4c4c"
text_size = 10
text_font = "Arial"
text_color = "black"
# widget_scaling = 1.0            #Option to scale widgets up or down (1.0 is no scaling)
# program_window_scaling = 1.0    #Option to scale the program_window up or down (1.0 is no scaling)


# #BACKGROUND CANVAS
# background_canvas_background_color = "red"#"white"
# scrollbar_width = 15
# scrollbar_border_spacing = 3
# scrollbar_background_color = "blue"#"#4c4c4c"


# #MAIN FRAME
# main_frame_width = 1225      
# main_frame_height = 503
# main_frame_background_color = "green"# "#00192c"
# main_frame_minimum_width = 600
# main_frame_minimum_height = 400



# #MATERIAL ADJUSTMENT PANEL
# material_adjustment_panel_width = 355
# material_adjustment_panel_height = 405

# material_adjustment_panel_minimum_width = 405
# material_adjustment_panel_minimum_height = 405


material_adjustment_panel_padding_top = 0
material_adjustment_panel_padding_bottom = 1
material_adjustment_panel_padding_right = 1
material_adjustment_panel_padding_left = 0
material_adjustment_panel_background_color = "#284154"
material_adjustment_panel_text_color = "white"
material_adjustment_panel_entry_background_color = "white"
# material_adjustment_panel_entry_width = 60
# material_adjustment_panel_entry_height = 10
# material_adjustment_panel_slider_width = 130
# material_adjustment_panel_slider_height = 17
material_adjustment_panel_slider_range_min = 0
material_adjustment_panel_slider_range_max = 6000
material_adjustment_panel_slider_color = "#00192c"
material_adjustment_panel_slider_hover_color = "#009ffb"
# material_adjustment_panel_button_color = "#0080ca"
material_adjustment_panel_button_hover_color = "#009ffb"


# #MATERIAL CONTROL PANEL
# material_control_panel_width = 378
# material_control_panel_height = 70
material_control_panel_background_color = material_adjustment_panel_background_color
material_control_panel_padding_top = 1
material_control_panel_padding_bottom = 0
material_control_panel_padding_right = 1
material_control_panel_padding_left = 0
material_control_panel_button_color = "#0080ca"
material_control_panel_button_hover_color = "#009ffb"
material_control_panel_text_color = "white"



# #ADD MATERIAL WINDOW
add_material_window_width = 400
add_material_window_height = 420
add_material_window_background_color = material_adjustment_panel_background_color
add_material_window_text_color = "white"
add_material_window_button_color = "#0080ca"
add_material_window_button_hover_color = "#009ffb"


# #MODIFY MATERIAL WINDOW
modify_material_window_width = 1100
modify_material_window_height = int(modify_material_window_width * 0.5625) #Same aspect as a HD and 4K screen
modify_material_window_background_color = "#444444"
modify_material_window_button_color = "#0080ca"
modify_material_window_button_hover_color = "#009ffb"
modify_material_window_text_size = 12
modify_material_window_text_color = "white"
modify_material_window_text_font = "Arial"
# modify_material_window_entry_width = 90
# modify_material_window_scrollable_frame_width = 1200
# modify_material_window_scrollable_frame_height = 300
modify_material_window_scrollable_frame_color = "#00192c" 


# #LAYER STACK CANVAS
# layer_stack_canvas_width = 1040
# layer_stack_canvas_height = 520
layer_stack_canvas_padding_top = 2
layer_stack_canvas_padding_bottom = 1
layer_stack_canvas_padding_left = 1
layer_stack_canvas_padding_right = 2
layer_stack_canvas_background_color = "white"#"#a1e9ff"
layer_stack_canvas_outline_color = "black"
layer_stack_canvas_text_indent = 150                                                #WIDTH OF RECTANGLES
layer_stack_canvas_text_color = "black"
layer_stack_canvas_text_size = 10
layer_stack_canvas_rectangle_outline_color = "black"#layer_stack_canvas_background_color
layer_stack_canvas_indent_right_side = 100
layer_stack_canvas_indent_left_side = 150
# layer_stack_canvas_indent_top = 0
layer_stack_canvas_stepped_indent_top = 0


# #CANVAS CONTROL PANEL
# canvas_control_panel_width = layer_stack_canvas_width * 0.8
# canvas_control_panel_height = 70
canvas_control_panel_padding_top = 1
canvas_control_panel_padding_bottom = 0
canvas_control_panel_padding_right = 1
canvas_control_panel_padding_left = 1
canvas_control_panel_background_color = material_adjustment_panel_background_color
canvas_control_panel_text_color = "white"
canvas_control_panel_button_color = "#0080ca"
canvas_control_panel_button_hover_color = "#009ffb"


# #GRAPH FRAME
# graph_frame_width = 585
# graph_frame_height = 500
# graph_frame_background_color = material_adjustment_panel_background_color
# graph_frame_padding_top = 5
# graph_frame_padding_bottom = 0
# graph_frame_padding_left = 5
# graph_frame_padding_right = 0


#GRAPH
# graph_width = 1
# graph_height = 1
graph_resolution = 75                  #resolution (100 = 100% original size)
graph_x_axis_range_min = -250
graph_x_axis_range_max = 250
graph_y_axis_range_min = -250
graph_y_axis_range_max = 250


# #GRAPH CONTROL PANEL
# graph_control_panel_width = 525 * 0.8
# graph_control_panel_height = 70
graph_control_panel_background_color = material_adjustment_panel_background_color
graph_control_panel_padding_top = 1
graph_control_panel_padding_bottom = 0
graph_control_panel_padding_left = 1
graph_control_panel_padding_right = 0
graph_control_panel_button_color = "#0080ca"
graph_control_panel_button_hover_color = "#009ffb"


#SVG
svg_text_size = 14