"""
@Filename : SVG_Floorplan.py
@Brief : Creates an SVG floorplan object from a given JSON floorplan file
@Author : Soumitra Pandit
"""

import svgwrite
import numpy as np
from Floorplan import Floorplan
import json

class SVG_Floorplan:
    def __init__(self, output_file: str, floorplan_file: str, sortplan_file = None ):
        #Set floorplan vars
        self.floorplan_file = floorplan_file
        self.floorplan_data = json.load(open(self.floorplan_file,'r'))
        self.floorplan = Floorplan(self.floorplan_file)

        #Initiate Drawing Object
        self.svg = svgwrite.Drawing(output_file,size=("100%","100%"))
        self.unit = "cm"
        self.scale = 100

        #Set Robot and bin Dimensions (in Meters):
        self.node_width = 0.8 * self.scale
        self.node_height = 0.6 * self.scale
        self.bin_width = 1 * self.scale
        self.bin_height = 1.2 * self.scale
        self.node_offset = 0.05 * self.scale
        self.bin_offset = 0.05 * self.scale
        self.stroke_width = 0.02 * self.scale
        
        
        self.node_coords = [] #Stores the centers of Nodes
        self.svg_nodes = [] #Stores svg.rect objects

        #Extraction Methods:
        self.__extract_node_coords()
        
        if sortplan_file is not None:
            self.sortplan_file = sortplan_file
            self.sortplan_data = json.load(open(self.sortplan_file,'r'))
            self.bin_coords = [] #Stores the centers of the Bins
            self.bin_types = [] #Stores the type of bin
            self.bin_sides = [] #Stores the sides on which the bin lies.
            self.__extract_bin_info()

        #initializing Methods:
        self.__find_limits()
        self.__scale_svg()

        #Drawing Methods:
        self.__draw_all_elements()
        self.flip_svg_vertically()





    #Print Out Object:
    def __repr__(self):
        return (f"SVG Floorplan:\n"
                f"Floor Plan Name: {self.floorplan_file}\n"
                f"Sort Plan Name: {self.sortplan_file}\n")






    #Scale Window Size:
    def __scale_svg(self):
        clearance_height = self.bin_height+self.node_height
        clearance_width = self.bin_width+self.node_width
        #viewbox(top_x,min_y,x_range,y_range)
        if self.x_min < 0:
            min_x = self.x_min-clearance_width
        else:
            min_x = self.x_min + clearance_width
        
        if self.y_min < 0:
            if self.y_max > 0:
                min_y = -self.y_max - clearance_height
            else: 
                min_y = self.y_min - clearance_height
        else:
            min_y = self.y_max + clearance_height

        self.frame_width = int(np.floor(abs(self.x_max) + abs(self.x_min) + 2 * clearance_width)) 
        self.frame_height = int(np.floor(abs(self.y_max) + abs(self.y_min) + 2 * clearance_height)) 

        self.svg.viewbox(min_x, 
                         min_y, 
                         self.frame_width, 
                         self.frame_height)
        
        #We're using json.dumps for string format with "" instead of ''
        #single_quoted = repr(f"{frame_width}{self.unit}").replace("'",'"')
        self.svg["width"] = str(self.frame_width)+self.unit
        self.svg["height"] = str(self.frame_height)+self.unit
        





    #Flip Vertically:
    def flip_svg_vertically(self):
        # Create a new group to wrap all elements
        group = self.svg.g(transform="scale(1, -1)")  # Adjust translation if necessary

        # Move all existing elements into the group
        for element in self.svg.elements:
            group.add(element)
        
        # Clear existing elements from dwg and add the group
        self.svg.elements = []  # Clear all elements from dwg
        self.svg.add(group)  # Add the group with the transformation
        
        # Save the flipped SVG
        self.svg.save(pretty=True)





    #Extract Node Coordinates (x,y,rad):
    def __extract_node_coords(self):
        floorplan = self.floorplan
        for cell in floorplan.cells.values():
            self.node_coords.append(cell.pose)

        #Scale Coordinates:
        for coord in self.node_coords:
            coord[0] = coord[0] * self.scale
            coord[1] = coord[1] * self.scale






    #If the Sortplan has been provided:
    #We need Bin Coords
    #We need the Type of Bin
    #We need the Side
    def __extract_bin_info(self):
        floorplan = self.floorplan
        sortplan_data = self.sortplan_data
        for key in sortplan_data.keys():
            self.bin_coords.append(floorplan.getCellFromId(key).pose)
            self.bin_types.append(sortplan_data[key]["type"])
            if sortplan_data[key]["type"] == "output":
                temp_key = list(sortplan_data[key]['sub_directions'].keys())
                self.bin_sides.append(sortplan_data[key]['sub_directions'][temp_key[0]]["side"])
            else:
                self.bin_sides.append(-1)





    #Find the min_x, min_y, max_x, max_y for scaling
    def __find_limits(self):
        self.x_min = +1000000
        self.y_min = +1000000
        self.x_max = -1000000
        self.y_max = -1000000

        for x,y,rad in self.node_coords:
            if x<self.x_min:
                self.x_min = x 
            if x>self.x_max:
                self.x_max = x 
            if y<self.y_min:
               self. y_min = y 
            if y>self.y_max:
                self.y_max = y 




    #Draw an Arrow
    def __draw_arrow(self,coords):
        # Draw the line (arrow shaft)
        #Scaling:
        #coords[0] = coords[0]*self.scale
        #coords[1] = coords[1]*self.scale
        
        #Drawing
        width = self.node_width 
        height = self.node_height
        svg = self.svg
        start = (coords[0],coords[1])
        end = (coords[0]+(width/2), coords[1])
        theta = np.degrees(coords[2])
        line = svg.line(start=(start[0],start[1]), 
                        end = (end[0],end[1]),
                        stroke='red', 
                        stroke_width=self.stroke_width)
        #line.set_markers((None, None, arrow_marker.get_funciri()))
        line.rotate(theta,center = (start))
        svg.add(line)
        svg.save(pretty=True)




    #Draw an Isolated Node:
    def __draw_node(self,coords,node_type):
        x_pos = coords[0] 
        y_pos = coords[1] 
        theta = np.degrees(coords[2])
        svg = self.svg

        #Node Dimensions
        node_offset = self.node_offset
        width = self.node_width
        height = self.node_height

        #Node Formatting
        # if node_type == "init":
        #     stroke_color = "rgb(0,0,255)"
        #     #fill_color = "rgb(255,0,255)"
        #     fill_color = "none"
        #     fill_opacity = "0.1"
        # elif node_type == "target":
        #     stroke_color = "rgb(0,100,100)"
        #     #fill_color = "rgb(0,100,100)"
        #     fill_color = "none"
        #     fill_opacity = "0.1"
        # elif node_type == "entry_and_exit":
        #     stroke_color = "rgb(255,0,0)"
        #     fill_color = "rgb(255,0,0)"
        #     fill_opacity = "0.1"
        
        stroke_color = "rgb(0,100,100)"
        stroke_width = self.stroke_width
        fill_color = "none"
        fill_opacity = "0.1"

        #Find the top Left Corner
        top_left = np.array([x_pos-width/2,y_pos-height/2])
        
        #Draw Rect
        rect = svg.rect(insert = (top_left[0], 
                                  top_left[1]),
                        size = (width,height-node_offset),
                        fill = fill_color,
                        fill_opacity = fill_opacity,
                        stroke = stroke_color,
                        stroke_width = stroke_width)
        rect.rotate(theta,center= (x_pos,y_pos))
        #self.svg_nodes.append(rect)
        svg.add(rect)
        svg.save(pretty = True)





    #Draw an Isolated Bin
    def __draw_bin(self,bin_coord, bin_type, bin_side):
        #Scaling:
        #bin_coord[0] = bin_coord[0] * self.scale
        #bin_coord[1] = bin_coord[1] * self.scale

        if self.floorplan_file==None:
            return
        svg = self.svg

        
        node_center = (bin_coord[0],bin_coord[1])
        theta = np.degrees(bin_coord[2])

        if  bin_type == "input":
            bin_width = 1 * self.scale
            bin_height = 1 * self.scale
        else:
            bin_width = self.bin_width
            bin_height = self.bin_height
        
        bin_offset = self.bin_offset

        if bin_side == -1: #Bin is on the Left Side:
            bin_x = bin_coord[0]
            bin_y = bin_coord[1] + bin_height/2 + self.node_height/2

        elif bin_side == 1: #Bin is on the Right Side:
            bin_x = bin_coord[0]
            bin_y = bin_coord[1] - (bin_height/2 + self.node_height/2)

        else:
            raise TypeError("Invalid Side")

        #Find the top_left for plotting
        top_left = [bin_x-(bin_width/2),bin_y-(bin_height/2)]

        #Bin Formatting
        fill_color = 'none'
        fill_opacity = "0.1"
        stroke_color = "rgb(100,100,0)"
        stroke_width = self.stroke_width


        rect = svg.rect(insert = (top_left[0], 
                                top_left[1]),
                    size = (bin_width-bin_offset,bin_height),
                    fill = fill_color,
                    fill_opacity = fill_opacity,
                    stroke = stroke_color,
                    stroke_width = stroke_width)
        
        rect.rotate(theta,center = node_center)
        svg.add(rect)
        svg.save(pretty=True)





    #Draw All Nodes:
    def __draw_all_nodes(self):
        for node_coord in self.node_coords:
            self.__draw_node(node_coord)
    




    #Draw All Lines:
    def __draw_all_lines(self):
        for node_coord in self.node_coords:
            self.__draw_arrow(node_coord)
    



    def __draw_all_bins(self):
        num_bins = len(self.bin_coords)
        for idx in range(num_bins):
            bin_coord = self.bin_coords[idx]
            bin_side = self.bin_sides[idx]
            bin_type = self.bin_types[idx]
            self.__draw_bin(bin_coord=bin_coord,bin_side=bin_side,bin_type=bin_type)



    #Draw All Elements:
    def __draw_all_elements(self):
        for node in self.floorplan.cells.values():
            self.__draw_node(coords=node.pose, node_type = node.cell_type)
        self.__draw_all_lines()
        self.__draw_all_bins()
        #self.__draw_all_nodes()
        #self.__draw_all_lines()
    

    #Convert SVG file to DXF File