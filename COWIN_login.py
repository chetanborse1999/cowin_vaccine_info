from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

driver = webdriver.Chrome("C:/Users/CHETAN/Downloads/chromedriver.exe")
driver.get("https://selfregistration.cowin.gov.in/")
time.sleep(1)

inputElement1 = driver.find_element_by_id("mat-input-0")
inputElement1.send_keys('1234567890')
time.sleep(1)

buttonotp = driver.find_element_by_xpath('//*[@id="main-content"]/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/ion-grid/form/ion-row/ion-col[2]/div/ion-button')
buttonotp.click()

x = ''
class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		global x
		self.send_response(200)
		x = self.path
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>LMAO</title></head>", "utf-8"))
		self.wfile.write(bytes("<body><p>The quick brown fox jumps over the lazy dog</p>", "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))
	
webServer = HTTPServer(("192.168.43.163", 8088), Handler)
webServer.handle_request()

x = x.replace("%20", " ")
index = x.find("CoWIN is")
OTP = x[index+9:index+15]
print(OTP)

inputElement2 = driver.find_element_by_id("mat-input-1")
inputElement2.send_keys(OTP)
time.sleep(1)

buttonsendotp = driver.find_element_by_xpath('//*[@id="main-content"]/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col/ion-grid/form/ion-row/ion-col[3]/div/ion-button')
buttonsendotp.click()

webServer.server_close()
