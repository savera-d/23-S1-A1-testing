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

    def __init__(self): #initialising set layer store 
        """
        initialise the set layer store class
        current layer = the current layer that is being applied on the grid 
        is special = creates a toggle which changes if special is applied or not 
        """
        self.current_layer = None
        self.is_special = False

    def add(self,layer): #implementing add in set layer store DO I NEED TO DO A DOCSTRING FOR THESE FUNCTIONS?
        self.current_layer = layer #the current layer will be replaced by the new chosen layer
        
    def erase(self,layer): #implementing erase in set layer store
        self.current_layer = None #the current layer will be removed 
    
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        start= start colour tuple (r,g,b)
        timestamp= integer value 
        x= x coordinate (int)
        y= y coordinate (int)
        """
        if self.current_layer == None: #if there is no current layer applied
            return start   #return the starting tuple as no effects have been added
        
        elif self.is_special: #if special effect is applied 
            i=0
            self.current_colour = self.current_layer.apply(start, timestamp,x,y) #get the currrent colour tuple without special being applied
            newtuple = tuple([255 - colours for colours in self.current_colour]) #special is applied by subtracting the current tuples from 255
            return newtuple #returns the special tuple with special applied to it 
        elif not self.is_special: #if special is not applied 
            return self.current_layer.apply(start, timestamp, x , y) #return the current colour tuple from the layer that is applied 

    def special(self): 
        """
        When special is applied SetLayerStore keeps the current layer, but always applies an inversion (255 minues the colour) of the colours after the layer has been applied
        """
        self.is_special = not self.is_special #acts as a toggle to switch self.special between true and false

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self):
        """
        initialising the additive layer store class 
        our queue- creating an empty queue to add layers to, its operations are applied first in first out 
        """
        self.our_queue = CircularQueue(1000) #creating the empty queue 
    
    def add(self,layer):
        self.our_queue.append(layer) #using the queue method append to add layers to our queue

    def erase(self,layer):
        self.our_queue.serve() #using the queue method to remove layers from our queue
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]: 
        """
        Returns the colour this square should show, given the current layers.
        start= start colour tuple (r,g,b)
        timestamp= integer value 
        x= x coordinate (int)
        y= y coordinate (int)
        """
        if self.our_queue.is_empty(): #if there are no layers in our queue
            return start #return the start tuple 
        else:
            new_queue = CircularQueue(1000) #creating an empty circular queue
            while not self.our_queue.is_empty(): #while our queue has layers in it
                oldest_layer = self.our_queue.serve() #remove the oldest layer that was added to the queue
                new_queue.append(oldest_layer) # add this oldest layer into our new circular queue
                oldest_colour = oldest_layer.apply(start, timestamp, x, y) #using apply to get the oldest colour as a tuple from the oldest layer
                oldest_layer = None #oldest layer is updated to none so that it doesnt become more than one layer for the purpose of accessing the oldest colour only
                start = oldest_colour

            self.our_queue = new_queue
            return oldest_colour
        
    def special(self):
        """
        When special is applied additive layer reverses the "ages" of each layer, so the oldest layer is now the youngest layer, etc
        """
        temp_stack = ArrayStack(1000) #creating an empty array stack 
        new_queue = CircularQueue(1000) #creating a new circular queue
        for i in range (len(self.our_queue)): #going through the layers in our queue 
            self.current_layer = self.our_queue.serve() #removing each layer from our queue one by one in a first in first out order
            temp_stack.push(self.current_layer) # pushing each layer into a temporary stack 
        for i in range(len(temp_stack)): #going through each layer pushed into the temporary stack
            current_item = temp_stack.pop() #popping/removing each layer in a last in first out orderr
            new_queue.append(current_item) #as the layers are popped off the temp stack they are added into our new queue. this will be in reversed age order of layers
            
        self.our_queue = new_queue # updating the self variable so it can be used everywhere else as the updated queue


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
        """
        initialises the Sequence layer store class
        array sorted list = storing our layers in an array sorted list 
        """
        self.array_sorted_list = ArraySortedList(1000)

    def add(self,layer: Layer):
        self.array_sorted_list.add(ListItem(layer, layer.index)) #using the sorted list's method append to add layers to our sorted list
        
    def erase(self,layer: Layer):
        index = self.array_sorted_list.index(ListItem(layer,layer.index)) #finding the index of the layer we are trying to delete
        self.array_sorted_list.delete_at_index(index) #using the sorted lists method to delete the layer at the index we want

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
        """
        special for sequential layer store removes the median "applying" layer based on its name, lexicographically ordered.
        - in the case of an even number of layers we select the lexicographically smaller ordered name
        median pos = 
        array sorted list = 
        """
        if len(self.array_sorted_list)%2 != 0:
                median_pos = len(list)/2 -1 # in order to change it from the position to an index value we minus 1
                median_pos += 0.5 # we add the 0.5 in order to get a whole number that we can index.
                list.delete_at_index(median_pos)
        if len(self.array_sorted_list)%2 == 0:
                median_pos = len(list)/2 -1 # we minus 1 in order to change the position to an index
                list.delete_at_index(median_pos)
        return self.array_sorted_list

