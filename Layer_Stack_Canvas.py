import tkinter
from tkinter import font
import customtkinter
import settings
import globals


#This class handles everything that happens on the canvas 
class Layer_Stack_Canvas:
    def __init__(self, window):
        #Create a canvas in a given window
        self.window = window

        self.current_scale = 1.0

        self.layer_stack_canvas = self.create_canvas()

        #Draw material stack
        self.draw_material_stack()
    

    """Returns a canvas created in the program window"""
    def create_canvas(self):
        #print("CREATE_CANVAS()")
        
        layer_stack_canvas = tkinter.Canvas(
            master=self.window,
            height=settings.layer_stack_canvas_height, 
            width=settings.layer_stack_canvas_width,
            bg=settings.layer_stack_canvas_background_color,
            highlightbackground="red", 
            highlightthickness=0,
        )
        layer_stack_canvas.grid(
            row=0, 
            column=1, 
            sticky="nw", 
            padx=(settings.layer_stack_canvas_padding_left, settings.layer_stack_canvas_padding_right), 
            pady=(settings.layer_stack_canvas_padding_top, settings.layer_stack_canvas_padding_bottom)
        )

        #Set canvas_bbox coordniates for later use
        self.visible_canvas_bbox_x0 = 0
        self.visible_canvas_bbox_y0 = 0
        self.visible_canvas_bbox_x1 = layer_stack_canvas.winfo_reqwidth() - 1
        self.visible_canvas_bbox_y1 = layer_stack_canvas.winfo_reqheight() - 1
        self.layer_stack_canvas_height = self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0
        self.layer_stack_canvas_width = self.visible_canvas_bbox_x1 - self.visible_canvas_bbox_x0
        #This is just a usefull function to find the bbox of the canvas: self.canvas.coords(self.canvas.find_withtag("canvas_bounding_box_rectangle"))[2]

        #Draw bounding box around canvas
        layer_stack_canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline=settings.layer_stack_canvas_outline_color, width=1)

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


            #Redraw text on stack
            match globals.option_menu:
                case "Stacked" | "Realistic" | "Stress":
                    self.write_text_on_stack()
                
                case "Stepped":
                    self.write_text_on_stack()
                    self.write_indent_on_stepped_stack()


    """Draws the material stack based on the value in the option box"""
    def draw_material_stack(self, *event):
        # print("DRAW MATERIAL STACK()")

        #Sort the materials dictionary after the "layer" value
        globals.materials = dict(sorted(globals.materials.items(), key=lambda item: item[1]["Layer"]))
                
        #Draw stack based on value in option menu
        match globals.option_menu:
            case "Stacked" | "Stress":
                self.draw_material_stack_stacked()
            case "Realistic":
                self.draw_material_stack_realistic()
            case "Stepped":
                self.draw_material_stack_stepped()
            

    # """Scales the material stack according to the program window"""
    # def program_window_resized(self, event):
        # print("PROGRAM_WINDOW_RESIZED NOT IMPLEMENTED!!!!!!!!")
        # #Only do something if the window size is changed. (The <configure> method calls this function everytime something about the program window is changed)
        # if(event.width != SETTINGS["PROGRAM_WINDOW_WIDTH"] or event.height != SETTINGS["PROGRAM_WINDOW_HEIGHT"]):
        #     #print("WINDOW RESIZED")
        
        #     #Set the new width of the canvas
        #     self.canvas.config(width=window.winfo_width() - self.user_interface_frame.winfo_reqwidth() - SETTINGS["CANVAS_PROGRAM_BORDER_WIDTH"])

        #     #Update the variables that track the actual visible parts of the canvas
        #     self.visible_canvas_bbox_x1 = self.canvas.winfo_reqwidth() - 1
        #     self.visible_canvas_bbox_y1 = self.canvas.winfo_reqheight() - 1

        #     #Redraw the material stack
        #     self.draw_material_stack()


    """
    -Draws the rectangle stack where "substrate" is 1/10 of the canvas no matter what
    """
    def draw_material_stack_stacked(self):       
        
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
        self.layer_stack_canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline=settings.layer_stack_canvas_outline_color, tags="canvas_bounding_box_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            if(material.lower() =="substrate"):
                continue    #Skip substrate
                
            rectangle_height = int(globals.materials[material]["Thickness"])
            sum_of_all_materials += rectangle_height
        
        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = round(self.layer_stack_canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y0 + (self.layer_stack_canvas_height*0.9)
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_text_indent
        rectangle_y1 = None #Calculated later
        
        #Draw rectangles on canvas
        for material in dict(reversed(globals.materials.items())):

            #Create material rectangle only if "thickness" is > zero
            if(int(globals.materials[material]["Thickness"]) > 0):

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
                    rectangle_height = int(globals.materials[material]["Thickness"])
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
        self.layer_stack_canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline=settings.layer_stack_canvas_outline_color , tags="canvas_bounding_box_rectangle")

        #Find the total height of all materials combined
        sum_of_all_materials = 0
        for material in globals.materials:
            rectangle_height = int(globals.materials[material]["Thickness"])
            sum_of_all_materials += rectangle_height
        
        #Prepare first rectangle drawing coordinates
        rectangle_x0 = self.visible_canvas_bbox_x0
        rectangle_y0 = self.visible_canvas_bbox_y1
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_text_indent
        rectangle_y1 = None #Calculated later

        #Materials (except "substrate") will be drawn on 9/10 of the canvas
        canvas_height = (self.visible_canvas_bbox_y1 - self.visible_canvas_bbox_y0)
        
        #Draw rectangles on canvas
        for material in dict(reversed(globals.materials.items())):
        
            #Create material rectangle only if "thickness" is > zero
            if(int(globals.materials[material]["Thickness"]) > 0):
                #find how many percent the current rectangle's height is of the total sum of materials
                rectangle_height = int(globals.materials[material]["Thickness"])
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
        self.layer_stack_canvas.create_rectangle(self.visible_canvas_bbox_x0, self.visible_canvas_bbox_y0, self.visible_canvas_bbox_x1, self.visible_canvas_bbox_y1, outline=settings.layer_stack_canvas_outline_color, tags="canvas_bounding_box_rectangle")
        
        #Find the total height of all materials combined and the thickest material
        sum_of_all_materials = 0
        biggest_material = 0
        for material in globals.materials:
            if(material.lower() == "substrate"):
                continue    #Skip substrate

            sum_of_all_materials += int(globals.materials[material]["Thickness"])
            if(biggest_material < int(globals.materials[material]["Thickness"])):
                biggest_material = int(globals.materials[material]["Thickness"])
        
        #Find how many nanometers 1 pixel should represent
        nanometers_per_pixel = sum_of_all_materials/round(self.layer_stack_canvas_height * 0.9)

        #Prepare first rectangle drawing coordinates (from bottom left corner)
        rectangle_x0 = self.visible_canvas_bbox_x0 + settings.layer_stack_canvas_indent_left_side
        rectangle_y0 = round(self.layer_stack_canvas_height*0.9) + settings.layer_stack_canvas_stepped_indent_top
        rectangle_x1 = self.visible_canvas_bbox_x1 - settings.layer_stack_canvas_indent_right_side
        rectangle_y1 = None #calculated later
        previous_rectangle_x1 = self.visible_canvas_bbox_x1

        #If a rectangles x1 coordinate is less than original start drawing point, then it will not be drawn 
        original_rectangle_x0 = rectangle_x0

        #Draw rectangles on canvas
        for material in dict(reversed(globals.materials.items())):

            #Draw "substrate" on the bottom 1/10 of the canvas
            if(material.lower() == "substrate"):
                #Find how many pixels is needed to represent the indent of the current material
                indent_width_pixels = int(globals.materials[material]["Indent [nm]"])/nanometers_per_pixel

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
            if(int(globals.materials[material]["Thickness"]) > 0):# and int(globals.materials[material]["indent"]) >= 0):

                #Find how many pixels is needed to represent the height of the current material
                rectangle_height_pixels = int(globals.materials[material]["Thickness"])/nanometers_per_pixel
                
                #Set the y1 coordinate of the rectangle
                rectangle_y1 = rectangle_y0 - rectangle_height_pixels

                #Find how many pixels is needed to represent the indent of the current material
                indent_width_pixels = int(globals.materials[material]["Indent [nm]"])/nanometers_per_pixel

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
            case "Stacked" | "Realistic" | "Stress":

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
                                tags="Material_label"
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
                                tags="Material_label"
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
                                tags="Material_label"
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
                                tags="Material_label"
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
            case "Stacked" | "Realistic" | "Stress":
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

                        #if the text_bbox overlaps with canvas right side:
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
        previous_material = None
        for material in globals.materials:
            if(globals.materials[material]["Text_bbox_id"] != None):
                #Get the coordinates of the current_material_text_bbox
                current_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                current_material_text_bbox_x0 = current_material_text_bbox[0]
                current_material_text_bbox_y0 = current_material_text_bbox[1]
                current_material_text_bbox_x1 = current_material_text_bbox[2]
                current_material_text_bbox_y1 = current_material_text_bbox[3]

                #if the text_bbox top overlaps with the canvas top
                if(current_material_text_bbox_y0 < self.visible_canvas_bbox_y0):
                    #find the overlap
                    overlap = self.visible_canvas_bbox_y0 - current_material_text_bbox_y0
                    #Move the text, text_bbox and line_id down
                    self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, overlap)
                    self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, overlap)

                    #Get the new text_bbox coordinates
                    current_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_material_text_bbox_x0 = current_material_text_bbox[0]
                    current_material_text_bbox_y0 = current_material_text_bbox[1]
                    current_material_text_bbox_x1 = current_material_text_bbox[2]
                    current_material_text_bbox_y1 = current_material_text_bbox[3]
                    current_material_text_bbox_middle_y = (current_material_text_bbox_y0 + current_material_text_bbox_y1) / 2
                    #Get coordinates of matching rectangle
                    rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                    #Move the pointer line based on stack view
                    match globals.option_menu:
                        case "Stacked" | "Realistic" | "Stress":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_material_text_bbox_x0, current_material_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                        case "Stepped":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_material_text_bbox_x1, current_material_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)

            
                #if there is a previous material
                if(previous_material != None):
                    #if the previous_material has a text_bbox
                    if(globals.materials[previous_material]["Text_bbox_id"] != None):
                        #Get the coordinates of the current_material text_bbox
                        current_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        current_material_text_bbox_x0 = current_material_text_bbox[0]
                        current_material_text_bbox_y0 = current_material_text_bbox[1]
                        current_material_text_bbox_x1 = current_material_text_bbox[2]
                        current_material_text_bbox_y1 = current_material_text_bbox[3]
                        
                        #Get the coordinates of the previous_material text_bbox
                        previous_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Text_bbox_id"])
                        previous_material_text_bbox_x0 = previous_material_text_bbox[0]
                        previous_material_text_bbox_y0 = previous_material_text_bbox[1]
                        previous_material_text_bbox_x1 = previous_material_text_bbox[2]
                        previous_material_text_bbox_y1 = previous_material_text_bbox[3]


                        #if the current_material text_bbox top is overlapping the previous_material text_bbox bottom
                        if(current_material_text_bbox_y0 < previous_material_text_bbox_y1):
                            #find the overlap
                            overlap = previous_material_text_bbox_y1 - current_material_text_bbox_y0 
                            #move the current_materials->text, text_bbox and line down
                            self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, overlap)
                            self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, overlap)

                            #Get the new text_bbox coordinates
                            current_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                            current_material_text_bbox_x0 = current_material_text_bbox[0]
                            current_material_text_bbox_y0 = current_material_text_bbox[1]
                            current_material_text_bbox_x1 = current_material_text_bbox[2]
                            current_material_text_bbox_y1 = current_material_text_bbox[3]
                            current_material_text_bbox_middle_y = (current_material_text_bbox_y0 + current_material_text_bbox_y1) / 2
                            #Get coordinates of matching rectangle
                            rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                            
                            #Move the pointer line based on stack view
                            match globals.option_menu:
                                case "Stacked" | "Realistic" | "Stress":
                                    self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_material_text_bbox_x0, current_material_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                                case "Stepped":
                                    self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_material_text_bbox_x1, current_material_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)

            
            #Set the previous_material to the current one
            previous_material = material


        #Loop through every material from LOWEST layer to TOP layer
        previous_material = None
        for material in dict(reversed(globals.materials.items())):
            if(globals.materials[material]["Text_bbox_id"] != None):
                #Get the coordinates of the current_material_text_bbox
                current_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                current_material_text_bbox_x0 = current_material_text_bbox[0]
                current_material_text_bbox_y0 = current_material_text_bbox[1]
                current_material_text_bbox_x1 = current_material_text_bbox[2]
                current_material_text_bbox_y1 = current_material_text_bbox[3]

                #if the text_bbox bottom overlaps with the canvas bottom
                if(current_material_text_bbox_y1 > self.visible_canvas_bbox_y1):
                    #find the overlap
                    overlap = current_material_text_bbox_y1 - self.visible_canvas_bbox_y1 
                    #Move the text, text_bbox and line_id down
                    self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, -overlap)
                    self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, -overlap)

                    #Get the new text_bbox coordinates
                    current_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                    current_material_text_bbox_x0 = current_material_text_bbox[0]
                    current_material_text_bbox_y0 = current_material_text_bbox[1]
                    current_material_text_bbox_x1 = current_material_text_bbox[2]
                    current_material_text_bbox_y1 = current_material_text_bbox[3]
                    current_material_text_bbox_middle_y = (current_material_text_bbox_y0 + current_material_text_bbox_y1) / 2
                    #Get coordinates of matching rectangle
                    rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                    #Move the pointer line based on stack view
                    match globals.option_menu:
                        case "Stacked" | "Realistic" | "Stress":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_material_text_bbox_x0, current_material_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                        case "Stepped":
                            self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_material_text_bbox_x1, current_material_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)

                #########GOOD SO FAR###################
            
                #if there is a previous material
                if(previous_material != None):
                    #if the previous_material has a text_bbox
                    if(globals.materials[previous_material]["Text_bbox_id"] != None):
                        #Get the coordinates of the current_material text_bbox
                        current_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                        current_material_text_bbox_x0 = current_material_text_bbox[0]
                        current_material_text_bbox_y0 = current_material_text_bbox[1]
                        current_material_text_bbox_x1 = current_material_text_bbox[2]
                        current_material_text_bbox_y1 = current_material_text_bbox[3]
                        
                        #Get the coordinates of the previous_material text_bbox
                        previous_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Text_bbox_id"])
                        previous_material_text_bbox_x0 = previous_material_text_bbox[0]
                        previous_material_text_bbox_y0 = previous_material_text_bbox[1]
                        previous_material_text_bbox_x1 = previous_material_text_bbox[2]
                        previous_material_text_bbox_y1 = previous_material_text_bbox[3]


                        #if the current_material text_bbox bottom is overlapping the previous_material text_bbox top
                        if(current_material_text_bbox_y1 > previous_material_text_bbox_y0):
                            #find the overlap
                            overlap = current_material_text_bbox_y1 - previous_material_text_bbox_y0  
                            #move the current_materials->text, text_bbox and line down
                            self.layer_stack_canvas.move(globals.materials[material]["Text_id"], 0, -overlap)
                            self.layer_stack_canvas.move(globals.materials[material]["Text_bbox_id"], 0, -overlap)

                            #Get the new text_bbox coordinates
                            current_material_text_bbox = self.layer_stack_canvas.bbox(globals.materials[material]["Text_bbox_id"])
                            current_material_text_bbox_x0 = current_material_text_bbox[0]
                            current_material_text_bbox_y0 = current_material_text_bbox[1]
                            current_material_text_bbox_x1 = current_material_text_bbox[2]
                            current_material_text_bbox_y1 = current_material_text_bbox[3]
                            current_material_text_bbox_middle_y = (current_material_text_bbox_y0 + current_material_text_bbox_y1) / 2
                            #Get coordinates of matching rectangle
                            rectangle_middle_y = (self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1] + self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]) / 2
                            
                            #Move the pointer line based on stack view
                            match globals.option_menu:
                                case "Stacked" | "Realistic" | "Stress":
                                    self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_material_text_bbox_x0, current_material_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2], rectangle_middle_y)
                                case "Stepped":
                                    self.layer_stack_canvas.coords(globals.materials[material]["Line_id"], current_material_text_bbox_x1, current_material_text_bbox_middle_y, self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0], rectangle_middle_y)

            
            #Set the previous_material to the current one
            previous_material = material



            #if materials->text_box_bottom is overlapping the BOTTOM of the canvas AND OR overlapping the previous materials->text_box_top
                #Calculate the overlapp and move it upwards


            #if the text 
            #Make one loop that goes through every text box for every material and checks if the top of the text box overlaps with the canvas top or the bottom of the previous material text box 

        

       
        #Write different texts based on current stack option
        # match globals.option_menu:
        #     case "Stacked" | "Realistic" | "Stress":
        #         #Find out the height of a potential text's bounding box
        #         text_font = font.Font(family=settings.text_font, size=settings.text_size)
        #         text_height = text_font.metrics()['linespace']
        #         previous_material = None

        #         #Loop through all the materials:
        #         # for material in dict(reversed(globals.materials.items())):
        #         for material in globals.materials:
        #             #If material has a rectangle that text can be written on
        #             if(globals.materials[material]["Rectangle_id"] != None):
        #                 #Find coordinates and height of current material_rectangle
        #                 current_rectangle_x0, current_rectangle_y0, current_rectangle_x1, current_rectangle_y1 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])
        #                 current_rectangle_height = current_rectangle_y1-current_rectangle_y0
        #                 current_rectangle_middle_x = (current_rectangle_x0 + current_rectangle_x1)/2
        #                 current_rectangle_middle_y = (current_rectangle_y0 + current_rectangle_y1)/2

        #                 #Text is drawn inside rectangle
        #                 if(text_height < current_rectangle_height):
        #                     created_text = self.layer_stack_canvas.create_text(
        #                         current_rectangle_middle_x, current_rectangle_middle_y, 
        #                         # text=f"{material} - {globals.materials[material]['thickness']}nm",
        #                         text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 
        #                         fill=settings.text_color, 
        #                         font=(settings.text_font, settings.text_size), 
        #                         anchor="center", 
        #                         tags="Material_label"
        #                     )

        #                     #If text is outside leftside of canvas, place it on the left canvas side
        #                     if(self.layer_stack_canvas.bbox(created_text)[0] < self.visible_canvas_bbox_x0):
        #                         overlap = self.visible_canvas_bbox_x0 - self.layer_stack_canvas.bbox(created_text)[0] 
        #                         self.layer_stack_canvas.coords(created_text, current_rectangle_middle_x+overlap, current_rectangle_middle_y)
                            
        #                     #If text is outside rightside of canvas, place it on the right canvas side
        #                     if(self.layer_stack_canvas.bbox(created_text)[2] > self.visible_canvas_bbox_x1):
        #                         overlap = self.layer_stack_canvas.bbox(created_text)[2] - self.visible_canvas_bbox_x1 
        #                         self.layer_stack_canvas.coords(created_text, current_rectangle_middle_x-overlap, current_rectangle_middle_y)
                            
        #                     #Add text element to dictionary
        #                     globals.materials[material]["Text_id"] = created_text

        #                 #Text is drawn outside rectangle
        #                 else:
        #                     #Create text, bbox and line and place them
        #                     created_text = self.layer_stack_canvas.create_text(
        #                         self.visible_canvas_bbox_x1, current_rectangle_middle_y, 
        #                         # text=f"{material} - {globals.materials[material]['thickness']}nm", 
        #                         text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 
        #                         fill=settings.text_color, 
        #                         font=(settings.text_font, settings.text_size), 
        #                         tags="Material_label"
        #                     )
        #                     created_text_bbox = self.layer_stack_canvas.create_rectangle(
        #                         self.layer_stack_canvas.bbox(created_text), 
        #                         outline=settings.text_color, 
        #                         tags="text_bbox"
        #                     )
        #                     #Get coordinates of text bounding box
        #                     current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1  = self.layer_stack_canvas.bbox(created_text)
        #                     current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2

        #                     created_arrow_line = self.layer_stack_canvas.create_line(
        #                         (current_text_bbox_x0, current_text_bbox_middle_y), (current_rectangle_x1, current_rectangle_middle_y), 
        #                         arrow=tkinter.LAST, 
        #                         fill=settings.text_color,
        #                         tags="arrow_line"
        #                     )

        #                     #Check for adjustments of text
        #                     #if(text top overlaps with canvas top):
        #                     if(current_text_bbox_y0 < self.visible_canvas_bbox_y0):
        #                         #Find how much is overlapping
        #                         overlap = self.visible_canvas_bbox_y0 - current_text_bbox_y0
        #                         #Move text and bbox down
        #                         self.layer_stack_canvas.move(created_text, 0, overlap)
        #                         self.layer_stack_canvas.move(created_text_bbox, 0, overlap)
        #                         #Find new coordinates of text bounding box
        #                         current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
        #                         current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
        #                         #Move the arrow line
        #                         self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)
                            
        #                     #if(Text bottom overlaps with canvas bottom):
        #                     if(current_text_bbox_y1 > self.visible_canvas_bbox_y1):
        #                         #Find how much is overlapping
        #                         overlap = current_text_bbox_y1 - self.visible_canvas_bbox_y1
        #                         #Move text and bounding box up
        #                         self.layer_stack_canvas.move(created_text, 0, -overlap)
        #                         self.layer_stack_canvas.move(created_text_bbox, 0, -overlap)
                                
        #                         #Find coordinates of new text bounding box
        #                         current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
        #                         current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
        #                         #Move the arrow line
        #                         self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)
                            
        #                     #if(text right side overlaps with canvas right side)
        #                     if(current_text_bbox_x1 > self.visible_canvas_bbox_x1):
        #                         #Find how much is overlapping
        #                         overlap = current_text_bbox_x1 - self.visible_canvas_bbox_x1
        #                         #Move text left
        #                         self.layer_stack_canvas.move(created_text, -overlap, 0)
        #                         self.layer_stack_canvas.move(created_text_bbox, -overlap, 0)
                                
        #                         #Find new coordinates of text bounding box
        #                         current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
        #                         current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
        #                         #Move the arrow line
        #                         self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)

        #                     #if(Text top overlaps with previous text bottom):
        #                     if(previous_material != None):
        #                         #If text, bounding box and lines has been created for this element
        #                         if(globals.materials[previous_material]["Text_id"] != None and globals.materials[previous_material]["Text_bbox_id"] != None and globals.materials[previous_material]["Line_id"] != None):
        #                             #Find necessary coordinated for previous material
        #                             previous_text_bbox_y1 = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Text_id"])[3]
        #                             #if(Text top overlaps with previous text bottom):
        #                             if(current_text_bbox_y0 < previous_text_bbox_y1):
        #                                 #Find how much is overlapping
        #                                 overlap = previous_text_bbox_y1 - current_text_bbox_y0
        #                                 #Move text down
        #                                 self.layer_stack_canvas.move(created_text, 0, overlap)
        #                                 self.layer_stack_canvas.move(created_text_bbox, 0, overlap)
        #                                 #Find new coordinates of text bounding box
        #                                 current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
        #                                 current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
        #                                 #Move the arrow line
        #                                 self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)

        #                     #Add created elements to dictionary
        #                     globals.materials[material]["Text_id"] = created_text
        #                     globals.materials[material]["Text_bbox_id"] = created_text_bbox
        #                     globals.materials[material]["Line_id"] = created_arrow_line
                            
        #                 #Set previous material to the current one
        #                 previous_material = material

        #     case "Stepped":
        #         #Find out the height of a potential text's bounding box
        #         text_font = font.Font(family=settings.text_font, size=settings.text_size)
        #         text_height = text_font.metrics()['linespace']
        #         previous_material = None

        #         #Loop through all the materials:
        #         # for material in dict(reversed(globals.materials.items())):
        #         for material in globals.materials:
        #             #If material has a rectangle that text can be written on
        #             if(globals.materials[material]["Rectangle_id"] != None):
        #                 #Find coordinates and height of current material_rectangle
        #                 current_rectangle_x0, current_rectangle_y0, current_rectangle_x1, current_rectangle_y1 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])
        #                 current_rectangle_height = current_rectangle_y1-current_rectangle_y0
        #                 current_rectangle_middle_x = (current_rectangle_x0 + current_rectangle_x1)/2
        #                 current_rectangle_middle_y = (current_rectangle_y0 + current_rectangle_y1)/2

        #                 #Text is drawn inside rectangle
        #                 if(text_height < current_rectangle_height):
        #                     created_text = self.layer_stack_canvas.create_text(
        #                         current_rectangle_middle_x, current_rectangle_middle_y, 
        #                         # text=f"{material} - {globals.materials[material]['thickness']}nm", 
        #                         text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 

        #                         fill=settings.text_color, 
        #                         font=(settings.text_font, settings.text_size), 
        #                         # anchor="center", 
        #                         tags="Material_label"
        #                     )

        #                     #If text is outside leftside of canvas, place it on the left canvas side
        #                     if(self.layer_stack_canvas.bbox(created_text)[0] < self.visible_canvas_bbox_x0):
        #                         overlap = self.visible_canvas_bbox_x0 - self.layer_stack_canvas.bbox(created_text)[0] 
        #                         self.layer_stack_canvas.coords(created_text, current_rectangle_middle_x+overlap, current_rectangle_middle_y)
                            
        #                     #If text is outside rightside of canvas, place it on the right canvas side
        #                     if(self.layer_stack_canvas.bbox(created_text)[2] > self.visible_canvas_bbox_x1):
        #                         overlap = self.layer_stack_canvas.bbox(created_text)[2] - self.visible_canvas_bbox_x1 
        #                         self.layer_stack_canvas.coords(created_text, current_rectangle_middle_x-overlap, current_rectangle_middle_y)
                            
        #                     #Add text element to dictionary
        #                     globals.materials[material]["Text_id"] = created_text

        #                 #Text is drawn outside rectangle
        #                 else:
        #                     #Create text, bbox and line and place them
        #                     created_text = self.layer_stack_canvas.create_text(
        #                         self.visible_canvas_bbox_x0, current_rectangle_middle_y, 
        #                         # text=f"{material} - {globals.materials[material]['thickness']}nm", 
        #                         text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 

        #                         fill=settings.text_color, 
        #                         font=(settings.text_font, settings.text_size), 
        #                         tags="Material_label"
        #                     )
        #                     created_text_bbox = self.layer_stack_canvas.create_rectangle(
        #                         self.layer_stack_canvas.bbox(created_text), 
        #                         outline=settings.text_color, 
        #                         tags="text_bbox"
        #                     )
        #                     #Get coordinates of text bounding box
        #                     current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1  = self.layer_stack_canvas.bbox(created_text)
        #                     current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2

        #                     created_arrow_line = self.layer_stack_canvas.create_line(
        #                         (current_text_bbox_x1, current_text_bbox_middle_y), (current_rectangle_x0, current_rectangle_middle_y), 
        #                         arrow=tkinter.LAST, 
        #                         fill=settings.text_color,
        #                         tags="arrow_line"
        #                     )

        #                     #Check for adjustments of text
        #                     #if(text top overlaps with canvas top):
        #                     if(current_text_bbox_y0 < self.visible_canvas_bbox_y0):
        #                         #Find how much is overlapping
        #                         overlap = self.visible_canvas_bbox_y0 - current_text_bbox_y0
        #                         #Move text and bbox down
        #                         self.layer_stack_canvas.move(created_text, 0, overlap)
        #                         self.layer_stack_canvas.move(created_text_bbox, 0, overlap)
        #                         #Find new coordinates of text bounding box
        #                         current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
        #                         current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
        #                         #Move the arrow line
        #                         self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)
                            
        #                     #if(Text bottom overlaps with canvas bottom):
        #                     if(current_text_bbox_y1 > self.visible_canvas_bbox_y1):
        #                         #Find how much is overlapping
        #                         overlap = current_text_bbox_y1 - self.visible_canvas_bbox_y1
        #                         #Move text and bounding box up
        #                         self.layer_stack_canvas.move(created_text, 0, -overlap)
        #                         self.layer_stack_canvas.move(created_text_bbox, 0, -overlap)
                                
        #                         #Find coordinates of new text bounding box
        #                         current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
        #                         current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
        #                         #Move the arrow line
        #                         self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)
                            
        #                     #if(text left side overlaps with canvas left side)
        #                     if(current_text_bbox_x0 < self.visible_canvas_bbox_x0):
        #                         #Find how much is overlapping
        #                         overlap = self.visible_canvas_bbox_x0 - current_text_bbox_x0
        #                         #Move text to right
        #                         self.layer_stack_canvas.move(created_text, overlap, 0)
        #                         self.layer_stack_canvas.move(created_text_bbox, overlap, 0)
                                
        #                         #Find new coordinates of text bounding box
        #                         current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
        #                         current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
        #                         #Move the arrow line
        #                         self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)

        #                     #if(Text top overlaps with previous text bottom):
        #                     if(previous_material != None):
        #                         #If text, bounding box and lines has been created for this element
        #                         if(globals.materials[previous_material]["Text_id"] != None and globals.materials[previous_material]["Text_bbox_id"] != None and globals.materials[previous_material]["Line_id"] != None):
        #                             #Find necessary coordinated for previous material
        #                             previous_text_bbox_y1 = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Text_id"])[3]
        #                             #if(Text top overlaps with previous text bottom):
        #                             if(current_text_bbox_y0 < previous_text_bbox_y1):
        #                                 #Find how much is overlapping
        #                                 overlap = previous_text_bbox_y1 - current_text_bbox_y0
        #                                 #Move text down
        #                                 self.layer_stack_canvas.move(created_text, 0, overlap)
        #                                 self.layer_stack_canvas.move(created_text_bbox, 0, overlap)
        #                                 #Find new coordinates of text bounding box
        #                                 current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
        #                                 current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
        #                                 #Move the arrow line
        #                                 self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)

        #                     #Add created elements to dictionary
        #                     globals.materials[material]["Text_id"] = created_text
        #                     globals.materials[material]["Text_bbox_id"] = created_text_bbox
        #                     globals.materials[material]["Line_id"] = created_arrow_line
                            
        #                 #Set previous material to the current one
        #                 previous_material = material

        
    """Writes the indent ranges on the stepped material stack"""
    def write_indent_on_stepped_stack(self):
        # print("WRITE_INDENT_ON_STEPPED_STACK()")

        #Delete all indet texts and arrows from canvas and dictionary
        for material in globals.materials:
            self.layer_stack_canvas.delete(globals.materials[material]["Indent_text_id"])
            self.layer_stack_canvas.delete(globals.materials[material]["Indent_text_bbox_id"])
            self.layer_stack_canvas.delete(globals.materials[material]["Indent_line_id"])
            self.layer_stack_canvas.delete(globals.materials[material]["Indent_arrow_pointer_id"])

            globals.materials[material]["Indent_text_id"] = None
            globals.materials[material]["Indent_text_bbox_id"] = None
            globals.materials[material]["Indent_line_id"] = None
            globals.materials[material]["Indent_arrow_pointer_id"] = None 
       
        #Save necessary information about current material and previous_material
        current_material_rect_coordinates = None              #[left,top, right,bottom]
        current_material_indent_textbox_coordinates = None
        current_material_arrow_line_coordinates = None

        #Save necessary information about previous material
        previous_material = None
        previous_material_rect_coordinates = None              #[left,top, right,bottom]
        previous_material_indent_textbox_coordinates = None
        previous_material_indent_line_coordinates = None
        

        #Go through every material
        for material in dict(reversed(globals.materials.items())):

            
            #There is a rectangle that text can be written on
            if(globals.materials[material]["Rectangle_id"] != None):

                #Skip first material (no indent or line should be drawn)
                if(previous_material != None):
                    #Only draw indent_text and lines if "indent" is > 0
                    if(int(globals.materials[material]["Indent [nm]"]) > 0):
                        #Find information about current material_rectangle
                        current_material_rect_coordinates = [
                            self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[0],
                            self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[1],
                            self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[2],
                            self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])[3]
                        ]

                        #Find information about previous_material
                        previous_material_rect_coordinates = [
                            self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])[0],
                            self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])[1],
                            self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])[2],
                            self.layer_stack_canvas.bbox(globals.materials[previous_material]["Rectangle_id"])[3]
                        ]

                        #Create a two sided arrow line between the differense of the two rectangles
                        indent_line = self.layer_stack_canvas.create_line(
                            current_material_rect_coordinates[2], current_material_rect_coordinates[3]-5, previous_material_rect_coordinates[2], previous_material_rect_coordinates[1]-3,                       
                            fill=settings.text_color,
                            arrow=tkinter.BOTH
                        )

                        #Save information about indent_line
                        current_material_indent_line_coordinates = [
                            self.layer_stack_canvas.bbox(indent_line)[0],
                            self.layer_stack_canvas.bbox(indent_line)[1],
                            self.layer_stack_canvas.bbox(indent_line)[2],
                            self.layer_stack_canvas.bbox(indent_line)[3]
                        ]


                        #Write indent number on the side of indent_line
                        indent_text = self.layer_stack_canvas.create_text(
                            self.visible_canvas_bbox_x1 - 50,
                            self.layer_stack_canvas.bbox(indent_line)[3] - 10,
                            text=f"{int(globals.materials[material]['Indent [nm]'])} {globals.materials[material]['Unit']}",
                            fill=settings.text_color, 
                            font=(settings.text_font, settings.text_size)
                        )

                        #Save information about indent_text bounding box
                        current_material_indent_textbox_coordinates = [
                            self.layer_stack_canvas.bbox(indent_text)[0],
                            self.layer_stack_canvas.bbox(indent_text)[1],
                            self.layer_stack_canvas.bbox(indent_text)[2],
                            self.layer_stack_canvas.bbox(indent_text)[3],
                        ]


                        #Check if indent_number bottom overlaps with previous indent_number top
                        if(previous_material_indent_textbox_coordinates != None):
                            #Move indent text and text bounding box up
                            if(current_material_indent_textbox_coordinates[3] > previous_material_indent_textbox_coordinates[1]):
                                overlap = previous_material_indent_textbox_coordinates[1] - current_material_indent_textbox_coordinates[3]
                                self.layer_stack_canvas.move(indent_text, 0, overlap)
                                self.layer_stack_canvas.move(self.layer_stack_canvas.bbox(indent_text), 0, overlap)

                                #update current material text coordinates
                                #Save information about indent_text bounding box
                                current_material_indent_textbox_coordinates = [
                                    self.layer_stack_canvas.bbox(indent_text)[0],
                                    self.layer_stack_canvas.bbox(indent_text)[1],
                                    self.layer_stack_canvas.bbox(indent_text)[2],
                                    self.layer_stack_canvas.bbox(indent_text)[3],
                                ]

                        #Draw bounding box around indent text
                        indent_text_bbox = self.layer_stack_canvas.create_rectangle(
                            self.layer_stack_canvas.bbox(indent_text), 
                            outline=settings.text_color, 
                            tags="indent_bbox"
                        )

                        #Draw an arrow from indent_text_bbox to indent_line 
                        indent_arrow_pointer = self.layer_stack_canvas.create_line(
                            current_material_indent_textbox_coordinates[0],
                            self.layer_stack_canvas.bbox(indent_text_bbox)[3] - ((self.layer_stack_canvas.bbox(indent_text_bbox)[3] - self.layer_stack_canvas.bbox(indent_text_bbox)[1]) / 2),
                            current_material_indent_line_coordinates[2],
                            current_material_indent_line_coordinates[3] - 5,
                            arrow=tkinter.LAST, 
                            fill=settings.text_color,
                            tags="indent_pointer_arrow"
                        )
                        
                        #Add created elements to dictionary
                        globals.materials[material]["Indent_line_id"] = indent_line
                        globals.materials[material]["Indent_text_id"] = indent_text
                        globals.materials[material]["Indent_text_bbox_id"] = indent_text_bbox
                        globals.materials[material]["Indent_arrow_pointer_id"] = indent_arrow_pointer 
                        

                        #Save necessary information about previous_material for next loop iteration
                        previous_material_rect_coordinates = current_material_rect_coordinates
                        previous_material_indent_textbox_coordinates = current_material_indent_textbox_coordinates
                        previous_material_indent_line_coordinates = current_material_indent_line_coordinates
        
                previous_material = material























    #  """Writes text on rectangles in the material stack"""
    # def write_text_on_stack(self):                                            #ORIGINAL (293 lines)
    #     # print("WRITE_TEXT_ON_STACK()")

    #     #Delete all texts from canvas and dictionary
    #     for material in globals.materials:
    #         self.layer_stack_canvas.delete(globals.materials[material]["Text_id"])
    #         self.layer_stack_canvas.delete(globals.materials[material]["Text_bbox_id"])
    #         self.layer_stack_canvas.delete(globals.materials[material]["Line_id"])

    #         globals.materials[material]["Text_id"] = None
    #         globals.materials[material]["Text_bbox_id"] = None
    #         globals.materials[material]["Line_id"] = None

       
    #     #Write different texts based on current stack option
    #     match globals.option_menu:
    #         case "Stacked" | "Realistic" | "Stress":
    #             #Find out the height of a potential text's bounding box
    #             text_font = font.Font(family=settings.text_font, size=settings.text_size)
    #             text_height = text_font.metrics()['linespace']
    #             previous_material = None

    #             #Loop through all the materials:
    #             # for material in dict(reversed(globals.materials.items())):
    #             for material in globals.materials:
    #                 #If material has a rectangle that text can be written on
    #                 if(globals.materials[material]["Rectangle_id"] != None):
    #                     #Find coordinates and height of current material_rectangle
    #                     current_rectangle_x0, current_rectangle_y0, current_rectangle_x1, current_rectangle_y1 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])
    #                     current_rectangle_height = current_rectangle_y1-current_rectangle_y0
    #                     current_rectangle_middle_x = (current_rectangle_x0 + current_rectangle_x1)/2
    #                     current_rectangle_middle_y = (current_rectangle_y0 + current_rectangle_y1)/2

    #                     #Text is drawn inside rectangle
    #                     if(text_height < current_rectangle_height):
    #                         created_text = self.layer_stack_canvas.create_text(
    #                             current_rectangle_middle_x, current_rectangle_middle_y, 
    #                             # text=f"{material} - {globals.materials[material]['thickness']}nm",
    #                             text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 
    #                             fill=settings.text_color, 
    #                             font=(settings.text_font, settings.text_size), 
    #                             anchor="center", 
    #                             tags="Material_label"
    #                         )

    #                         #If text is outside leftside of canvas, place it on the left canvas side
    #                         if(self.layer_stack_canvas.bbox(created_text)[0] < self.visible_canvas_bbox_x0):
    #                             overlap = self.visible_canvas_bbox_x0 - self.layer_stack_canvas.bbox(created_text)[0] 
    #                             self.layer_stack_canvas.coords(created_text, current_rectangle_middle_x+overlap, current_rectangle_middle_y)
                            
    #                         #If text is outside rightside of canvas, place it on the right canvas side
    #                         if(self.layer_stack_canvas.bbox(created_text)[2] > self.visible_canvas_bbox_x1):
    #                             overlap = self.layer_stack_canvas.bbox(created_text)[2] - self.visible_canvas_bbox_x1 
    #                             self.layer_stack_canvas.coords(created_text, current_rectangle_middle_x-overlap, current_rectangle_middle_y)
                            
    #                         #Add text element to dictionary
    #                         globals.materials[material]["Text_id"] = created_text

    #                     #Text is drawn outside rectangle
    #                     else:
    #                         #Create text, bbox and line and place them
    #                         created_text = self.layer_stack_canvas.create_text(
    #                             self.visible_canvas_bbox_x1, current_rectangle_middle_y, 
    #                             # text=f"{material} - {globals.materials[material]['thickness']}nm", 
    #                             text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 
    #                             fill=settings.text_color, 
    #                             font=(settings.text_font, settings.text_size), 
    #                             tags="Material_label"
    #                         )
    #                         created_text_bbox = self.layer_stack_canvas.create_rectangle(
    #                             self.layer_stack_canvas.bbox(created_text), 
    #                             outline=settings.text_color, 
    #                             tags="text_bbox"
    #                         )
    #                         #Get coordinates of text bounding box
    #                         current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1  = self.layer_stack_canvas.bbox(created_text)
    #                         current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2

    #                         created_arrow_line = self.layer_stack_canvas.create_line(
    #                             (current_text_bbox_x0, current_text_bbox_middle_y), (current_rectangle_x1, current_rectangle_middle_y), 
    #                             arrow=tkinter.LAST, 
    #                             fill=settings.text_color,
    #                             tags="arrow_line"
    #                         )

    #                         #Check for adjustments of text
    #                         #if(text top overlaps with canvas top):
    #                         if(current_text_bbox_y0 < self.visible_canvas_bbox_y0):
    #                             #Find how much is overlapping
    #                             overlap = self.visible_canvas_bbox_y0 - current_text_bbox_y0
    #                             #Move text and bbox down
    #                             self.layer_stack_canvas.move(created_text, 0, overlap)
    #                             self.layer_stack_canvas.move(created_text_bbox, 0, overlap)
    #                             #Find new coordinates of text bounding box
    #                             current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
    #                             current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
    #                             #Move the arrow line
    #                             self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)
                            
    #                         #if(Text bottom overlaps with canvas bottom):
    #                         if(current_text_bbox_y1 > self.visible_canvas_bbox_y1):
    #                             #Find how much is overlapping
    #                             overlap = current_text_bbox_y1 - self.visible_canvas_bbox_y1
    #                             #Move text and bounding box up
    #                             self.layer_stack_canvas.move(created_text, 0, -overlap)
    #                             self.layer_stack_canvas.move(created_text_bbox, 0, -overlap)
                                
    #                             #Find coordinates of new text bounding box
    #                             current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
    #                             current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
    #                             #Move the arrow line
    #                             self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)
                            
    #                         #if(text right side overlaps with canvas right side)
    #                         if(current_text_bbox_x1 > self.visible_canvas_bbox_x1):
    #                             #Find how much is overlapping
    #                             overlap = current_text_bbox_x1 - self.visible_canvas_bbox_x1
    #                             #Move text left
    #                             self.layer_stack_canvas.move(created_text, -overlap, 0)
    #                             self.layer_stack_canvas.move(created_text_bbox, -overlap, 0)
                                
    #                             #Find new coordinates of text bounding box
    #                             current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
    #                             current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
    #                             #Move the arrow line
    #                             self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)

    #                         #if(Text top overlaps with previous text bottom):
    #                         if(previous_material != None):
    #                             #If text, bounding box and lines has been created for this element
    #                             if(globals.materials[previous_material]["Text_id"] != None and globals.materials[previous_material]["Text_bbox_id"] != None and globals.materials[previous_material]["Line_id"] != None):
    #                                 #Find necessary coordinated for previous material
    #                                 previous_text_bbox_y1 = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Text_id"])[3]
    #                                 #if(Text top overlaps with previous text bottom):
    #                                 if(current_text_bbox_y0 < previous_text_bbox_y1):
    #                                     #Find how much is overlapping
    #                                     overlap = previous_text_bbox_y1 - current_text_bbox_y0
    #                                     #Move text down
    #                                     self.layer_stack_canvas.move(created_text, 0, overlap)
    #                                     self.layer_stack_canvas.move(created_text_bbox, 0, overlap)
    #                                     #Find new coordinates of text bounding box
    #                                     current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
    #                                     current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
    #                                     #Move the arrow line
    #                                     self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x0, current_text_bbox_middle_y, current_rectangle_x1, current_rectangle_middle_y)

    #                         #Add created elements to dictionary
    #                         globals.materials[material]["Text_id"] = created_text
    #                         globals.materials[material]["Text_bbox_id"] = created_text_bbox
    #                         globals.materials[material]["Line_id"] = created_arrow_line
                            
    #                     #Set previous material to the current one
    #                     previous_material = material

    #         case "Stepped":
    #             #Find out the height of a potential text's bounding box
    #             text_font = font.Font(family=settings.text_font, size=settings.text_size)
    #             text_height = text_font.metrics()['linespace']
    #             previous_material = None

    #             #Loop through all the materials:
    #             # for material in dict(reversed(globals.materials.items())):
    #             for material in globals.materials:
    #                 #If material has a rectangle that text can be written on
    #                 if(globals.materials[material]["Rectangle_id"] != None):
    #                     #Find coordinates and height of current material_rectangle
    #                     current_rectangle_x0, current_rectangle_y0, current_rectangle_x1, current_rectangle_y1 = self.layer_stack_canvas.bbox(globals.materials[material]["Rectangle_id"])
    #                     current_rectangle_height = current_rectangle_y1-current_rectangle_y0
    #                     current_rectangle_middle_x = (current_rectangle_x0 + current_rectangle_x1)/2
    #                     current_rectangle_middle_y = (current_rectangle_y0 + current_rectangle_y1)/2

    #                     #Text is drawn inside rectangle
    #                     if(text_height < current_rectangle_height):
    #                         created_text = self.layer_stack_canvas.create_text(
    #                             current_rectangle_middle_x, current_rectangle_middle_y, 
    #                             # text=f"{material} - {globals.materials[material]['thickness']}nm", 
    #                             text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 

    #                             fill=settings.text_color, 
    #                             font=(settings.text_font, settings.text_size), 
    #                             # anchor="center", 
    #                             tags="Material_label"
    #                         )

    #                         #If text is outside leftside of canvas, place it on the left canvas side
    #                         if(self.layer_stack_canvas.bbox(created_text)[0] < self.visible_canvas_bbox_x0):
    #                             overlap = self.visible_canvas_bbox_x0 - self.layer_stack_canvas.bbox(created_text)[0] 
    #                             self.layer_stack_canvas.coords(created_text, current_rectangle_middle_x+overlap, current_rectangle_middle_y)
                            
    #                         #If text is outside rightside of canvas, place it on the right canvas side
    #                         if(self.layer_stack_canvas.bbox(created_text)[2] > self.visible_canvas_bbox_x1):
    #                             overlap = self.layer_stack_canvas.bbox(created_text)[2] - self.visible_canvas_bbox_x1 
    #                             self.layer_stack_canvas.coords(created_text, current_rectangle_middle_x-overlap, current_rectangle_middle_y)
                            
    #                         #Add text element to dictionary
    #                         globals.materials[material]["Text_id"] = created_text

    #                     #Text is drawn outside rectangle
    #                     else:
    #                         #Create text, bbox and line and place them
    #                         created_text = self.layer_stack_canvas.create_text(
    #                             self.visible_canvas_bbox_x0, current_rectangle_middle_y, 
    #                             # text=f"{material} - {globals.materials[material]['thickness']}nm", 
    #                             text=f"{material} - {globals.materials[material]['Thickness']} {globals.materials[material]['Unit']}", 

    #                             fill=settings.text_color, 
    #                             font=(settings.text_font, settings.text_size), 
    #                             tags="Material_label"
    #                         )
    #                         created_text_bbox = self.layer_stack_canvas.create_rectangle(
    #                             self.layer_stack_canvas.bbox(created_text), 
    #                             outline=settings.text_color, 
    #                             tags="text_bbox"
    #                         )
    #                         #Get coordinates of text bounding box
    #                         current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1  = self.layer_stack_canvas.bbox(created_text)
    #                         current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2

    #                         created_arrow_line = self.layer_stack_canvas.create_line(
    #                             (current_text_bbox_x1, current_text_bbox_middle_y), (current_rectangle_x0, current_rectangle_middle_y), 
    #                             arrow=tkinter.LAST, 
    #                             fill=settings.text_color,
    #                             tags="arrow_line"
    #                         )

    #                         #Check for adjustments of text
    #                         #if(text top overlaps with canvas top):
    #                         if(current_text_bbox_y0 < self.visible_canvas_bbox_y0):
    #                             #Find how much is overlapping
    #                             overlap = self.visible_canvas_bbox_y0 - current_text_bbox_y0
    #                             #Move text and bbox down
    #                             self.layer_stack_canvas.move(created_text, 0, overlap)
    #                             self.layer_stack_canvas.move(created_text_bbox, 0, overlap)
    #                             #Find new coordinates of text bounding box
    #                             current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
    #                             current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
    #                             #Move the arrow line
    #                             self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)
                            
    #                         #if(Text bottom overlaps with canvas bottom):
    #                         if(current_text_bbox_y1 > self.visible_canvas_bbox_y1):
    #                             #Find how much is overlapping
    #                             overlap = current_text_bbox_y1 - self.visible_canvas_bbox_y1
    #                             #Move text and bounding box up
    #                             self.layer_stack_canvas.move(created_text, 0, -overlap)
    #                             self.layer_stack_canvas.move(created_text_bbox, 0, -overlap)
                                
    #                             #Find coordinates of new text bounding box
    #                             current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
    #                             current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
    #                             #Move the arrow line
    #                             self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)
                            
    #                         #if(text left side overlaps with canvas left side)
    #                         if(current_text_bbox_x0 < self.visible_canvas_bbox_x0):
    #                             #Find how much is overlapping
    #                             overlap = self.visible_canvas_bbox_x0 - current_text_bbox_x0
    #                             #Move text to right
    #                             self.layer_stack_canvas.move(created_text, overlap, 0)
    #                             self.layer_stack_canvas.move(created_text_bbox, overlap, 0)
                                
    #                             #Find new coordinates of text bounding box
    #                             current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
    #                             current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
    #                             #Move the arrow line
    #                             self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)

    #                         #if(Text top overlaps with previous text bottom):
    #                         if(previous_material != None):
    #                             #If text, bounding box and lines has been created for this element
    #                             if(globals.materials[previous_material]["Text_id"] != None and globals.materials[previous_material]["Text_bbox_id"] != None and globals.materials[previous_material]["Line_id"] != None):
    #                                 #Find necessary coordinated for previous material
    #                                 previous_text_bbox_y1 = self.layer_stack_canvas.bbox(globals.materials[previous_material]["Text_id"])[3]
    #                                 #if(Text top overlaps with previous text bottom):
    #                                 if(current_text_bbox_y0 < previous_text_bbox_y1):
    #                                     #Find how much is overlapping
    #                                     overlap = previous_text_bbox_y1 - current_text_bbox_y0
    #                                     #Move text down
    #                                     self.layer_stack_canvas.move(created_text, 0, overlap)
    #                                     self.layer_stack_canvas.move(created_text_bbox, 0, overlap)
    #                                     #Find new coordinates of text bounding box
    #                                     current_text_bbox_x0, current_text_bbox_y0, current_text_bbox_x1, current_text_bbox_y1 = self.layer_stack_canvas.bbox(created_text_bbox)
    #                                     current_text_bbox_middle_y = (current_text_bbox_y0 + current_text_bbox_y1) / 2
    #                                     #Move the arrow line
    #                                     self.layer_stack_canvas.coords(created_arrow_line, current_text_bbox_x1, current_text_bbox_middle_y, current_rectangle_x0, current_rectangle_middle_y)

    #                         #Add created elements to dictionary
    #                         globals.materials[material]["Text_id"] = created_text
    #                         globals.materials[material]["Text_bbox_id"] = created_text_bbox
    #                         globals.materials[material]["Line_id"] = created_arrow_line
                            
    #                     #Set previous material to the current one
    #                     previous_material = material

        