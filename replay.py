from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue

class ReplayTracker:
    def __init__(self):
        self.queue = CircularQueue(1000)


    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        pass
   


    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.
        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        arguments-
            action: the paint action that occured onto the grid
            is_undo: will be true or false to show if an action was undone or not
        complexity- the best and worst case of this function is o(1), 
        appending an element to the end of the queue stays constant, and for this task the queue will not require any resizing of the list.
        """
        self.queue.append((action, is_undo)) #add the action and whether it is an 'undo' action to our queue
        


    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        arguments-
            grid- the grid is an input in order to check what layers were applied to the grid object created
        returns- true if there is no action to do and false if the redo apply action is run
        complexity- the big o of the functions is empty and serve is o(1), therefore the best and worse case time complexity of this function is also o(1)
        HELP COMPLEXITY
        """
        if self.queue.is_empty(): #check that there is action to do 
            return True
        full_Action = self.queue.serve() #serve the tuple
        action = full_Action[0] # teh action is saved at index 0 of the tuple
        is_undo = full_Action[1] #the is_undo is saved at the index 1
        if is_undo: #if is_undo is true run the undo_apply of the action
            action.undo_apply(grid)
        else:# if it is not undo, than run the redo_apply of the action.
            action.redo_apply(grid)
        return False


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

