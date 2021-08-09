import csv
import math
import statistics
from itertools import islice
import numpy
import matplotlib.pyplot as plt

SensorMed = []
SensorMedUL = []
SensorMedLL = []

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

    return notoutliers

for sensorid in range(1, 15):
    with open('Healthy.csv','r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        temp = []

        for line in csv_reader:
            temp.append(float(line[sensorid-1]))
            # print(line[sensorid-1])

        #clean = remove_outliers(temp)

        med = numpy.median(temp)
        UL = med + 1.253 * 1.96 * numpy.std(temp) / math.sqrt(len(temp))
        LL = med - 1.253 * 1.96 * numpy.std(temp) / math.sqrt(len(temp))
        SensorMed.insert(sensorid, round(med, 3))
        SensorMedUL.insert(sensorid, round(UL, 3))
        SensorMedLL.insert(sensorid, round(LL, 3))

#for sensorid in range(1, 15):
#    print("Node = " + str(sensorid) + " | Median = " + str(SensorMed[sensorid-1]) + " | Upper Limit = " + str(SensorMedUL[sensorid-1]))

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

            #clean_dam = rem_out(temp)

            med = numpy.median(temp)
            print("\nNode = " + str(sensorid) + " | Current Median = " + str(med) + " | Upper Limit = " + str(SensorMedUL[sensorid - 1]))

            if SensorMedLL[sensorid-1] <= med <= SensorMedUL[sensorid-1]:
                print("No Damage around Sensor Node " + str(sensorid))
            else:
                print("Damage Occurred Nearby Sensor Node " + str(sensorid))

            etime = etime + t_win
            # print(count)
            #time.sleep(2)


