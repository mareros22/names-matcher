import json
class name:
   def __init__(self, name, count, biggest_year):
      self.obj = {
         "name": name,
         "count": count,
         "biggest_year": biggest_year
      }
   
   def __str__(self):
      return f"{self.obj['name']};{self.obj['count']};{self.obj['biggest_year']}"
   
   def toJSON(self):
      return json.dumps(self.obj)