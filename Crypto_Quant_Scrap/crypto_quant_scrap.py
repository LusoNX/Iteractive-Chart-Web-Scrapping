from datetime import datetime
import numpy as np
from dateutil.relativedelta import relativedelta
import time
import requests
import sqlite3
from selenium import webdriver  
from bs4 import BeautifulSoup
import random
from scipy.stats import norm
from pandas.io.json import json_normalize
import requests
import urllib
from sqlalchemy import create_engine
import pyodbc
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4_to_xpath import xpath_soup
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random




def get_ratio_information_prev(_url,_offest_value,_login,_indicator_name,data_part):
	PATH = r"C:\Users\35196\OneDrive\Desktop\Financial Tools- Tools\Trading Strategies\Price_Prediction_AI\CryptoQuant\chromedrive.exe"
	options = webdriver.ChromeOptions()
	options.add_experimental_option("detach", True)
	driver =webdriver.Chrome(options = options,executable_path =PATH)
	driver.get(_url)
	#driver.get("https://cryptoquant.com/asset/btc/chart/market-indicator/estimated-leverage-ratio?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=linear&metricScale=linear&chartStyle=line")
	driver.maximize_window()

	time.sleep(6)

	click_ads = driver.find_element_by_xpath("//*[@id='__next']/div/div/div/div[2]/button").click()

	
	if _login == True:

		test_drive = driver.page_source
		soup_test = BeautifulSoup(test_drive,"lxml")
		test_v =soup_test.find_all("button")
		login_q = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/button[1]").click()
		time.sleep(5)
		input_email = driver.find_element_by_id("email")
		input_email.send_keys("luanfpires@gmail.com")
		time.sleep(2)
		input_pw = driver.find_element_by_id("password")
		input_pw.send_keys("petrabrasil2010")
		time.sleep(2)
		login_p = driver.find_element_by_xpath("//*[@id='__next']/div/main/div/form/div[4]/div/div/div/button").click()
		time.sleep(4)
	else:
		pass



	#chart = driver.find_element_by_xpath("//*[@id='__next']/div/main/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div")
	new_source = driver.page_source
	soup = BeautifulSoup(new_source,"lxml")
	results = soup.find_all("div",{"class":"highcharts-container"})
	id_chart = results[0]['id']
	time.sleep(5)
	chart = driver.find_element_by_xpath("//*[@id='{}']".format(id_chart))

	
	#new_source = driver.page_source
	#soup = BeautifulSoup(new_source,"lxml")
	#results = soup.find_all("div",{"class":"highcharts-container"})

	date_values = []
	exchange_whale_ratio_values = []
	action = ActionChains(driver)

	
	action.move_to_element(chart)
	action.move_by_offset(0,0)
	action.click_and_hold(on_element =chart)
	action.move_by_offset(_offest_value,0)
			#action.click_and_hold(on_element =chart)
	action.click()
	action.perform()

	range_values = 445*2
	for i in range(0,range_values):# 445 for the (0,0) POS
		try:
			x = -445+i
			action.move_to_element(chart)
			action.move_by_offset(x, 0)
			action.perform()
			time.sleep(random.randint(1,3))
			new_source = driver.page_source
			soup = BeautifulSoup(new_source,"lxml")
			time.sleep(1)


				
			for i in soup:
				results_2 = i.find_all("div",{"class":"highcharts-label highcharts-tooltip highcharts-color-undefined"})
				values = results_2[0].find_all("b")
				values_2 = results_2[0].find_all("span")
					#values_3 = values_2[0].find_all("/b")

				data_v = []

				date = values[0]
				price = values[1]

				date = str(date).replace("<b>","")
				date = date.replace("</b>","")


				for i in values_2[0]:
					x = str(i)
					data_v.append(x)

				date_values.append(date)
				exchange_whale_ratio = data_v[-1].replace(":","")
				exchange_whale_ratio = exchange_whale_ratio.replace(" ","")
				exchange_whale_ratio_values.append(exchange_whale_ratio)
		except:

			print("Iteration Failed for values {}".format(_indicator_name))
			pass
	data_tuples = list(zip(date_values,exchange_whale_ratio_values))

	df = pd.DataFrame(data_tuples, columns = ["Date",_indicator_name])

	if data_part == 0:
		df.to_csv("data_{}_0.csv".format(_indicator_name))
	else:
		df.to_csv("data_{}_1.csv".format(_indicator_name))
	driver.quit()

	return df



