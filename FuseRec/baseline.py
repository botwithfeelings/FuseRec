import utility
import config
from itertools import islice
import operator

'''
dataset = utility.load_vectors()
function_total = dict()
print len(function_total)
for (user, data) in dataset.iteritems():
    for (function, count) in data.iteritems():
        if function_total.has_key(function):
            fcount = function_total.get(function)
            fcount = fcount + count
            function_total[function] = fcount
        else:
            function_total[function] = count
mostFrequent = sorted(function_total, key=function_total.get, reverse=True)
'''
def getMostFrequent(dataset):
    function_total = dict()
    for (user, data) in dataset.iteritems():
        for (function, count) in data.iteritems():
            if function_total.has_key(function):
                fcount = function_total.get(function)
                fcount = fcount + count
                function_total[function] = fcount
            else:
                function_total[function] = count
    mostFrequent = sorted(function_total, key = function_total.get, reverse=True)
    return mostFrequent

def baseline(dataset):
    successPerSet = []
    for i in range(config.num_slices):
        train, test = utility.get_data_split(dataset, i)
        # Retrieving functions and the counts from each training set
        mFrequentFunctions = getMostFrequent(train)
        success = recommendBaseline(mFrequentFunctions, test)
        successPerSet.append(success)
        print successPerSet


def recommendBaseline(orderedFunctions, testset):
    recList = []
    success = 0
    for (user, data) in testset.iteritems():
        fList = data.keys()
        rmFunction = data.popitem()
        #print type(rmFunction)
        for func in orderedFunctions:
            if func not in fList:
                recList.append(func)
            if len(recList) == 10:
                break
        if rmFunction[0] in recList:
            success = success + 1
    return success


def main():
    dataset = utility.load_vectors()
    baseline(dataset)

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