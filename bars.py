import json
import math
from urllib.request import urlopen


def load_data(filepath):
    bars_from_url = urlopen(filepath)
    bar_json = json.loads(bars_from_url.read().decode("utf-8"))
    return list(bar_json)


def get_biggest_bar(bar_list):
    list_biggest_bars = []
    for bars in list(bar_list):
        if bars["Cells"]["SeatsCount"] == \
        list(bar_list)[len(list(bar_list))-1]["Cells"]["SeatsCount"]:
            list_biggest_bars.append(bars["Cells"]["Name"])
    return list_biggest_bars


def get_smallest_bar(bar_list):
    list_smallest_bars = []
    for bars in list(bar_list):
        if bars["Cells"]["SeatsCount"] == \
        list(bar_list)[0]["Cells"]["SeatsCount"]:
            list_smallest_bars.append(bars["Cells"]["Name"])
    return list_smallest_bars


def get_closest_bar(bar_list, longitude, latitude):
    min_distance = float(50000)
    distance = 0
    min_distance_bar = 0
    list_closest_bar = []
    for i, bars in enumerate(list(bar_list)):
        x_diff = longitude-bars["Cells"]["geoData"]["coordinates"][0]
        y_diff = latitude-bars["Cells"]["geoData"]["coordinates"][1]
        distance = (math.sqrt(x_diff*x_diff+y_diff*y_diff))*111
        if distance < min_distance and distance != 0:
            min_distance = distance
            min_distance_bar = i
    list_closest_bar.append(list(bar_list)[min_distance_bar]["Cells"]["Name"])
    list_closest_bar.append(min_distance)
    return list_closest_bar


def get_version():
    Url_Version = "http://api.data.mos.ru/version"
    version = urlopen(Url_Version)
    version = json.loads(version.read().decode("utf-8"))["Version"]
    return version


def get_Id():
    url_Bars_Id = "http://api.data.mos.ru/v"+str(get_version())+"/datasets"
    json_Bars_Id = urlopen(url_Bars_Id)
    bars_Id = json.loads(json_Bars_Id.read().decode("utf-8"))
    for bars in bars_Id:
        bars_dataset = list(bars.values())
        for names in bars_dataset:
            if names == "Бары":
                return bars["Id"]
    return None


if __name__ == '__main__':
    Url_Bars_List = "http://api.data.mos.ru/v"+str(get_version()) +\
        "/datasets"+"/"+str(get_Id())+"/"+"rows?$orderby=SeatsCount"
    bar_list = load_data(Url_Bars_List)
    biggest_bar = get_biggest_bar(bar_list)
    smallest_bar = get_smallest_bar(bar_list)
    longitude = float(input("Input longitude"))
    latitude = float(input("Input latitude"))
    closest_bar = get_closest_bar(bar_list, longitude, latitude)
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
