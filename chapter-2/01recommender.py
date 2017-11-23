#!/usr/bin/python3

"""
推荐喜欢乐队
"""

users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                      "Norah Jones": 4.5, "Phoenix": 5.0,
                      "Slightly Stoopid": 1.5,
                      "The Strokes": 2.5, "Vampire Weekend": 2.0},

         "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5,
                  "Deadmau5": 4.0, "Phoenix": 2.0,
                  "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},

         "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                  "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5,
                  "Slightly Stoopid": 1.0},

         "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                 "Deadmau5": 4.5, "Phoenix": 3.0,
                 "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                 "Vampire Weekend": 2.0},

         "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                    "Norah Jones": 4.0, "The Strokes": 4.0,
                    "Vampire Weekend": 1.0},

         "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0,
                    "Norah Jones": 5.0, "Phoenix": 5.0,
                    "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                    "Vampire Weekend": 4.0},

         "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                 "Norah Jones": 3.0, "Phoenix": 5.0,
                 "Slightly Stoopid": 4.0, "The Strokes": 5.0},

         "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                      "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                      "The Strokes": 3.0}
         }

# 测试users格式正确性
# print(users['Veronica'])

def manhattan(rating1, rating2):
    """
    计算曼哈顿距离。
    :param rating1: 数据格式{"The Strokes": 2.5, "Vampire Weekend": 2.0}
    :param rating2: 数据格式"The Strokes": 2.5, "Vampire Weekend": 2.0}
    :return: 曼哈顿距离
    """
    distance = 0
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
    return distance

# 测试manhattan(rating1, rating2)
# print(manhattan(users['Hailey'], users['Veronica']))

def minkowski(rating1, rating2, r):
    """
    闵可夫斯基距离
    :param rating1:
    :param rating2:
    :param r:
    :return:
    """
    distance = 0
    for key in rating1:
        if key in rating2:
            distance += pow(abs(rating1[key] - rating2[key]), r)
    return pow(distance, 1.0/r)

def computerNearestNeighbor(username, users):
    """
    计算所有用户与username的距离，倒序排列并返回结果列表
    :param username: 用户
    :param users: 用户列表
    :return: 相似距离
    """
    distances = []
    for user in users:
        if user != username:
            distance = manhattan(users[user], users[username])
            distances.append((distance, user))
    # 按照相似距离排序 小-》大
    distances.sort()
    return distances

# 测试computerNearestNeighbor(username, users)
# print(computerNearestNeighbor("Hailey", users))

def recommend(username, users):
    """
    推荐结果列表
    :param username: 用户
    :param users: 用户列表
    :return: 推荐结果列表
    """
    # 找出最近用户
    nearest = computerNearestNeighbor(username, users)[0][1]
    recommendations = []
    # 找出这位用户评价过、但自己尚未评价的乐队
    neighborRatings = users[nearest]
    userRatings = users[username]
    for artist in neighborRatings:
        if not artist in userRatings:
            recommendations.append((artist, neighborRatings[artist]))
    # 按照评分进行排序 大-》小
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse=True)

# 测试recommend
print(recommend("Hailey", users))
