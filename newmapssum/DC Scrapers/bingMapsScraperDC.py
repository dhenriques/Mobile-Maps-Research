# import csv
import time
from selenium import webdriver
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig()
scheduler = BlockingScheduler()

db = pymysql.connect(host="ec2-52-14-113-176.us-east-2.compute.amazonaws.com",
                     user="Kean",
                     passwd="MobileMaps0718",
                     db="ScraperData",)

cursor = db.cursor()

url = 'https://binged.it/2B8Zawy'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path='..\chromedriver.exe',chrome_options=chrome_options)

def grabAndSave():
    ts = time.time()
    readable = time.ctime(ts)
    browser.get(url)
    time.sleep(5)
    
    # Selects Route 1 (unique) and retrieves route info
    nav = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[1]/a/table/tr/td[2]/div/table[1]/tr/td[1]/p[4]")
    data1 = (nav.text).splitlines()

    #Retrieves time data from Route 1
    time1 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li/a/table/tr/td[1]/div")
    timedata1 = (time1.text).splitlines()

    #Retrieves distance data from Route 1
    distance1 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[1]/a/table/tr/td[2]/div/table[1]/tr/td[2]")
    distancedata1 = (distance1.text).splitlines()
    
    #Prints out Route 1 results
    print("Route: " + data1[0] +" | Time: " + timedata1[0] + " | Distance: " + distancedata1[0])

    # Test if a Route 2 or Route 3 is available
    route2 = False;
    route3 = False;
    try:
        route2 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[2]/a/table/tr/td[1]/div/table")
    except:
        print("There is no route 2 this time!")
    try:
        route3 = browser.find_element_by_xpath(
            "//*[@id='directionsPanelRoot']/div[2]/ul/li[3]/a/table/tr/td[1]/div/table")
    except:
        print("There is no route 3 this time!")

    # If Route 2 is available, grab Route 2 data
    if (route2):
        # Gets route info from Route 2
        nav1 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[2]/a/table/tr/td[2]/div/table[1]/tr/td[1]/p[4]")
        data1 = (nav1.text).splitlines()

        #Retrieves time data from Route 2
        time2 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[2]/a/table/tr/td[1]/div/table")
        timedata2 = (time2.text).splitlines()

        #Retrieves distance data from Route 2
        distance2 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[2]/a/table/tr/td[2]/div/table[1]/tr/td[2]")
        distancedata2 = (distance2.text).splitlines()

        #Prints out Route 2 results
        print("Route: " + data1[0] +" | Time: " + timedata2[0] + " | Distance: " + distancedata2[0])



    if (route3):
        # Get route info from Route 3
        nav2 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[3]/a/table/tr/td[2]/div/table[1]/tr/td[1]/p[4]")
        data2 = (nav2.text).splitlines()
        #Retrieves time data from Route 3
        time3 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[3]/a/table/tr/td[1]/div/table")
        timedata3 = (time3.text).splitlines()
        #Retrieves distance data from Route 3
        distance3 = browser.find_element_by_xpath("//*[@id='directionsPanelRoot']/div[2]/ul/li[3]/a/table/tr/td[2]/div/table[1]/tr/td[2]")
        distancedata3 = (distance3.text).splitlines()
        #Prints out Route 3 results
        print("Route: " + data2[0] +" | Time: " + timedata3[0] + " | Distance: " + distancedata3[0])

    print(readable)
    writer.writerow({'Route Number': 1, 'ETA': timedata1[0] + " min", 'Distance': distancedata1[0], 'Route': data1[0], 'Time': readable})
    if (route2):
        writer.writerow({'Route Number': 2,'ETA': timedata2[0] + " min", 'Distance': distancedata2[0], 'Route': data1[0], 'Time': readable})
    if (route3):
        writer.writerow({'Route Number': 3,'ETA': timedata3[0] + " min", 'Distance': distancedata3[0], 'Route': data2[0], 'Time': readable})
    print ("Cycle completed\n\n")


    #upload to db
    sql = "INSERT INTO `BingMaps` (`routenum`, `eta`, `distance`, `route`, `time`) VALUES (%s, %s, %s, %s, %s)"

    routenum1 = 1
    eta1 = timedata1[0] + " min"
    routedistance1 = distancedata1[0]
    routeinfo1 = data1[0]
    currtime = readable

    if(route2):
        routenum2 = 2
        eta2 = timedata2[0] + " min"
        routedistance2 = distancedata2[0]
        routeinfo2 = data1[0]

    if(route3):
        routenum3 = 3
        eta3 = timedata3[0] + " min"
        routedistance3 = distancedata3[0]
        routeinfo3 = data2[0]

    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (routenum1, eta1, routedistance1, routeinfo1, currtime))
            db.commit()

            print("Route 1 data uploaded to database")
            if (route2):
                cursor.execute(sql, (routenum2, eta2, routedistance2, routeinfo2, currtime))
                db.commit()
                print("Route 2 data uploaded to database")

            if (route3):
                cursor.execute(sql, (routenum3, eta3, routedistance3, routeinfo3, currtime))
                db.commit()
                print("Route 3 data uploaded to database")

            print("All data uploaded to database")
    except Exception:
        print("Exception, there was an error uploading to the database")





with open('bingMapsDataCA.csv', 'w', newline='') as csvfile:
    fieldnames = ['Route Number', 'ETA', 'Distance', 'Route', 'Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    try:
        while True:
            ts = time.time()
            readable = time.ctime(ts)
            grabAndSave()
            time.sleep(5) # 298 second day, gives 2 seconds for the program to run
    except KeyboardInterrupt:
        print("\n\nStopped by KEYBOARD INTERRUMPTION\n\n")
        pass

browser.close()