import tkinter
from tkinter import font
import customtkinter
import settings
import globals


#This class handles everything that happens on the canvas 
class Layer_Stack_Canvas:
    def __init__(self, window, row_placement:int, column_placement:int):
        #Create a canvas in a given window
        self.program_window = window

        #Row/column placement in main program window
        self.row_placement = row_placement
        self.column_placement = column_placement

        self.current_scale = 1.0

        self.layer_stack_canvas = self.create_canvas()

        #Draw material stack
        self.draw_material_stack()


    def create_canvas(self):
        """
        -Returns a canvas created in the program window\n
        -Canvas coordinates x0/y0 = bottom left corner and x1/y1 = top right corner"""
        #print("CREATE_CANVAS()")
        
        layer_stack_canvas = tkinter.Canvas(
            master=self.program_window,
            bg=settings.layer_stack_canvas_background_color,
            # highlightbackground="red", 
            highlightthickness=0,
        )
        layer_stack_canvas.grid(
            row=self.row_placement, 
            column=self.column_placement, 
            sticky="nsew", 
            padx=(settings.layer_stack_canvas_padding_left, settings.layer_stack_canvas_padding_right), 
            pady=(settings.layer_stack_canvas_padding_top, settings.layer_stack_canvas_padding_bottom)
        )

        #Update program to get correct screen&frame sizes
        self.program_window.update()

        #Set canvas_bbox coordniates for later use
        self.visible_canvas_bbox_x0 = 0
        self.visible_canvas_bbox_y0 = layer_stack_canvas.winfo_height() - 1
        self.visible_canvas_bbox_x1 = layer_stack_canvas.winfo_width() - 1
        self.visible_canvas_bbox_y1 = 0
        self.layer_stack_canvas_height = self.visible_canvas_bbox_y0 - self.visible_canvas_bbox_y1
        self.layer_stack_canvas_width = self.visible_canvas_bbox_x1 - self.visible_canvas_bbox_x0
        #This is just a usefull function to find the bbox of the canvas: self.canvas.coords(self.canvas.find_withtag("canvas_bounding_box_rectangle"))[2]

        #Draw bounding box around canvas
        layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, 
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color, 
            width=1,
            tags="layer_stack_canvas_bounding_rectangle"
        )

        #Listen to mouse: buttonpress, motion and zoom events
        layer_stack_canvas.bind("<ButtonPress-1>", lambda event, canvas=layer_stack_canvas: self.click_on_canvas(event, layer_stack_canvas))
        layer_stack_canvas.bind("<B1-Motion>", lambda event, canvas=layer_stack_canvas: self.canvas_drag(event, layer_stack_canvas))
        layer_stack_canvas.bind("<MouseWheel>", lambda event, canvas=layer_stack_canvas: self.canvas_zoom(event, layer_stack_canvas))

        return layer_stack_canvas


    def click_on_canvas(self, event, canvas):
        """Remembers the initial mouse click-position on the canvas"""
        #print("CLICK_ON_CANVAS()")
        canvas.scan_mark(event.x, event.y)
    

    def canvas_drag(self, event, canvas):
        """Moves the position of the canvas"""
        #print("CANVAS_DRAG()")
        canvas.scan_dragto(event.x, event.y, gain=1)


    def canvas_zoom(self, event, canvas):
        """Scales all the elements on the canvas up or down"""
        
        # print("CANVAS_ZOOM()")
        zoom_factor = 1.05

        #Zoom in: Scale all items on the canvas around the mouse cursor
        if event.delta > 0:
            canvas.scale("all", event.x, event.y, zoom_factor, zoom_factor)
            self.current_scale *= zoom_factor

        #Zoom out: Scale all items on the canvas around the mouse cursor
        elif event.delta < 0:
            canvas.scale("all", event.x, event.y, 1.0/zoom_factor, 1.0/zoom_factor)
            self.current_scale /= zoom_factor


    def draw_material_stack(self, *event):
        """Draws the material stack based on the current view"""
        # print("DRAW MATERIAL STACK()")

        #Clear all existing elements on canvas and in dictionary
        self.layer_stack_canvas.delete("all")
        for material in globals.materials:
            globals.materials[material]["Rectangle_id"] = None
            globals.materials[material]["Text_id"] = None
            globals.materials[material]["Text_bbox_id"] = None
            globals.materials[material]["Line_id"] = None
            globals.materials[material]["Indent_text_id"] = None
            globals.materials[material]["Indent_text_bbox_id"] = None
            globals.materials[material]["Indent_line_id"] = None
            globals.materials[material]["Indent_arrow_pointer_id"] = None

        #Sort the materials dictionary after the "layer" value
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["Layer"].get()))
                
        #Draw stack based on value in option menu
        match globals.current_view.get():
            case "Stacked":
                self.draw_material_stack_stacked()
                self.write_text_on_stack()

            case "Realistic":
                self.draw_material_stack_realistic()
                self.write_text_on_stack()

            case "Stepped":
                self.draw_material_stack_stepped()
                self.write_text_on_stack()
                self.write_indent_on_stepped_stack()

            case "Multi":
                # self.draw_material_stack_multi()
                self.draw_material_stack_realistic()
                self.write_text_on_stack()
                self.draw_Zn_and_Zp()

  
    def draw_material_stack_stacked(self):       
        """Draws the rectangle stack where the lowest layer is 1/10 of the canvas no matter what"""
        
        # print("DRAW_MATERIAL_STACK_STACKED()")
        
        #Draw bounding box around canvas
        self.layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, 
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color, 
            tags="layer_stack_canvas_bounding_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            if(globals.materials[material]["Layer"].get() == 1):
                continue    #Skip lowest layer
            
            rectangle_height = globals.materials[material]["Thickness [nm]"].get()
            sum_of_all_materials += rectangle_height
        
        #Materials (except the lowest layer material) will be drawn on 9/10 of the canvas
        canvas_height = round(self.layer_stack_canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_stacked_offset_left_side
        rectangle_y0 = self.visible_canvas_bbox_y0 - (self.layer_stack_canvas_height*0.1)
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_stacked_offset_right_side
        rectangle_y1 = None #Calculated later
        
        #Draw rectangles on canvas
        for material in globals.materials:
            #Create material rectangle only if "Thickness [nm]" is > zero
            if(globals.materials[material]["Thickness [nm]"].get() > 0):

                #Lowest material will be drawn on the bottom 1/10 of the canvas
                if(globals.materials[material]["Layer"].get() == 1 ):  
                    created_rectangle = self.layer_stack_canvas.create_rectangle(
                        self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, rectangle_x1, rectangle_y0, 
                        fill=globals.materials[material]["Color"].get(), 
                        outline=settings.layer_stack_canvas_rectangle_outline_color,
                        tags="material_rectangle"
                    )
                    
                    #Add rectangle_id to its place in self.materials
                    globals.materials[material]["Rectangle_id"] = created_rectangle
                
                #Material is not the lowest in the stack
                else:
                    #find how many percent the current rectangle's height is of the total sum of materials
                    rectangle_height = globals.materials[material]["Thickness [nm]"].get()
                    rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
                    #Convert rectangle percentage to pixels
                    rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

                    #draw rectangle from top of canvas to its number of pixles in height
                    rectangle_y1 = rectangle_y0 - rectangle_height_pixels
                    created_rectangle = self.layer_stack_canvas.create_rectangle(
                        rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                        fill=globals.materials[material]["Color"].get(),
                        outline=settings.layer_stack_canvas_rectangle_outline_color, 
                        tags="material_rectangle"
                    )

                    #Add rectangle_id to its place in globals.materials
                    globals.materials[material]["Rectangle_id"] = created_rectangle

                    #Add rectangle height to prevent overlaping
                    rectangle_y0 -= rectangle_height_pixels

        
    def draw_material_stack_realistic(self):
        """Draws a realistic version of the rectangle stack"""

        # print("DRAW_MATERIAL_STACK_REALISTIC()")

        #Draw bounding box around canvas
        self.layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, 
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color , 
            tags="layer_stack_canvas_bounding_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            rectangle_height = globals.materials[material]["Thickness [nm]"].get()
            sum_of_all_materials += rectangle_height
        
        #Prepare first rectangle coordinates based on view
        match globals.current_view.get():
            case "Realistic":
                rectangle_x0 = self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_realistic_offset_left_side
                rectangle_y0 = self.visible_canvas_bbox_y0
                rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_realistic_offset_right_side
                rectangle_y1 = None #Calculated later
            
            case "Multi":
                rectangle_x0 = self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side
                rectangle_y0 = self.visible_canvas_bbox_y0
                rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_multi_offset_right_side
                rectangle_y1 = None #Calculated later

            case _:
                rectangle_x0 = self.visible_canvas_bbox_x0
                rectangle_y0 = self.visible_canvas_bbox_y0
                rectangle_x1 = self.visible_canvas_bbox_x1
                rectangle_y1 = None #Calculated later


        #Materials (except the lowest layer material) will be drawn on 9/10 of the canvas
        canvas_height = self.layer_stack_canvas_height
        
        #Draw rectangles on canvas
        for material in globals.materials:
        
            #Create material rectangle only if "Thickness [nm]" is > zero
            if(globals.materials[material]["Thickness [nm]"].get() > 0):
                #find how many percent the current rectangle's height is of the total sum of materials
                rectangle_height = globals.materials[material]["Thickness [nm]"].get()
                rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
                #Convert rectangle percentage to pixels
                rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

                #draw rectangle from top of canvas to its number of pixles in height
                rectangle_y1 = rectangle_y0 - rectangle_height_pixels
                created_rectangle = self.layer_stack_canvas.create_rectangle(
                    rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                    fill=globals.materials[material]["Color"].get(),
                    outline=settings.layer_stack_canvas_rectangle_outline_color, 
                    tags="material_rectangle"
                )

                #Add rectangle_id to its place in self.materials
                globals.materials[material]["Rectangle_id"] = created_rectangle

                #Add rectangle height to prevent overlaping
                rectangle_y0 -= rectangle_height_pixels
        

    def draw_material_stack_stepped(self):
        """
        -Draws a rectangle stack where each layer can have an "indent" decided by the user\n
        -The "indent" is in nanometers like the height of the materials. 
        -Each material is drawn from the bottom left corner
        """
        # print("DRAW_MATERIAL_STACK_STEPPED()")

        #Draw bounding box around canvas
        self.layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0,
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color, 
            tags="layer_stack_canvas_bounding_rectangle")
        
        #Find the total height of all materials combined and the thickest material
        sum_of_all_materials = 0
        biggest_material = 0
        for material in globals.materials:
            if(globals.materials[material]["Layer"].get() == 1):
                continue    #Skip lowest material

            sum_of_all_materials += globals.materials[material]["Thickness [nm]"].get()
            if(biggest_material < globals.materials[material]["Thickness [nm]"].get()):
                biggest_material = globals.materials[material]["Thickness [nm]"].get()
        
        #Find how many nanometers 1 pixel should represent
        nanometers_per_pixel = sum_of_all_materials/round(self.layer_stack_canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates (from bottom left corner)
        rectangle_x0 = self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_stepped_offset_left_side
        rectangle_y0 = self.visible_canvas_bbox_y0 - (self.layer_stack_canvas_height*0.1)
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_stepped_offset_right_side
        rectangle_y1 = None #calculated later
        previous_rectangle_x1 = self.visible_canvas_bbox_x1

        #If a rectangles x1 coordinate is less than original start drawing point, then it will not be drawn 
        original_rectangle_x0 = rectangle_x0

        #Draw rectangles on canvas
        for material in globals.materials:
            #Create material rectangle only if "Thickness [nm]" is > zero
            if(globals.materials[material]["Thickness [nm]"].get() > 0):

                #Draw lowest layer material on the bottom 1/10 of the canvas
                if(globals.materials[material]["Layer"].get() == 1):
                    
                    #Find how many pixels is needed to represent the indent of the current material
                    indent_width_pixels = globals.materials[material]["Indent [nm]"].get()/nanometers_per_pixel

                    #Set the width of the rectangle
                    rectangle_x1 = rectangle_x1 - indent_width_pixels

                    #Draw and create rectangle if its width is greater than the original start drawing point for rectangles
                    if(rectangle_x1 >= original_rectangle_x0):
                        #Create rectangle
                        created_rectangle = self.layer_stack_canvas.create_rectangle(
                            rectangle_x0, self.visible_canvas_bbox_y0, rectangle_x1, rectangle_y0,
                            fill=globals.materials[material]["Color"].get(),
                            outline=settings.layer_stack_canvas_rectangle_outline_color, 
                            tags="material_rectangle"
                        )
                        
                        #Add created rectangle to materials{}
                        globals.materials[material]["Rectangle_id"] = created_rectangle

                #Material is not the lowest in the stack
                else:
                    #Find how many pixels is needed to represent the height of the current material
                    rectangle_height_pixels = globals.materials[material]["Thickness [nm]"].get()/nanometers_per_pixel
                    
                    #Set the y1 coordinate of the rectangle
                    rectangle_y1 = rectangle_y0 - rectangle_height_pixels

                    #Find how many pixels is needed to represent the indent of the current material
                    indent_width_pixels = globals.materials[material]["Indent [nm]"].get()/nanometers_per_pixel

                    #Set the indent width for the current rectangle
                    rectangle_x1 =  rectangle_x1 - indent_width_pixels

                    #Draw and create rectangle if its width is greater than the original start drawing point for rectangles
                    if(rectangle_x1 >= original_rectangle_x0):
                        created_rectangle = self.layer_stack_canvas.create_rectangle(
                            rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                            fill=globals.materials[material]["Color"].get(), 
                            outline=settings.layer_stack_canvas_rectangle_outline_color,
                            tags="material_rectangle"
                        )
                    
                        #Add rectangle_id to its place in globals.materials{}
                        globals.materials[material]["Rectangle_id"] = created_rectangle

                    #Add rectangle height to prevent overlaping
                    rectangle_y0 -= rectangle_height_pixels
    

    def draw_material_stack_limited(self):
        """Draws a material stack only with materials that are "active" in globals.materials"""
        # print("DRAW_MATERIAL_STACK_LIMITED")

                
        #Draw bounding box around canvas
        self.layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, 
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color, 
            tags="layer_stack_canvas_bounding_rectangle")
        
        #Check how many materials are marked as "active"
        num_active_materials = 0
        for material in globals.materials:
            if(globals.materials[material]["Status"].get() == "active"):
                num_active_materials += 1

        #If the are no active materials to draw, then end the function
        if(num_active_materials <= 0):
            return

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            if(globals.materials[material]["Status"].get() == "active"):
                if(globals.materials[material]["Layer"].get() == 1):
                    continue    #Skip lowest material
                
                rectangle_height = globals.materials[material]["Thickness [nm]"].get()
                sum_of_all_materials += rectangle_height
            
        #Materials (except the lowest layer material) will be drawn on 9/10 of the canvas
        canvas_height = round(self.layer_stack_canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_limited_offset_left_side
        rectangle_y0 = self.visible_canvas_bbox_y0 - self.layer_stack_canvas_height*0.1
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_limited_offset_right_side
        rectangle_y1 = None #Calculated later
            
        #Draw rectangles on canvas
        for material in globals.materials:
            if(globals.materials[material]["Status"].get() == "active"):
                #Create material rectangle only if "Thickness [nm]" is > zero
                if(globals.materials[material]["Thickness [nm]"].get() > 0):

                    #Lowest layer material will be drawn on the bottom 1/10 of the canvas
                    if(globals.materials[material]["Layer"].get() == 1):  
                        created_rectangle = self.layer_stack_canvas.create_rectangle(
                            rectangle_x0, self.visible_canvas_bbox_y0, rectangle_x1, rectangle_y0, 
                            fill=globals.materials[material]["Color"].get(), 
                            outline=settings.layer_stack_canvas_rectangle_outline_color,
                            tags="material_rectangle"
                        )
                        
                        #Add rectangle_id to its place in self.materials
                        globals.materials[material]["Rectangle_id"] = created_rectangle
                    
                    #Material is not the lowest layer
                    else:
                        #find how many percent the current rectangle's height is of the total sum of materials
                        rectangle_height = globals.materials[material]["Thickness [nm]"].get()
                        rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
                        #Convert rectangle percentage to pixels
                        rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

                        #draw rectangle from top of canvas to its number of pixles in height
                        rectangle_y1 = rectangle_y0 - rectangle_height_pixels
                        created_rectangle = self.layer_stack_canvas.create_rectangle(
                            rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                            fill=globals.materials[material]["Color"].get(),
                            outline=settings.layer_stack_canvas_rectangle_outline_color, 
                            tags="material_rectangle"
                        )

                        #Add rectangle_id to its place in globals.materials
                        globals.materials[material]["Rectangle_id"] = created_rectangle

                        #Add rectangle height to prevent overlaping
                        rectangle_y0 -= rectangle_height_pixels


    def write_text_on_stack(self):
        """
        -Writes name_labels for each rectangle in the material stack
            -Labels are created on the left side for "stepped" mode and on the right side for "stacked and realistic" mode
        -Creates all texts either inside or outside of the rectangle box based on the rectangles height
        -Loops through all text_boxes, checks for overlaps and potentially moves them around to prevent overlap 
        """
        # print("WRITE_TEXT_ON_STACK()")              

        #Find what the height of a text's bounding box will be
        text_font = font.Font(family=settings.text_font, size=settings.text_size)
        text_height = text_font.metrics()['linespace']

        #CREATION OF TEXT, TEXT_BBOX AND LINES
        match globals.current_view.get():
            case "Stacked" | "Realistic" | "Multi":

                #Loop through every material:
                for material in globals.materials:
                    #If material has a rectangle that text can be written on
                    if(globals.materials[material]["Rectangle_id"] != None):
                        #Find coordinates and height of current material_rectangle
                        rectangle_x0 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0]
                        rectangle_y0 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1]
                        rectangle_x1 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2]
                        rectangle_y1 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]
                        rectangle_height = rectangle_y1-rectangle_y0
                        rectangle_middle_x = (rectangle_x0 + rectangle_x1)/2
                        rectangle_middle_y = (rectangle_y0 + rectangle_y1)/2

                        #Create text inside inside rectangle
                        if(text_height < rectangle_height):
                            created_text = self.layer_stack_canvas.create_text(
                                rectangle_middle_x, rectangle_middle_y, 
                                text=f"{material} - {globals.materials[material]['Thickness [nm]'].get()} {globals.materials[material]['Unit'].get()}", 
                                fill=settings.layer_stack_canvas_text_color, 
                                font=(settings.text_font, settings.layer_stack_canvas_text_size), 
                                anchor="center", 
                                tags="text"
                            )

                            #Add text element to dictionary
                            globals.materials[material]["Text_id"] = created_text
                        
                        #Create text, text_bbox and pointer line outside rectangle
                        else:
                            created_text = self.layer_stack_canvas.create_text(
                                self.visible_canvas_bbox_x1, rectangle_middle_y, 
                                text=f"{material} - {globals.materials[material]['Thickness [nm]'].get()} {globals.materials[material]['Unit'].get()}", 
                                fill=settings.layer_stack_canvas_text_color, 
                                font=(settings.text_font, settings.layer_stack_canvas_text_size), 
                                tags="text"
                            )
                            created_text_bbox = self.layer_stack_canvas.create_rectangle(
                                self.layer_stack_canvas.bbox(created_text), 
                                outline="black", 
                                tags="text_bbox"
                            )
                            #Get coordinates of text_bbox
                            text_bbox_x0 = self.layer_stack_canvas.bbox(created_text)[0]
                            text_bbox_y0 = self.layer_stack_canvas.bbox(created_text)[1]
                            text_bbox_x1 = self.layer_stack_canvas.bbox(created_text)[2]
                            text_bbox_y1 = self.layer_stack_canvas.bbox(created_text)[3]
                            text_bbox_middle_y = (text_bbox_y0 + text_bbox_y1) / 2

                            created_arrow_line = self.layer_stack_canvas.create_line(
                                (text_bbox_x0, text_bbox_middle_y), (rectangle_x1, rectangle_middle_y), 
                                arrow=tkinter.LAST, 
                                fill="black",
                                tags="arrow_line"
                            )

                            #Add created elements to dictionary
                            globals.materials[material]["Text_id"] = created_text
                            globals.materials[material]["Text_bbox_id"] = created_text_bbox
                            globals.materials[material]["Line_id"] = created_arrow_line
                            

            case "Stepped":
                #Loop through every material:
                for material in globals.materials:
                    #If there is a rectangle to draw text on
                    if(globals.materials[material]["Rectangle_id"] != None):
                        #Find coordinates and height of materials->rectangle
                        rectangle_x0 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0]
                        rectangle_y0 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1]
                        rectangle_x1 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2]
                        rectangle_y1 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]
                        rectangle_height = rectangle_y1 - rectangle_y0
                        rectangle_middle_x = (rectangle_x0 + rectangle_x1)/2
                        rectangle_middle_y = (rectangle_y0 + rectangle_y1)/2

                        #Create text inside rectangle
                        if(text_height < rectangle_height):
                            created_text = self.layer_stack_canvas.create_text(
                                rectangle_middle_x, rectangle_middle_y, 
                                text=f"{material} - {globals.materials[material]['Thickness [nm]'].get()} {globals.materials[material]['Unit'].get()}", 
                                fill=settings.layer_stack_canvas_text_color, 
                                font=(settings.text_font, settings.layer_stack_canvas_text_size), 
                                anchor="center", 
                                tags="text"
                            )

                            #Add text element to dictionary
                            globals.materials[material]["Text_id"] = created_text
                        
                        #Create text, text_bbox and line pointer outside rectangle
                        else:
                            created_text = self.layer_stack_canvas.create_text(
                                self.visible_canvas_bbox_x0, rectangle_middle_y, 
                                text=f"{material} - {globals.materials[material]['Thickness [nm]'].get()} {globals.materials[material]['Unit'].get()}", 
                                fill=settings.layer_stack_canvas_text_color, 
                                font=(settings.text_font, settings.layer_stack_canvas_text_size), 
                                tags="text"
                            )
                            created_text_bbox = self.layer_stack_canvas.create_rectangle(
                                self.layer_stack_canvas.bbox(created_text), 
                                outline=settings.layer_stack_canvas_text_color, 
                                tags="text_bbox"
                            )

                            #Get coordinates of text bounding box
                            text_bbox_x0 = self.layer_stack_canvas.bbox(created_text)[0]
                            text_bbox_y0 = self.layer_stack_canvas.bbox(created_text)[1]
                            text_bbox_x1 = self.layer_stack_canvas.bbox(created_text)[2]
                            text_bbox_y1  = self.layer_stack_canvas.bbox(created_text)[3]
                            text_bbox_middle_y = (text_bbox_y0 + text_bbox_y1) / 2

                            created_arrow_line = self.layer_stack_canvas.create_line(
                                (text_bbox_x1, text_bbox_middle_y), (rectangle_x0, rectangle_middle_y), 
                                arrow=tkinter.LAST, 
                                fill=settings.layer_stack_canvas_text_color,
                                tags="arrow_line"
                            )

                            #Add created elements to dictionary
                            globals.materials[material]["Text_id"] = created_text
                            globals.materials[material]["Text_bbox_id"] = created_text_bbox
                            globals.materials[material]["Line_id"] = created_arrow_line
                            

        #ADJUSTMENT OF TEXT: LEFT AND RIGHT            
        match globals.current_view.get():
            #Text overlaps with canvas right side
            case "Stacked" | "Realistic" | "Multi":
                #Loop through all materials
                for material in globals.materials:
                    if(globals.materials[material]["Text_bbox_id"] != None):

                        #Get the coordinates of the text_bbox
                        text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        text_bbox_x0 = text_bbox_coordinates[0]
                        text_bbox_y0 = text_bbox_coordinates[3]
                        text_bbox_x1 = text_bbox_coordinates[2]
                        text_bbox_y1 = text_bbox_coordinates[1]

                        #if the text_bbox overlaps with canvas right side:
                        if(text_bbox_x1 > self.visible_canvas_bbox_x1):
                            #find the overlap
                            overlap = text_bbox_x1 - self.visible_canvas_bbox_x1
                            #move the text, text_bbox and pointer line to the left
                            self.layer_stack_canvas.move(globals.materials[material]["Text_id"], -overlap, 0)
                            self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], -overlap, 0)

                            #Get the text_bbox new coordinates
                            text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"]) 
                            text_bbox_x0 = text_bbox_coordinates[0]
                            text_bbox_y0 = text_bbox_coordinates[3]
                            text_bbox_x1 = text_bbox_coordinates[2]
                            text_bbox_y1 = text_bbox_coordinates[1]
                            text_bbox_middle_y = (text_bbox_y0 + text_bbox_y1) / 2 
                            rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                            #Move the pointer line
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], text_bbox_x0, text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)


            #Text overlaps with canvas left side
            case "Stepped":
                #Loop through all materials
                for material in globals.materials:
                    if(globals.materials[material]["Text_bbox_id"] != None):

                        #Get the coordinates of the text_bbox
                        text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        text_bbox_x0 = text_bbox_coordinates[0]
                        text_bbox_y0 = text_bbox_coordinates[3]
                        text_bbox_x1 = text_bbox_coordinates[2]
                        text_bbox_y1 = text_bbox_coordinates[1]

                        #if the text_bbox overlaps with canvas left side:
                        if(text_bbox_x0 < self.visible_canvas_bbox_x0):
                            #find the overlap
                            overlap = self.visible_canvas_bbox_x0 - text_bbox_x0
                            #move the text, text_bbox and pointer line to the right
                            self.layer_stack_canvas.move(globals.materials[material]["Text_id"], overlap, 0)
                            self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], overlap, 0)

                            #Get the text_bbox new coordinates
                            text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"]) 
                            text_bbox_x0 = text_bbox_coordinates[0]
                            text_bbox_y0 = text_bbox_coordinates[3]
                            text_bbox_x1 = text_bbox_coordinates[2]
                            text_bbox_y1 = text_bbox_coordinates[1]
                            text_bbox_middle_y = (text_bbox_y0 + text_bbox_y1) / 2 
                            rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                            #Move the pointer line
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], text_bbox_x1, text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)
            
        
        #ADJUSTMENT OF TEXT: UP, DOWN AND OVERLAP
        #Loop through every material from TOP layer to LOWEST layer
        previous_text_bbox_id = None
        for material in dict(reversed(globals.materials.items())):
            if(globals.materials[material]["Text_bbox_id"] != None):
                #Get the coordinates of the current_material_text_bbox
                current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                current_text_bbox_x0 = current_text_bbox[0]
                current_text_bbox_y0 = current_text_bbox[3]
                current_text_bbox_x1 = current_text_bbox[2]
                current_text_bbox_y1 = current_text_bbox[1]

                #if the text_bbox top overlaps with the canvas top
                if(current_text_bbox_y1 < self.visible_canvas_bbox_y1):
                    #find the overlap
                    overlap = self.visible_canvas_bbox_y1 - current_text_bbox_y1
                    #Move the text, text_bbox and line_id down
                    self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, overlap)
                    self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, overlap)

                    #Get the new text_bbox coordinates
                    current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_text_bbox_x0 = current_text_bbox[0]
                    current_text_bbox_y0 = current_text_bbox[3]
                    current_text_bbox_x1 = current_text_bbox[2]
                    current_text_bbox_y1 = current_text_bbox[1]
                    current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                    #Get coordinates of matching rectangle
                    rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                    #Move the pointer line based on stack view
                    match globals.current_view.get():
                        case "Stacked" | "Realistic" | "Multi":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x0, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                        case "Stepped":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x1, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)

            
                #if there is a previous text_bbox
                if(previous_text_bbox_id != None):
                    #Get the coordinates of the current_material text_bbox
                    current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_text_bbox_x0 = current_text_bbox[0]
                    current_text_bbox_y0 = current_text_bbox[3]
                    current_text_bbox_x1 = current_text_bbox[2]
                    current_text_bbox_y1 = current_text_bbox[1]
                    
                    #Get the coordinates of the previous_material text_bbox
                    previous_text_bbox = self.layer_stack_canvas.bbox(previous_text_bbox_id)
                    previous_text_bbox_x0 = previous_text_bbox[0]
                    previous_text_bbox_y0 = previous_text_bbox[3]
                    previous_text_bbox_x1 = previous_text_bbox[2]
                    previous_text_bbox_y1 = previous_text_bbox[1]


                    #if the current_material text_bbox top is overlapping the previous_material text_bbox bottom
                    if(current_text_bbox_y1 < previous_text_bbox_y0):
                        #find the overlap
                        overlap = previous_text_bbox_y0 - current_text_bbox_y1 
                        #move the current_materials->text, text_bbox and line down
                        self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, overlap)
                        self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, overlap)

                        #Get the new text_bbox coordinates
                        current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        current_text_bbox_x0 = current_text_bbox[0]
                        current_text_bbox_y0 = current_text_bbox[3]
                        current_text_bbox_x1 = current_text_bbox[2]
                        current_text_bbox_y1 = current_text_bbox[1]
                        current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                        #Get coordinates of matching rectangle
                        rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                        
                        #Move the pointer line based on stack view
                        match globals.current_view.get():
                            case "Stacked" | "Realistic" | "Multi":
                                self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x0, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                            case "Stepped":
                                self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x1, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)

        
                #Set the previous_material_text_bbox_id to the current one
                previous_text_bbox_id = globals.materials[material]["Text_bbox_id"]


        #Loop through every material from LOWEST layer to TOP layer
        previous_text_bbox_id = None
        for material in globals.materials:
            if(globals.materials[material]["Text_bbox_id"] != None):
                #Get the coordinates of the current_material_text_bbox
                current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                current_text_bbox_x0 = current_text_bbox[0]
                current_text_bbox_y0 = current_text_bbox[3]
                current_text_bbox_x1 = current_text_bbox[2]
                current_text_bbox_y1 = current_text_bbox[1]

                #if the text_bbox bottom overlaps with the canvas bottom
                if(current_text_bbox_y0 > self.visible_canvas_bbox_y0):
                    #find the overlap
                    overlap = current_text_bbox_y0 - self.visible_canvas_bbox_y0 
                    #Move the text, text_bbox and line_id down
                    self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, -overlap)
                    self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, -overlap)

                    #Get the new text_bbox coordinates
                    current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_text_bbox_x0 = current_text_bbox[0]
                    current_text_bbox_y0 = current_text_bbox[3]
                    current_text_bbox_x1 = current_text_bbox[2]
                    current_text_bbox_y1 = current_text_bbox[1]
                    current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                    #Get coordinates of matching rectangle
                    rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                    #Move the pointer line based on stack view
                    match globals.current_view.get():
                        case "Stacked" | "Realistic" | "Multi":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x0, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                        case "Stepped":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x1, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)
            
                #if there is a previous text_bbix
                if(previous_text_bbox_id != None):
                    #Get the coordinates of the current_material text_bbox
                    current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_text_bbox_x0 = current_text_bbox[0]
                    current_text_bbox_y0 = current_text_bbox[3]
                    current_text_bbox_x1 = current_text_bbox[2]
                    current_text_bbox_y1 = current_text_bbox[1]
                    
                    #Get the coordinates of the previous_material_text_bbox text_bbox
                    previous_text_bbox = self.layer_stack_canvas.bbox(previous_text_bbox_id)
                    previous_text_bbox_x0 = previous_text_bbox[0]
                    previous_text_bbox_y0 = previous_text_bbox[3]
                    previous_text_bbox_x1 = previous_text_bbox[2]
                    previous_text_bbox_y1 = previous_text_bbox[1]


                    #if the current_material text_bbox bottom is overlapping the previous_material text_bbox top
                    if(current_text_bbox_y0 > previous_text_bbox_y1):
                        #find the overlap
                        overlap = current_text_bbox_y0 - previous_text_bbox_y1  
                        #move the current_materials->text, text_bbox and line down
                        self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, -overlap)
                        self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, -overlap)

                        #Get the new text_bbox coordinates
                        current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        current_text_bbox_x0 = current_text_bbox[0]
                        current_text_bbox_y0 = current_text_bbox[3]
                        current_text_bbox_x1 = current_text_bbox[2]
                        current_text_bbox_y1 = current_text_bbox[1]
                        current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                        #Get coordinates of matching rectangle
                        rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                        
                        #Move the pointer line based on stack view
                        match globals.current_view.get():
                            case "Stacked" | "Realistic" | "Multi":
                                self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x0, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                            case "Stepped":
                                self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x1, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)
            
                #Set the previous_material to the current one
                previous_text_bbox_id = globals.materials[material]["Text_bbox_id"]

        
    def write_indent_on_stepped_stack(self):
        """Writes the indent ranges on the stepped material stack"""
        
        #print("WRITE_INDENT_ON_STEPPED_STACK()")

        #TODO
            #loop through materials from top layer to bottom layer
            #if text_bbox_top overlaps with canvas_top
                #move text_bbox down
        
            #if text_bbox_bottom overlaps with canvas_bottom
                #move text_bbox_up

            #if current_text_bbox_top overlaps previous_text_bbox_bottom
                #move current_text_bbox down
    

            #loop through materials from bottom layer to top layer
            #if text_bbox_top overlaps with canvas_top
                #move text_bbox down
        
            #if text_bbox_bottom overlaps with canvas_bottom
                #move text_bbox_up

            #if current_text_bbox_bottom overlaps with previous_text_bbox_top
                #move current_text_bbox up 


        #CREATION OF INDENT_LINE, INDENT_TEXT, INDENT_TEXT_BBOX AND INDENT_ARROW_POINTER
        previous_material = None
        #Go through every material from LOWEST layer to TOP layer
        for material in globals.materials:
            #Only create indent text if the material has a rectangle that indent can be drawn on
            if(globals.materials[material]["Rectangle_id"] != None):
                #if there is a previous material
                if(previous_material != None):
                    #Only create indent text if material->indent value is bigger than zero
                    if(globals.materials[material]["Indent [nm]"].get() > 0):
                        current_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])
                        current_rectangle_x0 = current_material_rect_coordinates[0]
                        current_rectangle_y0 = current_material_rect_coordinates[3]
                        current_rectangle_x1 = current_material_rect_coordinates[2]
                        current_rectangle_y1 = current_material_rect_coordinates[1]

                        previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                        previous_rectangle_x0 = previous_material_rect_coordinates[0]
                        previous_rectangle_y0 = previous_material_rect_coordinates[3]
                        previous_rectangle_x1 = previous_material_rect_coordinates[2]
                        previous_rectangle_y1 = previous_material_rect_coordinates[1]

                        #Create a two sided arrow line between the differense of the two rectangles
                        indent_line = self.layer_stack_canvas.create_line(
                            current_rectangle_x1, current_rectangle_y0-5, previous_rectangle_x1, previous_rectangle_y1-3,                       
                            fill=settings.text_color,
                            arrow=tkinter.BOTH,
                            tags="arrow_line_both"
                        )

                        #Create a text on the side of the current material->rectangle with indent number
                        indent_text = self.layer_stack_canvas.create_text(
                            (self.visible_canvas_bbox_x1), (current_rectangle_y0 - 10),
                            text=f"{globals.materials[material]['Indent [nm]'].get()} {globals.materials[material]['Unit'].get()}",
                            fill=settings.text_color, 
                            font=(settings.text_font, settings.text_size),
                            tags="text"
                        )

                        #Create a bbox around the indent_text
                        indent_text_bbox = self.layer_stack_canvas.create_rectangle(
                            self.layer_stack_canvas.bbox(indent_text), 
                            outline=settings.text_color, 
                            tags="text_bbox"
                        )

                        #Find the coordinates of the indent_text_bbox
                        indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(indent_text_bbox)
                        indent_text_bbox_x0 = indent_text_bbox_coordinates[0]
                        indent_text_bbox_y0 = indent_text_bbox_coordinates[3]
                        indent_text_bbox_x1 = indent_text_bbox_coordinates[2]
                        indent_text_bbox_y1 = indent_text_bbox_coordinates[1]


                        #Draw an indent_arrow_pointer from indent_text_bbox to indent_line 
                        indent_arrow_pointer = self.layer_stack_canvas.create_line(
                            indent_text_bbox_x0, (indent_text_bbox_y1+indent_text_bbox_y0)/2,
                            previous_rectangle_x1+3, previous_rectangle_y1-2,
                            arrow=tkinter.LAST, 
                            fill=settings.text_color,
                            tags="arrow_line"
                        )

                        #add all elements to materials{} dictionary
                        globals.materials[material]["Indent_line_id"] = indent_line
                        globals.materials[material]["Indent_text_id"] = indent_text
                        globals.materials[material]["Indent_text_bbox_id"] = indent_text_bbox
                        globals.materials[material]["Indent_arrow_pointer_id"] = indent_arrow_pointer 


                #Set previous_material to current material
                previous_material = material


        #ADJUSTMENT OF TEXT: LEFT AND RIGHT   
        previous_material = None
        #Go through every material
        for material in globals.materials:
            if(globals.materials[material]["Rectangle_id"] != None):
                #if current material has a indent_text_bbox
                if(globals.materials[material]["Indent_text_bbox_id"] != None):
                    #Get coordinates of indent_text_bbox
                    indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                    indent_text_bbox_x0 = indent_text_bbox_coordinates[0]
                    indent_text_bbox_y0 = indent_text_bbox_coordinates[3]
                    indent_text_bbox_x1 = indent_text_bbox_coordinates[2]
                    indent_text_bbox_y1 = indent_text_bbox_coordinates[1]

                    #if indent_text_bbox overlaps with canvas RIGHT side
                    if(indent_text_bbox_x1 > self.visible_canvas_bbox_x1):
                        #find overlap
                        overlap = indent_text_bbox_x1 - self.visible_canvas_bbox_x1
                        #move indent_text and indent_text_bbox to the left
                        self.layer_stack_canvas.move(globals.materials[material]["Indent_text_id"], -overlap, 0)
                        self.layer_stack_canvas.move(globals.materials[material]["Indent_text_bbox_id"], -overlap, 0)
                        
                        #Get new coordinates of indent_text_bbox
                        indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                        indent_text_bbox_x0 = indent_text_bbox_coordinates[0]
                        indent_text_bbox_y0 = indent_text_bbox_coordinates[3]
                        indent_text_bbox_x1 = indent_text_bbox_coordinates[2]
                        indent_text_bbox_y1 = indent_text_bbox_coordinates[1]
                        indent_text_bbox_middle_y = (indent_text_bbox_y0 + indent_text_bbox_y1) / 2 

                        #Get coordinates of previous_material->rectangle
                        previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                        previous_rectangle_x0 = previous_material_rect_coordinates[0]
                        previous_rectangle_y0 = previous_material_rect_coordinates[3]
                        previous_rectangle_x1 = previous_material_rect_coordinates[2]
                        previous_rectangle_y1 = previous_material_rect_coordinates[1]

                        #Move indent_arrow_pointer to the left
                        self.layer_stack_canvas.coords(globals.materials[material]["Indent_arrow_pointer_id"], indent_text_bbox_x0, indent_text_bbox_middle_y, previous_rectangle_x1, previous_rectangle_y1-3)

                previous_material = material

        
        #ADJUSTMENT OF TEXT: UP, DOWN AND OVERLAP
        previous_material = None
        #Go through every material from LOWEST layer to TOP layer
        for material in globals.materials:
            #If current material has a rectangle
            if(globals.materials[material]["Rectangle_id"] != None):
                #if current material has a indent_text_bbox
                if(globals.materials[material]["Indent_text_bbox_id"] != None):
                    #Get current_indent_text_bbox coordinates
                    current_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                    current_indent_bbox_x0 = current_indent_text_bbox_coordinates[0]
                    current_indent_bbox_y0 = current_indent_text_bbox_coordinates[3]
                    current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                    current_indent_bbox_y1 = current_indent_text_bbox_coordinates[1]
                    current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2 

                    #if current_indent_text_bbox bottom overlaps with canvas bottom
                    if(current_indent_bbox_y0 > self.visible_canvas_bbox_y0):
                        #Find overlap
                        overlap = current_indent_bbox_y0 - self.visible_canvas_bbox_y0

                        #move indent_text, indent_text_bbox and indent_arrow_pointer up
                        self.layer_stack_canvas.move(globals.materials[material]["Indent_text_id"], 0, -overlap)
                        self.layer_stack_canvas.move(globals.materials[material]["Indent_text_bbox_id"], 0, -overlap)

                        #Get new coordinates of indent_text_bbox
                        current_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                        current_indent_bbox_x0 = current_indent_text_bbox_coordinates[0]
                        current_indent_bbox_y0 = current_indent_text_bbox_coordinates[3]
                        current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                        current_indent_bbox_y1 = current_indent_text_bbox_coordinates[1]
                        current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2  

                        #Get coordinates of previous_material->rectangle
                        previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                        previous_rectangle_x0 = previous_material_rect_coordinates[0]
                        previous_rectangle_y0 = previous_material_rect_coordinates[3]
                        previous_rectangle_x1 = previous_material_rect_coordinates[2]
                        previous_rectangle_y1 = previous_material_rect_coordinates[1]

                        #Move indent_arrow_pointer up
                        self.layer_stack_canvas.coords(globals.materials[material]["Indent_arrow_pointer_id"], current_indent_bbox_x0, current_indent_bbox_middle_y, previous_rectangle_x1, previous_rectangle_y1-3)

                    #current_indent_text_bbox top overlaps with canvas top
                    if(current_indent_bbox_y1 < self.visible_canvas_bbox_y1):
                        #Find overlap
                        overlap = current_indent_bbox_y1 - self.visible_canvas_bbox_y1
                        print(overlap)
                        #move indent_text, indent_text_bbox and indent_arrow_pointer down
                        self.layer_stack_canvas.move(globals.materials[material]["Indent_text_id"], 0, -overlap)
                        self.layer_stack_canvas.move(globals.materials[material]["Indent_text_bbox_id"], 0, -overlap)


                        #Get new coordinates of indent_text_bbox
                        current_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                        current_indent_bbox_x0 = current_indent_text_bbox_coordinates[0]
                        current_indent_bbox_y0 = current_indent_text_bbox_coordinates[3]
                        current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                        current_indent_bbox_y1 = current_indent_text_bbox_coordinates[1]
                        current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2  

                        #Get coordinates of previous_material->rectangle
                        previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                        previous_rectangle_x0 = previous_material_rect_coordinates[0]
                        previous_rectangle_y0 = previous_material_rect_coordinates[3]
                        previous_rectangle_x1 = previous_material_rect_coordinates[2]
                        previous_rectangle_y1 = previous_material_rect_coordinates[1]

                        #Move indent_arrow_pointer down
                        self.layer_stack_canvas.coords(globals.materials[material]["Indent_arrow_pointer_id"], current_indent_bbox_x0, current_indent_bbox_middle_y, previous_rectangle_x1, previous_rectangle_y1-3)

                    #if there is a previous_indent_text_bbox
                    if(globals.materials[previous_material]["Indent_text_bbox_id"] != None):
                        #get coordinates of current material indent_text_bbox
                        current_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                        current_indent_bbox_x0 = current_indent_text_bbox_coordinates[0]
                        current_indent_bbox_y0 = current_indent_text_bbox_coordinates[3]
                        current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                        current_indent_bbox_y1 = current_indent_text_bbox_coordinates[1]
                        current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2 

                        #get coordinates of previous material indent_text_bbox
                        previous_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Indent_text_bbox_id"])
                        previous_indent_bbox_x0 = previous_indent_text_bbox_coordinates[0]
                        previous_indent_bbox_y0 = previous_indent_text_bbox_coordinates[3]
                        previous_indent_bbox_x1 = previous_indent_text_bbox_coordinates[2]
                        previous_indent_bbox_y1 = previous_indent_text_bbox_coordinates[1]

                        #if current_indent_text_bbox bottom overlaps with previous indent_text_bbox top
                        if(current_indent_bbox_y0 > previous_indent_bbox_y1):
                            #find overlap
                            overlap = current_indent_bbox_y0 - previous_indent_bbox_y1

                            #move current indent_text_bbox, indent_text and arrow pointer up
                            self.layer_stack_canvas.move(globals.materials[material]["Indent_text_id"], 0, -overlap)
                            self.layer_stack_canvas.move(globals.materials[material]["Indent_text_bbox_id"], 0, -overlap)

                            #Get new coordinates of indent_text_bbox
                            current_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                            current_indent_bbox_x0 = current_indent_text_bbox_coordinates[0]
                            current_indent_bbox_y0 = current_indent_text_bbox_coordinates[3]
                            current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                            current_indent_bbox_y1 = current_indent_text_bbox_coordinates[1]
                            current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2  

                            #Get coordinates of previous_material->rectangle
                            previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                            previous_rectangle_x0 = previous_material_rect_coordinates[0]
                            previous_rectangle_y0 = previous_material_rect_coordinates[3]
                            previous_rectangle_x1 = previous_material_rect_coordinates[2]
                            previous_rectangle_y1 = previous_material_rect_coordinates[1]

                            #Move indent_arrow_pointer up
                            self.layer_stack_canvas.coords(globals.materials[material]["Indent_arrow_pointer_id"], current_indent_bbox_x0, current_indent_bbox_middle_y, previous_rectangle_x1, previous_rectangle_y1-3)


                        #if current_indent_text_bbox bottom overlaps with previous indent_text_bbox top


                #Set previous_material to current material
                previous_material = material


    def draw_Zn_and_Zp(self):
        """
        -Draws Zn and Zp lines on the stack\n
        -Draws neutral axis on the stack\n
        -Draws total height line on the stack
        """
        # print("DRAW_ZN_AND_ZP()")

        try:
            #Check for errors
            if(len(globals.materials) == 0):
                raise ValueError("No materials")

            if(globals.piezo_material_name.get() == ""):
                raise ValueError("No Piezo material selected")

            #Create line from bottom of stack to top of stack (total height line)
            self.layer_stack_canvas.create_line(
                (self.visible_canvas_bbox_x0 + 10, self.visible_canvas_bbox_y0), 
                (self.visible_canvas_bbox_x0 + 10, self.visible_canvas_bbox_y1), 
                arrow=tkinter.BOTH, 
                arrowshape=(10,10,5),
                width=3,
                fill="black",
                tags="arrow_line_both"
            ) 

            
            #Find the total height of all materials combined
            total_height_of_materials = 0
            for material in globals.materials:
                total_height_of_materials += globals.materials[material]["Thickness [nm]"].get()
            
            #Create text to explain the total height of the stack in "nm"
            self.layer_stack_canvas.create_text(
                self.visible_canvas_bbox_x0 + 90, self.visible_canvas_bbox_y1 + 30,
                text=f"Total height:\n{total_height_of_materials} nm", 
                fill=settings.layer_stack_canvas_text_color, 
                font=(settings.text_font, settings.layer_stack_canvas_text_size),
                tags="text" 
            )


            #Find nanometers needed to represent 1 pixel
            nm_per_pixel = total_height_of_materials/self.layer_stack_canvas_height

            #Create lists of modulus, thickness and poisson values
            E = []
            t = []
            nu = []

            for material in globals.materials:
                E.append(globals.materials[material]["Modulus [GPa]"].get() * 1e9)
                t.append(globals.materials[material]["Thickness [nm]"].get() / 1e9)
                nu.append(globals.materials[material]["Poisson"].get())

            #Calculate Zn
            # Zn = round(globals.equations.calculate_Zn(E, t, nu), 1)
            Zn = globals.equations.calculate_Zn(E, t, nu)
            if(isinstance(Zn, Exception)):
                raise ValueError(f"Zn could not be calculated.\nerror:'{Zn}'")

            #Convert Zn to nanometers
            Zn = Zn * 1e9

            #Convert Zn to pixels
            Zn_pixels = Zn / nm_per_pixel

            #Draw the neutral axis line on the canvas
            self.layer_stack_canvas.create_line(
                self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, self.visible_canvas_bbox_y0 - Zn_pixels,
                self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_multi_offset_right_side + 10, self.visible_canvas_bbox_y0 - Zn_pixels, 
                fill="orange",
                width=4,
                dash=1,
                tags="dotted_line"
            )

            #Draw line from bottom of stack up to neutral axis
            self.layer_stack_canvas.create_line(
                (self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, self.visible_canvas_bbox_y0),
                (self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, self.visible_canvas_bbox_y0 - Zn_pixels), 
                arrow=tkinter.BOTH, 
                arrowshape=(10,10,5),
                fill="black",
                width = 3,
                tags="arrow_line_both"
            ) 

            #Write "neutral axis" text
            self.layer_stack_canvas.create_text(
                self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 70, self.visible_canvas_bbox_y0 - Zn_pixels,
                text=f"Neutral axis", 
                fill="black", 
                font=(settings.text_font, settings.layer_stack_canvas_text_size), 
                tags="text"
            )

            #Write "Zn" text
            self.layer_stack_canvas.create_text(
                self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 70,
                self.visible_canvas_bbox_y0 - (self.visible_canvas_bbox_y0 - (self.visible_canvas_bbox_y0 - Zn_pixels))/2,
                text=f"Zn={round(Zn,1)}", 
                fill="black", 
                font=(settings.text_font, settings.layer_stack_canvas_text_size), 
                tags="text"
            )


            #Populate a list with thickness values from layer1 up until "PZT" material
            t_piezo_list = []
            for material in globals.materials:
                # if(material == globals.parameters_panel.piezo_material_entry.get()):
                if(material == globals.piezo_material_name.get()):
                    break

                #Convert thickness to nanometers and append it to list 
                t_piezo_list.append(globals.materials[material]["Thickness [nm]"].get() / 1e9)
                
            #Fetch thickness value for Piezo material
            # piezo_thickness = globals.materials[globals.parameters_panel.piezo_material_entry.get()]["Thickness [nm]"].get() / 1e9
            piezo_thickness = globals.materials[globals.piezo_material_name.get()]["Thickness [nm]"].get() / 1e9


            #Calculate Zp
            Zp = globals.equations.calculate_mid_piezo(t_piezo_list, Zn/1e9, piezo_thickness) + Zn/ 1e9
            if(isinstance(Zp, Exception)):
                raise ValueError(f"Zp could not be calculated.\nerror:'{Zp}'")


            #Convert Zn to nanometers
            Zp = Zp * 1e9

            #Convert Zp to pixels
            Zp_pixels = Zp / nm_per_pixel 

            #Draw the Zp line on the canvas
            self.layer_stack_canvas.create_line(
                self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, self.visible_canvas_bbox_y0 - Zp_pixels,
                self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_multi_offset_right_side + 10, self.visible_canvas_bbox_y0 - Zp_pixels, 
                fill="blue",
                width=4,
                dash=1,
                tags="dotted_line"
            )

            #Draw line from Zn to Zp
            self.layer_stack_canvas.create_line(
                (self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, self.visible_canvas_bbox_y0 - Zn_pixels),
                (self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, self.visible_canvas_bbox_y0 - Zp_pixels), 
                arrow=tkinter.BOTH, 
                arrowshape=(10,10,5),
                fill="black",
                width = 3,
                tags="arrow_line_both"
            )


            #Write "Zp" text
            self.layer_stack_canvas.create_text(
                self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 70, self.visible_canvas_bbox_y0 - Zp_pixels - (Zn_pixels - Zp_pixels)/2,
                text=f"Zp={round(Zp-Zn, 1)}", 
                fill="black", 
                font=(settings.text_font, settings.layer_stack_canvas_text_size), 
                tags="text"
            )

        except Exception as error:
            self.layer_stack_canvas.create_text(
                self.visible_canvas_bbox_x1/2, self.visible_canvas_bbox_y0/2,
                text=f"Could not draw Zn, neutral axis and Zp\n{error}", 
                fill="red", 
                font=(settings.text_font, settings.layer_stack_canvas_text_size), 
            )
            return