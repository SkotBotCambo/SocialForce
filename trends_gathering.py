import pytrends
from pytrends.request import TrendReq
import datetime
import time

avg_chicago = 48.8224852071
avg_newYork = 3.65877712032
avg_la = 21.8974358974
avg_to = 0.757396449704
avg_malibu = 3.25147928994


def pull_trends():
    pytrends = TrendReq(hl='en-US', tz=360)

    kw_list = ['Black Forest-Peyton']

    ####Code to get averages

    pytrends.build_payload(kw_list, cat=0, timeframe='now 1-H', geo='US', gprop='')
    y = pytrends.get_historical_interest(kw_list, year_start=2018, month_start=10, day_start=1, hour_start=0, year_end=2018, month_end=11, day_end=1, hour_end=0, cat=0, geo='US', gprop='', sleep=0)

    #print(y)
    #print(y["Chicago"].mean())
    #print(y["New York City"].mean())
    #print(y["Los Angeles"].mean())
    #print(y["Thousand Oaks"].mean())
    #print(y["Malibu"].mean())

    #Old time code (not used)
    '''
    now = datetime.datetime.now()
    #print (now)
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour

    if (hour == 0):
        pasthour = 22
    elif(hour==1):
        pasthour = 23
    else:
        pasthour = hour - 1
    '''

    ####Recent past hour of interest
    pytrends.build_payload(kw_list, cat=0, timeframe='now 1-H', geo='US', gprop='')
    z = pytrends.interest_over_time()
    #print(z)
    Chicago_Past_Hour = z["Chicago"].mean()
    NYC_Past_Hour = z["New York City"].mean()
    LA_Past_Hour = z["Los Angeles"].mean()
    TO_Past_Hour = z["Thousand Oaks"].mean()
    Malibu_Past_Hour = z["Malibu"].mean()
    #print(Chicago_Past_Hour)
    #print(NYC_Past_Hour)

    CRatio = Chicago_Past_Hour/avg_chicago
    NYCRatio = NYC_Past_Hour/avg_newYork
    LARatio = LA_Past_Hour/avg_la
    TORatio = TO_Past_Hour/avg_to
    MalibuRatio = Malibu_Past_Hour/avg_malibu

    print("Chicago Interest Ratio: " + str(CRatio) + "\n")
    print("NYC Interest Ratio: " + str(NYCRatio) + "\n")
    print("LA Interest Ratio: " + str(LARatio) + "\n")
    print("TO Interest Ratio: " + str(TORatio) + "\n")
    print("Malibu Interest Ratio: " + str(MalibuRatio) + "\n")

pull_trends()
