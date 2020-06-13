import yfinance as yf
from colorama import init 
from termcolor import colored 
import datetime
import math

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from models import WeekNet

from pycoingecko import CoinGeckoAPI
#cg = CoinGeckoAPI()

init() 
  
#bt = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=1000/24)
#print(bt)

### LOADER






### PREDICTER


model = WeekNet()
model.load_state_dict(torch.load("D:\\xampp\\htdocs\\node\\cryptoproject\\models\\2020-06-12_52979a40801072d329c0454fc80c92a5.pt"))


model.eval()




### AUSGABE
def reader():

    model.hidden = (
        torch.zeros(1, 1, model.hidden_layer_size),
        torch.zeros(1, 1, model.hidden_layer_size)
    )

    name = input("Crypto: ")+"-USD"

    startdate = datetime.datetime.now()
    mon_start = startdate - datetime.timedelta(days=90)
    data_month = yf.download(name,start=mon_start,end=startdate,interval="60m")
    values = data_month.Close.to_numpy().tolist()[-1000:]

    tensor = torch.FloatTensor(values)

    prediction = 0
    with torch.no_grad():
        prediction = model(tensor).item()

    print("\nKrusentwicklung 5d:")


    percent = math.copysign((abs(prediction)*5/values[-1])*100,prediction)
    
    if percent > 1:
        print(colored('WIN!', 'green')) 
        print(colored(f'{percent:10.2f}%', 'green'))
        

    elif percent < -1:
        print(colored('LOSS!', 'red') ) 
        print(colored(f'{percent:10.2f}%', 'red'))

    elif percent <= 1 and percent > 0.009:
        print(colored('SMALL WIN!', 'green')) 
        print(colored(f'{percent:10.3f}%', 'green'))

    elif percent >= -1 and percent < -0.009:
        print(colored('SMALL LOSS!', 'red') ) 
        print(colored(f'{percent:10.3f}%', 'red'))

    elif percent <= 0.009 and percent >= -0.009:
        print(colored('EQUALIBRIUM', 'cyan')) 
        print(colored(f'{percent:10.6f}%', 'cyan'))

    #Graph
    print(colored(f'Graph:', 'white'))
    print(colored(f'y= {prediction:10.4f}x +{values[-1]:10.4f}\n', 'white'))

if __name__ == "__main__":
    while True:
        try:
            reader()
        except:
            pass
            
    pass