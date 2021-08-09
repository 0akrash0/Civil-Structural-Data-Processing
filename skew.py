#Based on mean square, the damage is correctly detected for small chunks (5-30 mins) as well as for large cunks.
#It is giving correct result with or withour applying outlier detection

import csv
from typing import List, Any
import math
import statistics
from itertools import islice
import numpy
import matplotlib.pyplot as plt
from scipy.stats import skew

Sensorskw = []
SensorskwUL = []
SensorskwLL = []

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

    sk = skew(notoutliers)
    return sk
#-----------------------------------------------------------------------------------

for sensorid in range(1, 15):
    with open('Healthy.csv','r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        temp = []

        for line in csv_reader:
            temp.append(float(line[sensorid-1]))

        #skw = clean_mnsq(temp)
        temp = temp[:len(temp)//2]
        size = len(temp)

        skw = skew(temp)
        SES = math.sqrt((6*size*(size-1))/((size-2)*(size+1)*(size+3)))
        #SES = math.sqrt(6/size)
        UL = skw + 1.96 * SES
        LL = skw - 1.96 * SES

        Sensorskw.insert(sensorid, round(skw, 3))
        SensorskwUL.insert(sensorid, round(UL, 3))
        SensorskwLL.insert(sensorid, round(LL, 3))

# print(SensorMed)
# print(SensorMedUL)

for sensorid in range(1, 15):
    #print("Node = " + str(sensorid) + " | skew = " + str(Sensorskw[sensorid - 1]))
    print("Node = " + str(sensorid) + " | skew = " + str(Sensorskw[sensorid-1]) + " | Lower Limit = " + str(SensorskwLL[sensorid-1]) + " | Upper Limit = " + str(SensorskwUL[sensorid-1]))

Fs = 100
t_win = 1800

for sensorid in range(1, 15):
    etime = 0

    with open('Damage.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        while etime < 3600:
            temp = []

            for line in islice(csv_reader, 0, t_win*Fs):
                temp.append(float(line[sensorid-1]))

            #skw = clean_mnsq(temp)

            skw = skew(temp)
            norm = (skw - SensorskwLL[sensorid - 1]) / (SensorskwUL[sensorid - 1] - SensorskwLL[sensorid - 1])
            print("\nNode = " + str(sensorid) + " | Current skew = " + str(round(skw, 3)) + " | Normalized value = " + str(norm))

            if SensorskwLL[sensorid-1] <= skw <= SensorskwUL[sensorid-1]:
                print("NO Damage around Sensor Node " + str(sensorid))
            else:
                print("Damage Occurred Nearby Sensor Node " + str(sensorid))

            etime = etime + t_win
            # print(count)
            #time.sleep(2)