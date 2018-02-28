import math
import numpy as np
import logging

class inventory(object):
    def __init__(self):
        self.inventory = []

    def __iter__(self):
        self.iter_index = 0
        return self

    def __next__(self):
        if self.iter_index < len(self.inventory):
            result = self.inventory[self.iter_index]
        else:
            raise StopIteration

        self.iter_index += 1
        return result

    #Insert an item to the invenotry
    def insert(self, item):
        for inv_item in self.inventory:
            if inv_item.name == item.name:
                item = inv_item.insert(item)
       
        if item.count != 0:
            self.inventory.append(item)

    #Add items to spesific slot, return items
    #that didn't fit in to the inventory
    def insert_slot(self, slot, item):
        if len(self.inventory) < slot:
            return item

        return self.inventory[slot].insert(item)

    #Take spesific amout of item from one slot
    def take_from_slot(self, slot, count):
        if len(self.inventory) < slot:
            return None

        new_item = self.inventory[slot].split(count)

        #If the slot is empty remove it
        if self.inventory[slot].count == 0:
            del self.inventory[slot]

        return new_item
    
    #Take all items from one slot
    def take_all_from_slot(self, slot):
        if len(self.inventory) < slot:
            return None

        new_item = self.inventory[slot]
        #Remove the item from the inventory
        del self.inventory[slot]

        return new_item

    #Return list of slots that contain that item
    def find(self, item_name):
        slots = []
        for slot, item in enumerate(self.inventory):
            if item.name == item_name:
                slots.append(slot)
        return slots

    #Get name of all items
    def content(self):
        items = []
        for item in self.inventory:
            items.append((item.name, item.count))
        return items

    def get_mass(self):
        total_mass = 0
        for item in self.inventory:
            total_mass += item.get_mass()
        return total_mass


class item(object):
    def __init__(self, item_name, count):
        #Set the name
        self.name = item_name
        #Get the item info from the master list
        self.type = game_items[item_name]

        #Set the count based of the current type
        if not self.type:
            self.count = 0
        elif self.type.countable == True:
            self.count = math.floor(count)
        else:
            self.count = count

    #Calculate the total mass
    def get_mass(self):
        return self.count * self.type.unit_mass

    #Combine an other item to this. Returns the 
    #item with new count
    def insert(self, item):
        if self.name == item.name:
            self.count += item.count
            item.count = 0

        return item

    #Split the item stack to two items
    def split(self, count):
        if self.type.countable == True:
            count = math.floor(count)

        if self.count < count:
            new_stack = item(self.name, self.count)
            self.count = 0
            return new_stack
        else:
            self.count -= count
            return item(self.name, count)
    
#Generic class to contain properties of all 
#game items
class item_type(object):
    def __init__(self, unit_mass, description, countable=False):
        # Unit_mass is mass of one unit of item type in kg. For countable itmes
        # it is mass of the object. For noncountable it is mass of one 
        # cubic meter of stuff. 
        self.unit_mass = unit_mass
        self.description = description
        self.countable = countable


game_items = {
    "uranium":item_type(19100, "Can be used as fuel"),
    "gold":item_type(19300, "Shiny"),
    "iron":item_type(7874, "Looks more like rust"),
    "ice":item_type(917, "Ice ice baby"),
    "stone":item_type(2500, "Just pile of rubble"),
    "space_pistol":item_type(1, "Pew Pew", countable=True)
}