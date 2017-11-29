# -*- coding: UTF-8 -*-

users = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
         "Ben": {"Taylor Swift": 5, "PSY": 2},
         "Clara": {"PSY": 3.5, "Whitney Houston": 4},
         "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}
         }

class recommender:
    def __init__(self, data, k=1, metric='pearson', n=5):
        self.k = k
        self.n = n
        self.metric = metric
        if type(data).__name__ == 'dict':
            self.data = data
        self.frequencies = {}
        self.deviations = {}

    def computeDeviations(self):
        """
        Slope One算法
        :return:
        """
        # 获取每位用户的评分数据
        for ratings in self.data.values():
            # 对于该用户的每个评分项(歌手、分数)
            for (item, rating) in ratings.items():
                self.frequencies.setdefault(item, {})   # 键不存在时设置默认值
                self.deviations.setdefault(item, {})
                # 再次遍历该用户的每个评分项
                for (item2, raing2) in ratings.items():
                    if item != item2:
                        # 将评分的差异保存到变量中
                        self.frequencies[item].setdefault(item2, 0)
                        self.deviations[item].setdefault(item2, 0.0)
                        self.frequencies[item][item2] += 1
                        self.deviations[item][item2] += rating-raing2
        for (item, ratings) in self.deviations.items():
            for item2 in ratings:
                ratings[item2] /= self.frequencies[item][item2]

    def slopeOneRecommendations(self, userRatings):
        recommendations = {}
        frequencies = {}
        # 遍历目标用户的评分项（歌手、分数）
        for (userItem, userRating) in userRatings.items():
            # 对目标用户未评价的歌手进行计算
            for (diffItem, diffRatings) in self.deviations.items():
                if diffItem not in userRatings and userItem in self.deviations[diffItem]:
                    freq = self.frequencies[diffItem][userItem]
                    recommendations.setdefault(diffItem, 0.0)
                    frequencies.setdefault(diffItem, 0)
                    # 分子
                    recommendations[diffItem] += (diffRatings[userItem] + userRating)*freq
                    # 分母
                    frequencies[diffItem] += freq
        recommendations = [(k, v/frequencies[k]) for (k, v) in recommendations.items()]
        # 排序并返回
        recommendations.sort(key=lambda artistTuple:artistTuple[1], reverse=True)
        return recommendations

r = recommender(users)
r.computeDeviations()
print r.slopeOneRecommendations(users["Ben"])
