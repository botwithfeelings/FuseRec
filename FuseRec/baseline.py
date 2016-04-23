import utility
import config
from random import choice
from itertools import islice
import operator


# Getting the most Frequently used functions in this method
# Receive the training set data
def getMostFrequent(dataset):

    #define a dictionary with key:value corresponding to function:count
    function_total = dict()

    # Iterate through the training set
    for (user, data) in dataset.iteritems():
        # Iterate through the function dictionary for each user
        for (function, count) in data.iteritems():
            if function_total.has_key(function):    # Check if the main dictionary contains this function
                fcount = function_total.get(function)
                fcount = fcount + count             # If yes, add the current user's count to the overall total
                function_total[function] = fcount
            else:
                function_total[function] = count    # If not, add the function to the dictionary
    mostFrequent = sorted(function_total, key = function_total.get, reverse=True)   # Sorting the functions by count, return a list
    return mostFrequent


def getRecList(mFrequent, testUserFlist):

    # list of Recommendations
    recList = []

    #print type(testUserFlist)
    # Iterate through each function in Most Frequent list, received from training set.
    for function in mFrequent:

        # If function not in the list of functions used by the user, then add to list of recommendations
        if function not in testUserFlist.keys():
            recList.append(function)

    # If the list of recommendations is larger than the predefined number of recommendations, prune it.
    if len(recList) > config.tuning_param["num_recs"]:
        recList = recList[0:config.tuning_param["num_recs"]]

    return recList

def recommendBaseline(trainset, testset):

    success = 0
    # Calling the function to get most Frequent Functions from the training set
    mFrequentFunctions = getMostFrequent(trainset)

    # Iterating through each user in testset
    for (user, data) in testset.iteritems():

        # Leave out one function randomly from the list and pop it.
        testFunc = choice(data.keys())
        data.pop(testFunc)
        #print data

        # Call the function to get recommendations. Returns a list of recommendations
        if testFunc in getRecList(mFrequentFunctions, data):
            success = success + 1
    return success

def doCVBaseline():

    # Get the overall dataset of 6917 records
    dataset = utility.load_vectors()
    print len(dataset)

    # Storing successful recommendations per CV set
    successPerSet = []
    for i in range(config.num_slices):
        train, test = utility.get_data_split(dataset, i)
        print len(train)
        print len(test)

        # Calling the function for the Baseline algorithm
        success = recommendBaseline(train, test)
        successPerSet.append(success)

        # Printing successful number of recommendations in this test set.
        print success

def main():
    doCVBaseline()

if __name__== "__main__":
    main()

#nitems = take(4, sorted(function_total.iteritems(), key=operator.itemgetter(1), reverse=True))
#print nitems
'''
dict2 = {'x':5, 'a': 7, 'b':4, 'z':12, 'm':30}
sDict = dict2.keys()
#sDict = sorted(dict2.values(), reverse=True)
#s2 = sorted(dict2)
#print type(s2)
print sDict
item = dict2.popitem()
print item
print type(sDict)
#print sDict.has_key('z')
#nitems2 = take(3, sDict)
#print nitems2['z']
#print nitems2
#print len(function_total)

listx = dataset.values()
firstdict = listx[1]
print firstdict.get('Divide')
for i in range(4):
    print firstdict.popitem()'''