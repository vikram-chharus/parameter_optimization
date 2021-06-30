from os import stat
from pandas.core import indexing
import requests, pandas as pd
import input as input_data, xlwings as xw
import matplotlib.pyplot as plt

wb = xw.Book("D:\\Parameter Optimization_Planning Sheet.xlsx")
sheet = wb.sheets[0]

#Variables
max_return= None
backtest_data = None
total_rows = 0
plot_data = None
#backtesing and storing data
def send_request():
    global max_return, backtest_data, total_rows
    backtest_data = list()
    
    for count, period in enumerate(range(min, max)):
        try:
            response = requests.request(method="POST", json=input_data.set_input("AXISBANK", "rsi", period), url="http://localhost:3000/public/v1/backtest/run")
            data = response.json()[0]
            
            sheet.range("A"+str(count+14)).value = period
            sheet.range("B"+str(count+14)).value = data["percentage_profit"]
            sheet.range("C"+str(count+14)).value = data["maximum_drawdown"]
            sheet.range("D"+str(count+14)).value = data["sharpe_ratio"]
            
            ext_data = {
                "Period":period, 
                "percentage_profit":data["percentage_profit"], 
                "maximum_drawdown":data["maximum_drawdown"],
                "sharpe_ratio":data["sharpe_ratio"]
            }
            backtest_data.append(ext_data)
            
            if max_return is None:
                max_return = data["percentage_profit"]
                sheet.range("F7").value = max_return
                sheet.range("F8").value = period
            elif max_return < data["percentage_profit"]:
                max_return = data["percentage_profit"]
                sheet.range("F7").value = max_return
                sheet.range("F8").value = period
            
            total_rows += 1
        
        except Exception as e:
            print(e)
            if e == 'percentage_profit':
                return 

def status(status):
    sheet.range("D10").value = status


def get_Data():
    global backtest_data, min, max
    min = int(sheet.range("C3").value)
    max = int(sheet.range("D3").value)+1
    send_request()
    sheet.range("E11").value = "SELECT"

def on_ready():
    global plot_data, backtest_data
    if sheet.range("C3").value == None or sheet.range("D3").value == None:
        return False
    else:
        status("Running")
        get_Data()
        plot_data = pd.DataFrame(backtest_data)
        return True


def modify_data():
    global backtest_data, plot_data
    if backtest_data is None:
        return False
    ret_min = int(sheet.range("I2").value)
    ret_max = int(sheet.range("H2").value)+1
    backtest_data = pd.DataFrame(backtest_data)
    data = backtest_data[(backtest_data["percentage_profit"] >= ret_min )&( backtest_data["percentage_profit"] <= ret_max)]
    sheet.range("A14:D"+str(14+len(data))).value = data.to_numpy()
    plot_data = data
    return True

def on_modify():
    if sheet.range("H2").value == None or sheet.range("I2").value == None:
        return False
    else:
        status("Running")
        if not modify_data():
            status("Please run backtest before modifiaction")
            return False
        else:
            return True

def erase():
    sheet.range("A14:D"+str(14+total_rows)).value = [["" for x in range(4)] for x in range(total_rows)]

def plot():
    if plot_data is not None:
        plt.plot(plot_data)

def on_status_change():
    global total_rows
    if sheet.range("E11").value == "READY":
        if total_rows != 0:
            erase()
        if not on_ready():
            sheet.range("E11").value = "SELECT"
            status("Select a valid range in C3 and D3")
            return False
        else:
            return True
    elif sheet.range("E11").value == "MODIFY":
        if total_rows != 0:
            erase()
        if not on_modify():
            sheet.range("E11").value = "SELECT"
            status("Select a valid range in H2 and I2")
            return False
        else:
            return True

sheet.range("E11").value = "SELECT"
sheet.range("D10").value = "STATUS"

while True:
    if on_status_change():
        sheet.range("E11").value = "SELECT"
        sheet.range("D10").value = "Success"
        plot()