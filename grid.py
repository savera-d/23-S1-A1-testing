from __future__ import annotations
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.referential_array import ArrayR
from layer_store import *

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.draw_style=draw_style
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE
        self.x= x
        self.y=y
        self.grid = ArrayR(x)
        for i in range(x):
            self.grid[i] = ArrayR(y)
        

    
    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size <Grid.MAX_BRUSH:
            self.brush_size+=1
        else:
            raise ValueError("Brush Size is already Max")

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """

        if self.brush_size>Grid.MIN_BRUSH:
            self.brush_size-=1
        else:
            raise ValueError("Brush Size is already Min")
        

    def special(self):
        """
        Activate the special affect on all grid squares.
        """

        for i in range(self.x):
            for j in range(self.y):
                LayerStore.special()

    def colour(self,layer,drawstyle,x,y):
        self.draw_style = drawstyle
        coordinate_list = ArraySortedList(100)
        for i in range(self.width):
            for j in range (self.height): # this should check all the the points ini the grid slow byt works
                distance  = self.manhattan_distance(x,y,i,j)
                if distance <= self.brush_size:
                    coordinate_list[j] = [i,j] # to be used to apply the layer to 

    # FOR A GRID WHERE THERE IS ALREADY ITMES for x and y
        if self.grid[x][y] != None:
            if type(self.grid[x][y]) == SequenceLayerStore and self.draw_style == "SEQUENCE":
                self.grid[x][y].add(layer)
            elif type(self.grid[x][y]) == SetLayerStore and self.draw_style == "SET":
                self.grid[x][y].add(layer)
            elif type(self.grid[x][y]) == AdditiveLayerStore and self.draw_style == "ADD":
                self.grid[x][y].add(layer)
            #If the layerstore and the draw style is not hte same we override the current layerstore
            else: 
                if self.draw_style == "TO CHECK WHICH ONE":
                    self.grid[x][y] = SequenceLayerStore()# x will be the value and the y will be the key value
                    self.grid[x][y].add(layer) # this should use the method from the layer store to add the layer to the store
                    #current_position = my_grid[value.item][value.key] # this should save the sequance layer store into the current pos
                    #current_position.arraysortedlist[layer.index] = [layer, layer.name] #this should insert the layer and the name into the array sorted list of hte layer store

                if self.draw_style == "TO CHECK WHICH ONE":
                    self.grid[x][y] = SetLayerStore() # create a setlayerstore for this position
                    self.grid[x][y].add(layer) # this should simply use the add function to add the selected painted layer into the wanted grid positions
        
                if self.draw_style == "TO CHECK WHICH ONE":
                    self.grid[x][y] = AdditiveLayerStore()
                    self.grid[x][y].add(layer)

        elif self.grid[x][y] == None:
            if self.draw_style == "TO CHECK WHICH ONE":
                self.grid[x][y] = SequenceLayerStore()# x will be the value and the y will be the key value
                self.grid[x][y].add(layer) # this should use the method from the layer store to add the layer to the store
                #current_position = my_grid[value.item][value.key] # this should save the sequance layer store into the current pos
                #current_position.arraysortedlist[layer.index] = [layer, layer.name] #this should insert the layer and the name into the array sorted list of hte layer store

            if self.draw_style == "TO CHECK WHICH ONE":
                self.grid[x][y] = SetLayerStore() # create a setlayerstore for this position
                self.grid[x][y].add(layer) # this should simply use the add function to add the selected painted layer into the wanted grid positions
            
            
            if self.draw_style == "TO CHECK WHICH ONE":
                self.grid[x][y] = AdditiveLayerStore()
                self.grid[x][y].add(layer)

        #FOR MANHATTAN SQUARES
        for value in coordinate_list:
            if self.grid[value.item][value.key] == None: #CHECK IF THE MAHATTAN SQUARE IS EMPTY
                if self.draw_style == "SEQUENCE":
                    self.grid[value.item][value.key] = SequenceLayerStore()# x will be the value and the y will be the key value
                    self.grid[value.item][value.key].add(layer) # this should use the method from the layer store to add the layer to the store
                        #current_position = my_grid[value.item][value.key] # this should save the sequance layer store into the current pos
                        #current_position.arraysortedlist[layer.index] = [layer, layer.name] #this should insert the layer and the name into the array sorted list of hte layer store

                if self.draw_style == "SET":
                    self.grid[value.item][value.key] = SetLayerStore() # create a setlayerstore for this position
                    self.grid[value.item][value.key].add(layer) # this should simply use the add function to add the selected painted layer into the wanted grid positions
                    
                    
                if self.draw_style == "ADD":
                    self.grid[value.item][value.key] = AdditiveLayerStore()
                    self.grid[value.item][value.key].add(layer)

            else:
                if value.item == x and value.key == y:
                    pass
                elif type(self.grid[value.item][value.key]) ==SequenceLayerStore and self.draw_style == "SEQUENCE":
                    self.grid[value.item][value.key].add(layer)
                elif type(self.grid[value.item][value.key]) == SetLayerStore and self.draw_style == "SET":
                    self.grid[value.item][value.key].add(layer)
                elif type(self.grid[value.item][value.key]) == AdditiveLayerStore and self.draw_style == "ADD":
                    self.grid[value.item][value.key].add(layer)
                else:
                    if self.draw_style == "SEQUENCE":
                        self.grid[value.item][value.key] = SequenceLayerStore()# x will be the value and the y will be the key value
                        self.grid[value.item][value.key].add(layer) # this should use the method from the layer store to add the layer to the store
                        #current_position = my_grid[value.item][value.key] # this should save the sequance layer store into the current pos
                        #current_position.arraysortedlist[layer.index] = [layer, layer.name] #this should insert the layer and the name into the array sorted list of hte layer store

                    if self.draw_style == "SET":
                        self.grid[value.item][value.key] = SetLayerStore() # create a setlayerstore for this position
                        self.grid[value.item][value.key].add(layer) # this should simply use the add function to add the selected painted layer into the wanted grid positions
                    
                    
                    if self.draw_style == "ADD":
                        self.grid[value.item][value.key] = AdditiveLayerStore()
                        self.grid[value.item][value.key].add(layer)
            return self.grid


        




    # if the manhattan distance is smaller than the brush then the grid surrounding should be painted.
    def manhattan_distance(x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def __getitem__(self,item):
        """
        To get the item
        """
        return self[item]
    
    def __setitem__(self, item):
        """

        """
        #TODO

'''my_grid = Grid(Grid.DRAW_STYLE_SET, 3,3)
print(my_grid[1][1])
self.grid[3][2] = SetLayerStore()
self.grid[3][2].add(layer)'''
    