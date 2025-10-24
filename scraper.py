from bs4 import BeautifulSoup
import csv
import xml.etree.ElementTree as ET
import re
def main():
   wiki = open("Wikipedia-20250924013621.xml", "r")
   tree = ET.parse(wiki)
   root = tree.getroot()
   arr = root.findall("{http://www.mediawiki.org/xml/export-0.11/}page/{http://www.mediawiki.org/xml/export-0.11/}revision/{http://www.mediawiki.org/xml/export-0.11/}text")

   (male, female) = processXmlText(arr[1].text)

   wiki.close()        
   for i in range(1880, 2024):
      file = open(("./names/yob" + str(i) + ".txt"), "r")

      # print(soup)
      for line in file:
         #print(line)
         chars = line.split(",")
         name = chars[0]
         sex = chars[1]
         num = int(chars[2])
         # w = soup.find("title", string=name)
         #if not w == None:
         #   print(w.parent.string)
         #else:
          #  print(w)
         # print(name)
         if sex == "M":
            if name not in male:
               male[name] = {}
            if 'count' not in male[name]:
               male[name]['years'] = [i]
               male[name]['count'] = num
               male[name]['most_popular_year'] = (i, num)
            else:
               male[name]['years'].append(i)
               male[name]['count'] = male[name]['count'] + num
               if num > male[name]['most_popular_year'][1]:
                  male[name]['most_popular_year'] = (i, num)
         if sex == "F":
            if name not in female:
               female[name] = {}
            if 'count' not in female[name]:
               female[name]['years'] = [i]
               female[name]['count'] = num
               female[name]['most_popular_year'] = (i, num)
            else:
               female[name]['years'].append(i)
               female[name]['count'] = female[name]['count'] + num
               if num > female[name]['most_popular_year'][1]:
                  female[name]['most_popular_year'] = (i, num)
      file.close()


   file = open("results_m1.txt", 'w')
   for key in male:     
      s = str(key) +";" 
      if "count" in male[key]:
         s = s + str(male[key]['count']) + ";" + str(male[key]['most_popular_year'][0]) + ";"
      if "land" in male[key]:
         s = s + "["
         for l in male[key]['land']:
            s = s + str(l) + ","
         s = s + "];"
      #if "years" in male[key]:
      #   s = s+ "["
      #   for y in male[key]['years']:
      #      s = s + str(y) + ","
      #   s = s + "]"
      s = s + "\n"
      file.write(s)
   file.close()
   file = open("results_f1.txt", 'w')
   for key in female:     
      s = str(key) +";"
      if "count" in female[key]:
         s = s + str(female[key]['count']) + ";" + str(female[key]['most_popular_year'][0]) + ";"
      if 'land' in female[key]:
         s = s + "["
         for l in female[key]['land']:
            s = s + str(l) + ","
         s = s + "];"
      #if 'years' in female[key]:
      #   s = s + "["
      #   for y in female[key]['years']:
      #      s = str(s) + str(y) + ","
      #   s = s + "]"
      s = s + "\n"
      file.write(s)
   file.close()

def processXmlText(text):
   male = {}
   female = {}
   sex = "F"
   land = "US"
   elem = text.splitlines()
   for line in elem:
      if line.startswith("==") and line.endswith("=="):
         if line.find("Female names") > 0:
            sex = "F"
         elif line.find("Male names") >  0:
            sex = "M"
         else: 
            continue
         # print(sex)
      if line.startswith("|[["):
         if(line[line.find("]]")+2] == ","):
            #print(line)
            line = line[line.find("]]")+2:len(line)].strip()
            
            #print(line)
         l = line[3:line.find("]]")].strip()
         if l.find("name") < 0:
            if l.find("name") < 0 and l.find("|") > 0:
               l = l[l.find("|")+1:len(l)].strip()
            if l.find(",") > 0:
               l = l[l.find(",")+1:len(l)].strip()
            while l.startswith("["):
               l = l[1:len(l)].strip()
            land = l
         elems = re.findall("(\[\[[A-Za-z_]+\s?(\(given name\))?\|?[A-Za-z_\s]*\]\])", line)
         for i in range(1, len(elems)):
            name = elems[i][0]
            if(name.find("(given name)") > 0):
               name = name[2:name.find("(given name)")].strip()
            elif name.find("|") > 0:
               name = name[2:name.find("|")].strip()
            else:
               name =  name[2:name.find("]")].strip()
            if name != land:
               if sex == "F":
                  if name not in female:
                     female[name] = {}
                  if "land" not in female[name]:
                     # print(land)
                     female[name] = {}
                     female[name]["land"] = []
                  n = female[name]["land"]
                  if land not in n:
                     n.append(land)
               elif sex == "M":
                  if name not in male:
                     male[name] = {}
                  if "land" not in male[name]:
                     # print(land)
                     male[name] = {}
                     male[name]["land"] = []
                  n = male[name]["land"]
                  if land not in n:
                     n.append(land)
   #print(male)
   #print(female)
   return (male, female)
if __name__ == "__main__":
   main()