#return received arguments excluding the first one
class echo():
   def parse(self,args):
      try:
         return "Ok", str.join(' ', args[1:])
      except:
         return "Usage","echo <message>"

   def simulate(self, dt, power_factor):
      pass
