from os import stat
from pandas.core import indexing
import requests, pandas as pd
import input as input_data, xlwings as xw
import matplotlib.pyplot as plt

class optimization:
    
    def __init__(self):
        self.responses = list()
        self.parameters = None
        pass
        
    def send_request(self, parameters):
        self.parameters = parameters
        for period in range(parameters["window_range_min"], parameters["window_range_max"]+1):
            response = requests.request(method="POST", url="http://localhost:3000/public/v1/backtest/run",json=input_data.set_input("AXISBANK", parameters["indicator"], period))
            data = response.json()[0]
            ext_data = {
                "period":period, 
                "percentage_profit":data["percentage_profit"], 
                "maximum_drawdown":data["maximum_drawdown"],
                "sharpe_ratio":data["sharpe_ratio"],
                "max_loss":data["loss_trades"]["max_loss"]
            }
            self.responses.append(ext_data)
        
        if len(self.responses) > 0:
            self.responses= pd.DataFrame(self.responses)
            return self.responses
        else:
            return False

    def modify_data(self):
        return self.responses[(self.responses["percentage_profit"]>= self.parameters["return_min"])&(self.responses["max_loss"]<self.parameters["loss_max"])&(self.responses["sharpe_ratio"] <= self.parameters["sharpe_ratio_max"]) & (self.responses["sharpe_ratio"] >= self.parameters["sharpe_ratio_min"])]


obj = optimization()
input_ = {
"indicator": "rsi",
"window_range_min": 14,
"window_range_max": 18,
"entry_range_min": 20,
"entry_range_max": 40,
"exit_range_min": 60,
"exit_range_min": 80,
"return_min": 1,
"sharpe_ratio_min": -2,
"sharpe_ratio_max": 1,
"loss_max": 2
}

print(obj.send_request(input_))
print(obj.modify_data())