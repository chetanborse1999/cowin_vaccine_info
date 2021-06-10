import requests
import pickle
import datetime
from tkinter import *
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

PHONE = '1234567890' #enter registered mobile number
BLOCK_NAME = 'Nashik Corporation'
AGE = 18 	#for 18-44, 18; for 45+, 45 
MIN_AVAIL = 5 #min available stock for given dose1. To sort by dose2, change on line83 and 88: "available_capacity_dose1" to "available_capacity_dose2"

x = ''

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		global x
		self.send_response(200)
		x = self.path
		# self.send_header("Content-type", "text/html")
		# self.end_headers()
		# self.wfile.write(bytes("<html><head><title>LMAO</title></head>", "utf-8"))
		# self.wfile.write(bytes("<body><p>The quick brown fox jumps over the lazy dog</p>", "utf-8"))
		# self.wfile.write(bytes("</body></html>", "utf-8"))

def enterNo(driver):
	inputElement = driver.find_element_by_id("mat-input-0")
	inputElement.send_keys(PHONE)
	time.sleep(1)

	buttonotp = driver.find_element_by_xpath('//*[@id="main-content"]/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/ion-grid/form/ion-row/ion-col[2]/div/ion-button')
	buttonotp.click()

def launchChrome():
	driver = webdriver.Chrome("C:/Users/CHETAN/Downloads/chromedriver.exe")
	driver.get("https://selfregistration.cowin.gov.in/")
	time.sleep(1)
	return driver


def enterOTP(OTP, driver):
	inputElement2 = driver.find_element_by_id("mat-input-1")
	inputElement2.send_keys(OTP)
	time.sleep(1)

	buttonsendotp = driver.find_element_by_xpath('//*[@id="main-content"]/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col/ion-grid/form/ion-row/ion-col[3]/div/ion-button')
	buttonsendotp.click()

def getOTP():
	global x
	webServer = HTTPServer(("192.168.43.163", 8088), Handler)
	webServer.handle_request()
	x = x.replace("%20", " ")
	index = x.find("CoWIN is")
	OTP = x[index+9:index+15]
	return OTP

t = str(datetime.datetime.now())
parameter = {"district_id": 389, "date":"{}-{}-{}".format(t[8:10],t[5:7],t[0:4])}

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(parameter["district_id"], parameter["date"])

a = datetime.datetime.now()
while True:
	b = datetime.datetime.now()
	# print((b-a).seconds)
	if (b-a).seconds>5:    #call every '5' seconds.
		cowinfile = open("cowinpickle", "wb")
		response = requests.get(url)
		pickle.dump(response.json(), cowinfile)
		cowinfile.close()
		f = open("cowinpickle", "rb")
		x = pickle.load(f)
		session_set = set()
		# alsoset = set()
		for i in x["centers"]:
			# alsoset.add(i["block_name"])
			if i["block_name"]==BLOCK_NAME:
				for sess in i["sessions"]:
					if sess["min_age_limit"]==AGE and sess["available_capacity_dose1"]>MIN_AVAIL:
					# if sess["min_age_limit"]==18:
						# for j in i:
						# 	print("{}:{}\n".format(j, i[j]))
						# print(sess)
						session_set.add((sess["date"], i["pincode"], sess["available_capacity_dose1"]))
						# print("############\n")
		print("{}".format(b), session_set)
		# print("also", alsoset)
		if len(session_set)>0:
			driver = launchChrome()
			enterNo(driver)
			otp = getOTP()
			enterOTP(otp, driver)
			_ = input("Wait?")
			# messagebox.showinfo("Alert", "{}".format(session_set))   #uncomment to get an alert box
		
		a = datetime.datetime.now()
		f.close()

	else:
		continue