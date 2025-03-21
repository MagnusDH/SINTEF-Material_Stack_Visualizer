import tkinter
from tkinter import StringVar
import customtkinter
import settings
import globals
import os
from Graph import Graph
from Graph_Control_Panel import Graph_Control_Panel


#This class handles the buttons that perform actions on the canvas
class Canvas_Control_Panel:
    def __init__(self, window):
        # print("CANVAS_CONTROL_PANEL_INIT()")
        
        self.program_window = window

        self.canvas_control_panel_frame = self.create_canvas_control_panel()


    """Creates a frame with widgets that performs actions on the layer_stack_canvas"""
    def create_canvas_control_panel(self):
        # print("CREATE_CANVAS_CONTROL_PANEL()")

        #if canvas_control_panel_frame has NOT been created before, create it
        if not hasattr(self, 'canvas_control_panel_frame'):
            #Create Frame from the control panel and place it within given window
            canvas_control_panel_frame = customtkinter.CTkFrame(
                master=self.program_window,
                fg_color=settings.canvas_control_panel_background_color
            )
            canvas_control_panel_frame.grid(
                row=1,
                column=1,
                padx=(settings.canvas_control_panel_padding_left, settings.canvas_control_panel_padding_right),
                pady=(settings.canvas_control_panel_padding_top, settings.canvas_control_panel_padding_bottom),
                sticky="nsew"
            )

            #Define the row&column layout of the material_control_panel_frame
            canvas_control_panel_frame.columnconfigure(0, weight=33, uniform="group1")
            canvas_control_panel_frame.columnconfigure(1, weight=33, uniform="group1")
            canvas_control_panel_frame.columnconfigure(2, weight=33, uniform="group1")

            canvas_control_panel_frame.rowconfigure(0, weight=50, uniform="group1")
            canvas_control_panel_frame.rowconfigure(1, weight=50, uniform="group1") 

        #Export stack as SVG button
        export_stack_as_svg_button = customtkinter.CTkButton(
            master=canvas_control_panel_frame,
            text="Export stack",
            text_color=settings.canvas_control_panel_text_color,
            font=(settings.text_font, settings.canvas_control_panel_text_size),
            fg_color= settings.canvas_control_panel_button_color, 
            hover_color=settings.canvas_control_panel_button_hover_color, 
            command=self.export_stack_as_svg
        )
        export_stack_as_svg_button.grid(
            row=0, 
            column=0, 
            sticky="nsew", 
            padx=(5,5), 
            pady=(5,5)
        )

        #Export layers as SVG button
        export_layers_as_svg_button = customtkinter.CTkButton(
            master=canvas_control_panel_frame,
            text="Export layers",
            text_color=settings.canvas_control_panel_text_color,
            font=(settings.text_font, settings.canvas_control_panel_text_size),
            fg_color= settings.canvas_control_panel_button_color, 
            hover_color=settings.canvas_control_panel_button_hover_color, 
            command=self.export_layers_as_svg
        )
        export_layers_as_svg_button.grid(
            row=1, 
            column=0, 
            sticky="nsew", 
            padx=(5,5), 
            pady=(5,5)
        )

        #Reset canvas button
        reset_canvas_button = customtkinter.CTkButton(
            master=canvas_control_panel_frame, 
            text="Reset canvas", 
            text_color=settings.canvas_control_panel_text_color,
            font=(settings.text_font, settings.canvas_control_panel_text_size),
            fg_color=settings.canvas_control_panel_button_color, 
            hover_color=settings.canvas_control_panel_button_hover_color, 
            command=self.reset_canvas
        )
        reset_canvas_button.grid(
            row=1, 
            column=1, 
            sticky="nsew", 
            padx=(5,5), 
            pady=(5,5)
        )    

        #Option menu "view" label
        option_menu_view_label = customtkinter.CTkLabel(
            master=canvas_control_panel_frame,
            text="View", 
            text_color=settings.canvas_control_panel_text_color,
            font=(settings.text_font, settings.canvas_control_panel_text_size, "bold"),
            # font=(settings.text_font, 15, "bold")
            bg_color=settings.canvas_control_panel_background_color
        )
        option_menu_view_label.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(5,5),
            pady=(5,5)
        )

        #Switch layout option menu
        self.option_menu = customtkinter.CTkOptionMenu(
            master=canvas_control_panel_frame, 
            values=["Stacked", "Realistic", "Stepped", "Stoney", "Multi"],
            text_color=settings.canvas_control_panel_text_color,
            font=(settings.text_font, settings.canvas_control_panel_text_size),
            fg_color=settings.canvas_control_panel_button_color, 
            bg_color=settings.canvas_control_panel_background_color,
            button_hover_color=settings.canvas_control_panel_button_hover_color,
            command=self.switch_layout
        )
        self.option_menu.grid(
            row=1, 
            column=2, 
            sticky="nsew",
            padx=(5,5), 
            pady=(5,5)
        )

        self.option_menu.set(globals.option_menu)

        return canvas_control_panel_frame

    
    """Resets the scale of items and the start drawing point on the canvas back to their original scale and place"""
    def reset_canvas(self):
        # print("CLASS CANVAS_CONTROL_PANEL -> RESET_CANVAS()")

        #Find the original scale of the canvas
        inverse_scale = 1.0 / globals.layer_stack_canvas.current_scale

        #Scale all items back to their original size
        globals.layer_stack_canvas.layer_stack_canvas.scale("all", 0, 0, inverse_scale, inverse_scale)

        #Reset the original scale
        globals.layer_stack_canvas.current_scale = 1.0

        #Move the canvas back to its original drawing point
        globals.layer_stack_canvas.layer_stack_canvas.xview_moveto(0)
        globals.layer_stack_canvas.layer_stack_canvas.yview_moveto(0)

        #Redraw material stack
        globals.layer_stack_canvas.draw_material_stack()


    """
    -Changes the Label explaining what is being modified by sliders and entries in the Material_Adjustment_Panel
    -Changes the values for sliders and entries
    -Changes the layout of the program window for each 'view' mode
    """
    def switch_layout(self, *event):
        # print("SWITCH_LAYOUT()")

        #Switch the option in globals.option_menu
        globals.option_menu = self.option_menu.get()

        #Remove the graph if it exists
        if hasattr(globals.graph, 'graph_translator'):
            globals.graph.graph_translator.get_tk_widget().destroy()
            del globals.graph.graph_translator

        #Delete the graph_control_panel if it exists
        if(hasattr(globals.graph_control_panel, 'graph_control_panel')):
            globals.graph_control_panel.graph_control_panel.destroy()   #Destroy the widget
            del globals.graph_control_panel.graph_control_panel         #Delete the reference in memory

        #Create a new material_adjustment_panel with a different layout based on the option menu
        globals.material_adjustment_panel.create_material_adjustment_panel()
        
        #Switch UI layout based on option value
        match self.option_menu.get():
            case "Stacked" | "Realistic":
                #Change the layout of the program_window to only two columns
                self.program_window.columnconfigure(0, weight=1, minsize=500, uniform="group1")  #set this column to a specific size that won't change
                self.program_window.columnconfigure(1, weight=9, uniform="group1")  
                self.program_window.grid_columnconfigure(2, weight=0, uniform=None)

                #Set all material entry and slider values to "thickness" value, and mark all as "active"
                for material in globals.materials:
                    globals.materials[material]["Slider_id"].set(globals.materials[material]["Thickness"])
                    globals.materials[material]["Entry_id"].configure(textvariable=StringVar(value=str(globals.materials[material]["Thickness"])))
                    globals.materials[material]["Status"] = "active"


                #Update the sizes for layer_stack_canvas      
                self.program_window.update()
                globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_width() - 1
                globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_height() - 1
                globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0
                globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0

                #Draw material stack                
                globals.layer_stack_canvas.draw_material_stack()


            case "Stepped":
                #Change the layout of the program_window to only two columns
                self.program_window.columnconfigure(0, weight=1, minsize=500, uniform="group1")  #set this column to a specific size that won't change
                self.program_window.columnconfigure(1, weight=9, uniform="group1")  
                self.program_window.grid_columnconfigure(2, weight=0, uniform=None)


                #Set all material entry and slider values to "indent" value, and mark all as "active"
                for material in globals.materials:
                    globals.materials[material]["Slider_id"].set(globals.materials[material]["Indent [nm]"])
                    globals.materials[material]["Entry_id"].configure(textvariable=StringVar(value=str(globals.materials[material]["Indent [nm]"])))
                    globals.materials[material]["Status"] = "active"

                #Update the sizes for layer_stack_canvas      
                self.program_window.update()
                globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_width() - 1
                globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_height() - 1
                globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0
                globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0
                        
                #Draw the material stack
                globals.layer_stack_canvas.draw_material_stack()


            case "Stoney":
                #Change the layout of the program_window to make space for Graph
                self.program_window.columnconfigure(0, minsize=450, weight=0, uniform=None)
                self.program_window.columnconfigure(1, weight=1, uniform="group2")
                self.program_window.columnconfigure(2, weight=1, uniform="group2")

                #Set all material entry and slider values to "thickness" value
                #Set all materials "Status", except "substrate" to "inactive
                for material in globals.materials:
                    globals.materials[material]["Slider_id"].set(globals.materials[material]["Thickness"])
                    globals.materials[material]["Entry_id"].configure(textvariable=StringVar(value=str(globals.materials[material]["Thickness"])))
                    globals.materials[material]["Status"] = "inactive"
                    globals.materials[material]["Checkbox_id"].deselect()

                    if(material.lower() == "substrate"):
                        globals.materials[material]["Status"] = "active"
                        globals.materials[material]["Checkbox_id"].select()


                #Update the sizes for layer_stack_canvas      
                self.program_window.update()
                globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_width() - 1
                globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_height() - 1
                globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0
                globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0

                #Redraw material stack
                globals.layer_stack_canvas.draw_material_stack()

                #Create Graph
                globals.graph = Graph(self.program_window)

                #Create panel that controls the actions of the graph
                globals.graph_control_panel = Graph_Control_Panel(self.program_window)

            case "Multi":
                #Change the layout of the program_window to only two columns
                self.program_window.columnconfigure(0, weight=1, minsize=500, uniform="group1")  #set this column to a specific size that won't change
                self.program_window.columnconfigure(1, weight=9, uniform="group1")  
                self.program_window.grid_columnconfigure(2, weight=0, uniform=None)

                #Set all material entry and slider values to "thickness" value, and mark all as "active"
                for material in globals.materials:
                    globals.materials[material]["Slider_id"].set(globals.materials[material]["Thickness"])
                    globals.materials[material]["Entry_id"].configure(textvariable=StringVar(value=str(globals.materials[material]["Thickness"])))
                    globals.materials[material]["Status"] = "active"


                #Update the sizes for layer_stack_canvas      
                self.program_window.update()
                globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_width() - 1
                globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_height() - 1
                globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0
                globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0

                #Draw material stack                
                globals.layer_stack_canvas.draw_material_stack()

    """Exports the stack without material names as SVG file"""
    def export_stack_as_svg(self):
        # print("EXPORT_STACK_AS_SVG()")

        #CREATE FOLDER HIERARCHY
        main_folder = "exports"                                 #Name for main folder
        #Create main folder if it does not exist
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)
        
        sub_folder_name = globals.option_menu                            #Name for sub_folder
        #Create path for sub_folder
        sub_folder_path = os.path.join(main_folder, sub_folder_name)
        
        #Create sub_folder if it does not exist
        if not os.path.exists(f"{main_folder}/{sub_folder_name}"):
            os.makedirs(sub_folder_path)

        #Create name for the file
        filename = f"stack_{globals.option_menu}.svg"

        #Create path for the file to be saved in
        file_path = os.path.join(sub_folder_path, filename)

        #Open the file for writing
        with open(file_path, 'w') as f:
            #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

            #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
            f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.program_window.winfo_width(), self.program_window.winfo_height()))


            #Go through every rectangle found on canvas
            for material in globals.materials:
                #Only create element of rectangle if it is not "None"
                if(globals.materials[material]["Rectangle_id"] != None):

                    #Find the coordinates of the rectangle
                    rect_x0, rect_y0, rect_x1, rect_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Rectangle_id"])
                    #Construct an SVG <rect> element for the rectangle
                    svg_rect_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, globals.materials[material]["Color"])
                    #Write the SVG representation of the rectangle to the file
                    f.write(svg_rect_element)
                    #Construct an SVG <rect> element for the bounding box
                    svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, settings.layer_stack_canvas_rectangle_outline_color)
                    # Write the SVG representation of the bounding box to the file
                    f.write(svg_bbox_element)

            #Write the closing SVG tag to the file, completing the SVG file.
            f.write('</svg>\n')

        #Close the SVG file
        f.close()

   
    """Exports every layer of the stack with text and arrows as SVG-file"""
    def export_layers_as_svg(self):
        # print("EXPORT_LAYERS_AS_SVG()")

        #CREATE FOLDER HIERARCHY
        #Specify a folder where the SVG-files should be saved
        main_folder = "exports"
        #Create the folder if it doesn't exist
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        #Name for sub_folder
        sub_folder_name = globals.option_menu
        
        #Create path for sub_folder
        sub_folder_path = os.path.join(main_folder, sub_folder_name)
        
        #Create sub_folder if it does not exist
        if not os.path.exists(f"{main_folder}/{sub_folder_name}"):
            os.makedirs(sub_folder_path)

        
        #Each SVG-file is assigned a number based on how many layers are in each file
        layer_counter = 1
        previously_created_elements = []

        #Iterate through all the materials
        for material in dict(reversed(globals.materials.items())):
            #Only create svg element if there is a rectangle
            if(globals.materials[material]["Rectangle_id"] != None):

                #Create a name for the SVG file for the current layer
                filename = f"{layer_counter}_layer_{globals.option_menu}.svg"

                #Create the file path by joining the folder path and the filename
                file_path = os.path.join(sub_folder_path, filename)

                #Open file for writing
                with open(file_path, 'w') as f:
                    #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
                    f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                    #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
                    f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.program_window.winfo_width(), self.program_window.winfo_height())) 


                    #Write the previous created elements to the current file
                    if(len(previously_created_elements) != 0):
                        for element in previously_created_elements:
                            f.write(element)

                    #Create SVG-element of material rectangle
                    if(globals.materials[material]["Rectangle_id"] != None):
                        rect_x0, rect_y0, rect_x1, rect_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Rectangle_id"])

                        svg_rectangle_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, globals.materials[material]["Color"])
                        f.write(svg_rectangle_element)
                        previously_created_elements.append(svg_rectangle_element)

                        #Create SVG-element for the rectangle bounding box and write it to file
                        svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, settings.layer_stack_canvas_rectangle_outline_color)
                        f.write(svg_bbox_element)
                        previously_created_elements.append(svg_bbox_element)
                    else: 
                        break

                    #Create SVG-element for material text
                    if(globals.materials[material]["Text_id"] is not None):
                        text_x0, text_y0 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Text_id"])
                        text_content = globals.layer_stack_canvas.layer_stack_canvas.itemcget(globals.materials[material]["Text_id"], 'text')
                        svg_text_element = '<text x="{}" y="{}" fill="{}" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(text_x0, text_y0, settings.text_color, settings.svg_text_size, text_content)
                        f.write(svg_text_element)
                        previously_created_elements.append(svg_text_element)

                    #Create SVG-element for text bounding box
                    if(globals.materials[material]["Text_bbox_id"] is not None):
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black"/>\n'.format(bbox_x0, bbox_y0, bbox_x1-bbox_x0, bbox_y1-bbox_y0, settings.text_color)
                            
                        #Write the SVG representation of the bounding box to the file
                        f.write(svg_bbox_element)
                        previously_created_elements.append(svg_bbox_element)

                    #Create SVG-element for arrow line pointing from box to rectangle
                    if(globals.materials[material]["Line_id"] != None):
                        #Line must be drawn from the right side of stack to left side of text
                        if(globals.option_menu == "Stacked" or globals.option_menu == "Realistic" or globals.option_menu == "Stoney"):
                            line_coords = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Line_id"])
                            #Construct an SVG <line> element for arrows
                            bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                            svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" marker-end="url(#arrow-end)" />\n'.format(bbox_x0, line_coords[1], line_coords[2]+7, line_coords[3], settings.text_color)

                            #Add arrowhead on the left side of the line
                            svg_line_element += (
                            '<defs>\n'
                            '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="180">\n'
                            '        <path d="M0,0 L0,6 L9,3 z" fill="black" />\n'
                            '    </marker>\n'
                            '</defs>\n'
                            )

                        #Line must be drawn from the left side of stack to right side of text
                        elif(globals.option_menu == "Stepped"):
                            line_x0, line_y0, line_x1, line_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Line_id"])
                            #Construct an SVG <line> element for arrows
                            bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                            svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" marker-end="url(#arrow-end)" />\n'.format(bbox_x1, line_y0, line_x1-7, line_y1, settings.text_color)
                            
                            #Add arrowhead on right side of the line
                            svg_line_element += (
                                '<defs>\n'
                                '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="180">\n'
                                '        <path d="M0,3 L9,0 L9,6 z" fill="black" />\n'
                                '    </marker>\n'
                                '</defs>\n'
                            )
                        #Write the SVG representation of the arrow to the file
                        f.write(svg_line_element)
                        previously_created_elements.append(svg_line_element)

                    #Create SVG-element for indent_text
                    if(globals.materials[material]["Indent_text_id"] != None):
                        indent_text_x0, indent_text_y0 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Indent_text_id"])
                        indent_text_content = globals.layer_stack_canvas.layer_stack_canvas.itemcget(globals.materials[material]["Indent_text_id"], 'text')
                        svg_indent_text_element = '<text x="{}" y="{}" fill="black" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(indent_text_x0, indent_text_y0, settings.svg_text_size, indent_text_content)
                            
                        f.write(svg_indent_text_element)
                        previously_created_elements.append(svg_indent_text_element)

                    #Create SVG-element for indent_text bounding box
                    if(globals.materials[material]["Indent_text_bbox_id"] != None):
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                        svg_indent_text_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black"/>\n'.format(bbox_x0, bbox_y0, bbox_x1-bbox_x0, bbox_y1-bbox_y0, settings.text_color)
                            
                        #Write the SVG representation of the bounding box to the file
                        f.write(svg_indent_text_bbox_element)
                        previously_created_elements.append(svg_indent_text_bbox_element)

                    #Create SVG-element for indent_line
                    if(globals.materials[material]["Indent_line_id"] != None):
                        indent_line_x0, indent_line_y0, indent_line_x1, indent_line_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Indent_line_id"])
                        #Construct an SVG <line> element for arrows
                        svg_indent_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="black" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />\n'.format(indent_line_x0+8, indent_line_y0, indent_line_x1-10, indent_line_y1)
                        
                        #Add arrowheads on both sides of the line
                        svg_indent_line_element += (
                            '<defs>\n'
                            '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="0">\n'
                            '        <path d="M0,0 L0,6 L9,3 z" fill="black" />\n'
                            '    </marker>\n'
                            '    <marker id="arrow-start" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="0">\n'
                            '        <path d="M0,3 L9,0 L9,6 z" fill="black" />\n'
                            '    </marker>\n'
                            '</defs>\n'
                        )
                        
                        #Write the SVG representation of the arrow to the file
                        f.write(svg_indent_line_element)
                        previously_created_elements.append(svg_indent_line_element)

                    #Create SVG-element for arrow line pointing from indent_text to indent_line
                    if(globals.materials[material]["Indent_arrow_pointer_id"] != None):
                        line_coords = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Indent_arrow_pointer_id"])
                        #Construct an SVG <line> element for arrows
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                        svg_indent_arrow_pointer_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" marker-end="url(#arrow-start)" />\n'.format(bbox_x0, line_coords[1], line_coords[2]+7, line_coords[3], settings.text_color)

                        #Add arrowhead on the left side of the line
                        svg_indent_arrow_pointer_element += (
                            '<defs>\n'
                            '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="180">\n'
                            '        <path d="M0,0 L0,6 L9,3 z" fill="black" />\n'
                            '    </marker>\n'
                            '</defs>\n'
                        )

                        #Write the SVG representation of the arrow to the file
                        f.write(svg_indent_arrow_pointer_element)
                        previously_created_elements.append(svg_indent_arrow_pointer_element)

                    #Write the closing SVG tag to the file, completing the SVG file
                    f.write('</svg>\n')

                #Close the svg file
                f.close()

                #Increment layer_counter
                layer_counter += 1


    def new_export_layers_as_svg(self):
        all_items = globals.layer_stack_canvas.layer_stack_canvas.find_all()

        print(len(all_items))

        for item in all_items:
            print(globals.layer_stack_canvas.layer_stack_canvas.type(item))




        #CHATGPT
    #     """Export a Tkinter Canvas to an SVG file."""
    #     width = canvas.winfo_width()
    #     height = canvas.winfo_height()
        
    #     svg_content = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']

    #     for item in canvas.find_all():
    #         item_type = canvas.type(item)
    #         coords = canvas.coords(item)
    #         color = canvas.itemcget(item, "fill")
    #         outline = canvas.itemcget(item, "outline")
    #         stroke_width = canvas.itemcget(item, "width")

    #         if item_type == "rectangle":
    #             x1, y1, x2, y2 = coords
    #             svg_content.append(
    #                 f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="{color}" stroke="{outline}" stroke-width="{stroke_width}" />'
    #             )

    #         elif item_type == "oval":
    #             x1, y1, x2, y2 = coords
    #             rx = (x2 - x1) / 2
    #             ry = (y2 - y1) / 2
    #             cx = x1 + rx
    #             cy = y1 + ry
    #             svg_content.append(
    #                 f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" stroke="{outline}" stroke-width="{stroke_width}" />'
    #             )

    #         elif item_type == "line":
    #             points = " ".join(f"{coords[i]},{coords[i+1]}" for i in range(0, len(coords), 2))
    #             svg_content.append(
    #                 f'<polyline points="{points}" fill="none" stroke="{outline}" stroke-width="{stroke_width}" />'
    #             )

    #         elif item_type == "text":
    #             x, y = coords
    #             text = canvas.itemcget(item, "text")
    #             font_size = canvas.itemcget(item, "font").split()[-1]  # Extract font size
    #             svg_content.append(
    #                 f'<text x="{x}" y="{y}" fill="{color}" font-size="{font_size}" text-anchor="middle">{text}</text>'
    #             )

    #     svg_content.append("</svg>")

    #     with open(filename, "w") as f:
    #         f.write("\n".join(svg_content))

    #     print(f"SVG file saved as {filename}")

    # # Example usage
    # root = tk.Tk()
    # canvas = tk.Canvas(root, width=400, height=300, bg="white")
    # canvas.pack()

    # # Create shapes
    # canvas.create_rectangle(50, 50, 150, 150, fill="blue", outline="black")
    # canvas.create_oval(200, 50, 300, 150, fill="red", outline="black")
    # canvas.create_line(50, 200, 350, 200, width=3, fill="green")
    # canvas.create_text(200, 250, text="Hello SVG", font=("Arial", 14), fill="black")

    # # Convert to SVG
    # canvas_to_svg(canvas, "canvas_output.svg")

