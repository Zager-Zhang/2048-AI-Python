import math


def calculate_evaluation(mapp):
    emptyWeight = 2.7 + (math.log(17)-math.log(calculate_empty(mapp)+1)) * 0.1
    maxnumWeight = 1.0
    smoothWeight = 0.1
    monoWeight = 1.0

    return emptyWeight * math.log(calculate_empty(mapp)+1) + maxnumWeight * calculate_maxnum(
        mapp) + smoothWeight * calculate_smoothness(mapp) + monoWeight * calculate_monotonicity(mapp)


def calculate_empty(mapp):
    """计算空方块数：空方块越多说明局势越好"""
    empty = 0
    for i in range(4):
        for j in range(4):
            if mapp[i][j] == 0:
                empty += 1
    return empty


def calculate_maxnum(mapp):
    """计算最大数：最大数越大说明局势越好 -> 冒险 """
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
                if i + 1 <= 3:
                    smoothness -= abs(math.log2(mapp[i + 1][j] + 1) - val)
                if j + 1 <= 3:
                    smoothness -= abs(math.log2(mapp[i][j + 1] + 1) - val)
                if i - 1 >= 0:
                    smoothness -= abs(math.log2(mapp[i - 1][j] + 1) - val)
                if j - 1 >= 0:
                    smoothness -= abs(math.log2(mapp[i][j - 1] + 1) - val)
    return smoothness


def calculate_monotonicity(mapp):
    """单调性"""
    totals = [0, 0, 0, 0]  # 四个方向的单调性评估

    for i in range(4):
        current = 0
        _next = current + 1
        while _next < 4:
            while _next < 4 and mapp[i][_next] == 0:
                _next += 1
            if _next >= 4:
                _next -= 1
            currentValue = math.log2(mapp[i][current]) if mapp[i][current] != 0 else 0
            nextValue = math.log2(mapp[i][_next]) if mapp[i][_next] != 0 else 0
            if currentValue > nextValue:
                totals[0] += nextValue - currentValue
            else:
                totals[1] += currentValue - nextValue
            current = _next
            _next += 1
    for i in range(4):
        current = 0
        _next = current + 1
        while _next < 4:
            while _next < 4 and mapp[_next][i] == 0:
                _next += 1
            if _next >= 4:
                _next -= 1
            currentValue = math.log2(
                mapp[current][i]) if mapp[current][i] != 0 else 0
            nextValue = math.log2(mapp[_next][i]) if mapp[_next][i] != 0 else 0
            if currentValue > nextValue:
                totals[2] += nextValue - currentValue
            else:
                totals[3] += currentValue - nextValue
            current = _next
            _next += 1
    return max(totals[:2]) + max(totals[2:])


def calculate_islands(mapp):
    """计算棋盘中连通块的个数代表 整个棋盘的分散度"""
    islands = 0
    marked = [[True for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            if mapp[i][j] != 0:
                marked[i][j] = False
    for i in range(4):
        for j in range(4):
            if mapp[i][j] != 0 and not marked[i][j]:
                islands += 1
                mark(mapp, i, j, mapp[i][j], marked)
    return islands


def mark(mapp, x, y, value, marked):
    if 0 <= x <= 3 and 0 <= y <= 3 and mapp[x][y] != 0 and mapp[x][y] == value and not marked[x][y]:
        marked[x][y] = True
        mark(mapp, x, y + 1, value, marked)
        mark(mapp, x, y - 1, value, marked)
        mark(mapp, x + 1, y, value, marked)
        mark(mapp, x - 1, y, value, marked)


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


if __name__ == '__main__':
    mapp = [[8, 4, 2, 0],
            [2, 4, 2, 0],
            [4, 4, 2, 0],
            [0, 0, 0, 0]]
    print(calculate_monotonicity(mapp))
