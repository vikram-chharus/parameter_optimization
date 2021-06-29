import os, requests
path = 'C:\\Users\\Vivikram\\OneDrive\\Git Hub\\API\\angle_broking_api\\python-core-api'
os.chdir(path)
url = "http://localhost:3000"
def run():
    os.system("python app.py")
    if requests.request(method='GET', url=url).status_code == 200:
        return True
    else:
        return False
run()