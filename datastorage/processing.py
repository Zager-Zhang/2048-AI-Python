import matplotlib.pyplot as plt
import numpy as np


def data_processing(path):

    plt.rcParams["font.sans-serif"] = ['Microsoft YaHei']
    plt.rcParams["axes.unicode_minus"] = False

    step, maxnum, score = np.loadtxt(path, unpack=True, delimiter=',', skiprows=1)
    dict = {'512': 0, '1024': 0, '2048': 0, '4096': 0, '8192': 0}
    for x in maxnum:
        dict[str(int(x))] += 1
    last = 0
    all = len(maxnum)
    for key in dict.keys():
        all -= last
        plt.bar(key, all)
        print(all/len(maxnum))
        last = dict[key]

    plt.title("2048AI算法数据统计")
    plt.ylabel("达成次数")
    plt.savefig("gamedata/results.png")
    plt.show()


if __name__ == '__main__':
    path = "gamedata/data2048.csv"
    data_processing(path)
