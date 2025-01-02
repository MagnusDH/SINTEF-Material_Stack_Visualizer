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
main_frame_width = 1225      
main_frame_height = 503
main_frame_background_color = "#00192c"


#MATERIAL ADJUSTMENT PANEL
material_adjustment_panel_width = 355
material_adjustment_panel_height = 405
material_adjustment_panel_padding_top = 5
material_adjustment_panel_padding_bottom = 0
material_adjustment_panel_padding_right = 0
material_adjustment_panel_padding_left = 5
material_adjustment_panel_background_color = "#284154"
material_adjustment_panel_text_color = "white"
material_adjustment_panel_entry_background_color = "white"
material_adjustment_panel_entry_width = 60
material_adjustment_panel_entry_height = 10
material_adjustment_panel_slider_width = 130
material_adjustment_panel_slider_height = 17
material_adjustment_panel_slider_range_min = 0
material_adjustment_panel_slider_range_max = 6000
material_adjustment_panel_slider_color = "#00192c"
material_adjustment_panel_slider_hover_color = "#009ffb"
material_adjustment_panel_button_color = "#0080ca"
material_adjustment_panel_button_hover_color = "#009ffb"


#MATERIAL CONTROL PANEL
material_control_panel_width = 378
material_control_panel_height = 70
material_control_panel_background_color = material_adjustment_panel_background_color
material_control_panel_padding_top = 5
material_control_panel_padding_bottom = 0
material_control_panel_padding_right = 0
material_control_panel_padding_left = 5
material_control_panel_button_color = material_adjustment_panel_button_color
material_control_panel_button_hover_color = material_adjustment_panel_button_hover_color
material_control_panel_text_color = "white"



#ADD MATERIAL WINDOW
add_material_window_width = 400
add_material_window_height = 420
add_material_window_background_color = material_adjustment_panel_background_color
add_material_window_text_color = "white"
add_material_window_button_color = material_adjustment_panel_button_color
add_material_window_button_hover_color = material_adjustment_panel_button_hover_color


#MODIFY MATERIAL WINDOW
modify_material_window_width = 1550
modify_material_window_height = 500
modify_material_window_background_color = main_frame_background_color
modify_material_window_button_color = material_adjustment_panel_button_color
modify_material_window_button_hover_color = material_adjustment_panel_button_hover_color
modify_material_window_text_size = 14
modify_material_window_text_color = "white"
modify_material_window_text_font = "Arial"
modify_material_window_entry_width = 90
modify_material_window_scrollable_frame_width = 1200
modify_material_window_scrollable_frame_height = 300
modify_material_window_scrollable_frame_color = "#444444"


#LAYER STACK CANVAS
layer_stack_canvas_width = 1040
layer_stack_canvas_height = 520
layer_stack_canvas_padding_top = 5
layer_stack_canvas_padding_bottom = 0
layer_stack_canvas_padding_left = 5
layer_stack_canvas_padding_right = 0
layer_stack_canvas_background_color = "#a1e9ff"
layer_stack_canvas_outline_color = layer_stack_canvas_background_color
layer_stack_canvas_text_indent = 150                                                #WIDTH OF RECTANGLES
layer_stack_canvas_text_color = "black"
layer_stack_canvas_text_size = 10
layer_stack_canvas_rectangle_outline_color = layer_stack_canvas_background_color
layer_stack_canvas_indent_right_side = 100
layer_stack_canvas_indent_left_side = 150
# layer_stack_canvas_indent_top = 0
layer_stack_canvas_stepped_indent_top = 0


#CANVAS CONTROL PANEL
layer_stack_canvas_control_panel_width = layer_stack_canvas_width * 0.8
layer_stack_canvas_control_panel_height = 70
layer_stack_canvas_control_panel_padding_top = 5
layer_stack_canvas_control_panel_padding_bottom = 0
layer_stack_canvas_control_panel_padding_right = 0
layer_stack_canvas_control_panel_padding_left = 5
layer_stack_canvas_control_panel_background_color = material_adjustment_panel_background_color
layer_stack_canvas_control_panel_text_color = "white"
layer_stack_canvas_control_panel_button_color = material_adjustment_panel_button_color
layer_stack_canvas_control_panel_button_hover_color = material_adjustment_panel_button_hover_color


#GRAPH FRAME
graph_frame_width = 585
graph_frame_height = 500
graph_frame_background_color = material_adjustment_panel_background_color
graph_frame_padding_top = 5
graph_frame_padding_bottom = 0
graph_frame_padding_left = 5
graph_frame_padding_right = 0


#GRAPH
graph_width = 560
graph_height = 555
graph_dpi = 75                  #resolution (100 = 100% original size)
graph_x_axis_range_min = -100
graph_x_axis_range_max = 100
graph_y_axis_range_min = -100
graph_y_axis_range_max = 100


#GRAPH CONTROL PANEL
graph_control_panel_width = 525 * 0.8
graph_control_panel_height = 70
graph_control_panel_background_color = material_adjustment_panel_background_color
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
graph_control_panel_slider_button_color = material_adjustment_panel_button_color
graph_control_panel_slider_hover_color = material_adjustment_panel_button_hover_color


#SVG
svg_text_size = 14