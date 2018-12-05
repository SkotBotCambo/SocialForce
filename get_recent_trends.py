import pytrends
import time
import csv
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
cities = []
city_base_relevance = []

####################################################################################
#### csvwriter
#### Writes to csv file
#### Writes in rows of two
####################################################################################

def csvwriter(master_list, out):
    with open(out, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for i in range(0, len(master_list), 4):
            writer.writerow(master_list[i:i + 4])
    print("Finished scrape of csv\n")
    output.close()

####################################################################################
#### replace_data_and_write
#### This one is tricky
    #### First it opens the output files and reads what is currently there
    #### Then is compares the new data to the old data, replacing the ratios of each locality
    #### Then it writes the fixed data back to the csv by call csvwriter   
####################################################################################

def replace_data_and_write(new_data):
    path = "C:\\Users\\mikeb\\Documents\\Github\\Social-Focus\\static\\csv\\city-ratio-file.csv"
    master_list = []
    with open(path, "rb") as old_data:
        reader = csv.reader(old_data)
        master_list = list(reader)
    old_data.close()

    print(master_list)
    header = master_list[:1]
    master_list = master_list[1:]

    if master_list[0] == []:
        master_list = master_list[0]
    else:
        temp = master_list
        master_list = []
        for each in header[0]:
            master_list.append(each)

        for each in temp:
            master_list.append(each[0])
            master_list.append(float(each[1]))
            master_list.append(each[2])
            master_list.append(each[3])

    print("current: " + str(master_list))
    for each in new_data:
        #if each[0] in master_list:
            #print("Loc2: " + each[0])
        indx = master_list.index(each[0])
        master_list[indx+1] = each[1]
            #print("current:" + str(master_list))
        #else:
            #print("Loc: " + each[0])
            #master_list.append(each[0])
            #master_list.append(each[1])
            #print("current:" + str(master_list))

    csvwriter(master_list, path)

####################################################################################
#### split_into_fives
#### helper function
#### takes full list of locations and splits them into a an array 5 at a time
#### Google trends keywords only allows 5 to be request at a time
#### Returns a nested array [[city_1, city_2, city_3, city_4, city_5],
####                         [city_6, city_7, city_8, city_9, city_10],...]
####################################################################################

def split_into_fives(city_list):
    ln = len(city_list)
    indx = 0
    list_of_kw_lists = []
    while (indx < ln):
        kw_list = []
        if (ln - indx >= 5):
            kw_list = city_list[indx:indx+5]
            indx = indx + 5
            list_of_kw_lists.append(kw_list)
            #print(str("{0:.2f}".format(((indx + 5) / float(len))*100)) + "% complete")

        else:
            kw_list = city_list[indx:ln]
            indx = indx + 5
            list_of_kw_lists.append(kw_list)

    return list_of_kw_lists

####################################################################################
#### get_ratio
#### Takes a place, and running average
#### Return the ratio of relevance (hourly mean interest/historical mean interest)
####################################################################################

def get_ratio(name, mu):
    indx = cities.index(name)
    base_mean = city_base_relevance[indx]
    ratio = mu/float(base_mean)
    #print("ratio got")
    return ratio

####################################################################################
#### pull_trend_avg
#### makes a call of keywords to Google Trends
#### Returns a nested array [[city_1, mean_interest_1], ...]
####################################################################################

def pull_trend_avg(kw_list):
    #print("pulling data")
    mean_list = []
    try:
        pytrends.build_payload(kw_list, cat=0, timeframe='now 1-H', geo='US', gprop='')
        z = pytrends.interest_over_time()

        for each in kw_list:
            mu = z[str(each)].mean()
            ratio = get_ratio(each, mu)
            mean_list.append([each, ratio])

        return mean_list

    except:
        print("You got yourself an error")
        for each in kw_list:
            mean_list.append([each, 0])

        return mean_list
####################################################################################
#### analyze_set
#### Helper function
#### Calls the above function:
####    Split into fives
####    Pull_trend_avg called on a loop with a two-send wait time in between
####    Return Ratio data to frontend
####################################################################################


def analyze_set(data):
    list_of_kw_lists = split_into_fives(data)

    list_of_cities_and_means = []

    for kw_list in list_of_kw_lists:
        five_means_list = pull_trend_avg(kw_list)
        #print(five_means_list)
        list_of_cities_and_means += five_means_list
        time.sleep(2)

    return list_of_cities_and_means

####################################################################################
#### open_csv
#### Opens and reads the specified csv
#### Turns data from csv into a list
#### Returns the list and closes the file
####################################################################################

def open_csv(num):
    path = "C:\\Users\\mikeb\\Documents\\Github\\Social-Focus\\city-section-"
    pathend = ".csv"
    url = path + str(num) + pathend
    del cities[:]
    del city_base_relevance[:]

    print("Starting scrape of csv " + str(num) + "\n")

    with open(url, 'rb') as f:

        reader = csv.reader(f)
        city_list = list(reader)

        ln = len(city_list)
        i = 0
        lst = []

        while (i < ln):

            lst.append(city_list[i][0])
            cities.append(city_list[i][0])
            city_base_relevance.append(city_list[i][1])
            i += 1

        lst = sorted(lst)
        f.close()
        return lst


####################################################################################
#### main
#### Start a loop where you can one of the six files that stores location
#### Returns data to frontend to update that section of the map
#### Prevents Google from 429'ing you
####################################################################################

def ___main___():
    i = 1
    while True:

        if i == 1:
            lst = open_csv(i)
            lst_city_ratio = analyze_set(lst)
            i = 2
            replace_data_and_write(lst_city_ratio)
            time.sleep(720)
        elif i == 2:
            lst = open_csv(i)
            lst_city_ratio = analyze_set(lst)
            replace_data_and_write(lst_city_ratio)
            i = 3
            time.sleep(720)
        elif i == 3:
            lst = open_csv(i)
            lst_city_ratio = analyze_set(lst)
            replace_data_and_write(lst_city_ratio)
            i = 4
            time.sleep(720)
        elif i == 4:
            lst = open_csv(i)
            lst_city_ratio = analyze_set(lst)
            replace_data_and_write(lst_city_ratio)
            i = 5
            time.sleep(720)
        elif i == 5:
            lst = open_csv(i)
            lst_city_ratio = analyze_set(lst)
            replace_data_and_write(lst_city_ratio)
            i = 6
            time.sleep(720)
        else:
            lst = open_csv(i)
            lst_city_ratio = analyze_set(lst)
            replace_data_and_write(lst_city_ratio)
            i = 1
            time.sleep(720)
        print("Written")
___main___()

def test():

    replace_data_and_write([["a", 0],["b", 0],["c", 0],["e", 5],["a", 3],["a", 8],["d", 0],["z", 0]])

#test()