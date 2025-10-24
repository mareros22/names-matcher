import requests
def main():
   file = open("results_f1.txt", 'r')
   print("Ingesting female names...")
   f = 0
   for line in file:
      f += 1
      if (f % 1000) == 0:
         print(f, " names ingested...")
      info = line.split(';')
      s = len(info)
      name = info[0]
      count = None
      biggest_year = None
      lands =[]
      if (s == 2): # only name and land
         l = info[1].split(',')
         for i in l:
            lands.append(i)
      elif (s == 3): # only name, count and year
         count = info[1]
         biggest_year = info[2]
      else: #name, count, year and lands
         count = info[1]
         biggest_year = info[2]
         l = info[3][1:len(line)].split(',')
         for i in l:
            lands.append(i)
         lands.pop() # remove end bracket
      #print("[",name, count, biggest_year, lands,"]")
      r = requests.post('http://127.0.0.1:5000/auth/add_name', json={"name":name, "sex":"F", "year":biggest_year})
   file.close()
   print("Done ingesting female names, ", f, " names ingested.")
   
   file = open("results_m1.txt", 'r')
   print("Ingesting male names...")
   f = 0
   for line in file:
      f += 1
      if (f % 1000) == 0:
         print(f, " names ingested...")
      info = line.split(';')
      s = len(info)
      name = info[0]
      count = None
      biggest_year = None
      lands =[]
      if (s == 2): # only name and land
         l = info[1].split(',')
         for i in l:
            lands.append(i)
      elif (s == 3): # only name, count and year
         count = info[1]
         biggest_year = info[2]
      else: #name, count, year and lands
         count = info[1]
         biggest_year = info[2]
         l = info[3][1:len(line)].split(',')
         for i in l:
            lands.append(i)
         lands.pop() # remove end bracket
      #print("[",name, count, biggest_year, lands,"]")
      r = requests.post('http://127.0.0.1:5000/auth/add_name', json={"name":name, "sex":"M", "year":biggest_year})
   file.close()
if __name__ == "__main__":
   main()