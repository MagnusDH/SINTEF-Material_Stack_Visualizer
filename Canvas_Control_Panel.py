import tkinter
from tkinter import messagebox, StringVar
import customtkinter
import settings
import globals
import os
import pandas   #Excel-file reading
import openpyxl #Excel-file reading

from Graph import Graph
from Graph_Control_Panel import Graph_Control_Panel


#This class handles the buttons that perform actions on the canvas
class Canvas_Control_Panel:
    def __init__(self, window):
        # print("CANVAS_CONTROL_PANEL_INIT()")
        
        self.window = window

        self.layer_stack_canvas_control_panel = self.create_canvas_control_panel()


    """Creates a frame with widgets that performs actions on the layer_stack_canvas"""
    def create_canvas_control_panel(self):
        # print("CREATE_CANVAS_CONTROL_PANEL()")

        #Create Frame from the control panel and place it within given window
        layer_stack_canvas_control_panel_frame = customtkinter.CTkFrame(
            master=self.window,
            width=settings.layer_stack_canvas_control_panel_width,
            height=settings.layer_stack_canvas_control_panel_height,
            fg_color=settings.layer_stack_canvas_control_panel_background_color
        )
        layer_stack_canvas_control_panel_frame.grid(
            row=1,
            column=1,
            padx=(settings.layer_stack_canvas_control_panel_padding_left, settings.layer_stack_canvas_control_panel_padding_right),
            pady=(settings.layer_stack_canvas_control_panel_padding_top, settings.layer_stack_canvas_control_panel_padding_bottom),
            sticky="nw"
        )

        #Prevent the frame to downsize itself to fit widgets placed inside
        layer_stack_canvas_control_panel_frame.grid_propagate(False)

        #Reset canvas button
        reset_canvas_button = customtkinter.CTkButton(
            master=layer_stack_canvas_control_panel_frame, 
            text="Reset canvas", 
            fg_color=settings.layer_stack_canvas_control_panel_button_color, 
            hover_color=settings.layer_stack_canvas_control_panel_button_hover_color, 
            text_color=settings.layer_stack_canvas_control_panel_text_color,
            width=15,
            command=self.reset_canvas
        )
        reset_canvas_button.grid(
            row=0, 
            column=0, 
            sticky="nw", 
            padx=(2,2), 
            pady=(2,2)
        )

        #Reset values button
        reset_values_button = customtkinter.CTkButton(
            master=layer_stack_canvas_control_panel_frame,
            text="Reset values",
            fg_color= settings.layer_stack_canvas_control_panel_button_color, 
            hover_color=settings.layer_stack_canvas_control_panel_button_hover_color, 
            text_color=settings.layer_stack_canvas_control_panel_text_color,
            width=15,
            command=self.reset_values
        )
        reset_values_button.grid(
            row=1, 
            column=0, 
            sticky="nw", 
            padx=(2,2), 
            pady=(2,2)
        )       

        #Export stack as SVG button
        export_stack_as_svg_button = customtkinter.CTkButton(
            master=layer_stack_canvas_control_panel_frame,
            text="Export stack",
            fg_color= settings.layer_stack_canvas_control_panel_button_color, 
            hover_color=settings.layer_stack_canvas_control_panel_button_hover_color, 
            text_color=settings.layer_stack_canvas_control_panel_text_color,
            width=15,
            command=self.export_stack_as_svg
        )
        export_stack_as_svg_button.grid(
            row=0, 
            column=1, 
            sticky="n", 
            padx=(2,2), 
            pady=(2,2)
        )

        #Export layers as SVG button
        export_layers_as_svg_button = customtkinter.CTkButton(
            master=layer_stack_canvas_control_panel_frame,
            text="Export layers",
            fg_color= settings.layer_stack_canvas_control_panel_button_color, 
            hover_color=settings.layer_stack_canvas_control_panel_button_hover_color, 
            text_color=settings.layer_stack_canvas_control_panel_text_color,
            width=15,
            command=self.export_layers_as_svg
        )
        export_layers_as_svg_button.grid(
            row=1, 
            column=1, 
            sticky="n", 
            padx=(2,2), 
            pady=(2,2)
        )

        #Option menu "view" label
        option_menu_view_label = customtkinter.CTkLabel(
            master=layer_stack_canvas_control_panel_frame,
            text="View", 
            bg_color=settings.layer_stack_canvas_control_panel_background_color,
            text_color="#55b6ff",
            font=(settings.text_font, 15, "bold")
        )
        option_menu_view_label.grid(
            row=0,
            column=2,
            sticky="s",
            padx=(0,0),
            pady=(0,0)
        )

        #Switch layout option menu
        self.option_menu = customtkinter.CTkOptionMenu(
            master=layer_stack_canvas_control_panel_frame, 
            values=["Stacked", "Realistic", "Stepped", "Stress"],
            width=30,
            fg_color=settings.layer_stack_canvas_control_panel_button_color, 
            button_hover_color=settings.layer_stack_canvas_control_panel_button_hover_color,
            command=self.switch_layout
        )
        self.option_menu.grid(
            row=1, 
            column=2, 
            sticky="ne",
            padx=(2,2), 
            pady=(2,2)
        )

        return layer_stack_canvas_control_panel_frame

    
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


    """Reads the excel file again and repopulated the "thickness" in self.materials. Updates sliders and entries with new values"""
    def reset_values(self):
        # print("RESET_VALUES")
        
        excel_file = "Materials.xlsx"

        #If there is a "materials" file in the folder, read it and reset the thickness values of each material
        if(os.path.isfile(excel_file)):
            try:
                match globals.option_menu:

                    #Reset only the "thickness" values
                    case "Stacked" | "Realistic" | "Stress":
                        #Reload initial thickness values from given excel file
                        #Read given excel file into Pandas dataframe
                        excel_data = pandas.read_excel(excel_file)

                        #Loop through the rows in excel_file and populate "self.materials"
                        for index, row in excel_data.iterrows():
                            material_name = row["Material"]
                            material_thickness = row["Thickness"]
                                
                            #Populate material dictionary
                            if(material_name in globals.materials):

                                globals.materials[material_name]["thickness"] = material_thickness
                                
                                #Update sliders and Entries
                                globals.materials[material_name]["slider_id"].set(material_thickness)
                                globals.materials[material_name]["entry_id"].delete(0, tkinter.END)
                                globals.materials[material_name]["entry_id"].insert(0, material_thickness)
                            
                            #Reset text_size
                            # self.current_text_size = self.original_text_size
                            
                        #Draw rectangle stack with original values
                        globals.layer_stack_canvas.draw_material_stack()

                    #Reset only the "indent" values
                    case "Stepped":
                        #Reload initial indent values from given excel file
                        #Read given excel file into Pandas dataframe
                        excel_data = pandas.read_excel(excel_file)

                        #Loop through the rows in excel_file and populate "self.materials"
                        for index, row in excel_data.iterrows():
                            material_name = row["Material"]
                            material_indent = row["Indent"]
                                
                            #Populate material dictionary
                            if(material_name in globals.materials):

                                globals.materials[material_name]["indent"] = material_indent
                                    
                                #Update sliders and Entries
                                globals.materials[material_name]["slider_id"].set(material_indent)
                                globals.materials[material_name]["entry_id"].delete(0, tkinter.END)
                                globals.materials[material_name]["entry_id"].insert(0, material_indent)
                            
                                #Reset text_size
                                # self.current_text_size = self.original_text_size
                            
                        #Draw rectangle stack with original values
                        globals.layer_stack_canvas.draw_material_stack()
                
            #Handle errors
            except Exception as error:
                messagebox.showerror("Error", "Could not reset values\nMay be a issue with reading from excel-file")

        else:
            messagebox.showerror("Error", "Can not reset values because there is no 'materials.xlsx' file to fetch original values from")


    """
    -Changes the Label explaining what is being modified by sliders and entries in the material_control_panel
    -Changes the values for sliders and entries
    """
    def switch_layout(self, *event):
        # print("SWITCH_LAYOUT()")

        #Destroy the graph if it exists
        if hasattr(globals.graph, 'graph'):
            globals.graph.graph.get_tk_widget().destroy()
            globals.graph = None
            
        #Destroy the graph_control_panel if it exists
        if hasattr(globals.graph_control_panel, 'graph_control_panel'):
            globals.graph_control_panel.graph_control_panel.destroy()


        #Switch UI layout based on option value
        match self.option_menu.get():
            case "Stacked":
                globals.option_menu = "Stacked"

                #Change the label in user_interface_frame
                globals.material_control_panel.slider_label.configure(text="Thickness [nm]")

                #Set all material entry and slider values to "thickness" value, except the entries that are "disabled"
                for material in globals.materials:
                    globals.materials[material]["slider_id"].set(globals.materials[material]["thickness"])
                    
                    if(globals.materials[material]["status"] != "disabled"):
                        globals.materials[material]["entry_id"].configure(textvariable=StringVar(value=str(globals.materials[material]["thickness"])))
                
                #Set new dimensions for layer_stack_canvas back to the original
                globals.layer_stack_canvas.layer_stack_canvas.configure(width=settings.layer_stack_canvas_width)

                globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_reqwidth() - 1
                globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_reqheight() - 1

                globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0
                globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0

                #Draw material stack                
                globals.layer_stack_canvas.draw_material_stack()

                #Set new dimensions for canvas_control_panel back to the original
                globals.canvas_control_panel.layer_stack_canvas_control_panel.configure(width=settings.layer_stack_canvas_control_panel_width)

            case "Realistic":
                globals.option_menu = "Realistic"

                #Change the label in user_interface_frame
                globals.material_control_panel.slider_label.configure(text="Thickness [nm]")

                #Set all material entry and slider values to "thickness" value, except the entries that are "disabled"
                for material in globals.materials:
                    globals.materials[material]["slider_id"].set(globals.materials[material]["thickness"])
                    
                    if(globals.materials[material]["status"] != "disabled"):
                        globals.materials[material]["entry_id"].configure(textvariable=StringVar(value=str(globals.materials[material]["thickness"])))

                #Set new dimensions for layer_stack_canvas back to the original
                globals.layer_stack_canvas.layer_stack_canvas.configure(width=settings.layer_stack_canvas_width)
                globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_reqwidth() - 1
                globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_reqheight() - 1
                globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0
                globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0

                #Draw the material stack
                globals.layer_stack_canvas.draw_material_stack()

                #Set new dimensions for canvas_control_panel back to the original
                globals.canvas_control_panel.layer_stack_canvas_control_panel.configure(width=settings.layer_stack_canvas_control_panel_width)
            
            case "Stepped":
                globals.option_menu = "Stepped"

                #Change the label in UI frame
                globals.material_control_panel.slider_label.configure(text="Indent [nm]")

                #Set all material entry and slider values to "indent" value, except the entries that are "disabled"
                for material in globals.materials:
                    globals.materials[material]["slider_id"].set(globals.materials[material]["indent"])

                    if(globals.materials[material]["status"] != "disabled"):
                        globals.materials[material]["entry_id"].configure(textvariable=StringVar(value=str(globals.materials[material]["indent"])))
                
                #Set new dimensions for layer_stack_canvas back to the original
                globals.layer_stack_canvas.layer_stack_canvas.configure(width=settings.layer_stack_canvas_width)

                globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_reqwidth() - 1
                globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_reqheight() - 1

                globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0
                globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0
                
                #Draw the material stack
                globals.layer_stack_canvas.draw_material_stack()

                #Set new dimensions for canvas_control_panel back to the original
                globals.canvas_control_panel.layer_stack_canvas_control_panel.configure(width=settings.layer_stack_canvas_control_panel_width)

            case "Stress":
                #Set option menu status
                globals.option_menu = "Stress"

                #Change the label in user_interface_frame
                globals.material_control_panel.slider_label.configure(text="Thickness [nm]")

                #Set all material entry and slider values to "thickness" value, except the entries that are "disabled"
                for material in globals.materials:
                    globals.materials[material]["slider_id"].set(globals.materials[material]["thickness"])
                    
                    if(globals.materials[material]["status"] != "disabled"):
                        globals.materials[material]["entry_id"].configure(textvariable=StringVar(value=str(globals.materials[material]["thickness"])))

                #Set new dimensions for layer_stack_canvas
                globals.layer_stack_canvas.layer_stack_canvas.configure(width=525)
                globals.layer_stack_canvas.visible_canvas_bbox_x1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_reqwidth() - 1
                globals.layer_stack_canvas.visible_canvas_bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.winfo_reqheight() - 1
                globals.layer_stack_canvas.layer_stack_canvas_height = globals.layer_stack_canvas.visible_canvas_bbox_y1 - globals.layer_stack_canvas.visible_canvas_bbox_y0
                globals.layer_stack_canvas.layer_stack_canvas_width = globals.layer_stack_canvas.visible_canvas_bbox_x1 - globals.layer_stack_canvas.visible_canvas_bbox_x0

                #Redraw material stack
                globals.layer_stack_canvas.draw_material_stack()

                #Set new dimensions for canvas_control_panel
                globals.canvas_control_panel.layer_stack_canvas_control_panel.configure(width=globals.layer_stack_canvas.layer_stack_canvas_width*0.8)

                #Create Graph
                globals.graph = Graph(globals.main_frame)

                #Create panel that controls the actions of the graph
                globals.graph_control_panel = Graph_Control_Panel(globals.main_frame)

                globals.graph.draw_curvature_graph()



    """Exports the stack without material names as SVG file"""
    def export_stack_as_svg(self):
        # print("EXPORT_STACK_AS_SVG()")

        #Define the name of the svg file
        match globals.option_menu:
            case "Stacked":
                filename = "stack.svg"

            case "Realistic":
                filename = "stack_realistic.svg"

            case "Stepped":
                filename = "stack_stepped.svg"
            
            case "Stress":
                filename = "stack_stress.svg"
            
            #Default case
            case _:
                filename = "stack.svg"
        

        #Specify a folder where the SVG-file should be saved
        folder_path = "svg_exports"

        #Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #Create the file path by joining the folder path and the filename
        file_path = os.path.join(folder_path, filename)

        #Open the file for writing
        with open(file_path, 'w') as f:
            #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')

            #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
            # f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(globals.program_window.winfo_reqwidth(), globals.program_window.winfo_reqheight()))
            f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(globals.program_window.winfo_width(), globals.program_window.winfo_height()))


            #Go through every rectangle found on canvas
            for material in globals.materials:
                #Only create element of rectangle if it is not "None"
                if(globals.materials[material]["rectangle_id"] != None):

                    #Find the coordinates of the rectangle
                    rect_x0, rect_y0, rect_x1, rect_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["rectangle_id"])
                    #Construct an SVG <rect> element for the rectangle
                    svg_rect_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, globals.materials[material]["color"])
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

        #Specify a folder where the SVG-files should be saved
        folder_path = "svg_exports"
        #Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #Each SVG-file is assigned a number based on how many layers are in each file
        layer_counter = 1
        previously_created_elements = []

        #Iterate through all the materials
        for material in globals.materials:
            #Only create svg element if there is a rectangle
            if(globals.materials[material]["rectangle_id"] != None):

                #Create a name for the SVG file for the current layer
                match globals.option_menu:
                    case "Stacked":
                        filename = f"{layer_counter}_layer_stacked.svg"

                    case "Realistic":
                        filename = f"{layer_counter}_layer_realistic.svg"

                    case "Stepped":
                        filename = f"{layer_counter}_layer_stepped.svg"
                    
                    case "Stress":
                        filename = f"{layer_counter}_layer_stress.svg"

                    #Default case
                    case _:
                        filename = f"{layer_counter}_layer.svg"

                #Create the file path by joining the folder path and the filename
                file_path = os.path.join(folder_path, filename)

                #Open file for writing
                with open(file_path, 'w') as f:
                    #Write XML declaration for the SVG file, specifying the XML version, character encoding, and standalone status.
                    f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
                    #Write opening tag for the SVG file, specifying the width and height attributes based on the canvas dimensions. The xmlns attribute defines the XML namespace for SVG.
                    # f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(globals.program_window.winfo_reqwidth(), globals.program_window.winfo_reqheight()))
                    f.write('<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(globals.program_window.winfo_width(), globals.program_window.winfo_height())) 


                    #Write the previous created elements to the current file
                    if(len(previously_created_elements) != 0):
                        for element in previously_created_elements:
                            f.write(element)

                    #Create SVG-element of material rectangle
                    if(globals.materials[material]["rectangle_id"] != None):
                        rect_x0, rect_y0, rect_x1, rect_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["rectangle_id"])

                        svg_rectangle_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, globals.materials[material]["color"])
                        f.write(svg_rectangle_element)
                        previously_created_elements.append(svg_rectangle_element)

                        #Create SVG-element for the rectangle bounding box and write it to file
                        svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" />\n'.format(rect_x0, rect_y0, rect_x1 - rect_x0, rect_y1 - rect_y0, settings.layer_stack_canvas_rectangle_outline_color)
                        f.write(svg_bbox_element)
                        previously_created_elements.append(svg_bbox_element)
                    else: 
                        break

                    #Create SVG-element for material text
                    if(globals.materials[material]["text_id"] is not None):
                        text_x0, text_y0 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["text_id"])
                        text_content = globals.layer_stack_canvas.layer_stack_canvas.itemcget(globals.materials[material]["text_id"], 'text')
                        svg_text_element = '<text x="{}" y="{}" fill="{}" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(text_x0, text_y0, settings.text_color, settings.svg_text_size, text_content)
                        f.write(svg_text_element)
                        previously_created_elements.append(svg_text_element)

                    #Create SVG-element for text bounding box
                    if(globals.materials[material]["text_bbox_id"] is not None):
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["text_bbox_id"])
                        svg_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black"/>\n'.format(bbox_x0, bbox_y0, bbox_x1-bbox_x0, bbox_y1-bbox_y0, settings.text_color)
                            
                        #Write the SVG representation of the bounding box to the file
                        f.write(svg_bbox_element)
                        previously_created_elements.append(svg_bbox_element)

                    #Create SVG-element for arrow line pointing from box to rectangle
                    if(globals.materials[material]["line_id"] != None):
                        #Line must be drawn from the right side of stack to left side of text
                        if(globals.option_menu == "Stacked" or globals.option_menu == "Realistic" or globals.option_menu == "Stress"):
                            line_coords = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["line_id"])
                            #Construct an SVG <line> element for arrows
                            bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["text_bbox_id"])
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
                            line_x0, line_y0, line_x1, line_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["line_id"])
                            #Construct an SVG <line> element for arrows
                            bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["text_bbox_id"])
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
                    if(globals.materials[material]["indent_text_id"] != None):
                        indent_text_x0, indent_text_y0 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["indent_text_id"])
                        indent_text_content = globals.layer_stack_canvas.layer_stack_canvas.itemcget(globals.materials[material]["indent_text_id"], 'text')
                        svg_indent_text_element = '<text x="{}" y="{}" fill="black" font-size="{}" font-weight="bold" dominant-baseline="middle" text-anchor="middle">{}</text>\n'.format(indent_text_x0, indent_text_y0, settings.svg_text_size, indent_text_content)
                            
                        f.write(svg_indent_text_element)
                        previously_created_elements.append(svg_indent_text_element)

                    #Create SVG-element for indent_text bounding box
                    if(globals.materials[material]["indent_text_bbox_id"] != None):
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["indent_text_bbox_id"])
                        svg_indent_text_bbox_element = '<rect x="{}" y="{}" width="{}" height="{}" fill="none" stroke="black"/>\n'.format(bbox_x0, bbox_y0, bbox_x1-bbox_x0, bbox_y1-bbox_y0, settings.text_color)
                            
                        #Write the SVG representation of the bounding box to the file
                        f.write(svg_indent_text_bbox_element)
                        previously_created_elements.append(svg_indent_text_bbox_element)

                    #Create SVG-element for indent_line
                    if(globals.materials[material]["indent_line_id"] != None):
                        indent_line_x0, indent_line_y0, indent_line_x1, indent_line_y1 = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["indent_line_id"])
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
                    if(globals.materials[material]["indent_arrow_pointer_id"] != None):
                        line_coords = globals.layer_stack_canvas.layer_stack_canvas.coords(globals.materials[material]["indent_arrow_pointer_id"])
                        #Construct an SVG <line> element for arrows
                        bbox_x0, bbox_y0, bbox_x1, bbox_y1 = globals.layer_stack_canvas.layer_stack_canvas.bbox(globals.materials[material]["indent_text_bbox_id"])
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