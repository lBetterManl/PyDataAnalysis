# -*- coding: utf-8 -*-
import heapq
import random

class Classifier:
    def __init__(self, bucketPrefix, testBucketNumber, dataFormat, k):
        self.medianAndDeviation = []
        self.k = k
        self.format = dataFormat.strip().split('\t')
        self.data = []
        for i in range(1, 11):
            if i != testBucketNumber:
                filename = "%s-%02i" % (bucketPrefix, i)
                f = open(filename)
                lines = f.readlines()
                f.close()
                for line in lines[1:]:
                    fields = line.strip().split('\t')
                    ignore = []
                    vector = []
                    for i in range(len(fields)):
                        if self.format[i] == 'num':
                            vector.append(float(fields[i]))
                        if self.format[i] == 'comment':
                            ignore.append(fields[i])
                        if self.format[i] == 'class':
                            classification = fields[i]
                    self.data.append((classification, vector, ignore))
        self.rawData = list(self.data)
        self.vlen = len(self.data[0][1])
        for i in range(self.vlen):
            self.normalizeColumn(i)

    def getMedian(self, alist):
        if alist == []:
            return []
        blist = sorted(alist)
        length = len(alist)
        if length % 2 == 1:
            return blist[int(((length+1)/2)-1)]
        else:
            v1 = blist[int(length/2)]
            v2 = blist[(int(length/2)-1)]
            return (v1+v2)/2.0

    def getAbsoluteStandardDeviation(self, alist, median):
        sum = 0
        for item in alist:
            sum += abs(item-median)
        return sum/len(alist)

    def normalizeColumn(self, columnNumber):
        col = [v[1][columnNumber] for v in self.data]
        median = self.getMedian(col)
        asd = self.getAbsoluteStandardDeviation(col, median)
        self.medianAndDeviation.append((median, asd))
        for v in self.data:
            v[1][columnNumber] = (v[1][columnNumber]-median)/asd

    def normalizeVector(self, v):
        vector = list(v)
        for i in range(len(vector)):
            (median, asd) = self.medianAndDeviation[i]
            vector[i] = (vector[i]-median)/asd
        return vector

    def testBucket(self, bucketPrefix, bucketNumber):
        filename = "%s-%02i" % (bucketPrefix, bucketNumber)
        f = open(filename)
        lines = f.readlines()
        totals = {}
        f.close()
        for line in lines:
            data = line.strip().split('\t')
            vector = []
            classInColumn = -1
            for i in range(len(self.format)):
                if self.format[i] == 'num':
                    vector.append(float(data[i]))
                elif self.format[i] == 'class':
                    classInColumn = i
            theRealClass = data[classInColumn]
            classifiedAs = self.classify(vector)
            totals.setdefault(theRealClass, {})
            totals[theRealClass].setdefault(classifiedAs, 0)
            totals[theRealClass][classifiedAs] += 1
        return totals

    def manhattan(self, vector1, vector2):
        """计算曼哈顿距离"""
        return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))

    def nearestNeighbor(self, itemVector):
        """返回最近的 itemVector"""
        return min([(self.manhattan(itemVector, item[1]), item)
                    for item in self.data])

    def knn(self, itemVector):
        """knn邻近算法预测"""
        # changed from min to heapq.nsmallest to get the
        # k closest neighbors
        neighbors = heapq.nsmallest(self.k,
                                    [(self.manhattan(itemVector, item[1]), item)
                                     for item in self.data])
        # each neighbor gets a vote
        results = {}
        for neighbor in neighbors:
            theClass = neighbor[1][0]
            results.setdefault(theClass, 0)
            results[theClass] += 1
        resultList = sorted([(i[1], i[0]) for i in results.items()], reverse=True)
        # get all the classes that have the maximum votes
        maxVotes = resultList[0][0]
        possibleAnswers = [i[1] for i in resultList if i[0] == maxVotes]
        # randomly select one of the classes that received the max votes
        answer = random.choice(possibleAnswers)
        return (answer)

    def classify(self, itemVector):
        """Return class we think item Vector is in"""
        # k represents how many nearest neighbors to use
        return (self.knn(self.normalizeVector(itemVector)))


def tenfold(bucketPrefix, dataFormat, k):
    results = {}
    for i in range(1, 11):
        c = Classifier(bucketPrefix, i, dataFormat, k)
        t = c.testBucket(bucketPrefix, i)
        for (key, value) in t.items():
            results.setdefault(key, {})
            for (ckey, cvalue) in value.items():
                results[key].setdefault(ckey, 0)
                results[key][ckey] += cvalue

    # now print results
    categories = list(results.keys())
    categories.sort()
    print("\n       Classified as: ")
    header = "        "
    subheader = "      +"
    for category in categories:
        header += "% 2s   " % category
        subheader += "-----+"
    print (header)
    print (subheader)
    total = 0.0
    correct = 0.0
    for category in categories:
        row = " %s    |" % category
        for c2 in categories:
            if c2 in results[category]:
                count = results[category][c2]
            else:
                count = 0
            row += " %3i |" % count
            total += count
            if c2 == category:
                correct += count
        print(row)
    print(subheader)
    print("\n%5.3f percent correct" % ((correct * 100) / total))
    print("total of %i instances" % total)

print("SMALL DATA SET")
tenfold("pimaSmall/pimaSmall", "num	num	num	num	num	num	num	num	class", 3)
print("\n\nLARGE DATA SET")

tenfold("pima/pima", "num	num	num	num	num	num	num	num	class", 3)
