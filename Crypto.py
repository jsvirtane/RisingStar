from RisingStar import *

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
        return highest_volume_output(highest_volume(self.trading_data))


    def longest_bear(self):
        self.price_data = price_data(self.data)
        return(f'Longest bearish trend in {self.start_date} - {self.end_date} was {bear_trend(self.price_data)} days')


    
