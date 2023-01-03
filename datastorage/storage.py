import csv
import os
import datetime

def mkdir(path):
    folder = os.path.exists(path)

    if not folder:
        os.makedirs(path)

    else:
        print("this folder is exists!")


def write_data(data):
    dir_path = "./datastorage/gamedata"
    mkdir(dir_path)

    with open(dir_path + "/data2048.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["id", "max_num", "score"])
        if len(data) == 1:
            writer.writerow(data)
        else:
            writer.writerows(data)


if __name__ == '__main__':
    a = [[1, 2048, 20020], [2, 4096, 60002]]
    now = datetime.datetime.now()
    print(now)
    write_data(a)
