import csv
import time
from selenium import webdriver
import pymysql

db = pymysql.connect(host="ec2-18-216-116-132.us-east-2.compute.amazonaws.com",
                     user="Kean",
                     passwd="MobileMapsResearch0718!",
                     db="MapData_NY",)

cursor = db.cursor()

url = 'https://www.waze.com/livemap?from_lat=40.70162390000001&from_lon=-73.9896727&to_lat=40.6210946954629&to_lon=-74.16839003562929&at=now'
map_url = 'https://www.waze.com/livemap?%3Ffrom_lat=40.70162390000001&from_lon=-73.9896727&to_lat=40.6210946954629&to_lon=-74.16839003562929&at=now&lat=40.66241030513908&lng=-74.06845092773439&zoom=11'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

browser = webdriver.Chrome(executable_path='../chromedriver',chrome_options=chrome_options)


def grabAndSave():
    browser.get(map_url)
    browser.get(url)
    time.sleep(15)

    # Route 1 data
    # Route info
    route1 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[1]/div[2]")
    route1data = (route1.text).splitlines()
    
    # Distance info
    distance1 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[1]/div[1]/div[2]")
    distance1data = (distance1.text).splitlines()
    
    # Time info
    time1 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[1]/div[1]/div[1]")
    time1data = (time1.text).splitlines()

    # Print Route 1 info
    print("ETA: " + time1data[0] + " | Distance: " + distance1data[0] + " | Route: " + route1data[0])
    
    # Check for route 2
    check1 = False;
    try:
        check1 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[2]/div[2]")
    except:
        print("There is no route 2 this time!")

    if (check1):
        # Route 2 data
        # Route info
        route2 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[2]/div[2]")
        route2data = (route2.text).splitlines()
        
        # Distance info
        distance2 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[2]/div[1]/div[2]")
        distance2data = (distance2.text).splitlines()
        
        # Time info
        time2 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[2]/div[1]/div[1]")
        time2data = (time2.text).splitlines()
        
        # Print Route 2 info
        print("ETA: " + time2data[0] + " | Distance: " + distance2data[0] + " | Route: " + route2data[0])

    # Check for Route 3
    check2 = False;
    try:
        check2 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[3]/div[2]")
    except:
        print("There is no route 3 this time!")
    
    # Check if there is a route 3 available
    if (check2):
        # Route 3 data
        # Route info
        route3 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[3]/div[2]")
        route3data = (route3.text).splitlines()
        
        # Distance info
        distance3 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[3]/div[1]/div[2]")
        distance3data = (distance3.text).splitlines()
        
        # Time info
        time3 = browser.find_element_by_xpath("//*[@id='map']/div[2]/div/div/div[3]/div[2]/div/div/a[3]/div[1]/div[1]")
        time3data = (time3.text).splitlines()
        
        # Print Route 3 info
        print("ETA: " + time3data[0] + " | Distance: " + distance3data[0] + " | Route: " + route3data[0])
    


    print(readable)
    
    # Write to csv file
    writer.writerow({'Route Number': 1, 'ETA': time1data[0], 'Distance': distance1data[0], 'Route': route1data[0], 'Time': readable})
    if (check1):
        writer.writerow({'Route Number': 2, 'ETA': time2data[0], 'Distance': distance2data[0], 'Route': route2data[0], 'Time': readable})
    if (check2):
        writer.writerow({'Route Number': 3, 'ETA': time3data[0], 'Distance': distance3data[0], 'Route': route3data[0], 'Time': readable})


# upload to db
    sql = "INSERT INTO `Waze` (`routenum`, `eta`, `distance`, `route`, `time`) VALUES (%s, %s, %s, %s, %s)"

    routenum1 = 1
    eta1 = time1data[0]
    routedistance1 = distance1data[0]
    routeinfo1 = route1data[0]
    currtime = readable

    if (check1):
        routenum2 = 2
        eta2 = time2data[0]
        routedistance2 = distance2data[0]
        routeinfo2 = route2data[0]

    if (check2):
        routenum3 = 3
        eta3 = time3data[0]
        routedistance3 = distance3data[0]
        routeinfo3 = route3data[0]

    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (routenum1, eta1, routedistance1, routeinfo1, currtime))
            db.commit()

            print("Route 1 data uploaded to database")
            if (check1):
                cursor.execute(sql, (routenum2, eta2, routedistance2, routeinfo2, currtime))
                db.commit()
                print("Route 2 data uploaded to database")

            if (check2):
                cursor.execute(sql, (routenum3, eta3, routedistance3, routeinfo3, currtime))
                db.commit()
                print("Route 3 data uploaded to database")

            print("All data uploaded to database")
    except Exception:
        print("Exception, there was an error uploading to the database")



with open('wazeMapsDataCA.csv', 'w', newline='') as csvfile:
    fieldnames = ['Route Number', 'ETA', 'Distance', 'Route', 'Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    try:
        while True:
            ts = time.time()
            readable = time.ctime(ts)
            grabAndSave()
            time.sleep(1)  # 298 second day, gives 2 seconds for the program to run
    except KeyboardInterrupt:
        print("\nStopped by KEYBOARD INTERRUPTION\n\n")
        pass

browser.close()
