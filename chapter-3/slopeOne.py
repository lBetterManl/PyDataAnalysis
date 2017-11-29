# -*- coding: UTF-8 -*-

users = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
         "Ben": {"Taylor Swift": 5, "PSY": 2},
         "Clara": {"PSY": 3.5, "Whitney Houston": 4},
         "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}
         }

def slopeOne(band1, band2, userRatings):
    """
    Slope One计算物品差异
    :param band1:
    :param band2:
    :param userRatings:
    :return:
    """
    comUser = 0
    sum = 0
    for (user, ratings) in userRatings.items():
        if band1 in ratings and band2 in ratings:
            sum += (ratings[band2]-ratings[band1])
            comUser += 1
    return sum/comUser

print slopeOne("PSY", "Taylor Swift", users)

