from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import mysql.connector
import time


def lambda_handler(event= {"url":"https://www.google.com/"}, context=None):

	# chrome_options = Options()
	# chrome_options.add_argument('--headless')
	# driver = webdriver.Chrome(chrome_options=chrome_options)

	# TODO implement

	mydb = mysql.connector.connect(
	host="remotemysql.com",
	user="3QzXxevchm",
	passwd="Vae2yNz3rm",
	database="3QzXxevchm"
	)
	mycursor = mydb.cursor()
	print(mydb)



	urls = ["https://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(A%E2%80%93C)",
	"https://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(D%E2%80%93F)",
	"https://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(G%E2%80%93I)",
	"https://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(J%E2%80%93L)",
	"https://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(M%E2ll%80%93O)",
	"https://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(P%E2%80%93R)",
	"https://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(S%E2%80%93U)",
	"https://en.wikipedia.org/wiki/List_of_FIPS_region_codes_(V%E2%80%93Z)"]

	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--window-size=1280x1696')
	chrome_options.add_argument('--user-data-dir=/tmp/user-data')
	chrome_options.add_argument('--hide-scrollbars')
	chrome_options.add_argument('--enable-logging')
	chrome_options.add_argument('--log-level=0')
	chrome_options.add_argument('--v=99')
	chrome_options.add_argument('--single-process')
	chrome_options.add_argument('--data-path=/tmp/data-path')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--homedir=/tmp')
	chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
	chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
	# chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
	driver = webdriver.Chrome(chrome_options=chrome_options)

	for index,url in enumerate(urls):
		mydb = mysql.connector.connect(
		host="remotemysql.com",
		user="3QzXxevchm",
		passwd="Vae2yNz3rm",
		database="3QzXxevchm"
		)
		driver.get(url);
		test = driver.find_elements_by_tag_name("li")
		custom_list = []
		country_names_codes = []
		flag = False
		flag2 = True
		for i,t in enumerate(test):
			if flag==True:
				if "List of FIPS region codes" in t.text:
					break
				custom_list.append(t.text)
			if t.text.split(" ")[-1] == "References":
				flag = True
			if flag==False:
				if "See also" in t.text:
					flag2 = False
				if flag2:
					country_names_codes.append(t.text)
			
		location_current_name = []
		country = []
		location_within_country = []
		FIPS = []
		i1 = -1
		current_code = ""
		for elem in custom_list:
			area_code = elem[:2]
			if area_code!=current_code:
				i1+=1
				current_code = country_names_codes[i1].split(" ")[1][:-1]
				#Appending Country
				location_name =  country_names_codes[i1].split(" ")[-1]
				fips = current_code 
				location_current_name.append(location_name)
				country.append("Yes")
				location_within_country.append("No")
				FIPS.append(fips)

			#Appending Corresponding area
			location_name = elem.split(":")[1][1:]
			fips = elem.split(":")[0]
			location_current_name.append(location_name)
			country.append("No")
			location_within_country.append("Yes")
			FIPS.append(fips)

		counter = 0
		for a,b,c,d in zip(location_current_name,country,location_within_country,FIPS):
			mycursor = mydb.cursor()
			val = d
			sql = "SELECT * FROM  fips WHERE fc = " "'"+(str(val))+ "'"
			print(sql)
			mycursor.execute(sql)

			myresult = mycursor.fetchall()
			if myresult[0][0]!=a:
				mycursor = mydb.cursor()
				sql = "UPDATE fips SET hn = 'Yes' WHERE fc = " "'"+(str(val))+ "'"
				mycursor.execute(sql)
				mydb.commit()

				mycursor = mydb.cursor()
				sql = "UPDATE fips SET lc = " "'"+(str(a))+ "'" +" WHERE fc = " "'"+(str(val))+ "'"
				mycursor.execute(sql)
				mydb.commit()
				print("inside")

				if counter%30==0:
					print("Execution Progress")
					print(index,counter)
			counter+=1  



	driver.close()
	return "Execution Finished without problems"

lambda_handler()
