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
        # this creates an array for each existing array position, hence making a grid
        for i in range(x):
            self.grid[i] = ArrayR(y)
        if self.draw_style == 'SET':
            for xvals in range(x):
                for yvals in range(y):
                    self.grid[xvals][yvals] = SetLayerStore()  

        elif self.draw_style == 'SEQUENCE':
            for xvals in range(x):
                for yvals in range(y):
                    self.grid[xvals][yvals]= SequenceLayerStore()
        elif self.draw_style == 'ADD':
            for xvals in range(x):
                for yvals in range(y):
                    self.grid[xvals][yvals] = AdditiveLayerStore()
            
        

    
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

    def grid_paint(self, layer: Layer, x, y, brush_size):
        self.brush_size = brush_size
        for i in range(self.x):
            for j in range(self.y):
                distance = self.manhattan_distance(x,y,i,j)
                if distance < self.brush_size:
                    self.grid[i][j].add(layer)

    def manhattan_distance(x, y, x2, y2):
        return abs(x - x2) + abs(y - y2)

    def __getitem__(self,item):
        """
        To get the item`
        """
        return self.grid[item]
    
    def __setitem__(self, item, index):
        """

        """
        self.grid[index] = item

'''my_grid = Grid(Grid.DRAW_STYLE_SET, 3,3)
print(my_grid[1][1])
self.grid[3][2] = SetLayerStore()
self.grid[3][2].add(layer)'''
    