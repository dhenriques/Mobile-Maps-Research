import csv
import time
from selenium import webdriver
import pymysql

# Declare URL with mapping coordinates
url = 'https://www.mapquest.com/directions/from/near-38.33975,-77.4925/to/near-38.740322,-77.189608'

# Set up browser used by selenium
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

browser = webdriver.Chrome(executable_path='..\chromedriver',chrome_options=chrome_options)

# Set up database credentials
db = pymysql.connect(host="ec2-18-216-116-132.us-east-2.compute.amazonaws.com",
                     user="Kean",
                     passwd="MobileMapsResearch0718!",
                     db="MapData_DC",
                     )

cursor = db.cursor()


def grabAndSave():
    browser.get(url)
    time.sleep(3)
    
    # Prepare Route 1
    click = False;
    try:
        click = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/ol/li[1]")
    except:
        # Selects route 1 (unique) and retrieves route info        
        nav = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[1]")
        data = (nav.text).splitlines()

        #Retrieves time data from Route 1
        time1 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[2]/span[1]")
        timedata1 = (time1.text).splitlines()

        #Retrieves distance data from Route 1
        distance1 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[2]/div")
        distancedata1 = (distance1.text).splitlines()
    
    if (click):
        # Selects route 1 and retrieves route info
        nav = browser.find_element_by_class_name("container-fluid")
        data = (nav.text).splitlines()

        #Retrieves time data from Route 1
        time1 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[2]/span[1]")
        timedata1 = (time1.text).splitlines()
        
        #Retrieves distance data from Route 1
        distance1 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[2]/div")
        distancedata1 = (distance1.text).splitlines()
    
    #Prints out Route 1 results
    print("Route: " + data[0] +" | Time: " + timedata1[0] + " | Distance: " + distancedata1[0])

    # Prepare clicker for route 2
    click1 = False;
    try:
	    click1 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/ol/li[2]")
    except:
    	print("There is no route 2 this time!")

    if (click1):
	    # Click on route 2
	    click1.click()

	    # Gets route info from route 2
	    nav1 = browser.find_element_by_class_name("container-fluid")
	    data1 = (nav1.text).splitlines()

	    #Retrieves time data from Route 2
	    time2 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[2]/span[1]")
	    timedata2 = (time2.text).splitlines()

	    #Retrieves distance data from Route 2
	    distance2 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[2]/div")
	    distancedata2 = (distance2.text).splitlines()

	    #Prints out Route 2 results
	    print("Route: " + data1[0] +" | Time: " + timedata2[0] + " | Distance: " + distancedata2[0])

    # Prepare Clicker for Route 3
    click2 = False;
    try:
        click2 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/ol/li[3]")
    except:
        print("There is no route 3 this time!")
    # Check if there is a route 3 available
    if (click2):
        # Click on Route 3
        click2.click()
        # Get route info from Route 3
        nav2 = browser.find_element_by_class_name("container-fluid")
        data2 = (nav2.text).splitlines()
        #Retrieves time data from Route 1
        time3 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[2]/span[1]")
        timedata3 = (time3.text).splitlines()
        #Retrieves distance data from Route 1
        distance3 = browser.find_element_by_xpath("//*[@id='primaryPanel']/div[8]/div[1]/div/div[2]/div[1]/form/div[2]/div/div/div/route-info/div/div[2]/div[2]/div")
        distancedata3 = (distance3.text).splitlines()
        #Prints out Route 1 results
        print("Route: " + data2[0] +" | Time: " + timedata3[0] + " | Distance: " + distancedata3[0])

    print(readable)
    writer.writerow({'Route Number': 1, 'ETA': timedata1[0], 'Distance': distancedata1[0], 'Route': data[0], 'Time': readable})
    if (click1):
	    writer.writerow({'Route Number': 2,'ETA': timedata2[0], 'Distance': distancedata2[0], 'Route': data1[0], 'Time': readable})
    if (click2):
        writer.writerow({'Route Number': 3,'ETA': timedata3[0], 'Distance': distancedata3[0], 'Route': data2[0], 'Time': readable})
    print ("Cycle completed\n\n")

    # Assign Database storage variables
    routenum1 = 1
    routeinfo1 = data[0]
    routedistance1 = distancedata1[0]
    eta1 = timedata1[0]
    currtime = readable

    # Assign Database storage variables
    if (click1):
        routenum2 = 2
        routeinfo2 = data1[0]
        routedistance2 = distancedata2[0]
        eta2 = timedata2[0]

    # Assign Database storage variables
    if (click2):
        routenum3 = 3
        routeinfo3 = data2[0]
        routedistance3 = distancedata3[0]
        eta3 = timedata3[0]
       


    try:
        with db.cursor() as cursor:
            sql1 = "INSERT INTO `MapQuest` (`routenum`, `eta`, `distance`, `route`, `time`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql1, (routenum1, eta1, routedistance1, routeinfo1, currtime))
            db.commit()
            
            print("Route 1 data uploaded to database")
            if (click1):
                sql2 = "INSERT INTO `MapQuest` (`routenum`, `eta`, `distance`, `route`, `time`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql2, (routenum2, eta2, routedistance2, routeinfo2, currtime))
                db.commit()
                print("Route 2 data uploaded to database")

            if (click2):
                sql3 = "INSERT INTO `MapQuest` (`routenum`, `eta`, `distance`, `route`, `time`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql3, (routenum3, eta3, routedistance3, routeinfo3, currtime))
                db.commit()
                print("Route 3 data uploaded to database")

            print("All data uploaded to database")
    except Exception:
        print("Exception, there was an error uploading to the database")


with open('mapQuestDataCA.csv', 'w', newline='') as csvfile:
    fieldnames = ['Route Number', 'ETA', 'Distance', 'Route', 'Time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    try:
        while True:
            ts = time.time()
            readable = time.ctime(ts)
            grabAndSave()
            time.sleep(1) # 298 second day, gives 2 seconds for the program to run
    except KeyboardInterrupt:
        print("\n\nStopped by KEYBOARD INTERRUMPTION\n\n")
        pass

db.commit()
cursor.close()
browser.close()