import codecs

from math import sqrt

class recommender:
    def __init__(self, data, k=1, myfn='pearson', n=5):
        """
        初始化推荐模块
        :param data: 训练数据
        :param k: K邻近算法中的值
        :param metric: 使用何种距离计算方式
        :param n: 推荐结果的数量
        """
        self.k = k
        self.n = n
        self.username2id = {}   # 字典
        self.userid2name = {}
        self.productid2name = {}
        # 将距离计算方式保存下来
        self.myfn = myfn
        if self.myfn == 'pearson':
            self.fn = self.pearson
        # 如果data是一个字典类型，则板寸下来，否则忽略
        if type(data).__name__ == 'dict':
            self.data = data

    def convertProductID2name(self, id):
        """
        通过产品ID获取名称
        :param id: 产品ID
        :return: 产品名称
        """
        if id in self.productid2name:
            return self.productid2name[id]
        else:
            return id

    def userRatings(self, id, n):
        """
        返回用户评分最高的物品
        :param id: 用户id
        :param n: 返回数量
        :return: 评分结果
        """
        print("Ratings for " + self.userid2name[id])
        ratings = self.data[id]
        print(len(ratings))
        ratings = list(ratings.items())
        ratings = [(self.convertProductID2name(k), v) for (k, v) in ratings]
        # 排序并返回结果
        ratings.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        for rating in ratings:
            print("%s\t%i" % (rating[0], rating[1]))

    def loadBookDB(self, path=''):
        """
        加载BX数据集
        :param path: 数据文件位置
        :return: 数据集
        """
        self.data = {}
        i = 0

        # 将书籍评分放入self.data
        f = codecs.open(path + "BX-Book-Ratings.csv", 'r', 'utf8')
        for line in f:
            i += 1
            # 分割每行
            fields = line.split(";")
            user = fields[0].strip('"')
            book = fields[1].strip('"')
            rating = int(fields[2].strip().strip('"'))
            if user in self.data:
                currentRatings = self.data[user]
            else:
                currentRatings = {}
            currentRatings[book] = rating
            self.data[user] = currentRatings
        f.close()

        # 将书籍信息存入self.productid2name
        # 包括isbn号、书名、作者等
        f = codecs.open(path + "BX-Books.csv", 'r', 'utf8')
        for line in f:
            i += 1
            # 分割每行数据
            fields = line.split(';')
            isbn = fields[0].strip('"')
            title = fields[1].strip('"')
            author = fields[2].strip('"')
            title = title + 'by' + author
            self.productid2name[isbn] = title
        f.close()

        # 将用户信息存入self.userid2name和self.username2id
        f = codecs.open(path + "BX-Users.csv", 'r', 'utf8')
        for ine in f:
            i += 1
            # 分割每行数据
            fields = line.split(';')
            userid = fields[0].strip('"')
            location = fields[1].strip('"')
            if len(fields) > 3:
                age = fields[2].strip().strip('"')
            else:
                age = 'NULL'
            if age != 'NULL':
                value = location + ' (age: ' + age + ')'
            else:
                value = location
            self.userid2name[userid] = value
            self.username2id[location] = userid
        f.close()
        print("数据条数："+str(i))

    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        for key in rating1:
            if key in rating2:
                n += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x*y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        if n == 0:
            return 0
        # 计算分母
        denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / n) / denominator

    def computerNearestNeighbor(self, username):
        """
        获取邻近用户
        :param username:
        :return:
        """
        distances = []  #列表
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username], self.data[instance])
                distances.append((instance, distance))
        # 排序 小-》大
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return distances

    def recommend(self, user):
        """
        :param user:
        :return: 推荐列表
        """
        recommendations = {}
        # 1.获取邻近用户
        nearest = self.computerNearestNeighbor(user)
        # 2.获取用户评价过的商品
        userRatings = self.data[user]
        # 3.计算总距离
        totalDistance = 0.0
        for i in range(self.k):
            totalDistance += nearest[i][1]
        # 4.汇总K邻近用户的评分
        for i in range(self.k):
            weight = nearest[i][1] / totalDistance
            # 获取用户名称
            name = nearest[i][0]
            # 获取用户评分
            neighborRatings = self.data[name]
            # 获得没有评价过的商品
            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist]*weight)
                    else:
                        recommendations[artist] = (recommendations[artist] + neighborRatings[artist]*weight)
        # 开始推荐
        recommendations = list(recommendations.items())
        recommendations = [(self.convertProductID2name(k), v) for (k, v) in recommendations]
        # 排序返回
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        # 返回前n个结果
        return recommendations[:self.n]

r = recommender({})
r.loadBookDB('../chapter-2-rs/')
print(r.recommend('171118'))

