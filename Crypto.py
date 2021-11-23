from RisingStar import *

# TO-DO: Add comments
class Crypto:
    # For now this is like this. Searching other cryptos than BTC, requires function to fetch right coin id from CG-API.
    coin_id = 'bitcoin'

    def __init__(self):
        self.start_date, self.end_date = get_dates()
        self.start_date_unix = get_date_as_unix(self.start_date)
        self.end_date_unix = get_date_as_unix(self.end_date, False)
        self.data = get_raw_data(self.start_date_unix, self.end_date_unix, self.coin_id)
        
    def update_range(self):
        self.start_date, self.end_date = get_dates()
        self.start_date_unix = get_date_as_unix(self.start_date)
        self.end_date_unix = get_date_as_unix(self.end_date, False)
        self.data = get_raw_data(self.start_date_unix, self.end_date_unix, self.coin_id)

    def top_volume_24h_(self):
        self.trading_data = trading_data(self.data)
        date = unix_to_date(highest_volume(self.trading_data)[0])
        top_volume = highest_volume(self.trading_data)[1]
        return f'Highest volume between selected days were on {date}. Volume were {top_volume} euros.'

    def longest_bear(self):
        self.price_data = price_data(self.data)
        return f'Longest bearish trend in {self.start_date} - {self.end_date} was {bear_trend(self.price_data)} days'

    def check_optimal_dates(self):
        self.price_data = price_data(self.data)
        self.optimal_dates = optimal_dates(self.price_data)

        if self.optimal_dates == []:
            return 'Price will only decrease on selected days. Dont buy!'

        self.buy_date = unix_to_date(self.optimal_dates[0][0])
        self.sell_date = unix_to_date(self.optimal_dates[1][0])
        return f'Best day to buy is {self.buy_date}. Best day to sell is {self.sell_date}.'


    
