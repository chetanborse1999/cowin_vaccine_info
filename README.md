# Cowin Vaccine Info
Using API to get session info and login using Selenium. Tasker (Android app for automating tasks) is required to fetch OTP.

## Steps:

1. Enter your Phone number, block name, age, and minimum available stock in the code.
2. Get your district id from https://github.com/bhattbhavesh91/cowin-vaccination-slot-availability/blob/main/district_mapping.csv. Also uncomment line 78,80,91 to get list of available block names in the chosen District. Choose Block and enter it in the parameters at the beginning.
3. Can sort by other parameters based on GET request response. Response format available at API Setu.
4. Install Tasker > Create Profile > Event > Received Text > Type: SMS; Sender: "VD-NHPSMS" (or whichever name you get OTP from) > Task1 > Wait 3seconds > Task2 > HTTP Get > Server:Port = "http://192.168.xx.xxx:port" (PC IP address, as mentioned in the code, change accordingly) ; Path:"%SMSRB" > Link Profile and Task > Enable Tasker.
5. Install chromedriver, if not done already and mention path in the code.

If all goes well (:/), then, it will check every 5 seconds for any available slots based on your parameters. And when it gets a valid session, it will quickly login and take you to the Registered Users screen, without you requiring to touch your phone. Here onwards you have to manually book the appointment because you need to select user, and session and CAPTCHA.

## Note:
#### 1. As of now (June 2021), the supply is a lot more than demand therefore the sessions get completely booked in fraction of seconds. The API returns availability data that is cached and may be upto 5 minutes old. The session gets completely booked before the API can return updated data. So not that great at rapid booking. But still works alright for second dose for all ages as well as first dose for 45+.
#### 2. If Tasker setup does not work, just comment out the functions related to OTP and should work still.
