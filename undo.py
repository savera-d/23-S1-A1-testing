from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:
    def __init__(self) -> None: 
        """
        inititalising where actions are stored for undo and redo by creating stacks
        """
        self.redo_stack = ArrayStack(10000)# creatinig an empty arraystack for redo
        self.undo_stack = ArrayStack(10000)#creating an empty arraystack for undo
        

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        arguments= 
         action: is an object of painaction with steps of type painstep
        complexity-
        """
        self.undo_stack.push(action)#paintaction is pushed into undo stack 
        

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.
        arguments-
        grid - the grid on which we do the undo action of type Grid
        return: The action that was undone of type Paintaction, or None.
        complexity-
        """
        if len (self.undo_stack)>0:  #check if undo stack is empty 
            action = self.undo_stack.pop()#paintaction is removed from undo stack
            self.redo_stack.push(action) #paintaction is added to redo stack
            action.undo_apply(grid) #this removes the item we are undoing from the grid object
            return action
        return None #if undo stack is empty 
        
    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing
        arguments-
         grid:the grid on which we do the redo action of type Grid
        return: The action that was redone of type Paintaction, or None.
        complexity-
        """
        if len (self.redo_stack)>0:  #check if redo stack is empty 
            item = self.redo_stack.pop()#paintaction is removed from redo stack
            self.undo_stack.push(item) #paintaction is added to undo stack
            item.redo_apply(grid) #this adds the item we are redoing to the grid object
            return grid 
        return None #if redo stack is empty     