def transform_data(DF_1,DF_2):
	df_1 = DF_1.copy()
	df_2 = DF_2.copy()
	df_1["Date"] = df_1["Date"].str.replace("'","20")
	df_1 = df_1.drop(df_1.columns[[0]],axis =1)
	df_1.set_index("Date",inplace = True)
	df_2["Date"] = df_2["Date"].str.replace("'","20")
	df_2 = df_2.drop(df_2.columns[[0]],axis =1)
	df_2.set_index("Date",inplace = True)
	df_final = pd.concat([df_1,df_2],axis = 0)
	name_final = df_final.columns.values[0]
	#df_final[name_final] = df_final[name_final].astype(float)
	df_final = df_final[~df_final.index.duplicated(keep='first')]
	df["Date"] = pd.to_datetime(df["Date"])
	df =df.sort_values(by = ["Date"])
	df_final.to_csv("df_final_{}.csv".format(name_final))
	return df_final

##
#df_1 = pd.read_csv("data_long-liquidations-usd_0.csv")
#df_2 = pd.read_csv("data_long-liquidations-usd_1.csv")
df = pd.read_csv("df_final_exchange-whale-ratio.csv")



def sort_values(df,name):
	df["Date"] = pd.to_datetime(df["Date"])
	df =df.sort_values(by = ["Date"])
	df.set_index("Date",inplace = True)

	print(df.head())

	#print(pd.date_range(start="2019-03-13", end="2022-02-27").difference(df.index))
	df_whale_index = df.reindex(pd.date_range('2019-03-30', '2022-02-27')).isnull().all(1)
	df_whale_index.to_csv("estimated_leverage_ratio.csv")
	#print(pd.date_range(start="13-03-19", end="2022-02-27").difference(df_2["Date"]))
	#print(pd.date_range(start="13-03-19", end="2022-02-27").difference(df_3["Date"]))


sort_values(df,"test")





def main():

	url_1 = "https://cryptoquant.com/asset/btc/chart/flow-indicator/exchange-whale-ratio"
	url_2 = "https://cryptoquant.com/asset/btc/chart/market-indicator/estimated-leverage-ratio?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=linear&metricScale=linear&chartStyle=line"
	url_3 = "https://cryptoquant.com/asset/btc/chart/derivatives/open-interest?exchange=all_exchange&symbol=all_symbol&window=DAY&sma=0&ema=0&priceScale=linear&metricScale=linear&chartStyle=line"
	url_4 = "https://cryptoquant.com/asset/btc/chart/derivatives/long-liquidations-usd?exchange=all_exchange&symbol=all_symbol&window=DAY&sma=0&ema=0&priceScale=linear&metricScale=linear&chartStyle=column"
	url_5 = "https://cryptoquant.com/asset/btc/chart/derivatives/short-liquidations-usd?exchange=all_exchange&symbol=all_symbol&window=DAY&sma=0&ema=0&priceScale=linear&metricScale=linear&chartStyle=column"
	


	list_names = ["short-liquidations-usd"]
	#url_list = [url_4,url_5] ## ADD uRl 3 open-interest
	url_list = [url_5]
	for i,x in zip(url_list,list_names):
		if x == "exchange-whale-ratio":
			df_1 =get_ratio_information_prev(i,-445,False,x,0)
			df_2 =get_ratio_information_prev(i,445,False,x,1)
			df_final = transform_data(df_1,df_2)
		else:
			df_1 =get_ratio_information_prev(i,-445,True,x,0)
			df_2 =get_ratio_information_prev(i,445,True,x,1)
			df_final = transform_data(df_1,df_2)

main()




