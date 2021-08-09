#Based on STD, the damage is correctly detected for small chunks (30 mins) as well as for large cunks.
#It is giving correct result with or withour applying outlier detection

import scipy
#import Adafruit_CharLCD as LCD
import csv
import time
import math
#import statistics
from itertools import islice
import numpy
from scipy.stats.distributions import chi2
#import matplotlib.pyplot as plt

SensorStd = []
SensorStdUL = []
SensorStdLL = []

# Raspberry Pi pin setup
#rs = 7
#en = 8
#d4 = 25
#d5 = 24
#d6 = 23
#d7 = 18
#backlight = 2

# Define LCD column and row size for 16x2 LCD.
#columns = 16
#rows = 2

#lcd = LCD.Adafruit_CharLCD(rs,en,d4,d5,d6, d7,columns,rows,backlight)



def rem_out(data):
    mean = numpy.mean(data, axis=0)
    sd = numpy.std(data, axis=0)

    final_list = [x for x in data if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]
    return final_list

def remove_outliers(data):
    notoutliers = []
    q1, q3 = numpy.percentile(temp, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    for y in temp:
        if lower_bound < y < upper_bound:
            notoutliers.append(y)

    standev = numpy.std(notoutliers)

    return standev, len(notoutliers)
#-----------------------------------------------------------------------------------#

for sensorid in range(1, 2):
    with open('Healthy.csv','r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        temp = []

        for line in csv_reader:
            temp.append(float(line[sensorid-1]))
            # print(line[sensorid-1])

        #standev, size = remove_outliers(temp)
        standev = numpy.std(temp)
        size = len(temp)
        LL = standev * (math.sqrt((size-1)/chi2.ppf(0.025, size-1)))
        UL = standev * (math.sqrt((size-1)/chi2.ppf(1-0.025, size-1)))

        #UL = standev * (math.sqrt(2 * size - 1) + 1.96) / math.sqrt(2 * size - 1)
        #LL = standev * (math.sqrt(2 * size - 1) - 1.96) / math.sqrt(2 * size - 1)

        SensorStd.insert(sensorid, round(standev,6))
        SensorStdUL.insert(sensorid, round(UL,6))
        SensorStdLL.insert(sensorid, round(LL,6))

# print(SensorMed)
# print(SensorMedUL)

for sensorid in range(1, 2):
    print("Node = " + str(sensorid) + " | STD = " + str(SensorStd[sensorid-1]) + " | Lower Limit = " + str(SensorStdLL[sensorid-1]) + " | Upper Limit = " + str(SensorStdUL[sensorid-1]))

Fs = 100
t_win = 900

for sensorid in range(1, 2):
    etime = 0

    with open('Damage.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        while etime < 3600:
            temp = []
            for line in islice(csv_reader, 0, t_win*Fs):
                temp.append(float(line[sensorid-1]))

            #clean_dam = rem_out(temp)
            #print("original "+ str(temp))
            #print("Processed "+ str(clean_dam))

            std = numpy.std(temp)
            print("\nNode = " + str(sensorid) + " | Current STD = " + str(round(std,3)))

            if SensorStdLL[sensorid-1] <= std <= SensorStdUL[sensorid-1]:
                print("NO Damage around Sensor Node " + str(sensorid))
            else:
                print("Damage Occurred Nearby Sensor Node " + str(sensorid))
	       # lcd.message('DAMAGE Detected')
	#	time.sleep(5)
	#	lcd.clear()

            etime = etime + t_win
            # print(count)
            time.sleep(10)


