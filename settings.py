#PROGRAM WINDOW
program_window_title = "Layer stack visualizer"
program_window_width = 1300
program_window_height = int(program_window_width * 0.5625) #Same aspect as a HD and 4K screen
program_window_background_color = "black"
text_size = 10
text_font = "Arial"
text_color = "black"

#MATERIAL ADJUSTMENT PANEL
material_adjustment_panel_background_color = "#284154"
material_adjustment_panel_padding_top = 4
material_adjustment_panel_padding_bottom = 2
material_adjustment_panel_padding_right = 2
material_adjustment_panel_padding_left = 4
material_adjustment_panel_text_color = "#B1E0FF"

material_adjustment_panel_label_size = 15

material_adjustment_panel_entry_background_color = "#284154"
material_adjustment_panel_entry_border_color = "#B1E0FF"
material_adjustment_panel_entry_text_color = "#B1E0FF"

material_adjustment_panel_slider_range_min = 0
material_adjustment_panel_slider_range_max = 6000
material_adjustment_panel_slider_background_color = "black"
material_adjustment_panel_slider_button_color = "#B1E0FF"
material_adjustment_panel_slider_progress_color = "blue"
material_adjustment_panel_slider_hover_color = "#85A8BF"

material_adjustment_panel_button_color = "#B1E0FF"
material_adjustment_panel_button_hover_color = "#85A8BF"
material_adjustment_panel_button_text_color = "black"

material_adjustment_panel_delete_button_color = "#B1E0FF"
material_adjustment_panel_delete_button_hover_color = "#da0000"

material_adjustment_panel_checkbox_background_color = "#284154"
material_adjustment_panel_checkbox_border_color = "#B1E0FF"
material_adjustment_panel_checkbox_hover_color = "#85A8BF"
material_adjustment_panel_checkbox_checkmark_color = "#B1E0FF"


#MATERIAL CONTROL PANEL
material_control_panel_background_color = material_adjustment_panel_background_color
material_control_panel_padding_top = 2
material_control_panel_padding_bottom = 4
material_control_panel_padding_right = 2
material_control_panel_padding_left = 4
material_control_panel_button_color = "#B1E0FF"#"#0080ca"
material_control_panel_button_hover_color = "#85A8BF"#"#009ffb"
material_control_panel_button_text_color = "black" 
# material_control_panel_text_color = 
material_control_panel_text_size = 12


#ADD MATERIAL WINDOW
add_material_window_background_color = material_adjustment_panel_background_color
add_material_window_width = 400
add_material_window_height = 420
add_material_window_text_color = "#B1E0FF"

add_material_window_button_color = "#B1E0FF"
add_material_window_button_hover_color = "#85A8BF"
add_material_window_button_text_color = "black"

add_material_window_entry_background_color = "#284154"
add_material_window_entry_border_color = "#B1E0FF"
add_material_window_entry_text_color = "#B1E0FF"


#MODIFY MATERIAL WINDOW
modify_material_window_background_color = material_adjustment_panel_background_color
modify_material_window_scrollable_frame_background_color = material_adjustment_panel_background_color
modify_material_window_width = 1100
modify_material_window_height = int(modify_material_window_width * 0.5625) #Same aspect as a HD and 4K screen
modify_material_window_text_color = "#B1E0FF"
modify_material_window_text_font = "Arial"

modify_material_window_button_color = "#B1E0FF"
modify_material_window_button_hover_color = "#85A8BF"
modify_material_window_button_text_color = "black"

modify_material_window_entry_background_color = "#284154"
modify_material_window_entry_border_color = "#B1E0FF"
modify_material_window_entry_text_color = "#B1E0FF"

modify_material_window_text_size = 12


#LAYER STACK CANVAS
layer_stack_canvas_background_color = "white"
layer_stack_canvas_padding_top = 4
layer_stack_canvas_padding_bottom = 2
layer_stack_canvas_padding_left = 2
layer_stack_canvas_padding_right = 2
layer_stack_canvas_outline_color = "black"
layer_stack_canvas_text_color = "black"
layer_stack_canvas_text_size = 10
layer_stack_canvas_rectangle_outline_color = "black"
#STACKED
layer_stack_canvas_stacked_offset_right_side = 230             #HOW MUCH SPACE IS GIVEN TO TEXT ON THE RIGHT SIDE OF THE CANVAS IN STACKED/REALISTIC/STONEY VIEW
layer_stack_canvas_stacked_offset_left_side = 0
#REALISTIC
layer_stack_canvas_realistic_offset_left_side = 0
layer_stack_canvas_realistic_offset_right_side = 230
#STEPPED
layer_stack_canvas_stepped_offset_right_side = 200             #HOW MUCH SPACE IS GIVEN TO TEXT ON THE RIGHT SIDE OF THE CANVAS IN STEPPED VIEW 
layer_stack_canvas_stepped_offset_left_side = 200              #HOW MUCH SPACE IS GIVEN TO TEXT ON THE LEFT SIDE OF THE CANVAS IN STEPPED VIEW
#LIMITED
layer_stack_canvas_limited_offset_left_side = 0
layer_stack_canvas_limited_offset_right_side = 230
#MULTI
layer_stack_canvas_multi_offset_left_side = 250                     #HOW MUCH SPACE IS BETWEEN CANVAS WALL AND START OF STACK IN THE MULTI-VIEW
layer_stack_canvas_multi_offset_right_side = 150                    #HOW MUCH SPACE IS BETWEEN CANVAS WALL AND START OF STACK IN THE MULTI-VIEW


#CANVAS CONTROL PANEL
canvas_control_panel_background_color = material_adjustment_panel_background_color
canvas_control_panel_padding_top = 2
canvas_control_panel_padding_bottom = 4
canvas_control_panel_padding_right = 4
canvas_control_panel_padding_left = 2
canvas_control_panel_text_color = "#B1E0FF"
canvas_control_panel_button_color = "#B1E0FF"
canvas_control_panel_button_hover_color = "#85A8BF"
canvas_control_panel_button_text_color = "black"

canvas_control_panel_dropdown_color = "#B1E0FF"
canvas_control_panel_dropdown_button_color = "#B1E0FF"
canvas_control_panel_dropdown_button_hover_color = "#85A8BF"
canvas_control_panel_dropdown_text_color = "black"#"#B1E0FF"
canvas_control_panel_dropdown_background_color = "#B1E0FF"#material_adjustment_panel_background_color
canvas_control_panel_dropdown_hover_color = "#85A8BF"
canvas_control_panel_text_size = 12


#GRAPHS
graph_resolution = 75                  #resolution (100 = 100% original size)
stoney_graph_x_axis_range_min = -100
stoney_graph_x_axis_range_max = 100
stoney_graph_y_axis_range_min = -10
stoney_graph_y_axis_range_max = 50

stress_graph_x_axis_range_min = -100
stress_graph_x_axis_range_max = 100
stress_graph_y_axis_range_min = -100
stress_graph_y_axis_range_max = 100


#GRAPH CONTROL PANEL
graph_control_panel_background_color = material_adjustment_panel_background_color
graph_control_panel_padding_top = 1
graph_control_panel_padding_bottom = 0
graph_control_panel_padding_left = 1
graph_control_panel_padding_right = 0
graph_control_panel_button_color = "#B1E0FF"
graph_control_panel_button_hover_color = "#85A8BF"
graph_control_panel_button_text_color = "black"

#SVG
svg_text_size = 14
