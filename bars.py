import json
import math
from urllib.request import urlopen


def load_data(filepath):
    version = urlopen(filepath)
    data = json.loads(version.read().decode("utf-8"))
    return list(data)


def get_biggest_bar(data):
    list_biggest_bars = []
    for bars in list(data):
        if bars["Cells"]["SeatsCount"] == \
        list(data)[len(list(data))-1]["Cells"]["SeatsCount"]:
            list_biggest_bars.append(bars["Cells"]["Name"])
    return list_biggest_bars


def get_smallest_bar(data):
    list_smallest_bars = []
    for bars in list(data):
        if bars["Cells"]["SeatsCount"] == \
        list(data)[0]["Cells"]["SeatsCount"]:
            list_smallest_bars.append(bars["Cells"]["Name"])
    return list_smallest_bars


def get_closest_bar(data, longitude, latitude):
    min_dist = float(50000)
    distance = 0
    min_bar = 0
    list_closest_bar = []
    for i, bars in enumerate(list(data)):
        x_diff = longitude-bars["Cells"]["geoData"]["coordinates"][0]
        y_diff = latitude-bars["Cells"]["geoData"]["coordinates"][1]
        distance = (math.sqrt(x_diff*x_diff+y_diff*y_diff))*111
        if distance < min_dist and distance != 0:
            min_dist = distance
            min_bar = i
    list_closest_bar.append(list(data)[min_bar]["Cells"]["Name"])
    list_closest_bar.append(min_dist)
    return list_closest_bar


def get_version():
    UrlVersion = "http://api.data.mos.ru/version"
    version = urlopen(UrlVersion)
    version = json.loads(version.read().decode("utf-8"))["Version"]
    return version


def get_Id():
    urlBarsId = "http://api.data.mos.ru/v"+str(get_version())+"/datasets"
    jsonBarsId = urlopen(urlBarsId)
    barsId = json.loads(jsonBarsId.read().decode("utf-8"))
    for bars in barsId:
        value = list(bars.values())
        for names in value:
            if names == "Бары":
                return bars["Id"]
    return None


if __name__ == '__main__':
    UrlBarsList = "http://api.data.mos.ru/v"+str(get_version()) +\
        "/datasets"+"/"+str(get_Id())+"/"+"rows?$orderby=SeatsCount"
    bar_list = load_data(UrlBarsList)
    biggest_bar = get_biggest_bar(bar_list)
    smallest_bar = get_smallest_bar(bar_list)
    closest_bar = get_closest_bar(bar_list, 37.585283, 55.797827)
    print()
    print()
    print("Biggest bar")
    print("-------------------------------")
    for bars in biggest_bar:
        print(bars)
    print("-------------------------------")
    print()
    print()
    print("Smallest bar")
    print("-------------------------------")
    for bars in smallest_bar:
        print(bars)
    print("-------------------------------")
    print()
    print()
    print("Closest bar")
    print("-------------------------------")
    km = "%.3f" % closest_bar[1]
    print(closest_bar[0]+"  ---  "+km+" км.")
    print()
    print()
