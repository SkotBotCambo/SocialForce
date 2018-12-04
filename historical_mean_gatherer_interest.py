from pytrends.request import TrendReq

means = []
def get_means(next_five):
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = next_five

    pytrends.build_payload(kw_list, cat=0, timeframe='now 1-H', geo='US', gprop='')
    historic_trends = pytrends.get_historical_interest(kw_list, year_start=2018, month_start=10, day_start=1, hour_start=0, year_end=2018, month_end=11, day_end=1, hour_end=0, cat=0, geo='US', gprop='', sleep=0)

    means.append(y["Chicago"].mean())
    return 0

def pull_next_five():
    next_five = 0
    return next_five





