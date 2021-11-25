import requests
from datetime import datetime, timezone, date

# Parameter: User input dates
# Return: [] where [0] = start date, [1] end date
def get_dates():
    start_date = input('Enter start date in DD.MM.YYYY format: ')
    end_date = input('Enter end date in DD.MM.YYYY format: ')
    return [start_date, end_date]

# Parameter: date format = DD.MM.YYYY 
# Return: Unix timestamp midnight UTC-timezone
def get_date_as_unix(date, is_startDate=True):
    day, month, year = map(int, date.split('.'))
    if is_startDate:
        dmy = datetime(year, month, day, 0, 0, tzinfo=timezone.utc)
        timestamp = int(dmy.timestamp())
        return timestamp
    dmy = datetime(year, month, day, 1, 0, tzinfo=timezone.utc)
    timestamp = int(dmy.timestamp())
    return timestamp

# Return: raw data as a json. Includes prices, market cap, total volumes
def get_raw_data(start_date, end_date, coin_id):
    request_url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=eur&from={start_date}&to={end_date}'
    request = requests.get(request_url)
    return request.json()

# Parameter: Unix timestamp as milliseconds
# Return: Unix timestamp as seconds
def timestamp_converter(milliseconds):
    seconds = milliseconds/1000.0
    return seconds

# Parameter: timestamp = Unix timestamp as seconds,
# Return: Date in DD.MM.YYYY-format
def unix_to_date(timestamp, milliseconds=True):
    if milliseconds:
        timestamp = timestamp_converter(timestamp)
    date = datetime.utcfromtimestamp(timestamp)
    formatted_date = date.strftime("%d.%m.%Y")
    return formatted_date

# Parameter: List = [DD.MM.YYYY, DD.MM.YYYY], where [0] = startDay, [1] = endDay
# Return: Number of days between given dates
def days_between(list):
    start_date, end_date = list
    start_day, start_month, start_year = map(int, start_date.split('.'))
    end_day, end_month, end_year = map(int, end_date.split('.'))
    delta = date(end_year, end_month, end_day) - \
        date(start_year, start_month, start_day)
    return delta.days

# Parameter: json = Raw data from 'getRawData'-function
# Return: [] that have []'s as a values where [0] = day(Unix), [1] = price of bitcoin
# Api returns data from every hour if date range is under 90 days. If its over 90, data is from once a day (midnight).
# Function filters unnecessary data from data set under 90 days by taking every 24th data_cell (every 24h).
# First one is by default closest to midnight, so the rest will be too.
def price_data(json):
    prices = json['prices']
    days = days_between([unix_to_date(
        prices[0][0]), unix_to_date(prices[-1][0])])
    if days < 90:
        prices_at_midnight = prices[::24]
        return prices_at_midnight
    return prices

# Parameter: json = Raw data from 'getRawData'-function
# Return: [] that have []'s as a values where [0] = day(Unix), [1] = 24h volume of bitcoin
# Api returns data from every hour if date range is under 90 days. If its over 90, data is from once a day (midnight).
# Function filters unnecessary data from data set under 90 days by taking every 24th data_cell (every 24h).
# First one is by default closest to midnight, so the rest will be too.
def trading_data(json):
    volumes = json['total_volumes']
    days = days_between([unix_to_date(timestamp_converter(
        volumes[0][0])), unix_to_date(timestamp_converter(volumes[-1][0]))])
    if days < 90:
        volumes_at_midnight = volumes[::24]
        return volumes_at_midnight
    return volumes

# Parameter: List of lists, where [0] = day, [1] = 24h volume
# Return: day = Unix time stamp of the date of top volume, highest = top 24h vol
def highest_volume(trading_data):
    top_volume = 0
    day = ''
    for data in trading_data:
        if data[1] > top_volume:
            top_volume = data[1]
            day = data[0]
    return day, top_volume

# Parameter: Data from 'price_data'-function (json)
# Return: Longest streak of days that coin has had lower price than day before.
def bear_trend(price_data):
    bear_trend = 0
    previous = 0
    length_of_trends = []
    for data in price_data:
        if data[1] < previous:
            bear_trend = bear_trend +1
        if data[1] > previous:
            length_of_trends.append(bear_trend)
            bear_trend = 0
        previous = data[1]
    length_of_trends.append(bear_trend)
    return max(length_of_trends)

# Parameter: Data from 'price_data'-function (json)
# Return: List including dates and prices for optimal profit. [0] = buy date, price [1] = sell date, price
def optimal_dates(price_data):
    max_diff = price_data[0][1] - price_data[0][1]
    min_max = []
    arr_size = len(price_data)

    for i in range(0, arr_size):
        for j in range(i+1, arr_size):
            if(price_data[j][1] - price_data[i][1] > max_diff):
                max_diff = price_data[j][1] - price_data[i][1]
                min_max = [price_data[i], price_data[j]]
    return min_max           




        

