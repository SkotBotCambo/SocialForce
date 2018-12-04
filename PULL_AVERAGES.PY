import pytrends
from pytrends.request import TrendReq
import csv
import time

path = "C:\\Users\\mikeb\\Documents\\Northwestern\\FQ2018\\DSGN375\\"
pathend = ".csv"

city_mean_list = []

def csvwriter(master_list, out):
    with open(out, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for i in range(0, len(master_list), 2):
            writer.writerow(master_list[i:i + 2])
    #del city_mean_list[:]
    output.close()

def open_csv(filename):
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        city_list = list(reader)

        ln = len(city_list)
        i = 0
        lst = []

        while (i < ln):

            lst.append(city_list[i][0])
            i += 1

        lst = sorted(lst)
        f.close()
        return lst


def pull_five(city_list, len):
    indx = 0

    while (indx < len):
        kw_list = []
        if (len - indx >= 5):
            kw_list = city_list[indx:indx+5]
            #print(kw_list)
            time.sleep(2)
            pull_trends(kw_list)
            print(str("{0:.2f}".format(((indx + 5) / float(len))*100)) + "% complete")
            indx = indx + 5
        else:
            kw_list = city_list[indx:len]
            #print(kw_list)
            pull_trends(kw_list)
            print(str("{0:.2f}".format(((indx + 5) / float(len)) * 100)) + "% complete")
            indx = indx + 5


def pull_trends(kw_list):
    pytrends = TrendReq(hl='en-US', tz=360)
    print(kw_list)

    ####Code to get averages
    #try:
    pytrends.build_payload(kw_list, cat=0, timeframe='now 1-H', geo='US', gprop='')
    y = pytrends.get_historical_interest(kw_list, year_start=2018, month_start=8, day_start=1, hour_start=0, year_end=2018, month_end=10, day_end=10, hour_end=0, cat=0, geo='US', gprop='', sleep=0)
    print(y)
    for each in kw_list:
        mu = y[str(each)].mean()
        city_mean_list.append(each)
        city_mean_list.append(mu)

    #except:
        #print('An Error Occurred')

def ___main___():

    city_list = open_csv("big-cities-with-states-missed.csv")
    ln = len(city_list)
    pull_five(city_list, ln)
    csvwriter(city_mean_list, path + "big-cities-with-states-missed-plus-mean" + pathend)

    #print ("DONE " * 100 + "\n" + "DONE " * 100 + "\n" + "DONE " * 100)

___main___()


