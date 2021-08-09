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
temph = [[] for x in range(1, 15)]
tempd = [[] for x in range(1, 15)]
sumh = [[] for x in range(1, 15)]
sumd = [[] for x in range(1, 15)]

for sensorid in range(1, 15):
    with open('Healthy.csv','r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        temp = []

        for line in csv_reader:
            temp.append(float(line[sensorid-1]))

        temph[sensorid-1] = temp
        sumh[sensorid-1] = sum(map(lambda i: i * i, temph[sensorid-1]))

Fs = 100
t_win = 1800

for sensorid in range(1, 15):
    etime = 0

    with open('Healthy.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        while etime < 3600:
            temp = []
            for line in islice(csv_reader, 0, t_win*Fs):
                temp.append(float(line[sensorid-1]))

            tempd[sensorid-1] = temp
            sumd[sensorid-1] = sum(map(lambda i: i * i, tempd[sensorid - 1]))

            acrr = sum([i*j for i,j in zip(temph[sensorid-1],tempd[sensorid-1])])/(math.sqrt(sumh[sensorid-1]*sumd[sensorid-1]))
            print("\nNode = " + str(sensorid) + " | Normalized Auto Correlation = " + str(acrr))

            etime = etime + t_win