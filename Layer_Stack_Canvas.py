import tkinter
from tkinter import font
import customtkinter
import settings
import globals


#This class handles everything that happens on the canvas 
class Layer_Stack_Canvas:
    def __init__(self, window):
        #Create a canvas in a given window
        self.program_window = window

        self.current_scale = 1.0

        self.layer_stack_canvas = self.create_canvas()

        #Draw material stack
        self.draw_material_stack()


    """Returns a canvas created in the program window"""
    def create_canvas(self):
        #print("CREATE_CANVAS()")
        
        layer_stack_canvas = tkinter.Canvas(
            master=self.program_window,
            bg=settings.layer_stack_canvas_background_color,
            # highlightbackground="red", 
            highlightthickness=0,
        )
        layer_stack_canvas.grid(
            row=0, 
            column=1, 
            sticky="nsew", 
            padx=(settings.layer_stack_canvas_padding_left, settings.layer_stack_canvas_padding_right), 
            pady=(settings.layer_stack_canvas_padding_top, settings.layer_stack_canvas_padding_bottom)
        )

        #Update program to get correct screen&frame sizes
        self.program_window.update()

        #Set canvas_bbox coordniates for later use
        self.visible_canvas_bbox_x0 = 0
        self.visible_canvas_bbox_y0 = 0
        self.visible_canvas_bbox_x1 = layer_stack_canvas.winfo_width() - 1
        self.visible_canvas_bbox_y1 = layer_stack_canvas.winfo_height() - 1
        self.layer_stack_canvas_height = self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0
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


    """Remembers the initial mouse click-position on the canvas"""
    def click_on_canvas(self, event, canvas):
        #print("CLICK_ON_CANVAS()")
        canvas.scan_mark(event.x, event.y)
    

    """Moves the position of the canvas"""
    def canvas_drag(self, event, canvas):
        #print("CANVAS_DRAG()")
        canvas.scan_dragto(event.x, event.y, gain=1)


    """Scales all the elements on the canvas up or down"""
    def canvas_zoom(self, event, canvas):
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


    """Draws the material stack based on the value in the option box"""
    def draw_material_stack(self, *event):
        # print("DRAW MATERIAL STACK()")

        #Sort the materials dictionary after the "layer" value
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["Layer"]))
                
        #Draw stack based on value in option menu
        match globals.option_menu:
            case "Stacked":
                self.draw_material_stack_stacked()
            case "Realistic":
                self.draw_material_stack_realistic()
            case "Stepped":
                self.draw_material_stack_stepped()
            case "Stoney":
                self.draw_material_stack_limited()
            case "Multi":
                self.draw_material_stack_multi()
  

    """
    -Draws the rectangle stack where "substrate" is 1/10 of the canvas no matter what
    """
    def draw_material_stack_stacked(self):       
        # print("DRAW_MATERIAL_STACK_STACKED()")
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


        #Draw bounding box around canvas
        self.layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, 
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color, 
            tags="layer_stack_canvas_bounding_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            if(material.lower() =="substrate"):
                continue    #Skip substrate
            
            rectangle_height = float(globals.materials[material]["Thickness"])
            sum_of_all_materials += rectangle_height
        
        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = round(self.layer_stack_canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y0 + (self.layer_stack_canvas_height*0.9)
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_stacked_text_indent_right_side
        rectangle_y1 = None #Calculated later
        
        #Draw rectangles on canvas
        for material in globals.materials:
            #Create material rectangle only if "thickness" is > zero
            if(float(globals.materials[material]["Thickness"]) > 0):

                #"substrate" will be drawn on the bottom 1/10 of the canvas
                if(material.lower() == "substrate"):  
                    created_rectangle = self.layer_stack_canvas.create_rectangle(
                        # self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y1, rectangle_x1, canvas_height, 
                        self.visible_canvas_bbox_x0, round(self.layer_stack_canvas_height*0.9), rectangle_x1, self.visible_canvas_bbox_y1, 
                        fill=globals.materials[material]["Color"], 
                        outline=settings.layer_stack_canvas_rectangle_outline_color,
                        tags="material_rectangle"
                    )
                    
                    #Add rectangle_id to its place in self.materials
                    globals.materials[material]["Rectangle_id"] = created_rectangle
                
                #Material is not "substrate"
                else:
                    #find how many percent the current rectangle's height is of the total sum of materials
                    rectangle_height = float(globals.materials[material]["Thickness"])
                    rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
                    #Convert rectangle percentage to pixels
                    rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

                    #draw rectangle from top of canvas to its number of pixles in height
                    rectangle_y1 = rectangle_y0 - rectangle_height_pixels
                    created_rectangle = self.layer_stack_canvas.create_rectangle(
                        rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                        fill=globals.materials[material]["Color"],
                        outline=settings.layer_stack_canvas_rectangle_outline_color, 
                        tags="material_rectangle"
                    )

                    #Add rectangle_id to its place in globals.materials
                    globals.materials[material]["Rectangle_id"] = created_rectangle

                    #Add rectangle height to prevent overlaping
                    rectangle_y0 -= rectangle_height_pixels

        #Write text on the stack
        self.write_text_on_stack()

              
    """
    -Draws a realistic version of the rectangle stack
    """
    def draw_material_stack_realistic(self):
        # print("DRAW_MATERIAL_STACK_REALISTIC()")
            
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

        #Draw bounding box around canvas
        self.layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, 
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color , 
            tags="layer_stack_canvas_bounding_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            rectangle_height = float(globals.materials[material]["Thickness"])
            sum_of_all_materials += rectangle_height
        
        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y1
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_stacked_text_indent_right_side
        rectangle_y1 = None #Calculated later

        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = (self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0)
        
        #Draw rectangles on canvas
        for material in globals.materials:
        
            #Create material rectangle only if "thickness" is > zero
            if(float(globals.materials[material]["Thickness"]) > 0):
                #find how many percent the current rectangle's height is of the total sum of materials
                rectangle_height = float(globals.materials[material]["Thickness"])
                rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
                #Convert rectangle percentage to pixels
                rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

                #draw rectangle from top of canvas to its number of pixles in height
                rectangle_y1 = rectangle_y0 - rectangle_height_pixels
                created_rectangle = self.layer_stack_canvas.create_rectangle(
                    rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                    fill=globals.materials[material]["Color"],
                    outline=settings.layer_stack_canvas_rectangle_outline_color, 
                    tags="material_rectangle"
                )

                #Add rectangle_id to its place in self.materials
                globals.materials[material]["Rectangle_id"] = created_rectangle

                #Add rectangle height to prevent overlaping
                rectangle_y0 -= rectangle_height_pixels
            
        
        #Write text on the stack
        self.write_text_on_stack()


    """
    Draws a stepped rectangle stack where "indent" decide the width of each rectangle
    -Each material is drawn from the bottom left corner
    """
    def draw_material_stack_stepped(self):
        # print("DRAW_MATERIAL_STACK_STEPPED()")

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
            if(material.lower() == "substrate"):
                continue    #Skip substrate

            sum_of_all_materials += float(globals.materials[material]["Thickness"])
            if(biggest_material < float(globals.materials[material]["Thickness"])):
                biggest_material = float(globals.materials[material]["Thickness"])
        
        #Find how many nanometers 1 pixel should represent
        nanometers_per_pixel = sum_of_all_materials/round(self.layer_stack_canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates (from bottom left corner)
        rectangle_x0 = self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_stepped_text_indent_left_side
        rectangle_y0 = round(self.layer_stack_canvas_height*0.9)
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_stepped_text_indent_right_side
        rectangle_y1 = None #calculated later
        previous_rectangle_x1 = self.visible_canvas_bbox_x1

        #If a rectangles x1 coordinate is less than original start drawing point, then it will not be drawn 
        original_rectangle_x0 = rectangle_x0

        #Draw rectangles on canvas
        for material in globals.materials:

            #Draw "substrate" on the bottom 1/10 of the canvas
            if(material.lower() == "substrate"):
                #Find how many pixels is needed to represent the indent of the current material
                indent_width_pixels = float(globals.materials[material]["Indent [nm]"])/nanometers_per_pixel

                #Set the width of the rectangle
                rectangle_x1 = rectangle_x1 - indent_width_pixels

                #Create rectangle
                created_rectangle = self.layer_stack_canvas.create_rectangle(
                    rectangle_x0, rectangle_y0, rectangle_x1, self.visible_canvas_bbox_y1,
                    fill=globals.materials[material]["Color"],
                    outline=settings.layer_stack_canvas_rectangle_outline_color, 
                    tags="material_rectangle"
                )
                
                #Add created rectangle to materials{}
                globals.materials[material]["Rectangle_id"] = created_rectangle

                #Jump to the next material
                continue

            #Create material rectangle only if "thickness" and "indent" is > zero
            if(float(globals.materials[material]["Thickness"]) > 0):# and float(globals.materials[material]["indent"]) >= 0):

                #Find how many pixels is needed to represent the height of the current material
                rectangle_height_pixels = float(globals.materials[material]["Thickness"])/nanometers_per_pixel
                
                #Set the y1 coordinate of the rectangle
                rectangle_y1 = rectangle_y0 - rectangle_height_pixels

                #Find how many pixels is needed to represent the indent of the current material
                indent_width_pixels = float(globals.materials[material]["Indent [nm]"])/nanometers_per_pixel

                #Set the indent width for the current rectangle
                rectangle_x1 =  rectangle_x1 - indent_width_pixels

                #Draw and create rectangle if its width is greater than the original start drawing point for rectangles
                if(rectangle_x1 >= original_rectangle_x0):
                    created_rectangle = self.layer_stack_canvas.create_rectangle(
                        rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                        fill=globals.materials[material]["Color"], 
                        outline=settings.layer_stack_canvas_rectangle_outline_color,
                        tags="material_rectangle"
                    )
                
                    #Add rectangle_id to its place in globals.materials{}
                    globals.materials[material]["Rectangle_id"] = created_rectangle

                #Add rectangle height to prevent overlaping
                rectangle_y0 -= rectangle_height_pixels


        #Write text and indent on stack
        self.write_text_on_stack()
        self.write_indent_on_stepped_stack()
    

    """Draws a material stack only with materials that are "active" in globals.materials"""
    def draw_material_stack_limited(self):
        # print("DRAW_MATERIAL_STACK_LIMITED")

        num_active_materials = 0
        for material in globals.materials:
            if(globals.materials[material]["Status"] == "active"):
                num_active_materials += 1
                
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


        #Draw bounding box around canvas
        self.layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, 
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color, 
            tags="layer_stack_canvas_bounding_rectangle")

        #If the are no active materials to draw, then end the function
        if(num_active_materials <= 0):
            return

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            if(globals.materials[material]["Status"] == "active"):
                if(material.lower() =="substrate"):
                    continue    #Skip substrate
                
                rectangle_height = float(globals.materials[material]["Thickness"])
                sum_of_all_materials += rectangle_height
            
        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = round(self.layer_stack_canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y0 + (self.layer_stack_canvas_height*0.9)
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_stacked_text_indent_right_side
        rectangle_y1 = None #Calculated later
            
        #Draw rectangles on canvas
        # for material in globals.materials:
        for material in globals.materials:
            if(globals.materials[material]["Status"] == "active"):
                #Create material rectangle only if "thickness" is > zero
                if(float(globals.materials[material]["Thickness"]) > 0):

                    #"substrate" will be drawn on the bottom 1/10 of the canvas
                    if(material.lower() == "substrate"):  
                        created_rectangle = self.layer_stack_canvas.create_rectangle(
                            # self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y1, rectangle_x1, canvas_height, 
                            self.visible_canvas_bbox_x0, round(self.layer_stack_canvas_height*0.9), rectangle_x1, self.visible_canvas_bbox_y1, 
                            fill=globals.materials[material]["Color"], 
                            outline=settings.layer_stack_canvas_rectangle_outline_color,
                            tags="material_rectangle"
                        )
                        
                        #Add rectangle_id to its place in self.materials
                        globals.materials[material]["Rectangle_id"] = created_rectangle
                    
                    #Material is not "substrate"
                    else:
                        #find how many percent the current rectangle's height is of the total sum of materials
                        rectangle_height = float(globals.materials[material]["Thickness"])
                        rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
                        #Convert rectangle percentage to pixels
                        rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

                        #draw rectangle from top of canvas to its number of pixles in height
                        rectangle_y1 = rectangle_y0 - rectangle_height_pixels
                        created_rectangle = self.layer_stack_canvas.create_rectangle(
                            rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                            fill=globals.materials[material]["Color"],
                            outline=settings.layer_stack_canvas_rectangle_outline_color, 
                            tags="material_rectangle"
                        )

                        #Add rectangle_id to its place in globals.materials
                        globals.materials[material]["Rectangle_id"] = created_rectangle

                        #Add rectangle height to prevent overlaping
                        rectangle_y0 -= rectangle_height_pixels

        #Write text on the stack
        self.write_text_on_stack()


    """Draws a stacked material stack but with the 'neutral axis'"""
    def draw_material_stack_multi(self):
        # print("DRAW_MATERIAL_STACK_MULTI()")

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

        #Draw bounding box around canvas
        self.layer_stack_canvas.create_rectangle(
            self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, 
            self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, 
            outline=settings.layer_stack_canvas_outline_color , 
            tags="layer_stack_canvas_bounding_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            rectangle_height = float(globals.materials[material]["Thickness"])
            sum_of_all_materials += rectangle_height
        
        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side
        rectangle_y0 = self.visible_canvas_bbox_y1
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_multi_offset_right_side
        rectangle_y1 = None #Calculated later

        canvas_height = (self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0)
        
        #Draw rectangles on canvas
        for material in globals.materials:
            #Create material rectangle only if "thickness" is > zero
            if(float(globals.materials[material]["Thickness"]) > 0):
                #find how many percent the current rectangle's height is of the total sum of materials
                rectangle_height = float(globals.materials[material]["Thickness"])
                rectangle_percentage = (rectangle_height/sum_of_all_materials)*100
                #Convert rectangle percentage to pixels
                rectangle_height_pixels = (rectangle_percentage/100)*canvas_height

                #draw rectangle from bottom left corner of canvas to its number of pixles in height
                rectangle_y1 = rectangle_y0 - rectangle_height_pixels
                created_rectangle = self.layer_stack_canvas.create_rectangle(
                    rectangle_x0, rectangle_y0, rectangle_x1, rectangle_y1, 
                    fill=globals.materials[material]["Color"],
                    outline=settings.layer_stack_canvas_rectangle_outline_color, 
                    tags="material_rectangle"
                )

                #Add rectangle_id to its place in self.materials
                globals.materials[material]["Rectangle_id"] = created_rectangle

                #Add rectangle height to prevent overlaping
                rectangle_y0 -= rectangle_height_pixels

        #Write text on the stack
        self.write_text_on_stack()


        #Create line from bottom of stack to top of stack (total height line)
        self.layer_stack_canvas.create_line(
            (self.visible_canvas_bbox_x0 + 10, self.visible_canvas_bbox_y1), 
            (self.visible_canvas_bbox_x0 + 10, self.visible_canvas_bbox_y0), 
            arrow=tkinter.BOTH, 
            arrowshape=(10,10,5),
            width=3,
            fill="black",
            tags="arrow_line_both"
        ) 

        #Create text to explain the total height of the stack in "nm"
        self.layer_stack_canvas.create_text(
            self.visible_canvas_bbox_x0 + 90, self.visible_canvas_bbox_y0 + 30,
            text=f"Total height:\n{sum_of_all_materials} nm", 
            fill=settings.layer_stack_canvas_text_color, 
            font=(settings.text_font, settings.layer_stack_canvas_text_size),
            tags="text" 
        )

        #Draw neutral axis
        self.draw_Zn_and_Zp()


    """
    -Writes name_labels for each rectangle in the material stack
        -Labels are created on the left side for "stepped" mode and on the right side for "stacked, realistic and stress" mode
    -Creates all texts either inside or outside of the rectangle box based on the rectangles height
    -Loops through all text_boxes, checks for overlaps and potentially moves them around to prevent overlap 
    """
    def write_text_on_stack(self):
        # print("WRITE_TEXT_ON_STACK()")

        #Delete all texts from canvas and dictionary
        for material in globals.materials:
            self.layer_stack_canvas.delete(globals.materials[material]["Text_id"])
            self.layer_stack_canvas.delete(globals.materials[material]["Text_bbox_id"])
            self.layer_stack_canvas.delete(globals.materials[material]["Line_id"])

            globals.materials[material]["Text_id"] = None
            globals.materials[material]["Text_bbox_id"] = None
            globals.materials[material]["Line_id"] = None

        #Find what the height of a text's bounding box will be
        text_font = font.Font(family=settings.text_font, size=settings.text_size)
        text_height = text_font.metrics()['linespace']

        #CREATION OF TEXT, TEXT_BBOX AND LINES
        match globals.option_menu:
            case "Stacked" | "Realistic" | "Stoney" | "Multi":

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
                                text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 
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
                                text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 
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
                                text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 
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
                                text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 
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
        match globals.option_menu:
            #Text overlaps with canvas right side
            case "Stacked" | "Realistic" | "Stoney" | "Multi":
                #Loop through all materials
                for material in globals.materials:
                    if(globals.materials[material]["Text_bbox_id"] != None):

                        #Get the coordinates of the text_bbox
                        text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        text_bbox_x0 = text_bbox_coordinates[0]
                        text_bbox_y0 = text_bbox_coordinates[1]
                        text_bbox_x1 = text_bbox_coordinates[2]
                        text_bbox_y1 = text_bbox_coordinates[3]

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
                            text_bbox_y0 = text_bbox_coordinates[1]
                            text_bbox_x1 = text_bbox_coordinates[2]
                            text_bbox_y1 = text_bbox_coordinates[3]
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
                        text_bbox_y0 = text_bbox_coordinates[1]
                        text_bbox_x1 = text_bbox_coordinates[2]
                        text_bbox_y1 = text_bbox_coordinates[3]

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
                            text_bbox_y0 = text_bbox_coordinates[1]
                            text_bbox_x1 = text_bbox_coordinates[2]
                            text_bbox_y1 = text_bbox_coordinates[3]
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
                current_text_bbox_y0 = current_text_bbox[1]
                current_text_bbox_x1 = current_text_bbox[2]
                current_text_bbox_y1 = current_text_bbox[3]

                #if the text_bbox top overlaps with the canvas top
                if(current_text_bbox_y0 < self.visible_canvas_bbox_y0):
                    #find the overlap
                    overlap = self.visible_canvas_bbox_y0 - current_text_bbox_y0
                    #Move the text, text_bbox and line_id down
                    self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, overlap)
                    self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, overlap)

                    #Get the new text_bbox coordinates
                    current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_text_bbox_x0 = current_text_bbox[0]
                    current_text_bbox_y0 = current_text_bbox[1]
                    current_text_bbox_x1 = current_text_bbox[2]
                    current_text_bbox_y1 = current_text_bbox[3]
                    current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                    #Get coordinates of matching rectangle
                    rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                    #Move the pointer line based on stack view
                    match globals.option_menu:
                        case "Stacked" | "Realistic" | "Stoney" | "Multi":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x0, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                        case "Stepped":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x1, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)

            
                #if there is a previous text_bbox
                if(previous_text_bbox_id != None):
                    #Get the coordinates of the current_material text_bbox
                    current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_text_bbox_x0 = current_text_bbox[0]
                    current_text_bbox_y0 = current_text_bbox[1]
                    current_text_bbox_x1 = current_text_bbox[2]
                    current_text_bbox_y1 = current_text_bbox[3]
                    
                    #Get the coordinates of the previous_material text_bbox
                    previous_text_bbox = self.layer_stack_canvas.bbox(previous_text_bbox_id)
                    previous_text_bbox_x0 = previous_text_bbox[0]
                    previous_text_bbox_y0 = previous_text_bbox[1]
                    previous_text_bbox_x1 = previous_text_bbox[2]
                    previous_text_bbox_y1 = previous_text_bbox[3]


                    #if the current_material text_bbox top is overlapping the previous_material text_bbox bottom
                    if(current_text_bbox_y0 < previous_text_bbox_y1):
                        #find the overlap
                        overlap = previous_text_bbox_y1 - current_text_bbox_y0 
                        #move the current_materials->text, text_bbox and line down
                        self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, overlap)
                        self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, overlap)

                        #Get the new text_bbox coordinates
                        current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        current_text_bbox_x0 = current_text_bbox[0]
                        current_text_bbox_y0 = current_text_bbox[1]
                        current_text_bbox_x1 = current_text_bbox[2]
                        current_text_bbox_y1 = current_text_bbox[3]
                        current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                        #Get coordinates of matching rectangle
                        rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                        
                        #Move the pointer line based on stack view
                        match globals.option_menu:
                            case "Stacked" | "Realistic" | "Stoney" | "Multi":
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
                current_text_bbox_y0 = current_text_bbox[1]
                current_text_bbox_x1 = current_text_bbox[2]
                current_text_bbox_y1 = current_text_bbox[3]

                #if the text_bbox bottom overlaps with the canvas bottom
                if(current_text_bbox_y1 > self.visible_canvas_bbox_y1):
                    #find the overlap
                    overlap = current_text_bbox_y1 - self.visible_canvas_bbox_y1 
                    #Move the text, text_bbox and line_id down
                    self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, -overlap)
                    self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, -overlap)

                    #Get the new text_bbox coordinates
                    current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_text_bbox_x0 = current_text_bbox[0]
                    current_text_bbox_y0 = current_text_bbox[1]
                    current_text_bbox_x1 = current_text_bbox[2]
                    current_text_bbox_y1 = current_text_bbox[3]
                    current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                    #Get coordinates of matching rectangle
                    rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                    #Move the pointer line based on stack view
                    match globals.option_menu:
                        case "Stacked" | "Realistic" | "Stoney" | "Multi":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x0, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                        case "Stepped":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x1, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)
            
                #if there is a previous text_bbix
                if(previous_text_bbox_id != None):
                    #Get the coordinates of the current_material text_bbox
                    current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_text_bbox_x0 = current_text_bbox[0]
                    current_text_bbox_y0 = current_text_bbox[1]
                    current_text_bbox_x1 = current_text_bbox[2]
                    current_text_bbox_y1 = current_text_bbox[3]
                    
                    #Get the coordinates of the previous_material_text_bbox text_bbox
                    previous_text_bbox = self.layer_stack_canvas.bbox(previous_text_bbox_id)
                    previous_text_bbox_x0 = previous_text_bbox[0]
                    previous_text_bbox_y0 = previous_text_bbox[1]
                    previous_text_bbox_x1 = previous_text_bbox[2]
                    previous_text_bbox_y1 = previous_text_bbox[3]


                    #if the current_material text_bbox bottom is overlapping the previous_material text_bbox top
                    if(current_text_bbox_y1 > previous_text_bbox_y0):
                        #find the overlap
                        overlap = current_text_bbox_y1 - previous_text_bbox_y0  
                        #move the current_materials->text, text_bbox and line down
                        self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, -overlap)
                        self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, -overlap)

                        #Get the new text_bbox coordinates
                        current_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        current_text_bbox_x0 = current_text_bbox[0]
                        current_text_bbox_y0 = current_text_bbox[1]
                        current_text_bbox_x1 = current_text_bbox[2]
                        current_text_bbox_y1 = current_text_bbox[3]
                        current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
                        #Get coordinates of matching rectangle
                        rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                        
                        #Move the pointer line based on stack view
                        match globals.option_menu:
                            case "Stacked" | "Realistic" | "Stoney" | "Multi":
                                self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x0, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                            case "Stepped":
                                self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_text_bbox_x1, current_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)
            
                #Set the previous_material to the current one
                previous_text_bbox_id = globals.materials[material]["Text_bbox_id"]

        
    """Writes the indent ranges on the stepped material stack"""
    def write_indent_on_stepped_stack(self):
        # print("WRITE_INDENT_ON_STEPPED_STACK()")

        #Delete all indent texts and arrows from canvas and dictionary
        for material in globals.materials:
            self.layer_stack_canvas.delete(globals.materials[material]["Indent_text_id"])
            self.layer_stack_canvas.delete(globals.materials[material]["Indent_text_bbox_id"])
            self.layer_stack_canvas.delete(globals.materials[material]["Indent_line_id"])
            self.layer_stack_canvas.delete(globals.materials[material]["Indent_arrow_pointer_id"])

            globals.materials[material]["Indent_text_id"] = None
            globals.materials[material]["Indent_text_bbox_id"] = None
            globals.materials[material]["Indent_line_id"] = None
            globals.materials[material]["Indent_arrow_pointer_id"] = None 


        #CREATION OF INDENT_LINE, INDENT_TEXT, INDENT_TEXT_BBOX AND INDENT_ARROW_POINTER
        previous_material = None
        #Go through every material from LOWEST layer to TOP layer
        for material in globals.materials:
            #Only create indent text if the material has a rectangle that indent can be drawn on
            if(globals.materials[material]["Rectangle_id"] != None):
                #if there is a previous material
                if(previous_material != None):
                    #Only create indent text if material->indent value is bigger than zero
                    if(float(globals.materials[material]["Indent [nm]"]) > 0):
                        current_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])
                        current_rectangle_x0 = current_material_rect_coordinates[0]
                        current_rectangle_y0 = current_material_rect_coordinates[1]
                        current_rectangle_x1 = current_material_rect_coordinates[2]
                        current_rectangle_y1 = current_material_rect_coordinates[3]

                        previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                        previous_rectangle_x0 = previous_material_rect_coordinates[0]
                        previous_rectangle_y0 = previous_material_rect_coordinates[1]
                        previous_rectangle_x1 = previous_material_rect_coordinates[2]
                        previous_rectangle_y1 = previous_material_rect_coordinates[3]

                        #Create a two sided arrow line between the differense of the two rectangles
                        indent_line = self.layer_stack_canvas.create_line(
                            current_rectangle_x1, current_rectangle_y1-5, previous_rectangle_x1, previous_rectangle_y0-3,                       
                            fill=settings.text_color,
                            arrow=tkinter.BOTH,
                            tags="arrow_line_both"
                        )

                        #Create a text on the side of the current material->rectangle with indent number
                        indent_text = self.layer_stack_canvas.create_text(
                            (self.visible_canvas_bbox_x1), (current_rectangle_y1 - 10),
                            text=f"{float(globals.materials[material]['Indent [nm]'])} {globals.materials[material]['Unit']}",
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
                        indent_text_bbox_y0 = indent_text_bbox_coordinates[1]
                        indent_text_bbox_x1 = indent_text_bbox_coordinates[2]
                        indent_text_bbox_y1 = indent_text_bbox_coordinates[3]


                        #Draw an indent_arrow_pointer from indent_text_bbox to indent_line 
                        indent_arrow_pointer = self.layer_stack_canvas.create_line(
                            indent_text_bbox_x0, (indent_text_bbox_y1+indent_text_bbox_y0)/2,
                            previous_rectangle_x1+3, previous_rectangle_y0-2,
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
                    indent_text_bbox_y0 = indent_text_bbox_coordinates[1]
                    indent_text_bbox_x1 = indent_text_bbox_coordinates[2]
                    indent_text_bbox_y1 = indent_text_bbox_coordinates[3]

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
                        indent_text_bbox_y0 = indent_text_bbox_coordinates[1]
                        indent_text_bbox_x1 = indent_text_bbox_coordinates[2]
                        indent_text_bbox_y1 = indent_text_bbox_coordinates[3]
                        indent_text_bbox_middle_y = (indent_text_bbox_y0 + indent_text_bbox_y1) / 2 

                        #Get coordinates of previous_material->rectangle
                        previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                        previous_rectangle_x0 = previous_material_rect_coordinates[0]
                        previous_rectangle_y0 = previous_material_rect_coordinates[1]
                        previous_rectangle_x1 = previous_material_rect_coordinates[2]
                        previous_rectangle_y1 = previous_material_rect_coordinates[3]

                        #Move indent_arrow_pointer to the left
                        self.layer_stack_canvas.coords(globals.materials[material]["Indent_arrow_pointer_id"], indent_text_bbox_x0, indent_text_bbox_middle_y, previous_rectangle_x1, previous_rectangle_y0-3)

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
                    current_indent_bbox_y0 = current_indent_text_bbox_coordinates[1]
                    current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                    current_indent_bbox_y1 = current_indent_text_bbox_coordinates[3]
                    current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2 

                    #if current_indent_text_bbox bottom overlaps with canvas bottom
                    if(current_indent_bbox_y1 > self.visible_canvas_bbox_y1):
                        #Find overlap
                        overlap = current_indent_bbox_y1 - self.visible_canvas_bbox_y1

                        #move indent_text, indent_text_bbox and indent_arrow_pointer up
                        self.layer_stack_canvas.move(globals.materials[material]["Indent_text_id"], 0, -overlap)
                        self.layer_stack_canvas.move(globals.materials[material]["Indent_text_bbox_id"], 0, -overlap)

                        #Get new coordinates of indent_text_bbox
                        current_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                        current_indent_bbox_x0 = current_indent_text_bbox_coordinates[0]
                        current_indent_bbox_y0 = current_indent_text_bbox_coordinates[1]
                        current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                        current_indent_bbox_y1 = current_indent_text_bbox_coordinates[3]
                        current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2  

                        #Get coordinates of previous_material->rectangle
                        previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                        previous_rectangle_x0 = previous_material_rect_coordinates[0]
                        previous_rectangle_y0 = previous_material_rect_coordinates[1]
                        previous_rectangle_x1 = previous_material_rect_coordinates[2]
                        previous_rectangle_y1 = previous_material_rect_coordinates[3]

                        #Move indent_arrow_pointer up
                        self.layer_stack_canvas.coords(globals.materials[material]["Indent_arrow_pointer_id"], current_indent_bbox_x0, current_indent_bbox_middle_y, previous_rectangle_x1, previous_rectangle_y0-3)


                    #if there is a previous_indent_text_bbox
                    if(globals.materials[previous_material]["Indent_text_bbox_id"] != None):
                        #get coordinates of current material indent_text_bbox
                        current_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                        current_indent_bbox_x0 = current_indent_text_bbox_coordinates[0]
                        current_indent_bbox_y0 = current_indent_text_bbox_coordinates[1]
                        current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                        current_indent_bbox_y1 = current_indent_text_bbox_coordinates[3]
                        current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2 

                        #get coordinates of previous material indent_text_bbox
                        previous_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Indent_text_bbox_id"])
                        previous_indent_bbox_x0 = previous_indent_text_bbox_coordinates[0]
                        previous_indent_bbox_y0 = previous_indent_text_bbox_coordinates[1]
                        previous_indent_bbox_x1 = previous_indent_text_bbox_coordinates[2]
                        previous_indent_bbox_y1 = previous_indent_text_bbox_coordinates[3]

                        #if current_indent_text_bbox bottom overlaps with previous indent_text_bbox top
                        if(current_indent_bbox_y1 > previous_indent_bbox_y0):
                            #find overlap
                            overlap = current_indent_bbox_y1 - previous_indent_bbox_y0

                            #move current indent_text_bbox, indent_text and arrow pointer up
                            self.layer_stack_canvas.move(globals.materials[material]["Indent_text_id"], 0, -overlap)
                            self.layer_stack_canvas.move(globals.materials[material]["Indent_text_bbox_id"], 0, -overlap)

                            #Get new coordinates of indent_text_bbox
                            current_indent_text_bbox_coordinates = self.layer_stack_canvas.bbox(globals.materials[material]["Indent_text_bbox_id"])
                            current_indent_bbox_x0 = current_indent_text_bbox_coordinates[0]
                            current_indent_bbox_y0 = current_indent_text_bbox_coordinates[1]
                            current_indent_bbox_x1 = current_indent_text_bbox_coordinates[2]
                            current_indent_bbox_y1 = current_indent_text_bbox_coordinates[3]
                            current_indent_bbox_middle_y = (current_indent_bbox_y0 + current_indent_bbox_y1) / 2  

                            #Get coordinates of previous_material->rectangle
                            previous_material_rect_coordinates = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])
                            previous_rectangle_x0 = previous_material_rect_coordinates[0]
                            previous_rectangle_y0 = previous_material_rect_coordinates[1]
                            previous_rectangle_x1 = previous_material_rect_coordinates[2]
                            previous_rectangle_y1 = previous_material_rect_coordinates[3]

                            #Move indent_arrow_pointer up
                            self.layer_stack_canvas.coords(globals.materials[material]["Indent_arrow_pointer_id"], current_indent_bbox_x0, current_indent_bbox_middle_y, previous_rectangle_x1, previous_rectangle_y0-3)

                #Set previous_material to current material
                previous_material = material


    """Draws lines on the stack describing the Zn value"""
    def draw_Zn_and_Zp(self):
        # print("DRAW_NEUTRAL_AXIS()")

        #Find the total height of all materials combined
        total_height_of_materials_nm = 0
        for material in globals.materials:
            total_height_of_materials_nm += float(globals.materials[material]["Thickness"])

        #Find the height of the canvas is pixels
        canvas_height_pixels = self.layer_stack_canvas_height

        #Find nanometers needed to represent 1 pixel
        nm_per_pixel = total_height_of_materials_nm / canvas_height_pixels

        #Calculate Zn
        Zn = round(globals.equations.calculate_Zn(), 1)

        #Convert Zn to pixels
        Zn_pixels = Zn / nm_per_pixel 

        #Draw the neutral axis line on the canvas
        self.layer_stack_canvas.create_line(
            self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, Zn_pixels,
            self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_multi_offset_right_side + 10, Zn_pixels, 
            fill="orange",
            width=7,
            dash=1,
            tags="dotted_line"
        )

        #Draw line from bottom of stack up to neutral axis
        self.layer_stack_canvas.create_line(
            (self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, self.visible_canvas_bbox_y1),
            (self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, Zn_pixels), 
            arrow=tkinter.BOTH, 
            arrowshape=(10,10,5),
            fill="black",
            width = 3,
            tags="arrow_line_both"
        ) 

        #Write "neutral axis" text
        self.layer_stack_canvas.create_text(
            self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 70, Zn_pixels,
            text=f"Neutral axis", 
            fill="black", 
            font=(settings.text_font, settings.layer_stack_canvas_text_size), 
            tags="text"
        )

        #Write "Zn" text
        self.layer_stack_canvas.create_text(
            self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 80,
            self.visible_canvas_bbox_y1 - (self.visible_canvas_bbox_y1 - Zn_pixels)/2,
            text=f"Zn = {Zn}", 
            fill="black", 
            font=(settings.text_font, settings.layer_stack_canvas_text_size), 
            tags="text"
        )


        #Calculate Zp
        Zp = round(globals.equations.calculate_mid_piezo(Zn), 1)

        #Convert Zp to pixels
        Zp_pixels = Zp / nm_per_pixel 

        #Draw the Zp line on the canvas
        self.layer_stack_canvas.create_line(
            self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, Zp_pixels,
            self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_multi_offset_right_side + 10, Zp_pixels, 
            fill="blue",
            width=7,
            dash=1,
            tags="dotted_line"
        )

        #Draw line from Zn to Zp
        self.layer_stack_canvas.create_line(
            (self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, Zn_pixels),
            (self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 10, Zp_pixels), 
            arrow=tkinter.BOTH, 
            arrowshape=(10,10,5),
            fill="black",
            width = 3,
            tags="arrow_line_both"
        ) 


        #Write "Zp" text
        self.layer_stack_canvas.create_text(
            self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_multi_offset_left_side - 80, Zn_pixels - (Zn_pixels - Zp_pixels)/2,
            text=f"Zp = {Zp}", 
            fill="black", 
            font=(settings.text_font, settings.layer_stack_canvas_text_size), 
            tags="text"
        )
