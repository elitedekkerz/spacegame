import logging
import numpy as np
import items

logger = logging.getLogger('cargo')

class cargo():
   def __init__(self):
       self.inventory = items.inventory()

   def parse(self, args):
      commands = {
      "list":self.list_items,
      "give":self.give,
      "dump":self.dump,
      "mass":self.get_mass,
      }
      try:
         return commands[args[1]](args)
      except:
         logger.debug('incorrect command %s', str.join(' ', args))
         return self.help()

   def list_items(self, args):
      try:
         items = self.inventory.content()
         if len(items) == 0:
            output = "Cargo bay is empty."
         else:
            output = "Cargo manifest:\n"
            for item in items:
               output += "{:40s}{}\n".format(item[0], item[1])

      except:
         return self.help()
      
      return player.response.ok, output

   def give(self, args):
      item_name = args[2]
      amount = float(args[3])
      logger.info('Player give {} {}'.format(amount, item_name))
      try:
         item = items.item(item_name, amount)
      except:
         logger.info("Player requested item that doesn't exist: {}".format(item_name))
         return player.response.ok, "There is no such thing as \"{}\" in the universe".format(item_name)
      self.inventory.insert(item)
      reply = "{} {} added to your inventory, you dirty little cheater.".format(amount, item_name)
      return player.response.ok, reply

   def dump(self, args):
      item_name = args[2]
      slots = self.inventory.find(item_name)
      if len(slots) == 0:
         return player.response.ok, "You don't have any \"{}\".".format(item_name)
      
      amount_dumped = 0

      if len(args) == 3:
         for slot in slots:
            item = self.inventory.take_all_from_slot(slot)
            amount_dumped += item.count
      else:
         amount = float(args[3])
         for slot in slots:
            item = self.inventory.take_from_slot(slot, amount- amount_dumped)
            amount_dumped += item.count

      reply = "You shoved {} {} out of airlock.".format(amount_dumped, item_name)
      return player.response.ok, reply

   def get_mass(self, args):
      mass = self.inventory.get_mass()
      reply = "Total mass of the invetory is {} kg.".format(mass)
      return player.response.ok, reply

   def help(self):
      usage = "cargo list\n"
      usage += "cargo mass\n"
      usage += "cargo give <item> <amount>\n"
      usage += "cargo dump <item> <amount>\n"
      return player.response.usage, usage

   def simulate(self, dt, power_factor):
      pass
   
   def getPowerGenerated(self):
      return self.reactor_level * self.max_power_output
