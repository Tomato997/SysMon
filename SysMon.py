"""
	System Monitor v1.0 Script for Python 2 using psutil
	Copyright(C) 2017 by Felix Knobl.
	https://twitter.com/felix_knobl

"""

# From Twitter Library
# https://pypi.python.org/packages/ea/1e/ffb8dafa9539c68bd0994d98c1cf55760b2efe0e29189cd486bf4f23907d/twitter-1.17.1-py2.py3-none-any.whl#md5=ca1aa70131eb3b5a71d3ad76c7f030f5

from twitter import *
import time

# psutil 5.2.2 required
import psutil

# From Twitter Example Project on GitHub
# https://github.com/ideoforms/python-twitter-examples
# Required Twitter App registration: https://apps.twitter.com
consumer_key = "fL9ddJed3hNZo3imj2vRix2xr"
consumer_secret = "GEJDAHqZAmdkGiAckDE9GNKW4sSCTiQ0epwj4gnhZ58Foo55pI"
access_key = "877194539743707136-GkArzen7tPib8JIgqszNk4o0ujkzpX6"
access_secret = "iSfE6oiikROTsnjxv2E958Z4ZOQW0fR3H2dFB0uZaaZhu"

 # How many times the current values should be posted before an average post is posted
LONG_POST_INTERVAL = 10

# Timeout betweet current values posts
SHORT_POST_TIMEOUT = 60

longPostCounter = LONG_POST_INTERVAL

def sendTwitter(text):
	try:
		# Create Twitter object using API credentials
		twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))
		
		# Send text to twitter
		retVal = twitter.statuses.update(status = text)
		
		# Print text and send result
		print(text + "\n\n")
		# print(retVal) # Too much output
	
	except:
		print("ERROR: Could not send tweet: " + text)
	

averageCpuUsage = 0
averageDiskUsage = 0
averageUsersCount = 0
averageTemperature = 0

# Start a infinite loop for this script
while (True):
	currentTime = time.strftime("%d.%m.%Y %H:%M")
	currentCpuPercent = psutil.cpu_percent(interval = 1, percpu = True)
	currentCpuCount = psutil.cpu_count(logical = True)
	currentDiskUsage = psutil.disk_usage('/')
	currentUsersCount = psutil.users()

	# Calculate the CPU usages from all cores
	currentCpuUsage = 0
	
	for n in range(0, currentCpuCount):
		currentCpuUsage = currentCpuUsage + currentCpuPercent[n]
	
	currentCpuUsage = currentCpuUsage / currentCpuCount
	
	# Calculate current disk usage
	currentDiskUsage = currentDiskUsage[3]
	
	# Calculate logged in users
	currentUsersCount = len(currentUsersCount)
	
	# Calculate system temperature
	currentTemperature = psutil.sensors_temperatures()
	
	# sensors_temperatures does not work in a virtual machine, set to 0
	if not currentTemperature:
		currentTemperature = 0
	else:
		# 29.06.2017 psutil docu @ https://pythonhosted.org/psutil/ is offline.
		# Do not know expected return values to deal with could not find any other useful documentation :(
		# Setting temporarily to 0
		currentTemperature = 0

	# Add current values to average values
	averageCpuUsage = averageCpuUsage + currentCpuUsage
	averageDiskUsage = averageDiskUsage + currentDiskUsage
	averageUsersCount = averageUsersCount + currentUsersCount
	averageTemperature = averageTemperature + currentTemperature

	# Create the string with current values
	# Degree sign from example @ https://stackoverflow.com/questions/3215168/how-to-get-character-in-a-string-in-python
	currentData = "SysMon on " + currentTime + " - Current values:\nCPU usage: " + str(currentCpuUsage) + "%\nDisk usage: " + str(currentDiskUsage) + "%\nNumber of logged-in users: " + str(currentUsersCount) + "\nSystem temperature: " + str(currentTemperature) + u'\N{DEGREE SIGN}' + "C"
	
	# Send current values to twitter
	sendTwitter(currentData)
	
	longPostCounter = longPostCounter - 1
	
	# Send average data to twitter if the counter reaches 0
	if longPostCounter == 0:
		averageCpuUsage = averageCpuUsage / LONG_POST_INTERVAL
		averageDiskUsage = averageDiskUsage / LONG_POST_INTERVAL
		averageUsersCount = averageUsersCount / LONG_POST_INTERVAL
		averageTemperature = averageTemperature / LONG_POST_INTERVAL

		# Create the string with average values
		averageData = "SysMon on " + currentTime + " - Average values:\nCPU usage: " + str(averageCpuUsage) + "%\nDisk usage: " + str(averageDiskUsage) + "%\nNumber of logged-in users: " + str(averageUsersCount) + "\nSystem temperature: " + str(averageTemperature) + u'\N{DEGREE SIGN}' + "C"

		# Send average values to twitter
		sendTwitter(averageData)

		# Reset the counter
		longPostCounter = LONG_POST_INTERVAL
		
		# Reset average counters
		averageCpuUsage = 0
		averageDiskUsage = 0
		averageUsersCount = 0
		averageTemperature = 0

	# Sleep	until next current values post
	time.sleep(SHORT_POST_TIMEOUT)






