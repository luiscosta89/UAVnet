#!/usr/bin/python

#import seaborn as sns
import re
import matplotlib.pyplot as plt
import numpy as np

from scipy.stats.mstats import hmean

#sns.set(style="whitegrid")

def main():

     N = 5

     ind = np.arange(N)    # the x locations for the groups
     width = 0.35       # the width of the bars: can also be len(x) sequence

     lines = []

     name = "res1_p4.txt"

     sta1 = []
     sta2 = []
     sta3 = []
     sta4 = []
     sta5 = []
     sta6 = []

     stations_means = []
     number_packets = []

     file = open(name,"r")

     with open(name, "r") as file:
         for line in file:
             if '10.0.0.1' in line:
                 line = line.strip() #preprocess line
                 line = line.replace('10.0.0.1 : ', '')
                 sta1 = map(float, re.findall('\d+\.\d+', line ))
                 # print(sta1)
                 # raw_input("Press Enter to continue...")
                 number_packets.append(len(sta1))
                 sta1_mean = hmean(sta1)
                 stations_means.append(sta1_mean)
             elif '10.0.0.2' in line:
                 line = line.strip() #preprocess line
                 line = line.replace('10.0.0.2 : ', '')
                 sta2 = map(float, re.findall('\d+\.\d+', line ))
                 # print(sta2)
                 # raw_input("Press Enter to continue...")
                 number_packets.append(len(sta2))
                 sta2_mean = hmean(sta2)
                 stations_means.append(sta2_mean)
             elif '10.0.0.3' in line:
                 line = line.strip() #preprocess line
                 line = line.replace('10.0.0.3 : ', '')
                 sta3 = map(float, re.findall('\d+\.\d+', line ))
                 # print(sta3)
                 # raw_input("Press Enter to continue...")
                 number_packets.append(len(sta3))
                 sta3_mean = hmean(sta3)
                 stations_means.append(sta3_mean)
             elif '10.0.0.4' in line:
                 line = line.strip() #preprocess line
                 line = line.replace('10.0.0.4 : ', '')
                 sta4 = map(float, re.findall('\d+\.\d+', line ))
                 number_packets.append(len(sta4))
                 sta4_mean = hmean(sta4)
                 # print(sta4)
                 # raw_input("Press Enter to continue...")
                 stations_means.append(sta4_mean)
             elif '10.0.0.5' in line:
                 line = line.strip() #preprocess line
                 line = line.replace('10.0.0.5 : ', '')
                 sta5 = map(float, re.findall('\d+\.\d+', line ))
                 # print(sta5)
                 # raw_input("Press Enter to continue...")
                 number_packets.append(len(sta5))
                 sta5_mean = hmean(sta5)
                 stations_means.append(sta5_mean)
             elif '10.0.0.6' in line:
                 line = line.strip() #preprocess line
                 line = line.replace('10.0.0.6 : ', '')
                 sta6 = map(float, re.findall('\d+\.\d+', line ))
                 # print(sta6)
                 # raw_input("Press Enter to continue...")
                 number_packets.append(len(sta6))
                 sta6_mean = hmean(sta6)
                 stations_means.append(sta6_mean)
             else:
                 print("Nothing!")

     file.close()

     #p1 = plt.bar(ind, stations_means, width)
     #p2 = plt.bar(ind, number_packets, width, bottom=stations_means)
     p2 = plt.bar(ind, number_packets, width, color=('orange'))

     plt.ylabel('Number of packets')
     #plt.ylabel('Harmonic mean of RTT in ms ')
     plt.title('Number of packets sent from STA6 to all stations')
     #plt.title('RTT of traffic from STA1 to all stations')
     plt.xticks(ind, ('STA2', 'STA3', 'STA4', 'STA5', 'STA6'))
     plt.yticks(np.arange(0, 2001, 500)) #From 0 to 101 with intervals of 107
     #plt.yticks(np.arange(0, 61, 10))
     #plt.legend((p1[0], p2[0]), ('RTT Mean', 'Num of sent packets'))

     plt.show()

if __name__== "__main__":
  main()
