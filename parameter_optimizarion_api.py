from os import stat
import json, constants
import requests, pandas as pd
import input as input_data, xlwings as xw
import matplotlib.pyplot as plt
import constants

class optimization:
    
    def __init__(self):
        self.responses = list()
        self.parameters = {}
        
    def update_parameters(self, updated_parameters):
        self.parameters = updated_parameters
        
    def validateParameters(self, parameters):
        for key in parameters.keys():
            if parameters[key] != constants.constant:
                self.parameters[key] = parameters[key]
    
    def send_request(self, parameters):
        self.responses.clear()
        self.validateParameters(parameters)
        parameter = "window" if "window_range_min" in self.parameters.keys() else "entry" if "entry_range_min" in self.parameters.keys() else "exit" if "exit_range_min" in self.parameters.keys() else None
        min = int(self.parameters[parameter+"_range_min"])
        max = int(self.parameters[parameter+"_range_max"])
        for i in range(min, max):
            self.parameters[parameter] = i
            response = requests.request(method="POST", url="http://localhost:3000/public/v1/backtest/run",json=input_data.set_input("AXISBANK", "rsi", self.parameters))
            data = response.json()[0]
            ext_data = {
                parameter:i,
                "percentage_profit":data["percentage_profit"], 
                "sharpe_ratio":data["sharpe_ratio"],
                 "maximum_drawdown":data["maximum_drawdown"],
                "max_loss":data["loss_trades"]["max_loss"]
            }
            self.responses.append(ext_data)
        
        if len(self.responses) > 0:
            data = {"parameters":parameters, "data":self.responses}
            print(data)
            return data
        else:
            return False

    def modify_data(self, parameters):
        data = pd.DataFrame(self.responses)
        # if parameters["min_return"] != constants.constant:
        #     data = data[(data["percentage_profit"] >= parameters["min_return"])]
        # if parameters["max_loss"] != constants.constant:
        #     data = data[(data["max_loss"] >= parameters["max_loss"])]
        # if parameters["sharpe_ratio_min"] != constants.constant and parameters["sharpe_ratio_max"] != constants.constant:
        #     data = data[(data["sharpe_ratio"] > parameters["sharpe_ratio_min"]) & (data["sharpe_ratio"] < parameters["sharpe_ratio_max"])]
        filters= [key+parameters[key][1]+str(parameters[key][0])+" and " for key in parameters.keys() if parameters[key][0] != constants.constant]
        qur= "".join(filters).rsplit(" and ", 1)[0]    
        data = data.query(qur)
        print(data)
        return data