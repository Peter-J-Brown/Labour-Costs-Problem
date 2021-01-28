"""
Please write you name here: Peter Brown
"""

import numpy as np
from datetime import *
import collections

format = '%H:%M' #defines time format for the datetime module to accept

transactionTime = [] # initialises the various lists to be used
transactionAndHour = {}
transactionsOverHour = []
transactionValue = []

breaks = [] # list of breaks in the format they were provided in
breakStart = [] # times breaks end at
breakEnd = [] # times breaks start at

startTimes = [] # times shifts start at
endTimes = [] # times shifts end at
payRates = [] # pay rate of each staff member
salesHour = []
salesHourReduced = []

salesOverHour = {}
sales = {}
shifts = {}
costPerHour = {}
percentageCostPerSale = {}
bestAndWorstPercentages = []

listOfHours = []

x = 0
while x <= 23:  # creates a 24 member list of hours, e.g. ['00:00','1:00','2:00',...'24:00']
    stringTime = str(x) + ':00'
    listOfHours.append(stringTime)
    x = x + 1

def costOverHour(time): # enter time in format 'HH:MM' including apostrophes

    t1 = datetime.strptime(time, format)
    t2 = t1 + timedelta(hours=1)
    counter = 0
    labourCost = 0

    for i in startTimes:

        if t1 <= i and i < t2:
            # shift starts during the considered hour, therefore contributes partial hour labour cost
            fractionWorked =  (t2 - i) / timedelta(hours=1)
            labourCost = labourCost + payRates[counter] * fractionWorked

        elif i < t1 and t2 <= breakStart[counter]:
            # considered hour sits between the start of the shift and the start of the break, contributes a full hour of labour cost
            labourCost = labourCost + payRates[counter]

        elif t1 <= breakStart[counter] and breakStart[counter] < t2:
            # the considered hour straddles the start of the shift break, only partial hour labour cost
            fractionWorked = (1 - (t2 - breakStart[counter]) / timedelta(hours=1))
            labourCost = labourCost + payRates[counter] * fractionWorked

        elif t1 <= breakEnd[counter] and t2 >= breakEnd[counter]:
            # considered hour straddles the end of workers break, only partial contribution to labour cost
            fractionWorked = (t2 - breakEnd[counter]) / timedelta(hours=1)
            labourCost = labourCost + payRates[counter] * fractionWorked

        elif t1 > breakEnd[counter] and t2 < endTimes[counter]:
            # considered hour sits between workers break end and shift end, contributes full hour of labour cost
            labourCost = labourCost + payRates[counter]

        elif t1 <= endTimes[counter] and t2 >= endTimes[counter]:
            # considered hour straddles workers shift end, partial hour contribution to labour cost
            fractionWorked = ( 1 - (t2 - endTimes[counter]) / timedelta(hours=1))
            labourCost = labourCost + payRates[counter] * fractionWorked

        counter = counter + 1
    return labourCost


def process_shifts(path_to_csv):

    """
        :param path_to_csv: The path to the work_shift.csv
        :type string:
        :return: A dictionary with time as key (string) with format %H:%M
            (e.g. "18:00") and cost as value (Number)
        For example, it should be something like :
        {
            "17:00": 50,
            "22:00: 40,
        }
        In other words, for the hour beginning at 17:00, labour cost was
        50 pounds
        :rtype dict:
    """

    shifts = np.genfromtxt(path_to_csv, delimiter=',', skip_header=1, dtype=[('breakTime', 'U10'), ('endTime', 'U5'), ('payRate', 'd'), ('startTime', 'U5')])

    # separates the work_shifts.csv out into separate lists for break notes, end times, start times and pay rates
    for i in shifts['breakTime']:
        breaks.append(i)
    for j in shifts['endTime']:
        endTimes.append(j)
    for k in shifts['payRate']:
        payRates.append(k)
    for l in shifts['startTime']:
        startTimes.append(l)

    for i in breaks:
        start, end = i.split('-')
        for char in start:
            if not char.isdigit() and char != '.':
                start = start.replace(char, '')
            if char == '.':
                start = start.replace(char, ':')
        for char in end:
            if not char.isdigit() and char != '.':
                end = end.replace(char, '')
            if char == '.':
                end = end.replace(char, ':')
        breakStart.append(start)
        breakEnd.append(end)

    counter = 0
    for i in startTimes:
        Time = datetime.strptime(i, format)
        i = Time
        startTimes[counter] = Time
        counter = counter + 1

    counter = 0
    for i in endTimes:
        Time = datetime.strptime(i, format)
        i = Time
        endTimes[counter] = Time
        counter = counter + 1

    counter = 0
    for i in breakStart:
        if len(i) == 1 or len(i) == 2:
            i = i + ':00'
            Time = datetime.strptime(i, format)
            breakStart[counter] = Time
            if breakStart[counter].time() < startTimes[counter].time():
                Time = Time + timedelta(hours=12)
                breakStart[counter] = Time
        else:
            Time = datetime.strptime(i, format)
            breakStart[counter] = Time
            if breakStart[counter].time() < startTimes[counter].time():
                Time = Time + timedelta(hours=12)
                breakStart[counter] = Time
        counter = counter + 1

    counter = 0
    for i in breakEnd:
        if len(i) == 1 or len(i) == 2:
            i = i + ':00'
            Time = datetime.strptime(i, format)
            breakEnd[counter] = Time
            if breakEnd[counter].time() < startTimes[counter].time():
                Time = Time + timedelta(hours=12)
                breakEnd[counter] = Time
        else:
            Time = datetime.strptime(i, format)
            breakEnd[counter] = Time
            if breakEnd[counter].time() < startTimes[counter].time():
                Time = Time + timedelta(hours=12)
                breakEnd[counter] = Time
        counter = counter + 1

    for i in listOfHours:
        costPerHour[i] = costOverHour(i)

    return costPerHour


