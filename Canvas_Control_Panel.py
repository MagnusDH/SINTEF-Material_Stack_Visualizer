import tkinter
from tkinter import StringVar
import customtkinter
import settings
import globals
import os


#This class handles the buttons that perform actions on the canvas
class Canvas_Control_Panel:
    def __init__(self, window, row_placement:int, column_placement:int):
        # print("CANVAS_CONTROL_PANEL_INIT()")
        
        self.program_window = window

        #Row/column placement in main program window
        self.row_placement = row_placement
        self.column_placement = column_placement

        self.option_menu = None

        self.canvas_control_panel_frame = self.create_canvas_control_panel()


    def create_canvas_control_panel(self):
        """Creates a frame with widgets that performs actions on the layer_stack_canvas"""

        # print("CREATE_CANVAS_CONTROL_PANEL()")

        #if canvas_control_panel_frame has NOT been created before, create it
        if not hasattr(self, 'canvas_control_panel_frame'):
            #Create Frame from the control panel and place it within given window
            canvas_control_panel_frame = customtkinter.CTkFrame(
                master=self.program_window,
                fg_color=settings.canvas_control_panel_background_color
            )
            canvas_control_panel_frame.grid(
                row=self.row_placement,
                column=self.column_placement,
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


        #Export Option menu label
        export_option_menu_label = customtkinter.CTkLabel(
            master=canvas_control_panel_frame,
            text="Export", 
            text_color=settings.canvas_control_panel_text_color,
            font=(settings.text_font, settings.canvas_control_panel_text_size, "bold"),
            bg_color=settings.canvas_control_panel_background_color
        )
        export_option_menu_label.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(5,5),
            pady=(5,5)
        )

        #Export option menu
        self.export_option_menu = customtkinter.CTkOptionMenu(
            master=canvas_control_panel_frame, 
            values=["Full stack", "Material rectangles", "Layers"],
            font=(settings.text_font, settings.canvas_control_panel_text_size),
            bg_color=settings.canvas_control_panel_background_color,
            fg_color=settings.canvas_control_panel_dropdown_color,
            text_color=settings.canvas_control_panel_dropdown_text_color,
            button_color=settings.canvas_control_panel_dropdown_button_color,
            button_hover_color=settings.canvas_control_panel_dropdown_button_hover_color,
            dropdown_text_color=settings.canvas_control_panel_dropdown_text_color,
            dropdown_fg_color=settings.canvas_control_panel_dropdown_background_color,
            dropdown_hover_color=settings.canvas_control_panel_dropdown_hover_color,
            command=self.choose_stack_export
        )
        self.export_option_menu.grid(
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
            font=(settings.text_font, settings.canvas_control_panel_text_size),
            fg_color=settings.canvas_control_panel_button_color, 
            hover_color=settings.canvas_control_panel_button_hover_color, 
            text_color=settings.canvas_control_panel_button_text_color,
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
            values=["Stacked", "Realistic", "Stepped", "Multi"],
            variable=globals.current_view,
            font=(settings.text_font, settings.canvas_control_panel_text_size),
            bg_color=settings.canvas_control_panel_background_color,
            fg_color=settings.canvas_control_panel_dropdown_color,
            text_color=settings.canvas_control_panel_dropdown_text_color,
            button_color=settings.canvas_control_panel_dropdown_button_color,
            button_hover_color=settings.canvas_control_panel_dropdown_button_hover_color,
            dropdown_text_color=settings.canvas_control_panel_dropdown_text_color,
            dropdown_fg_color=settings.canvas_control_panel_dropdown_background_color,
            dropdown_hover_color=settings.canvas_control_panel_dropdown_hover_color,
            # command=self.switch_layout
        )
        self.option_menu.grid(
            row=1, 
            column=2, 
            sticky="nsew",
            padx=(5,5), 
            pady=(5,5)
        )


        return canvas_control_panel_frame

    
    def reset_canvas(self):
        """Resets the scale of items and the start drawing point on the canvas back to their original scale and place"""
        
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


    #???????????????????????????????????????????
    # def switch_layout(self, *event):
    #     """?????????????????????????"""
    #     globals.current_view.set(self.option_menu.get())
        
    #     globals.app.set_layout()


    def choose_stack_export(self, *event):
        """Calls different export functions based on the 'export_option_menu' value"""
       
        # print("CHOOSE_STACK_EXPORT()")

        #Call functions based on export_option_menu value
        match self.export_option_menu.get():
            case "Full stack":
                self.export_full_stack_as_svg()

            case "Material rectangles":
                self.export_material_stack_as_svg()

            case "Layers":
                self.export_layers_as_svg()


    def export_material_stack_as_svg(self):
        """Exports only the material rectangles from the stack as SVG file"""

        # print("EXPORT_MATERIAL_STACK_AS_SVG")
        all_items = globals.layer_stack_canvas.layer_stack_canvas.find_all()

        #Return if there are no items on canvas
        if(len(all_items)-1 == 0):
            return

        #Create folders and filenames
        main_folder = "exports"
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        #Create sub_folder if it does not already exist
        sub_folder = globals.current_view.get()
        if not os.path.exists(f"{main_folder}/{sub_folder}"):
            os.makedirs(f"{main_folder}/{sub_folder}")
        
        #Create path for file to be saved in
        filename = f"Material_Stack_{globals.current_view.get()}.svg"
        file_path = os.path.join(f"{main_folder}/{sub_folder}/{filename}")

        #Open the file for writing
        with open(file_path, 'w') as f:
            #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

            #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
            f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.program_window.winfo_width(), self.program_window.winfo_height()))
 
            #Iterate through all the items
            for item in all_items:
                tag = globals.layer_stack_canvas.layer_stack_canvas.gettags(item)
                if(tag):
                    match tag[0]:
                        case "material_rectangle":
                            #Create SVG-element of material rectangle
                            rect_x0, rect_y0, rect_x1, rect_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(item)
                            rectangle_color = globals.layer_stack_canvas.layer_stack_canvas.itemcget(item, "fill")
                            if(rectangle_color == ""):
                                rectangle_color = "white"
                            svg_rectangle_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, rectangle_color)
                            
                            f.write(svg_rectangle_element)

                            #Create SVG-element for the rectangle bounding box and write it to file
                            svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, settings.layer_stack_canvas_rectangle_outline_color)
                            f.write(svg_bbox_element)
            
            #Write the closing SVG tag to the file, completing the SVG file
            f.write('</svg>\n')

        #Close the svg file
        f.close()

   
    def export_layers_as_svg(self):
        """Exports every layer of the stack with text and arrows as SVG-file"""     
        # print("EXPORT_LAYERS_AS_SVG()")

        all_items = globals.layer_stack_canvas.layer_stack_canvas.find_all()

        #Return if there are no items on canvas
        if(len(all_items)-1 == 0):
            return

        #Create folders and filenames
        main_folder = "exports"
        #Create the folder if it doesn't exist
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        #Create sub_folder if it does not already exist
        sub_folder = globals.current_view.get()
        if not os.path.exists(f"{main_folder}/{sub_folder}"):
            os.makedirs(f"{main_folder}/{sub_folder}")
        

        #Each SVG-file is assigned a number based on how many layers are in each file
        layer_counter = 1
        previously_created_elements = []

        #Iterate through all the materials
        for material in globals.materials:
            #Only create svg element if there is a rectangle
            if(globals.materials[material]["Rectangle_id"] != None):

                #Create a name for the SVG file for the current layer
                # filename = f"{layer_counter}materials_{material}_{globals.current_view.get()}.svg"
                filename = f"{layer_counter}materials_{list(globals.materials)[0]}-{material}.svg"
                

                #Create the file path by joining the folder path and the filename
                file_path = os.path.join(f"{main_folder}/{sub_folder}/{filename}")

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
                    rect_x0, rect_y0, rect_x1, rect_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Rectangle_id"])

                    svg_rectangle_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, globals.materials[material]["Color"].get())
                    f.write(svg_rectangle_element)
                    previously_created_elements.append(svg_rectangle_element)

                    #Create SVG-element for the rectangle bounding box and write it to file
                    svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, settings.layer_stack_canvas_rectangle_outline_color)
                    f.write(svg_bbox_element)
                    previously_created_elements.append(svg_bbox_element)

                    #Create SVG-element for material text
                    if(globals.materials[material]["Text_id"] != None):

                        text_x0, text_y0 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["Text_id"])
                        text_content = globals.layer_stack_canvas.layer_stack_canvas.itemcget(globals.materials[material]["Text_id"], 'text')
                        svg_text_element = '<text x="{}" y="{}" fill="{}" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(text_x0, text_y0, settings.text_color, settings.svg_text_size, text_content)
                        f.write(svg_text_element)
                        previously_created_elements.append(svg_text_element)

                    #Create SVG-element for text bounding box
                    if(globals.materials[material]["Text_bbox_id"] != None):

                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black"/>\n'.format(bbox_x0, bbox_y0, bbox_x1-bbox_x0, bbox_y1-bbox_y0, settings.text_color)
                            
                        #Write the SVG representation of the bounding box to the file
                        f.write(svg_bbox_element)
                        previously_created_elements.append(svg_bbox_element)

                    #Create SVG-element for arrow line pointing from box to rectangle
                    if(globals.materials[material]["Line_id"] != None):
                        #Line must be drawn from the right side of stack to left side of text
                        match globals.current_view.get():
                            case "Stacked" | "Realistic" | "Multi":
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

                                #Write the SVG representation of the arrow to the file
                                f.write(svg_line_element)
                                previously_created_elements.append(svg_line_element)


                            #Line must be drawn from the left side of stack to right side of text
                            case "Stepped":
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
        

    def export_full_stack_as_svg(self):
        """Exports all details on the stack as SVG-file"""
        # print("EXPORT_FULL_STACK_AS_SVG")
        all_items = globals.layer_stack_canvas.layer_stack_canvas.find_all()

        #Return if there are no items on canvas
        if(len(all_items)-1 == 0):
            return

        #Create folders and filenames
        main_folder = "exports"
        if not os.path.exists(main_folder):
            os.makedirs(main_folder)

        #Create sub_folder if it does not already exist
        sub_folder = globals.current_view.get()
        if not os.path.exists(f"{main_folder}/{sub_folder}"):
            os.makedirs(f"{main_folder}/{sub_folder}")
        
        #Create path for file to be saved in
        filename = f"Full_Stack_{globals.current_view.get()}.svg"
        file_path = os.path.join(f"{main_folder}/{sub_folder}/{filename}")

        #Open the file for writing
        with open(file_path, 'w') as f:
            #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

            #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
            f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(self.program_window.winfo_width(), self.program_window.winfo_height()))
 

            #Iterate through all the items
            for item in all_items:
                tag = globals.layer_stack_canvas.layer_stack_canvas.gettags(item)
                if(tag):
                    match tag[0]:
                        case "layer_stack_canvas_bounding_rectangle":
                            continue

                        case "material_rectangle":
                            #Create SVG-element of material rectangle
                            rect_x0, rect_y0, rect_x1, rect_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(item)
                            rectangle_color = globals.layer_stack_canvas.layer_stack_canvas.itemcget(item, "fill")
                            if(rectangle_color == ""):
                                rectangle_color = "white"
                            svg_rectangle_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, rectangle_color)
                            
                            f.write(svg_rectangle_element)

                            #Create SVG-element for the rectangle bounding box and write it to file
                            svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, settings.layer_stack_canvas_rectangle_outline_color)
                            f.write(svg_bbox_element)

                        case "text":
                            #Create SVG-element for text
                            text_x0, text_y0 = globals.layer_stack_canvas.layer_stack_canvas.coords(item)
                            text_content = globals.layer_stack_canvas.layer_stack_canvas.itemcget(item, 'text')
                            text_color = globals.layer_stack_canvas.layer_stack_canvas.itemcget(item, 'fill')
                            svg_text_element = '<text x="{}" y="{}" fill="{}" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(text_x0, text_y0, text_color, settings.svg_text_size, text_content)
                            
                            f.write(svg_text_element)

                        case "text_bbox":
                            #Create SVG-element of text bbox
                            rect_x0, rect_y0, rect_x1, rect_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(item)
                            svg_rectangle_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black" stroke-width="1" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0)
                            
                            f.write(svg_rectangle_element)
                        
                        case "line":
                            #Create line SVG-element
                            line_coords = globals.layer_stack_canvas.layer_stack_canvas.coords(item)
                            line_color = globals.layer_stack_canvas.layer_stack_canvas.itemcget(item, "fill")
                            svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="1" />\n'.format(line_coords[0], line_coords[1], line_coords[2], line_coords[3], line_color)

                            f.write(svg_line_element)

                        case "dotted_line":
                            #Create line SVG-element
                            line_coords = globals.layer_stack_canvas.layer_stack_canvas.coords(item)
                            line_color = globals.layer_stack_canvas.layer_stack_canvas.itemcget(item, "fill")
                            svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="2" stroke-dasharray="5,5" />\n'.format(line_coords[0], line_coords[1], line_coords[2], line_coords[3], line_color)

                            f.write(svg_line_element)

                        case "arrow_line":
                            line_coords = globals.layer_stack_canvas.layer_stack_canvas.coords(item)
                            line_color = globals.layer_stack_canvas.layer_stack_canvas.itemcget(item, "fill")

                            svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" marker-end="url(#arrow-end)" />\n'.format(line_coords[0], line_coords[1], line_coords[2], line_coords[3], line_color)

                            #Add arrowhead on top of line
                            svg_line_element += (
                            '<defs>\n'
                            '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="10" refY="3" orient="auto">\n'
                            '        <path d="M0,0 L0,6 L9,3 z" fill="black" />\n'
                            '    </marker>\n'
                            '</defs>\n'
                            )

                            f.write(svg_line_element)

                        case "arrow_line_both":
                            line_coords = globals.layer_stack_canvas.layer_stack_canvas.coords(item)
                            line_color = globals.layer_stack_canvas.layer_stack_canvas.itemcget(item, "fill")
                            svg_line_element = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" marker-start="url(#arrow-start)" marker-end="url(#arrow-end)" />\n'.format(line_coords[0], line_coords[1], line_coords[2], line_coords[3], line_color)

                            #Add arrowheads on both sides of the line
                            svg_line_element += (
                                '<defs>\n'
                                '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="10" refY="3" orient="auto">\n'
                                '        <path d="M0,0 L0,6 L9,3 z" fill="black" />\n'
                                '    </marker>\n'
                                '    <marker id="arrow-start" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto">\n'
                                '        <path d="M0,3 L9,0 L9,6 z" fill="black" />\n'
                                '    </marker>\n'
                                '</defs>\n'
                            )
                            f.write(svg_line_element)


            #Write the closing SVG tag to the file, completing the SVG file
            f.write('</svg>\n')

        #Close the svg file
        f.close()
