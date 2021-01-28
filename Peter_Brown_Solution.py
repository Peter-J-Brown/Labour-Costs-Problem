"""
Please write you name here: Peter Brown
"""

"""
I know that the transaction value given for 20:00 is wrong, and I know why that is. I believe everything
else is right, however. I would love to discuss the flaws of this code, what I could have done better and what I have 
learned in an interview, if you would be willing.

I thought involving datetimes would makes things easier for me - it did not - however, I was too deep down the rabbit 
hole by the time I realised my mistake.

If anything here behaves not as expected, or you want clarification of how something works if you
feel I haven't been clear enough, then please let me know.

"""

import collections
from datetime import *
import numpy as np

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
salesHour = [] # list for storing only the hour in which a sale took place, not the minutes

salesOverHour = {} # dictionary with time as key in format HH:00 and total sales over that hour as value
costPerHour = {} # dictionary with time as key in format HH:00 and total labour cost over that hour as value
percentageCostPerSale = {} # dictionary with time as key and total labour cost/per sale over that hour as value

listOfHours = [] # a list of hours in the day, e.g. ['00:00','1:00','2:00',...'24:00']

x = 0 # initialises counter
while x <= 23:  # creates a 24 member list of hours, e.g. ['00:00','1:00','2:00',...'24:00']
    stringTime = str(x) + ':00' # adds :00 to get to HH:00 format desired
    listOfHours.append(stringTime)
    x = x + 1 # increments counter

def costOverHour(time):

    """
    Input: Hour in format 'HH:00' including apostrophes, string.
    Output: Total labour cost for that hour, float.

    """
    t1 = datetime.strptime(time, format) # converts the string time input into a datetime object, represents start of hour to be considered
    t2 = t1 + timedelta(hours=1)    # adds one hour to the start hour, creating an hour window defined by t1 and t2
    counter = 0 # initialises a counter
    labourCost = 0 # initialises labour cost

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

        counter = counter + 1 # increments counter

    return labourCost # returns labour cost as float for the hour


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
    # ingests the CSV and defines what data type each is and how many bytes it needs
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

    # this section deals with the awkward formatting the breaks were given in
    # it splits by '-' and removes letters like PM etc
    # whether a time is 24 or 12 hour is inferred by whether the break starts before the shift does
    # if this is the case, then add 12 hours to the time to convert it to 24 hour format
    # it then converts the string format times into datetime objects
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

    # ingests the CSV and defines what data type each is and how many bytes it needs
    transactions = np.genfromtxt(path_to_csv, delimiter=',', skip_header=1, dtype=[('Value', 'd'), ('Time', 'U5')], encoding=None)
    transactionAndHour = collections.defaultdict(float)

    # separates sale values in its own list
    for i in transactions['Value']:
        transactionValue.append(i)

    # separates sale time into its own list, corrects formatting to HH:00 since minutes not important
    # only sales over the whole hour considered
    for j in transactions['Time']:
        hh , mm = j.split(':')
        hh = hh + ':00'
        salesHour.append(hh)

    counter = 0 # initialises counter
    while counter < len(salesHour): # merges transaction values that occur in the same hour
        transactionAndHour[salesHour[counter]] += transactionValue[counter]
        counter += 1 # increments counter

    return dict(transactionAndHour) # returns the required dictionary



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
        salesThatHour = sales.get(i) #gets the value in the sales dict associated with the time i
        if salesThatHour != None: # percentage of labour cost per sale
            labourCost = shifts.get(i)
            percentageLabourCost = (labourCost / salesThatHour) * 100
            percentageCostPerSale[i] = percentageLabourCost
        else:
            labourCost = -1 * shifts.get(i) # If the sales are null, then return -cost instead of percentage
            percentageCostPerSale[i] = labourCost

    return dict(percentageCostPerSale)


def best_and_worst_hour(percentages):

    # wording is slightly ambiguous, but I am assuming the 'best' hour, is the hour for which labour costs represent
    # the smallest percentage of sales and cost is not negative. I.E. the best profit margin for the business owner.

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

    for key1 in percentages.keys(): # finds the lowest percentage that is non zero and non negative
        value1 = percentages[key1]  # and the key associated with that percentage
        if value1 <= 0.0:
            continue

        if value1 < lowest_value1:
            lowest_key1 = key1
            lowest_value1 = value1

    lowest_key2 = ''
    lowest_value2 = float(0)

    for key2 in percentages.keys(): # finds the most negative cost and the key associated with that cost
        value2 = percentages[key2]
        if value2 >= 0.0:
            continue

        if value2 < lowest_value2:
            lowest_key2 = key2
            lowest_value2 = value2

    bestAndWorst.append(lowest_key1) # adds these best and worst keys to the required list
    bestAndWorst.append(lowest_key2)

    return bestAndWorst # returns the required 2 member list


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

print(main("work_shifts.csv", "transactions.csv")) # testing that the main function is working as intended

# Please write you name here: Peter Brown
