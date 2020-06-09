import time
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json
import os, sys
import pymongo #yDGTNy2WK52Bqsm


client = pymongo.MongoClient("mongodb+srv://lol:yDGTNy2WK52Bqsm@cluster0-gijx9.mongodb.net/bcdata?retryWrites=true&w=majority")
#db = client.test

db = client["bcdata"]

dlong = db["60d"]
dshort = db["kd"]


def scraper():
	
	names = [
		"BTC-EUR",
		"ETH-EUR",
		"XRP-EUR",
		"USDT-EUR",
		"BCH-EUR",
		"LTC-EUR",
		"BNB-EUR",
		"EOS-EUR",
		"XLM-EUR",
		"TRX-EUR",
		"ADA-EUR",
		"LINK-EUR",
		"XMR-EUR",
		"DASH-EUR",
		"ETC-EUR",
		"NEO-EUR",
		"XEM-EUR",
		"BAT-EUR",
		"DOGE-EUR",
		"ZEC-EUR",
		"ZRX-EUR",
		"GBYTE-EUR",
		"BNB-EUR",
		"GNO-EUR",
		"VERI-EUR",
		"DCR-EUR",
		"DGD-EUR",
		"REP-EUR",
		"BTG-EUR",
		"XZC-EUR",
		"ZEN-EUR",
		"MCO-EUR",
		"MLN-EUR",
		"FCT-EUR",
		"QTUM-EUR",
		"XUC-EUR",
		"BLOCK-EUR",
		"MONA-EUR",
		"PART-EUR",
		"BTC-USD",
		"ETH-USD",
		"XRP-USD",
		"USDT-USD",
		"BCH-USD",
		"LTC-USD",
		"BNB-USD",
		"EOS-USD",
		"XLM-USD",
		"TRX-USD",
		"ADA-USD",
		"LINK-USD",
		"XMR-USD",
		"DASH-USD",
		"ETC-USD",
		"NEO-USD",
		"XEM-USD",
		"BAT-USD",
		"DOGE-USD",
		"ZEC-USD",
		"ZRX-USD",
		"GBYTE-USD",
		"BNB-USD",
		"GNO-USD",
		"VERI-USD",
		"DCR-USD",
		"DGD-USD",
		"REP-USD",
		"BTG-USD",
		"XZC-USD",
		"ZEN-USD",
		"MCO-USD",
		"MLN-USD",
		"FCT-USD",
		"QTUM-USD",
		"XUC-USD",
		"BLOCK-USD",
		"MONA-USD",
		"PART-USD",

		#FONDS
		"^DJI",
		"^CMC200",
		"^GDAXI",
		"^FTSE",
		"^FCHI",
		"^NYA",
		"^SPX",
		"^GSPC",
		"^IXIC",

		#ROHSTOFFE
		"GC=F",
		"SI=F",
		"HG=F",
		"CL=F",
		"NG=F",
		"C=F",
		"S=F",
		"KC=F",
		"LB=F",
		"OJ=F",

		] #
	
	for name in names:
		print(name)
	
		startdate = datetime.datetime.now().date() - datetime.timedelta(days=5)
		
		today = datetime.datetime.now().date()
		
		
		mon_start = startdate - datetime.timedelta(days=90)
		week_end = startdate + datetime.timedelta(days=5)

		data_month = yf.download(name,start=mon_start,end=startdate,interval="60m")
		data_week = yf.download(name,start=startdate,end=week_end,interval="5m")

		values = data_month.Close.to_numpy().tolist()		
		y_data_arr = data_week.Close.to_numpy().tolist()

		t_array = [x * 5 for x in range(len(y_data_arr))]

		trend = np.polyfit(t_array,y_data_arr,1)
		trendpoly = np.poly1d(trend)

		d = trendpoly(0)
		k = trendpoly(1)-d

		scrape_id = name+"@"+startdate.strftime('%m_%d_%Y')

		sdate = datetime.datetime.combine(startdate, datetime.datetime.min.time())

		dlong.insert_one({"scrape_id":scrape_id,"coin":name,"date":sdate,"values":values})

		dshort.insert_one({"scrape_id":scrape_id,"coin":name,"date":sdate,"values":{"k":k,"d":d}})

		plt.plot(t_array,trendpoly(t_array))

		
		




#schedule.every().day.at("12:00").do(scraper)

if __name__ == '__main__':
	print("ran scrape")
	scraper()

	#while True:
		#schedule.run_pending()
		#time.sleep(1)