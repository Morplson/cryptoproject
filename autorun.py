import time
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime
import random
import json
import os, sys
from operator import add
import pymongo #yDGTNy2WK52Bqsm


client = pymongo.MongoClient("mongodb+srv://lol:yDGTNy2WK52Bqsm@cluster0-gijx9.mongodb.net/bcdata?retryWrites=true&w=majority")
#db = client.test

db = client["bcdata"]

dlong = db["60d"]
dshort = db["kd"]
dsupershort = db["kd1d"]


def scraper():
	
	crypto = [
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
		"PART-USD"

		#FONDS
		#"^DJI",
		#"^CMC200",
		#"^GDAXI",
		#"^FTSE",
		#"^FCHI",
		#"^NYA",
		#"^SPX",
		#"^GSPC",
		#"^IXIC",

		#ROHSTOFFE
		#"GC=F",
		#"SI=F",
		#"HG=F",
		#"CL=F",
		#"NG=F",
		#"C=F",
		#"S=F",
		#"KC=F",
		#"LB=F",
		#"OJ=F",

		] #
	
	composits_crypto = [
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
		"PART-USD"
		] 
	
	for i in range(len(crypto)+len(composits_crypto)):

		charts = []
		
		if i < len(crypto):
			charts = getCryptoChart(crypto[i])
		else:
			charts = getCompositChart(composits_crypto, i-len(crypto))

		for chart in charts:
			print(chart["coin"])

			month_data_arr = chart["values_60d"]
			week_data_arr = chart["values_5d"]
			day_data_arr = chart["values_1d"]
		
			week_array = [x * 5 for x in range(len(week_data_arr))]
			day_array = [x for x in range(len(day_data_arr))]

			#WEEK
			week_trend = np.polyfit(week_array,week_data_arr,1)
			week_trendpoly = np.poly1d(week_trend)

			week_d = week_trendpoly(0)
			week_k = week_trendpoly(1)-week_d

			#DAY
			day_trend = np.polyfit(day_array,day_data_arr,1)
			day_trendpoly = np.poly1d(day_trend)

			day_d = day_trendpoly(0)
			day_k = day_trendpoly(1)-day_d


			_id = dlong.insert_one({"scrape_id":chart["scrape_id"],"coin":chart["coin"],"date":chart["date"],"values":month_data_arr, "version": 2.0})
			
			#insert_id = ObjectId(_id.inserted_id)

			dshort.insert_one({"60d_id":_id.inserted_id,"scrape_id":chart["scrape_id"],"coin":chart["coin"],"date":chart["date"],"values":{"k":week_k,"d":week_d}, "version": 2.0})

			dsupershort.insert_one({"60d_id":_id.inserted_id,"scrape_id":chart["scrape_id"],"coin":chart["coin"],"date":chart["date"],"values":{"k":day_k,"d":day_d}, "version": 2.0})

			#plt.plot(t_array,trendpoly(t_array))

		
		
def getCryptoChart(short_id):
	out = []

	startdate = datetime.datetime.now().date() - datetime.timedelta(days=5)
		
	today = datetime.datetime.now().date()
		
		
	mon_start = startdate - datetime.timedelta(days=90)
	week_end = startdate + datetime.timedelta(days=5)
	day_end = startdate + datetime.timedelta(days=1)

	data_month = yf.download(short_id,start=mon_start,end=startdate,interval="60m")
	data_week = yf.download(short_id,start=startdate,end=week_end,interval="5m")
	data_day = yf.download(short_id,start=startdate,end=week_end,interval="1m")

	data_arr_60d = data_month.Close.to_numpy().tolist()		
	data_arr_5d = data_week.Close.to_numpy().tolist()
	data_arr_1d = data_day.Close.to_numpy().tolist()


	scrape_id = short_id+"@"+startdate.strftime('%m_%d_%Y')

	sdate = datetime.datetime.combine(startdate, datetime.datetime.min.time())
	
	out.append({
		"scrape_id": scrape_id,
		"coin": short_id,
		"date": sdate,
		"values_60d": data_arr_60d,
		"values_5d": data_arr_5d,
		"values_1d": data_arr_1d
	})
	return out

def getCompositChart(short_ids, i, chart_num=4):
	out = []
	startdate = datetime.datetime.now().date() - datetime.timedelta(days=5)

	components = []
	component_1 = getCryptoChart(short_ids[i])[0]
	comp_name = "COMP:"+component_1["coin"]
	components.append(component_1)

	for x in range(1,chart_num):
		comp_temp = getCryptoChart(random.choice(short_ids))[0]
		comp_name += ";"+comp_temp["coin"]
		components.append(comp_temp)

	multipyer = 1
	max_mul = 1
	for h in range(3):
		coin_name = comp_name
		scrape_id = comp_name
		
		if h == 0:
			scrape_id += ":25"
			multipyer = 0.25
		elif h == 1:
			scrape_id += ":50"
			multipyer = 0.5
		elif h == 2:
			scrape_id += ":75"
			multipyer = 0.75
	
		data_60d_1 = [abs(x * multipyer) for x in components[0]["values_60d"]]
		data_5d_1 = [abs(x * multipyer) for x in components[0]["values_5d"]]
		data_1d_1 = [abs(x * multipyer) for x in components[0]["values_1d"]]
		max_mul -= multipyer
		multipyer = max_mul/2

		data_60d_2 = [abs(x * multipyer) for x in components[1]["values_60d"]]
		data_5d_2 = [abs(x * multipyer) for x in components[1]["values_5d"]]
		data_1d_2 = [abs(x * multipyer) for x in components[1]["values_1d"]]
		max_mul -= multipyer
		multipyer = max_mul/2

		data_60d_3 = [abs(x * multipyer) for x in components[2]["values_60d"]]
		data_5d_3 = [abs(x * multipyer) for x in components[2]["values_5d"]]
		data_1d_3 = [abs(x * multipyer) for x in components[2]["values_1d"]]

		data_60d_4 = [abs(x * multipyer) for x in components[3]["values_60d"]]
		data_5d_4 = [abs(x * multipyer) for x in components[3]["values_5d"]]
		data_1d_4 = [abs(x * multipyer) for x in components[3]["values_1d"]]

		data_arr_60d = [sum(x) for x in zip(data_60d_1, data_60d_2, data_60d_3, data_60d_4)]
		data_arr_5d = [sum(x) for x in zip(data_5d_1, data_5d_2, data_5d_3, data_5d_4)]
		data_arr_1d = [sum(x) for x in zip(data_1d_1, data_1d_2, data_1d_3, data_1d_4)]

		
		sdate = datetime.datetime.combine(startdate, datetime.datetime.min.time())
		scrape_id += "@"+startdate.strftime('%m_%d_%Y')

		out.append({
			"scrape_id": scrape_id,
			"coin": coin_name,
			"date": sdate,
			"values_60d": data_arr_60d,
			"values_5d": data_arr_5d,
			"values_1d": data_arr_1d
		})
	

	return out

#schedule.every().day.at("12:00").do(scraper)

if __name__ == '__main__':
	print("ran scrape")
	scraper()

	#while True:
		#schedule.run_pending()
		#time.sleep(1)