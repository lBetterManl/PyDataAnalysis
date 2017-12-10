# -*- coding: utf-8 -*-
#
# 将数据等分成十份的示例代码
import random

def toBeBuckets(filename, bucketName, separator, classColumn):
    """
    :param filename: 源文件名
    :param bucketName: 十个目标文件名的前缀
    :param separator: 分隔符
    :param classColumn: 数据所属分类那一列的序号
    :return:
    """

    # 将数据分为10份
    numberOfBuckets = 10
    data = {}
    # 读取数据，并按分类放置
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if separator != '\t':
            line = line.replace(separator, '\t')
        # 获取分类
        category = line.split()[classColumn]
        data.setdefault(category, [])
        data[category].append(line)
    # 初始化分桶
    buckets = []
    for i in range(numberOfBuckets):
        buckets.append([])
    # 将各个类别的数据均匀地放置到桶中
    for k in data.keys():
        # 打乱分类顺序
        random.shuffle(data[k])
        bNum = 0
        # 分桶
        for item in data[k]:
            buckets[bNum].append(item)
            bNum = (bNum+1) % numberOfBuckets

    # 写入文件
    for bNum in range(numberOfBuckets):
        f = open("%s-%02i" % (bucketName, bNum+1), 'w')
        for item in buckets[bNum]:
            f.write(item)
        f.close()

# 调用示例
toBeBuckets("pimaSmall.txt", 'pimaSmall', ',', 8)
