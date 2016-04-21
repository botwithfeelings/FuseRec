import utility
import config
from itertools import islice
import operator

dataset = utility.load_vectors()

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def baseline():
    for i in range(config.num_slices):
        train, test = utility.get_data_split(dataset, i)
        # Retrieving functions and the counts from each training set
        orderedFunctions = getOrderedFunctions(train)
        totalRecommendations = recommendBaseline(orderedFunctions, test)


def recommendBaseline(orderedFunctions, testset):
    top10 = orderedFunctions[:10]
    totalRecommendations = []
    for (user, data) in testset.iteritems():
        foreachuser = []
        for function in top10:
            if data.has_key(function)==False:
                foreachuser.append(function)
        totalRecommendations.append(foreachuser)

    return totalRecommendations

def getOrderedFunctions(dataset):
    functionCount = dict()
    for (user, data) in dataset.iteritems():
        for (function, count) in data.iteritems():
            if functionCount.has_key(function):
                fcount = functionCount.get(function)
                fcount = fcount + count
                functionCount[function] = fcount
            else:
                functionCount[function] = count

    orderedFunctionList = sorted(functionCount, key=functionCount.__getitem__, reverse=True)

    return orderedFunctionList




'''dataset = utility.load_vectors()
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



#nitems = take(4, sorted(function_total.iteritems(), key=operator.itemgetter(1), reverse=True))
#print nitems
'''
dict2 = {'x':5, 'a': 7, 'b':4, 'z':12}
sDict = sorted(dict2, key=dict2.__getitem__, reverse=True)
#sDict = sorted(dict2.values(), reverse=True)
#s2 = sorted(dict2)
#print type(s2)
print sDict
#print type(sDict[0])
#print sDict.has_key('z')
#nitems2 = take(3, sDict)
#print nitems2['z']
#print nitems2
#print len(function_total)
'''
listx = dataset.values()
firstdict = listx[1]
print firstdict.get('Divide')
for i in range(4):
    print firstdict.popitem()'''