import urllib2
import csv
from bs4 import BeautifulSoup

path = "http://www.city-data.com/city/"
pathend = ".html"
csvfile = "C:\\Users\\mikeb\\Documents\\Northwestern\\FQ2018\\DSGN375\\big-cities-with-states.csv"

states = ["Alabama", "Alaska", "Arizona", "Arkansas",
          "California", "Colorado", "Connecticut",
          "Delaware", "Florida", "Georgia", "Hawaii",
          "Idaho", "Illinois", "Indiana", "Iowa", "Kansas",
          "Kentucky", "Louisiana", "Maine", "Maryland",
          "Massachusetts", "Michigan", "Minnesota",
          "Mississippi", "Missouri", "Montana", "Nebraska",
          "Nevada", "New-Hampshire", "New-Jersey", "New-Mexico",
          "New-York", "North-Carolina", "North-Dakota", "Ohio",
          "Oklahoma", "Oregon", "Pennsylvania", "Rhode-Island",
          "South-Carolina", "South-Dakota", "Tennessee",
          "Texas", "Utah", "Vermont", "Virginia", "Washington",
          "West-Virginia", "Wisconsin", "Wyoming"]

town_names = []

def scraper():
    for state in states:
        page = urllib2.urlopen(path + state + pathend)
        soup = BeautifulSoup(page, 'html.parser')
        #print(soup)
        table = soup.find('table', attrs={'id': 'cityTAB'})
        tbody = table.find('tbody')
        tBig = tbody.find_all('tr', attrs = {'class': 'rB'})
        #print(tBig)

        #towns = tbody.find_all('a')

        #print(towns)

        #for each in towns:
            #str = each.text.strip()
            #if ',' in str:
                #str = str.split(",", 1)[0]
            #town_names.append(str)

        for each in tBig:
            temp = each.findAll('td')
            pop = temp[2].text.strip()
            pop = pop.replace(",","")
            if int(pop) < 30000:
                continue
            strx = each.find('a')
            str =strx.text.strip()
            if ',' in str:
                str = str.split(",", 1)[0]
            str += ", " + state.replace("-", " ")

            #print(str)

            town_names.append(str)

    return (town_names)
    #return set(town_names)

def csvwriter(nameset):
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in nameset:
            writer.writerow([val])

names = scraper()

print(names)

csvwriter(names)

