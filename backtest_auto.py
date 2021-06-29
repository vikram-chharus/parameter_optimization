import requests, pandas as pd
import input as input_data, xlwings as xw

#open excel file/ workbook 
wb = xw.Book("Files\\Parameter Optimization_Planning Sheet.xlsx")
sheet = wb.sheets[0]
#define the range 
start = 5
end = 45
max_return= None

#backtesing and storing data
def send_request():
    global max_return
    last_4_values = list()
    for count, period in enumerate(range(start, end)):
        try:
            #send a request to get backtest data
            response = requests.request(method="POST", json=input_data.set_input("AXISBANK", "rsi", period), url="http://localhost:3000/public/v1/backtest/run")
            data = response.json()[0]
            #store data into excel file
            sheet.range("A"+str(count+14)).value = period
            sheet.range("B"+str(count+14)).value = data["percentage_profit"]
            sheet.range("C"+str(count+14)).value = data["maximum_drawdown"]
            sheet.range("D"+str(count+14)).value = data["sharpe_ratio"]
            if max_return is None:
                max_return = data["percentage_profit"]
                sheet.range("G7").value = max_return
                sheet.range("G8").value = period
            elif max_return < data["percentage_profit"]:
                max_return = data["percentage_profit"]
                sheet.range("G7").value = max_return
                sheet.range("G8").value = period
        except Exception as e:
            print(e)
            if e == 'percentage_profit':
                return

def start_excel_testing():
    #check if we are ready to test
    global start, end
    print("Waiting for confirmation...")
    while sheet.range("E11").value != "Ready":
        continue
    print("Status: Running")
    start = int(sheet.range("D2").value)
    end = int(sheet.range("D3").value)
    sheet.range("E11").value= "Running"
    send_request()
    sheet.range("E11").value= "Completed"
    print("Status: Completed")

def start_python_testing():
    returns = list()
    for count, period in enumerate(range(start, end)):
        try:
            #send a request to get backtest data
            response = requests.request(method="POST", json=input_data.set_input("AXISBANK", "rsi", period), url="http://localhost:3000/public/v1/backtest/run")
            data = response.json()[0]
            returns.append({"Period":period, "% Return":data["percentage_profit"], "Maximum drawdown": data["maximum_drawdown"], "Sharpe ratio":data["sharpe_ratio"]})
        except Exception as e:
            print(e)
            if e == 'percentage_profit':
                return pd.DataFrame(returns)
    return pd.DataFrame(returns)

#Check if we want to check from excel or python
start_from_excel = sheet.range("E10").value

if start_from_excel:
    start_excel_testing()
else:
    input("Status: Press a Key to Continue..")
    print("Status: Running")
    data = start_python_testing()
    print(data)
    sheet.range("A14:B"+str(14+len(data))).value = data.to_numpy()
    print("Status: Completed")

