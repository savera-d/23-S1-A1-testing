from __future__ import annotations
from abc import ABC, abstractmethod
from data_structures.stack_adt import ArrayStack
from layer_util import Layer

from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
class LayerStore(ABC):

    def __init__(self) -> None:
        """
        initialising the layerstore class
        worse and best case Big O complexity = O(1)
        """
        #defining variables that will be used within our class
        #worst case complexity = O(1)
        self.current_layer = None
        #worst case complexity = O(1)
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
        worst and beset complexity = O(1) as these are assignments
        """
        #worst case complexity = O(1)
        self.current_layer = None
        #worst case complexity = O(1)
        self.is_special = False

    def add(self,layer)->bool: 
        """
        adds a layer to set layer store
        returns a boolean of true if the set layer store is changed due to an addition 
        argument-
            layer: the layer type chosen to be applied by the user 
        return: returns true if a layer is added
        complexity: O(1) best and worst complexity
        """
        #implementing add in set layer store
        #worst case complexity = O(1)
        self.current_layer = layer #the current layer will be replaced by the new chosen layer
        #worst case complexity = O(1)
        return True #function returns true if a layer is added
        
    def erase(self,layer) ->bool: #implementing erase in set layer store
        """
        removes a layer from the set layer store
        returns a boolean of true if the layer is removed using the erase function
        argument-
            layer: the layer that is being removed from the layer store
        return: returns true if a layer is erased
        complexity: o(1) best and worst complexity
        """
        #implementing erase
        #worst case complexity = O(1)
        self.current_layer = None #the current layer will be removed 
        #worst case complexity = O(1)
        return True #function returns true if erase is applied
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        arguments-
            start= start colour tuple (r,g,b)
            timestamp= integer value 
            x= x coordinate (int)
            y= y coordinate (int)
        return: return start as a tuple if no effect is applied, or else return the new applied colour as a tuple
        best case complexity = O(1), if isspecial is flase only assigments and returns and comparisions are run
        worst complexity: O(n) where n is the number of items in the tuple. As it will  iterate through
        every value in the tuple in order to apply the special when is special is true
        """
        #implementing get colour
        #worst case complexity = O(1)
        if self.current_layer == None: #if there is no current layer applied
            #worst case complexity = O(1)
            return start   #return the starting tuple as no effects have been added
        #worst case complexity = O(1)
        elif self.is_special: #if special effect is applied 
            #worst case complexity = O(1)
            i=0
            #worst case complexity = O(1)
            self.current_colour = self.current_layer.apply(start, timestamp,x,y) #get the currrent colour tuple without special being applied
            #worst and best case complexity = O(n) where n is the number of items in the tuple
            newtuple = tuple([255 - colours for colours in self.current_colour]) #special is applied by subtracting the current tuples from 255
            #worst case complexity = O(1)
            return newtuple #returns the special tuple with special applied to it 
            #worst case complexity = O(1)
        elif not self.is_special: #if special is not applied 
            #worst case complexity = O(1)
            return self.current_layer.apply(start, timestamp, x , y) #return the current colour tuple from the layer that is applied 

    def special(self): 
        """
        When special is applied SetLayerStore keeps the current layer, but always applies an inversion (255 minues the colour) of the colours after the layer has been applied
        best and worst complexities = O(1) there is only one assigment statement
        """
        #worst case complexity = O(1)
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
        worst and best case complexity = O(1) only one assignment
        """
        #worst case complexity = O(1)
        self.our_queue = CircularQueue(1000) #creating the empty queue 
     
    def add(self,layer)-> bool:
        """
        adds a layer the additive layer store 
        if the additive layer store queue is full then no layer is added and the function will return boolean false
        if the additive layer store queue is not full then a layer is added and the function will return a boolean true
        layer: the layer type chosen to be applied by the user 
        returns a boolean value based on whether the layer was added or not.
        worst and best case complexity = O(1) all functions and of O(1) and the rest are return statements or assignments

        """
        #implementing add
        #worst case complexity = O(1)
        if self.our_queue.is_full(): #checks if our queue is full
            #worst case complexity = O(1)
            return False #if the queue is full return false
            #worst case complexity = O(1)
        self.our_queue.append(layer)  #using the queue method append to add layers to our queue if it is not full
        #worst case complexity = O(1)
        return True #if a layer is added return true

    def erase(self,layer)-> bool:
        """
        removes a layer the additive layer store 
        if the additive layer store queue is empty then no layer is removed and the function will return boolean false
        if the additive layer store queue is not empty then a layer is removed and the function will return a boolean true
        layer: the layer type chosen to be applied by the user 
        returns a boolean based on whether a layer was removed or not
        best and worst case complexity = O(1) all assignments and the functions used are O(1 ) such as serve
        all return statements are also O(1)

        """
        #implementing erase
        #worst case complexity = O(1)
        if self.our_queue.is_empty():#checking if the queue is empty 
            #worst case complexity = O(1)
            return False #return false if the queue is empty 
        #worst case complexity = O(1)
        self.our_queue.serve() #using the queue method to remove layers from our queue if it is not empty 
        #worst case complexity = O(1)
        return True #if a layer is removed return true 
        

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]: 
        """
        Returns the colour this square should show, given the current layers.
        start= start colour tuple (r,g,b)
        timestamp= integer value 
        x= x coordinate (int)
        y= y coordinate (int)
        returns a tuple in format (r,g,b) which is the colour for the current square
        worst case complexity is = O(n*apply) as we iterate through the queue and n is hte number of items in teh queue
        and the O(apply) is the complexity of hte apply function for the layer
        best case complexity = O(1) where the queue is empty and we just return True
        """
        #implmementing get colour 
        #worst case complexity = O(1)
        if self.our_queue.is_empty(): #if there are no layers in our queue
            #worst case complexity = O(1)
            return start #return the start tuple 
        #worst case complexity = O(1)
        else:
            #worst case complexity = O(1)
            new_queue = CircularQueue(1000) #creating an empty circular queue
            #worst case complexity = O(n) where n is the length of the queue
            while not self.our_queue.is_empty(): #while our queue has layers in it
                #worst case complexity = O(1)
                oldest_layer = self.our_queue.serve() #remove the oldest layer that was added to the queue
                #worst case complexity = O(1)
                new_queue.append(oldest_layer) # add this oldest layer into our new circular queue
                #worst case complexity = O(apply)
                oldest_colour = oldest_layer.apply(start, timestamp, x, y) #using apply to get the oldest colour as a tuple from the oldest layer
                #worst case complexity = O(1)
                oldest_layer = None #oldest layer is updated to none so that it doesnt become more than one layer for the purpose of accessing the oldest colour only
                #worst case complexity = O(1)
                start = oldest_colour
            #worst case complexity = O(1)
            self.our_queue = new_queue
            #worst case complexity = O(1)
            return oldest_colour
        
    def special(self):
        """
        When special is applied additive layer reverses the "ages" of each layer, so the oldest layer is now the youngest layer, etc
        returns nothing
        best and worst case complexity = O(1) as we will always transverse through the queue and the stack of length n
        """
        #implementing special
        #worst case complexity = O(1)
        temp_stack = ArrayStack(1000) #creating an empty array stack 
        #worst case complexity = O(1)
        new_queue = CircularQueue(1000) #creating a new circular queue
        #worst case complexity = O(n) where n is hte length of the queue
        for i in range (len(self.our_queue)): #going through the layers in our queue 
            #worst case complexity = O(1)
            self.current_layer = self.our_queue.serve() #removing each layer from our queue one by one in a first in first out order
            #worst case complexity = O(1)
            temp_stack.push(self.current_layer) # pushing each layer into a temporary stack 
        #worst case complexity = O(n) where n is the length of the arraystack
        for i in range(len(temp_stack)): #going through each layer pushed into the temporary stack
            #worst case complexity = O(1)
            current_item = temp_stack.pop() #popping/removing each layer in a last in first out orderr
            #worst case complexity = O(1)
            new_queue.append(current_item) #as the layers are popped off the temp stack they are added into our new queue. this will be in reversed age order of layers
        #worst case complexity = O(1) 
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
        returns nothing
        worst aand best case Big O complexity = O(1)
        """
        #worst case complexity = O(1)
        self.array_sorted_list = ArraySortedList(1000) #creating an empty array sorted list
        #worst case complexity = O(1)
        self.lexico = ArraySortedList(1000) #lexicogrphically ordered empty array sorted list
    
    def add(self,layer):
        """
        adds a layer the sequential layer store 
        if the sequential layer store list is full then no layer is added and the function will return boolean false
        if the sequential layer store queue is not full then a layer is added and the function will return a boolean true
        layer: the layer type chosen to be applied by the user of type Layer
        returns nothing

        Worst case Big O complexity = O(N) where n is the length of the arraysortedlist, when we go through every
        value in the array_Srotedlist to find the item
        best case complexity = O(1) where the list is full and False is returned

        """
        #worst case complexity = O(1)
        if self.array_sorted_list.is_full() or self.lexico.is_full():
            #worst case complexity = O(1)
            return False
        #worst case complexity = O(1)
        else:
            #worst case complexity = O(1)
            if type(layer)==Layer:
                #worst case complexity = O(n) where n is the length of the array sorted list
                for i in range(len(self.array_sorted_list)):
                    #worst case complexity = O(1)
                    if self.lexico[i].value == layer:
                        #worst case complexity = O(1)
                        if self.lexico[i].key == layer.name:
                            #worst case complexity = O(1)
                            return True
                    #worst case complexity = O(1)
                    else: 
                        #worst case complexity = O(1)
                        continue
                #worst case complexity = O(n) where n is the length of the array sorted list
                self.array_sorted_list.add(ListItem(layer, layer.index))
                #worst case complexity = O(n) where n is the length of the array sorted list
                self.lexico.add(ListItem(layer, layer.name))
                #worst case complexity = O(1)
                return True
            #worst case complexity = O(1)
            else:
                #worst case complexity = O(1)
                return False



    def erase(self,layer: Layer) ->bool:
        """
        erase removes an item from the sequential layer store, by finding the positin that it is in and using the delete at index
        returns a boolean value based on whether an item was erased or not
        takes input of layer, of type Layer
        worse case Big O complexity = O(n^2) as we go through every value in the arraysorted list and we delete at index which also has
        a complexity of O(n).
        best case complexity = O(1) where the list is empty and False is returned
        
        """
        #worst case complexity = O(1)
        if self.array_sorted_list.is_empty(): # makesure that the list is not empty
            #worst case complexity = O(1)
            return False
        #worst case complexity = O(n) where n is the length of teh array sorted list
        for i in range(self.array_sorted_list.length):
            #worst case complexity = O(1)
            if self.array_sorted_list[i].value == layer and self.array_sorted_list[i].key == layer.index: #finding the index of the layer we are trying to delete
                #worst case complexity = O(n) the complexitiy of delete at index is O(n) due to shuffle left
                self.array_sorted_list.delete_at_index(i)#using the sorted lists method to delete the layer at the index we want
            #worst case complexity = O(1)
            if self.lexico[i].value == layer and self.lexico[i].key == layer.name:
                #worst case complexity = O(n) the complexitiy of delete at index is O(n)
                self.lexico.delete_at_index(i)
        #worst case complexity = O(1)
        return True
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        
         Returns the colour this square should show, given the current layers.
         arguments
            - start: of type tuple, the initial colour
            -timestamp: of type integer, the timestamp for the colour
            -x: of type integer, the x coordinate of the square
            -y: of type integer, the y coordinate of the square


        Worst Case Big O complexity = O(n) where n in the length of the array sorted list.
        best base complexity = O(1) where the array sorted list is empty and start tuple is returned
        """
        #worst case complexity = O(1) as is_empty() = O(1)
        if not self.array_sorted_list.is_empty():
            #worse case complexity = O(n) where n is the length of the array sorted list.
            for i in range (len(self.array_sorted_list)):
                #worse case complexity = O(1)
                layer = self.array_sorted_list[i].value
                #worse case complexity = O(1) #CHECK THIS ONE
                colour = layer.apply(start, timestamp,x,y)
                ##worse case complexity = O(1)
                start = colour
            #worse case complexity = O(1)
        return start

    
    
    def special(self):
        """
         special for sequential layer store removes the median "applying" layer based on its name, lexicographically ordered.
         - in the case of an even number of layers we select the lexicographically smaller ordered name
         no values are returned
         Worse case Big O = O(n) when the erase is called which has a complexity of O(n)
        best case complexity = O(1) where the list is empty and an expeption is raised
        """
        #worst case complexity = O(1)
        if len(self.array_sorted_list) == 0:
            #worst case complexity = O(1)
            raise ValueError("nothing to apply special to ")
        #wost case complexity = O(1)
        if len(self.lexico)%2!=0: # check if the length is even or not
            #worst case complexity = O(1)
            median_pos = self.lexico.length//2 #if it not even the median position is length divided by 2
        # worst case complexitity = O(1)
        elif len(self.lexico)%2 == 0: # if it is even
            #worst case complexity = O(1)
            median_pos = self.lexico.length//2 - 1 # median pos is hte len divided by 2 -1
        #worse case complexity = O(1)
        lexico_del = self.lexico[median_pos] #get the layer to delete
        #worse case complexity = O(1)
        layer = lexico_del.value # get the layer from the listitem
        #worse case complexity = O(n)
        self.erase(layer) #erase the layer
