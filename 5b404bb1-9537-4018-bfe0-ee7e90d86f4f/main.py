from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Option, ohlcv
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["GME"]
        self.rsi_period = 14  # Usually, a 14-day period is used for RSI calculation
        self.options = [Option(i, "call", "nearest", "OTM") for i in self.tickers] + \
                       [Option(i, "put", "nearest", "OTM") for i in self.tickers]
        # Consider nearest expiration and out-of-the-money options for simplicity

    @property
    def interval(self):
        return "1day"  # Daily intervals for computing RSI

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.options + [ohlcv(i) for i in self.tickers]

    def run(self, data):
        allocation_dict = {}
        gme_data = data["ohlcv"]["GME"]
        gme_rsi = RSI("GME", gme_data, self.rsi_period)
        
        if not gme_rsi:
            log("RSI data not available")
            return TargetAllocation({})

        current_rsi = gme_rsi[-1]

        if current_rsi < 30:
            # Indicative of an oversold condition, buy a call option
            allocation_dict["GME_call"] = 1
            log("Buying call option for GME")

        elif current_rsi > 70:
            # Indicative of an overbought condition, buy a put option
            allocation_dict["GME_put"] = 1
            log("Buying put option for GME")
            
        else:
            # No clear signal, do not hold any options
            allocation_dict["GME_call"] = 0
            allocation_strat["GME_put"] = 0
            log("No clear option signal for GME")

        return TargetAllocation(allocation_dict)