def main():
   file = open("results_f1.txt", 'r')
   f = 0
   for line in file:
      f += 1
      if f > 20:
         return
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
      print("[",name, count, biggest_year, lands,"]")
   file.close()

   file = open("results_m1.txt", 'r')
   for line in file:
      info = line.split(';')
      print(info)
   file.close()
if __name__ == "__main__":
   main()