from __future__ import annotations
from abc import ABC, abstractmethod
from data_structures.stack_adt import ArrayStack
from layer_util import Layer
from grid import * # this should import everything
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
class LayerStore(ABC):

    def __init__(self) -> None:
        
        self.current_layer = None
        self.current_colour= None
    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self):
        self.current_layer = None
        self.is_special = False

    def add(self,layer):
        self.current_layer = layer
        
    def erase(self,layer):
        self.current_layer = None
    
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.current_layer == None:
            return start   
        
        elif self.is_special:
            i=0
            self.current_colour = self.current_layer.apply(start, timestamp,x,y)
            newtuple = tuple([255 - colours for colours in self.current_colour])
            return newtuple
        elif not self.is_special:
            return self.current_layer.apply(start, timestamp, x , y)

    def special(self):
        self.is_special = not self.is_special

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self):
        self.our_queue = CircularQueue(1000)
    
    def add(self,layer):
        self.our_queue.append(layer)

    def erase(self,layer):
        self.our_queue.serve()
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if self.our_queue.is_empty():
            return start
        else:
            new_queue = CircularQueue(1000)
            while not self.our_queue.is_empty():
                oldest_layer = self.our_queue.serve()
                new_queue.append(oldest_layer)
                oldest_colour = oldest_layer.apply(start, timestamp, x, y)
                oldest_layer = None
                start = oldest_colour

            self.our_queue = new_queue
            
            return oldest_colour
        

    def special(self):
        temp_stack = ArrayStack(1000)
        new_queue = CircularQueue(1000)
        for i in range (len(self.our_queue)):
            self.current_colour = self.our_queue.serve()
            temp_stack.push(self.current_colour) # this saves the values of the queue to the stack to be put back into the queue
        for i in range(len(temp_stack)):
            current_item = temp_stack.pop()
            new_queue.append(current_item)
            
        self.our_queue = new_queue


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self):
        self.array_sorted_list = ArraySortedList(1000)

    def add(self,layer: Layer):
        self.array_sorted_list.add(ListItem(layer, layer.index))
        
    def erase(self,layer: Layer):
        index = self.array_sorted_list.index(ListItem(layer,layer.index))
        self.array_sorted_list.delete_at_index(index)

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if len(self.array_sorted_list) == 0:
            return start
        
        for layer in self.array_sorted_list:
            if layer != None:
                layer = layer.value
      
                colour = layer.apply(start, timestamp, x, y)
                start = colour
                

        
        return colour
           
  

    
    
    def special(self):
        if len(self.array_sorted_list)%2 != 0:
                median_pos = len(list)/2 -1 # in order to change it from the position to an index value we minus 1
                median_pos += 0.5 # we add the 0.5 in order to get a whole number that we can index.
                list.delete_at_index(median_pos)
        if len(self.array_sorted_list)%2 == 0:
                median_pos = len(list)/2 -1 # we minus 1 in order to change the position to an index
                list.delete_at_index(median_pos)
        return self.array_sorted_list

