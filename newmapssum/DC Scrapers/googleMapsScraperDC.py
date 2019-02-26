# import csv
import time
from selenium import webdriver
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

db = pymysql.connect(host="ec2-52-14-113-176.us-east-2.compute.amazonaws.com",
                     user="Kean",
                     passwd="MobileMaps0718",
                     db="ScraperData",)
cursor = db.cursor()

url = 'https://www.google.com/maps/dir/38.3401459,-77.4927847/38.7402636,-77.1897071/@38.7420607,-77.1920187,16.54z/data=!4m2!4m1!3e0'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path='/home/ec2-user/chromedriver',chrome_options=chrome_options)


def grabAndSave():
    ts = time.time()
    timeOfRetrieval = time.ctime(ts)
    browser.get(url)
    time.sleep(5)
    
    route1(timeOfRetrieval)
    route2(timeOfRetrieval)
    route3(timeOfRetrieval)


def route1(timeOfRetrieval):
    # Selects route 1 and retrieves route info
    route = browser.find_element_by_xpath("//*[@id='section-directions-trip-0']/div[2]/div[1]/div[2]/h1[1]/span")
    route = (route.text).splitlines()

    # Retrieves time data from Route 1
    eta = browser.find_element_by_xpath("//*[@id='section-directions-trip-0']/div[2]/div[1]/div[1]/div[1]/span[1]")
    eta = (eta.text).splitlines()

    # Retrieves distance data from Route 1
    distance = browser.find_element_by_xpath("//*[@id='section-directions-trip-0']/div[2]/div[1]/div[1]/div[2]")
    distance = (distance.text).splitlines()

    route = route[0]
    eta = eta[0]
    distance = distance[0]

    # Prints out Route 1 results
    print("Route 1: " + route + " | Time: " + eta + " | Distance: " + distance)

    upload(1, eta, distance, route, timeOfRetrieval)


def route2(timeOfRetrieval):
    # If Route 2 is available, grab Route 2 data
    route2 = False

    try:
        route2 = browser.find_element_by_xpath("//*[@id='section-directions-trip-1']/div[2]/div[1]/div[2]/h1[1]/span")
    except:
        print("There is no route 2 this time!")

    if (route2):
        # Gets route info from Route 2
        route = browser.find_element_by_xpath("//*[@id='section-directions-trip-1']/div[2]/div[1]/div[2]/h1[1]/span")
        route = (route.text).splitlines()

        # Retrieves time data from Route 2
        eta = browser.find_element_by_xpath(
            "//*[@id='section-directions-trip-1']/div[2]/div[1]/div[1]/div[1]/span[1]")
        timedata2 = (eta.text).splitlines()

        # Retrieves distance data from Route 2
        distance = browser.find_element_by_xpath("//*[@id='section-directions-trip-1']/div[2]/div[1]/div[1]/div[2]")
        distance = (distance.text).splitlines()

        eta = eta[0]
        distance = distance[0]
        route = route[0]

        # Prints out Route 2 results
        print("Route 2: " + route + " | Time: " + eta + " | Distance: " + distance)

        upload(2, eta, distance, route, timeOfRetrieval)


def route3():
    # If Route 3 is available, grab Route 3 data
    route3 = False;

    try:
        route3 = browser.find_element_by_xpath(
            "//*[@id='section-directions-trip-2']/div[2]/div[1]/div[2]/h1[1]/span")
    except:
        print("There is no route 3 this time!")

    if (route3):
        # Get route info from Route 3
        route = browser.find_element_by_xpath("//*[@id='section-directions-trip-2']/div[2]/div[1]/div[2]/h1[1]/span")
        route = (route.text).splitlines()

        # Retrieves time data from Route 3
        eta = browser.find_element_by_xpath(
            "//*[@id='section-directions-trip-2']/div[2]/div[1]/div[1]/div[1]/span[1]")
        eta = (eta.text).splitlines()

        # Retrieves distance data from Route 3
        distance = browser.find_element_by_xpath("//*[@id='section-directions-trip-2']/div[2]/div[1]/div[1]/div[2]")
        distance = (distance.text).splitlines()

        eta = eta[0]
        distance = distance[0]
        route = route[0]

        # Prints out Route 3 results
        print("Route 3: " + route + " | Time: " + eta + " | Distance: " + distance)

        upload()


def upload(routeNum, eta, distance, road, timeOfRetrieval):
    # upload to db
    sql = "INSERT INTO `DC_GoogleMaps` (`routenum`, `eta`, `distance`, `route`, `time`) VALUES (%s, %s, %s, %s, %s)"

    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (routeNum, eta, distance, road, timeOfRetrieval))
            db.commit()
            print("Route data uploaded to database")

    except Exception:
        print("Exception, there was an error uploading to the database")


def apscheduler():
    logging.basicConfig()
    scheduler = BlockingScheduler()
    # Adds new scraping job every 15 minutes
    scheduler.add_job(grabAndSave, 'cron', minute='00,15,30,45')
    # Begins jobs
    scheduler.start()
    scheduler.print_jobs()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)


apscheduler()
browser.close()

    #Old CSV Code below

    # print(readable)
    # writer.writerow({'Route Number': 1, 'ETA': timedata1[0], 'Distance': distancedata1[0], 'Route': data[0], 'Time': readable})
    # if (route2):
    #     writer.writerow({'Route Number': 2,'ETA': timedata2[0], 'Distance': distancedata2[0], 'Route': data1[0], 'Time': readable})
    # if (route3):
    #     writer.writerow({'Route Number': 3,'ETA': timedata3[0], 'Distance': distancedata3[0], 'Route': data2[0], 'Time': readable})
    # print ("Cycle completed\n\n")

# with open('googleMapsDataCA.csv', 'w', newline='') as csvfile:
#     fieldnames = ['Route Number', 'ETA', 'Distance', 'Route', 'Time']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#
#     try:
#         while True:
#             ts = time.time()
#             readable = time.ctime(ts)
#             grabAndSave()
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("\n\mnStopped by KEYBOARD INTERRUPTION\n\n")
#         pass