#Based on mean square, the damage is correctly detected for small chunks (30 mins) as well as for large cunks.
#It is giving correct result with or withour applying outlier detection

import csv
import math
import statistics
from itertools import islice
import numpy
import matplotlib.pyplot as plt

SensorMnsq = []
SensorMnsqUL = []
SensorMnsqLL = []

def rem_out(data):
    mean = numpy.mean(data, axis=0)
    sd = numpy.std(data, axis=0)

    final_list = [x for x in data if (x > mean - 2 * sd)]
    final_list = [x for x in final_list if (x < mean + 2 * sd)]
    return final_list

def clean_mnsq(data):
    notoutliers = []
    sum = 0
    q1, q3 = numpy.percentile(temp, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    for y in temp:
        if lower_bound < y < upper_bound:
            notoutliers.append(y)
            sum += y ** 2

    return sum, len(notoutliers)
#-----------------------------------------------------------------------------------

for sensorid in range(1, 15):
    with open('Healthy.csv','r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        temp = []
        sum = 0
        for line in csv_reader:
            temp.append(float(line[sensorid-1]))
            sum += float(line[sensorid-1])**2

        size = len(temp)
        #sum, size = clean_mnsq(temp)

        mnsq = sum/size
        UL = mnsq + 1.96 * 2 * (numpy.mean(temp)) * (numpy.std(temp))
        LL = mnsq - 1.96 * 2 * (numpy.mean(temp)) * (numpy.std(temp))
        SensorMnsq.insert(sensorid, round(mnsq,3))
        SensorMnsqLL.insert(sensorid, round(LL, 3))
        SensorMnsqUL.insert(sensorid, round(UL, 3))

# print(SensorMed)
# print(SensorMedUL)

for sensorid in range(1, 15):
    print("Node = " + str(sensorid) + " | Mean Square = " + str(SensorMnsq[sensorid-1]) + " | Lower Limit = " + str(SensorMnsqLL[sensorid-1]) + " | Upper Limit = " + str(SensorMnsqUL[sensorid-1]))

Fs = 100
t_win = 3600

for sensorid in range(1, 15):
    etime = 0

    with open('Damage.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        while etime < 3600:
            temp = []
            sum = 0
            for line in islice(csv_reader, 0, t_win*Fs):
                temp.append(float(line[sensorid-1]))
                sum += float(line[sensorid - 1])**2

            size = len(temp)
            #sum, size = clean_mnsq(temp)

            mnsq = sum/size
            norm = (mnsq - SensorMnsqLL[sensorid-1]) / (SensorMnsqUL[sensorid-1] - SensorMnsqLL[sensorid-1])
            print("\nNode = " + str(sensorid) + " | Current Mean Square = " + str(round(mnsq, 3)) + " | Normalized Value = " + str(norm))

            if mnsq <= SensorMnsqUL[sensorid-1]:
                print("No Damage around Sensor Node " + str(sensorid))
            else:
                print("Damage Occurred Nearby Sensor Node " + str(sensorid))

            etime = etime + t_win
            # print(count)
            #time.sleep(2)


