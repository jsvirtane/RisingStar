import requests
from datetime import datetime, timezone, date

# Variable: User input dates
# Return: [] where [0] = start date, [1] end date


def getDates():
    startDate = input('Enter start date in DD.MM.YYYY format: ')
    endDate = input('Enter end date in DD.MM.YYYY format: ')
    return [startDate, endDate]

# Return: [] where [0] = start date as Unix timestamp, [1] = end date as Unix timestamp


def getDatesAsUnix():
    startDate, endDate = getDates()
    startDay, startMonth, startYear = map(int, startDate.split('.'))
    endDay, endMonth, endYear = map(int, endDate.split('.'))
    sdt = datetime(startYear, startMonth, startDay, 0, 0, tzinfo=timezone.utc)
    edt = datetime(endYear, endMonth, endDay, 1, 0, tzinfo=timezone.utc)
    startTimeStamp = int(sdt.timestamp())
    endTimeStamp = int(edt.timestamp())
    return [startTimeStamp, endTimeStamp]

# Return: raw data as a json. Includes prices, market cap, total volumes


def getRawData():
    startDate, endDate = getDatesAsUnix()
    requestUrl = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=eur&from={startDate}&to={endDate}'
    request = requests.get(requestUrl)
    return request.json()

# Variable: timestamp = Unix timestamp as seconds,
# Return: Date in DD.MM.YYYY-format


def UnixToDate(timestamp):
    date = datetime.utcfromtimestamp(timestamp)
    formattedDate = date.strftime("%d.%m.%Y")
    return formattedDate

# Variable: Unix timestamp as milliseconds
# Return: Unix timestamp as seconds


def timestampConverter(milliseconds):
    seconds = milliseconds/1000.0
    return seconds

# Variable: List = [DD.MM.YYYY, DD.MM.YYYY], where [0] = startDay, [1] = endDay
# Return: Number of days between given dates


def daysBetween(list):
    startDate, endDate = list
    startDay, startMonth, startYear = map(int, startDate.split('.'))
    endDay, endMonth, endYear = map(int, endDate.split('.'))
    delta = date(endYear, endMonth, endDay) - \
        date(startYear, startMonth, startDay)
    return(delta.days)

# Variable: Json = Raw data from 'getRawData'-function
# Return: [] that have []'s as a values where [0] = day(UNIX), [1] = price of bitcoin


def priceData(json):
    prices = json['prices']
    days = daysBetween([UnixToDate(timestampConverter(
        prices[0][0])), UnixToDate(timestampConverter(prices[-1][0]))])
    if days < 90:
        pricesAtMidnight = prices[::24]
        return pricesAtMidnight
    return(prices)


def tradingData(json):
    volumes = json['total_volumes']
    days = daysBetween([UnixToDate(timestampConverter(
        volumes[0][0])), UnixToDate(timestampConverter(volumes[-1][0]))])
    if days < 90:
        volumesAtMidnight = volumes[::24]
        return volumesAtMidnight
    return(volumes)


def highestVolume(tradingData):
    highest = 0
    day = ''
    for data in tradingData:
        if data[1] > highest:
            highest = data[1]
            day = data[0]
    return day, highest
        

