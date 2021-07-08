from numpy import result_type
from pandas.core import indexing
import requests, pandas as pd
import input as input_data, xlwings as xw
import matplotlib.pyplot as plt
import constants
import parameter_optimizarion_api as api
wb = xw.Book("D:\\Parameter Optimization_Planning Sheet.xlsx")
sheet = wb.sheets[0]

#Variables
max_return= None
backtest_data = None
total_rows = 0
plot_data = None
server = None



def createAPIinput(modify=False):
    if not modify:
        return {
            "indicator": "rsi",
            "window_range_min": int(sheet.range("C3").value) if sheet.range("B3").value == "Window" else constants.constant,
            "window_range_max": int(sheet.range("D3").value) if sheet.range("B3").value == "Window" else constants.constant,
            "entry_range_min": int(sheet.range("C3").value) if sheet.range("B3").value == "Entry" else constants.constant,
            "entry_range_max": int(sheet.range("D3").value) if sheet.range("B3").value == "Entry" else constants.constant,
            "exit_range_min": int(sheet.range("C3").value) if sheet.range("B3").value == "Exit" else constants.constant,
            "exit_range_max": int(sheet.range("D3").value) if sheet.range("B3").value == "Exit" else constants.constant,
        }
    elif modify:
        return {
            "min_return": float(sheet.range("H2").value) if sheet.range("H2").value != None else constants.constant,
            "max_loss": float(sheet.range("H3").value) if sheet.range("H3").value != None else constants.constant,
            "sharpe_ratio_min": float(sheet.range("H4").value) if sheet.range("H4").value != None else constants.constant,
            "sharpe_ratio_max": float(sheet.range("I4").value) if sheet.range("I4").value != None else constants.constant
        }
    else:
        return None


#backtesing and storing data
def send_request():
    global server
    if server is not None:
        del server
    server = api.optimization()
    response = server.send_request(createAPIinput(modify= False))   
    if response  is not None:
        data = pd.DataFrame(response["data"])
        row = data[data["maximum_drawdown"] == data["maximum_drawdown"].max()].round(2)
        sheet.range("G5").value = row.iloc[0,3]
        sheet.range("G7").value = row.iloc[0,3]
        sheet.range("G8").value = row.iloc[0,0]
        sheet.range("A7:E"+str(9+len(response["data"]))).value = data.round(2).to_numpy()

def status(status):
    sheet.range("C4").value = status

def on_ready():
    global plot_data, backtest_data
    if (sheet.range("C3").value == None or sheet.range("D3").value == None):
        return False
    else:
        erase()
        status("Running")
        send_request()
        plot_data = pd.DataFrame(backtest_data)
        return True


def modify_data():
    responses = server.modify_data(createAPIinput(modify= True))
    if responses is not None:
        erase()
        row = responses[responses["maximum_drawdown"] == responses["maximum_drawdown"].max()].round(2)
        sheet.range("G7").value = row.iloc[0,3]
        sheet.range("G8").value = row.iloc[0,0]
        sheet.range("A7:E"+str(9+len(responses))).value = responses.round(2).to_numpy()
    else:
        status("Something went wrong")

def on_modify():
    if not (sheet.range("H2").value != None or sheet.range("H3").value != None or (sheet.range("H4").value != None and sheet.range("I4").value != None)):
        return False
    else:
        status("Running")
        modify_data()
        return True

def erase():
    sheet.range("A7:E"+str(7+wb.sheets[0].range('E' + str(wb.sheets[0].cells.last_cell.row)).end('up').row)).value = [["" for x in range(5)] for x in range(wb.sheets[0].range('E' + str(wb.sheets[0].cells.last_cell.row)).end('up').row)]

def plot():
    if plot_data is not None:
        try:
            plot_data.plot(x= "Period", y= ["percentage_profit", "sharpe_ratio"], kind="bar")
            plt.show()
        except:
            pass

def on_status_change():
    global total_rows
    if sheet.range("D5").value == "READY":
        if not on_ready():
            sheet.range("D5").value = "SELECT"
            status("Select a valid range in C3 and D3")
            return False
        else:
            return True
    elif sheet.range("D5").value == "MODIFY":
        if not on_modify():
            sheet.range("D5").value = "SELECT"
            status("Select a valid range in H2 and I2")
            return False
        else:
            return True

sheet.range("D5").value = "SELECT"
sheet.range("C4").value = "STATUS"
sheet.range("C3").value = ""
sheet.range("D3").value = ""
sheet.range("H2").value = ""
sheet.range("I2").value = ""
sheet.range("G7").value = ""
sheet.range("G8").value = ""
while True:
    if on_status_change():
        sheet.range("D5").value = "SELECT"
        sheet.range("C4").value = "Success"
        plot()