def process_sales(path_to_csv):

    """

        :param path_to_csv: The path to the transactions.csv
        :type string:
        :return: A dictionary with time (string) with format %H:%M as key and
        sales as value (string),
        and corresponding value with format %H:%M (e.g. "18:00"),
        and type float)
        For example, it should be something like :
        {
            "17:00": 250,
            "22:00": 0,
        },
        This means, for the hour beginning at 17:00, the sales were 250 dollars
        and for the hour beginning at 22:00, the sales were 0.

        :rtype dict:

    """
    transactions = np.genfromtxt(path_to_csv, delimiter=',', skip_header=1, dtype=[('Value', 'd'), ('Time', 'U5')], encoding=None)
    transactionAndHour = collections.defaultdict(float)

    for i in transactions['Value']:
        transactionValue.append(i)

    for j in transactions['Time']:
        hh , mm = j.split(':')
        hh = hh + ':00'
        salesHour.append(hh)

    counter = 0
    while counter < len(salesHour):
        transactionAndHour[salesHour[counter]] += transactionValue[counter]
        counter += 1

    return dict(transactionAndHour)



def compute_percentage(shifts, sales):

    """

        :param shifts:
        :type shifts: dict
        :param sales:
        :type sales: dict
        :return: A dictionary with time as key (string) with format %H:%M and
        percentage of labour cost per sales as value (float),
        If the sales are null, then return -cost instead of percentage
        For example, it should be something like :
        {
            "17:00": 20,
            "22:00": -40,
        }
        :rtype: dict
    """

    percentageCostPerSale = collections.defaultdict(float)

    for i in listOfHours:
        #print("i: ", i)
        salesThatHour = sales.get(i) #gets the value in the sales dict associated with the time i
        #print("Sales that hour: ", salesThatHour)
        if salesThatHour != None:
            labourCost = shifts.get(i)
            percentageLabourCost = (labourCost / salesThatHour) * 100
            percentageCostPerSale[i] = percentageLabourCost
        else:
            labourCost = -1 * shifts.get(i)
            percentageCostPerSale[i] = labourCost

    return dict(percentageCostPerSale)



#print(compute_percentage(process_shifts("work_shifts.csv"), process_sales("transactions.csv")))


def best_and_worst_hour(percentages):

    # wording is slightly ambiguous, but I am assuming the 'best' hour, is the hour for which labour costs represent
    # the smallest percentage of sales and cost is not negative

    """

        Args:
        percentages: output of compute_percentage
        Return: list of strings, the first element should be the best hour,
        the second (and last) element should be the worst hour. Hour are
        represented by string with format %H:%M
        e.g. ["18:00", "20:00"]

    """

    bestAndWorst = []

    lowest_key1 = ''
    lowest_value1 = float('inf')

    for key1 in percentages.keys():
        value1 = percentages[key1]
        if value1 <= 0.0:
            continue

        if value1 < lowest_value1:
            lowest_key1 = key1
            lowest_value1 = value1

    lowest_key2 = ''
    lowest_value2 = float(0)

    for key2 in percentages.keys():
        value2 = percentages[key2]
        if value2 >= 0.0:
            continue

        if value2 < lowest_value2:
            lowest_key2 = key2
            lowest_value2 = value2

    bestAndWorst.append(lowest_key1)
    bestAndWorst.append(lowest_key2)

    return bestAndWorst


def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    return best_hour, worst_hour

print()
print(main("work_shifts.csv", "transactions.csv"))

# Please write you name here: Peter Brown
