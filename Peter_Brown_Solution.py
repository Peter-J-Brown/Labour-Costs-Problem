"""
Please write you name here: Peter Brown
"""

import numpy as np
from datetime import *

format = '%H:%M' #defines time format for the datetime module to accept

transactionTime = [] # initialises the various lists to be used
transactionValue = []

breaks = [] # list of breaks in the format they were provided in
breakStart = [] # times breaks end at
breakEnd = [] # times breaks start at

startTimes = [] # times shifts start at
endTimes = [] # times shifts end at
payRates = [] # pay rate of each staff member
sales = {}
shifts = {}
costPerHour = {}

listOfHours = []

x = 0
while x <= 23:  # creates a 24 member list of hours, e.g. ['00:00','1:00','2:00',...'24:00']
    stringTime = str(x) + ':00'
    listOfHours.append(stringTime)
    x = x + 1

'''

transactions = np.genfromtxt("transactions.csv", delimiter = ',', skip_header = 1, dtype = [('Value', 'd'), ('Time', 'U5')], encoding = None)
shifts = np.genfromtxt("work_shifts.csv", delimiter=',', skip_header = 1, dtype = [('breakTime', 'U10'), ('endTime', 'U5'), ('payRate', 'd'), ('startTime', 'U5')])

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
    
'''

'''
for i in transactions['Value']:
    transactionValue.append(i)

for j in transactions['Time']:
    Time = datetime.strptime(j, format)
    transactionTime.append(Time.time())
    sales[Time.hour] = i
    
'''

def costOverHour(time): # enter time in format 'HH:MM' including apostrophes

    t1 = datetime.strptime(time, format)
    t2 = t1 + timedelta(hours=1)
    counter = 0
    labourCost = 0

    for i in startTimes:

        #print("Considering hour starting at: ", t1.time())
        #print("Worker being checked: ", counter + 1)

        if t1 <= i and i < t2:
            # shift starts during the considered hour, therefore contributes partial hour labour cost
            fractionWorked =  (t2 - i) / timedelta(hours=1)
            #print("worker: ", counter+1, ", partial hour worked")
            #print("fraction worked1: ", fractionWorked)
            #print("adding1: ", payRates[counter]*fractionWorked, "to labour costs total")
            labourCost = labourCost + payRates[counter] * fractionWorked

        elif i < t1 and t2 <= breakStart[counter]:
            # considered hour sits between the start of the shift and the start of the break, contributes a full hour of labour cost
            #print("worker: ", counter + 1, ", full hour worked")
            #print("adding2: ", payRates[counter], "to labour costs total")
            labourCost = labourCost + payRates[counter]

        elif t1 <= breakStart[counter] and breakStart[counter] < t2:
            # the considered hour straddles the start of the shift break, only partial hour labour cost
            fractionWorked = (1 - (t2 - breakStart[counter]) / timedelta(hours=1))
            #print("worker: ", counter + 1, ", partial hour worked")
            #print("fraction worked3: ", fractionWorked)
            #print("adding3: ", payRates[counter]*fractionWorked, "to labour costs total")
            labourCost = labourCost + payRates[counter] * fractionWorked

        elif t1 <= breakEnd[counter] and t2 >= breakEnd[counter]:
            # considered hour straddles the end of workers break, only partial contribution to labour cost
            fractionWorked = (t2 - breakEnd[counter]) / timedelta(hours=1)
            #print("worker: ", counter + 1, ", partial hour worked")
            #print("fraction worked5: ", fractionWorked)
            #print("adding5: ", payRates[counter]*fractionWorked, "to labour costs total")
            labourCost = labourCost + payRates[counter] * fractionWorked

        elif t1 > breakEnd[counter] and t2 < endTimes[counter]:
            # considered hour sits between workers break end and shift end, contributes full hour of labour cost
            #print("worker: ", counter + 1, ", full hour worked")
            #print("adding6: ", payRates[counter], "to labour costs total")
            labourCost = labourCost + payRates[counter]

        elif t1 <= endTimes[counter] and t2 >= endTimes[counter]:
            # considered hour straddles workers shift end, partial hour contribution to labour cost
            #print("(t2 - endTimes[counter]) ", (t2 - endTimes[counter]))
            #print("( 1 - (t2 - endTimes[counter]) / timedelta(hours=1)) ", ( 1 - (t2 - endTimes[counter]) / timedelta(hours=1)))
            #print("worker: ", counter + 1, ", partial hour worked")
            fractionWorked = ( 1 - (t2 - endTimes[counter]) / timedelta(hours=1))
            #print("fraction worked7: ", fractionWorked)
            #print("adding7: ", payRates[counter] * fractionWorked, "to labour costs total")
            labourCost = labourCost + payRates[counter] * fractionWorked

        '''
        if t1 > endTimes[counter]:
            # considered hour occurs after workers shift has ended, no contribution to labour cost
            labourCost = labourCost  # I know this is a pointless assignment, I have added the permutation for completeness
        '''

        counter = counter + 1
    return labourCost

#print(costOverHour('20:00'))


def process_shifts(path_to_csv):

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

    transactions = np.genfromtxt(path_to_csv, delimiter=',', skip_header=1, dtype=[('Value', 'd'), ('Time', 'U5')], encoding=None)

    for i in transactions['Value']:
        transactionValue.append(i)

    counter = 0
    for j in transactions['Time']:
        sales[j] = transactionValue[counter]
        counter = counter + 1

    return sales

print(process_shifts("work_shifts.csv"))
print(process_sales("transactions.csv"))





'''
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
    return


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
    return

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
    return

def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """

    return

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


if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = ""
    path_to_shifts = ""
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)
'''

# Please write you name here: Peter Brown
