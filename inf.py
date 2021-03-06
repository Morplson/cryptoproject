import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os, sys
import pymongo #yDGTNy2WK52Bqsm


client = pymongo.MongoClient("mongodb+srv://lol:yDGTNy2WK52Bqsm@cluster0-gijx9.mongodb.net/bcdata?retryWrites=true&w=majority")


#db = client.test

db = client["test"]
dlong = db["60d"]
dshort = db["kd"]


os.chdir(os.path.dirname(os.path.abspath(__file__)))


names = ["BTC-USD","ETH-USD","XRP-USD","USDT-USD","BCH-USD","LTC-USD","BNB-USD","EOS-USD","XLM-USD","TRX-USD","ADA-USD","LINK-USD","XMR-USD","DASH-USD","ETC-USD","NEO-USD","XEM-USD","BAT-USD","DOGE-USD","ZEC-USD","ZRX-USD","GBYTE-USD","BNB-USD","GNO-USD","VERI-USD","DCR-USD","DGD-USD","REP-USD","BTG-USD","XZC-USD","ZEN-USD","MCO-USD","MLN-USD","FCT-USD","QTUM-USD","XUC-USD","BLOCK-USD","MONA-USD","PART-USD"] #
#sys.exit()

for name in names:
	print(name)

	startdate = datetime.datetime.now().date() - datetime.timedelta(days=5)
	
	dump_file = open("crypto_datadump"+str(datetime.datetime.now().date())+".json-plus", "a")
	
	
	for x in range(32):
		print(startdate)
	
		mon_start = startdate - datetime.timedelta(days=90)
		week_end = startdate + datetime.timedelta(days=5)
	
		data_month = yf.download(name,start=mon_start,end=startdate,interval="60m")
		data_week = yf.download(name,start=startdate,end=week_end,interval="5m")
	
		
		values = data_month.Close.to_numpy().tolist()
	
		print (len(values))
		
		y_data_arr = data_week.Close.to_numpy().tolist()
		t_array = [x * 5 for x in range(len(y_data_arr))]
	
		trend = np.polyfit(t_array,y_data_arr,1)
		trendpoly = np.poly1d(trend)
	
		d = trendpoly(0)
		k = trendpoly(1)-d
	
		#print("{ "+str(d)+"; "+str(k)+"};")
	
	
		
		scrape_id = name+"@"+startdate.strftime('%m_%d_%Y')

		sdate = datetime.datetime.combine(startdate, datetime.datetime.min.time())

		dlong.insert_one({"scrape_id":scrape_id,"coin":name,"date":sdate,"values":values})

		dshort.insert_one({"scrape_id":scrape_id,"coin":name,"date":sdate,"values":{"k":k,"d":d}})

	
		startdate = startdate - datetime.timedelta(days=1)

		plt.plot(t_array,trendpoly(t_array))

		plt.show()
	

