import math


def calculate_evaluation(mapp):
    emptyWeight = 10
    maxnumWeight = 1.0
    smoothWeight = 0.1

    return emptyWeight * calculate_empty(mapp) + maxnumWeight * calculate_maxnum(
        mapp) + smoothWeight * calculate_smoothness(mapp)


def calculate_predictions(mapp):
    """计算未来一步的预测得分情况"""

    tmp = 0
    for i in range(4):
        for j in range(4):
            if j + 1 <= 3 and mapp[i][j] == mapp[i][j + 1]:
                tmp += mapp[i][j]
            elif j - 1 >= 0 and mapp[i][j] == mapp[i][j - 1]:
                tmp += mapp[i][j]
            elif i + 1 <= 3 and mapp[i][j] == mapp[i + 1][j]:
                tmp += mapp[i][j]
            elif i - 1 >= 0 and mapp[i][j] == mapp[i - 1][j]:
                tmp += mapp[i][j]
    return tmp


def calculate_empty(mapp):
    """计算空方块数：空方块越多说明局势越好"""
    empty = 0
    for i in range(4):
        for j in range(4):
            if mapp[i][j] == 0:
                empty += 1
    return empty


def calculate_maxnum(mapp):
    """计算最大数：最大数越大说明局势越好"""
    maxnum = 0
    for i in range(4):
        for j in range(4):
            maxnum = max(maxnum, mapp[i][j])
    return maxnum


def calculate_smoothness(mapp):
    """计算平滑度：计算每个方块向下方和右方的差值作为平滑度的标准"""

    smoothness = 0
    for i in range(4):
        for j in range(4):
            if mapp[i][j] != 0:
                val = math.log2(mapp[i][j]+1)
                # if i - 1 >= 0:
                #     smoothness -= abs(math.log2(mapp[i-1][j])-val)
                if i + 1 <= 3:
                    smoothness -= abs(math.log2(mapp[i + 1][j]+1) - val)
                # if j - 1 >= 0:
                #     smoothness -= abs(math.log2(mapp[i][j-1])-val)
                if j + 1 <= 3:
                    smoothness -= abs(math.log2(mapp[i][j + 1]+1) - val)
    return smoothness
