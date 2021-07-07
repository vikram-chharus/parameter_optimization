from os import stat
import json
import requests, pandas as pd
import input as input_data, xlwings as xw
import matplotlib.pyplot as plt
import constants

class optimization:
    
    def __init__(self):
        self.responses = list()
        self.result = {}
        self.parameters = {}
        
    def validateParameters(self, parameters):
        for key in parameters.keys():
            if parameters[key] != constants.constant:
                self.parameters[key] = parameters[key]
    
    def send_request(self, parameters):
        self.validateParameters(parameters)
        min = self.parameters["window_range_min"] if "window_range_min" in self.parameters.keys() else self.parameters["entry_range_min"] if "entry_range_min" in self.parameters.keys() else self.parameters["exit_range_min"] if "exit_range_min" in self.parameters.keys() else None
        max = self.parameters["window_range_max"] if "window_range_max" in self.parameters.keys() else self.parameters["entry_range_max"] if "entry_range_max" in self.parameters.keys() else self.parameters["exit_range_max"] if "exit_range_max" in self.parameters.keys() else None
        for period in range(min, max):
            response = requests.request(method="POST", url="http://localhost:3000/public/v1/backtest/run",json=input_data.set_input("AXISBANK", "rsi", self.parameters))
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
            self.result["responses"]= pd.DataFrame(self.responses).to_dict()
            self.result["parameters"]= parameters
            return self.result
        else:
            return False

    def modify_data(self):
        return self.responses[(self.responses["percentage_profit"]>= self.parameters["return_min"])&(self.responses["max_loss"]<self.parameters["loss_max"])&(self.responses["sharpe_ratio"] <= self.parameters["sharpe_ratio_max"]) & (self.responses["sharpe_ratio"] >= self.parameters["sharpe_ratio_min"])]


obj = optimization()
input_format = {
"indicator": "rsi",
"window_range_min": constants.constant,
"window_range_max": constants.constant,
"entry_range_min": constants.constant,
"entry_range_max": constants.constant,
"exit_range_min": 60,
"exit_range_max": 65,
"return_min": 1,
"sharpe_ratio_min": -2,
"sharpe_ratio_max": 1,
"loss_max": 2
}

print(obj.send_request(input_format))
# print(obj.modify_data())