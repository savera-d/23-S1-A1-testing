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
        #initialising the variables that will be used within the class Grid
        self.draw_style=draw_style #draw style will choose the layerstore
        self.brush_size = Grid.DEFAULT_BRUSH_SIZE #the brrush size will be initialised as the default brush size
        self.x= x #x width of the  grid
        self.y=y #y height of the grid
        self.grid = ArrayR(x) #creating an array for the grid
        for i in range(x):  # this creates an array for each existing array position- x and y coordinate, hence making a grid
            self.grid[i] = ArrayR(y)

        if self.draw_style == 'SET': #checks if draw style chosen by user is for set layer store
            for xvals in range(x): #goes through each x and y value in the grid
                for yvals in range(y):
                    self.grid[xvals][yvals] = SetLayerStore() #allocates each grid square to set layer store type

        elif self.draw_style == 'SEQUENCE': #checks if draw style chosen by user is sequence layer store
            for xvals in range(x): #goes through each x and y value in the grid
                for yvals in range(y):
                    self.grid[xvals][yvals]= SequenceLayerStore() #allocates each grid square to sequence layer store type

        elif self.draw_style == 'ADD':# checks if draw style chosen by user is add layer store
            for xvals in range(x): #goes through each x and y value in the grid
                for yvals in range(y):
                    self.grid[xvals][yvals] = AdditiveLayerStore() #allocates each grid square to additive layer store type
            
        

    
    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        #checks if brush size is less than max brush size
        if self.brush_size <Grid.MAX_BRUSH:
            self.brush_size+=1 #increases brush size by one
        else:
            raise ValueError("Brush Size is already Max") #if brush size is not less than max brush size

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        #checks if brush size is greater than min brush size
        if self.brush_size>Grid.MIN_BRUSH:
            self.brush_size-=1 #reduces brush size by one 
        else:
            raise ValueError("Brush Size is already Min") #if brush size is not greater than min brush size
        

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        for i in range(self.x):#goes through all x values in grid
            for j in range(self.y): #for each x value, it selects each grid square by selecting the corresponding y value
                LayerStore.special() #activates special to every grid square


    def grid_paint(self, layer: Layer, x, y, brush_size):
        """
        called from on paint in main.py
        Called when a grid square is clicked on, which should trigger painting in the vicinity.
        Vicinity squares outside of the range [0, GRID_SIZE_X) or [0, GRID_SIZE_Y) can be safely ignored.

        layer: The layer being applied.
        px: x position of the brush.
        py: y position of the brush.
        """
        coordinate_list = ArraySortedList(1000) #creating an empty array sorted list to return with the coordinates at the end of the function
        self.brush_size = brush_size 
        for i in range(self.x): #goes through all grid squares (each x and corresponding y coordinate)
            for j in range(self.y):
                distance = self.manhattan_distance(x,y,i,j)  #distance is the manhattan distance calculated by the function below
                if distance < self.brush_size: #checks that the manhattan distance is less than the brush size
                    self.grid[i][j].add(layer) #the coordinates within  manhattan distance will have the layer applied to them
                    coordinate_list.add(ListItem(i,j)) #adds the x y coordinates to the list we created

        return coordinate_list #returns sorted list with the x y coordinates 
    
    #calculates the manhattan distance given 2 coordinates
    def manhattan_distance(x, y, x2, y2): #two x and y coordinates are inputs to the function
        return abs(x - x2) + abs(y - y2)  #sum the absolute differences between the coordinates

    def __getitem__(self,item):
        """
        To get the item`
        """
        return self.grid[item]
    
    def __setitem__(self, item, index):
        """

        """
        self.grid[index] = item

    