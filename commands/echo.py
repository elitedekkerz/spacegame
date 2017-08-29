#return received arguments excluding the first one
class echo():
   def parse(self,args):
      try:
         return str.join(' ', args[1:])
      except:
         return "Error. Usage: echo <message>"

   def simulate(self,dt):
      pass
