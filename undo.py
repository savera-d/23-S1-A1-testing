from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:
    def __init__(self) -> None: 
        """
        inititalising where actions are stored for undo and redo by creating stacks
        best and worst case complexity = O(1) all of the items are assigments
        """
        #worst complexity = O(1)
        self.redo_stack = ArrayStack(10000)# creatinig an empty arraystack for redo
        #worst complexity = O(1)
        self.undo_stack = ArrayStack(10000)#creating an empty arraystack for undo
        

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        arguments= 
         action: is an object of painaction with steps of type painstep
        complexity best and worst = O(1)
        """
        #worst complexity = O(1)
        self.undo_stack.push(action)#paintaction is pushed into undo stack 
        

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.
        arguments-
        grid - the grid on which we do the undo action of type Grid
        return: The action that was undone of type Paintaction, or None.
        complexity worst = O(undo_apply)everything else is O(1) this is of the greatest complexity
        best complexity = O(1) where the undostack is empty
        """
        #worst complexity = O(1)
        if len (self.undo_stack)>0:  #check if undo stack is empty 
            #worst complexity = O(1)
            action = self.undo_stack.pop()#paintaction is removed from undo stack
            #worst complexity = O(1)
            self.redo_stack.push(action) #paintaction is added to redo stack
            #worst complexity = O(undo_apply)
            action.undo_apply(grid) #this removes the item we are undoing from the grid object
            #worst complexity = O(1)
            return action
        #worst complexity = O(1)
        return None #if undo stack is empty 
        
    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing
        arguments-
         grid:the grid on which we do the redo action of type Grid
        return: The action that was redone of type Paintaction, or None.
        complexity worst = O(redo_apply) evrything else is O(1 ) so the worst is O(redo_apply)
        best case complexity = O(1) where the redo stack is emoty and None is retured.
        """
        #worst complexity = O(1)
        if len (self.redo_stack)>0:  #check if redo stack is empty
            #worst complexity = O(1) 
            item = self.redo_stack.pop()#paintaction is removed from redo stack
            #worst complexity = O(1)
            self.undo_stack.push(item) #paintaction is added to undo stack
            #worst complexity = O(redo_apply)
            item.redo_apply(grid) #this adds the item we are redoing to the grid object
            return grid 
        return None #if redo stack is empty     