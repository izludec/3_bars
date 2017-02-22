import json
import math
from urllib.request import urlopen


def load_data(filepath):
    bars_from_url = urlopen(filepath)
    bar_json = json.loads(bars_from_url.read().decode("utf-8"))
    print(json.dumps(
    bar_json, sort_keys=True, indent=4, ensure_ascii=False))
    return list(bar_json)


def get_biggest_bar(bar_list):
    list_biggest_bars = []
    for bars in list(bar_list):
        if bars["Cells"]["SeatsCount"] == \
        list(bar_list)[-1]["Cells"]["SeatsCount"]:
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
        x_diff = (longitude-bars["Cells"]["geoData"]["coordinates"][0])*63
        y_diff = (latitude-bars["Cells"]["geoData"]["coordinates"][1])*111
        distance = (math.sqrt((x_diff**2)+(y_diff**2)))
        if distance < min_distance and distance != 0:
            min_distance = distance
            min_distance_bar = i
    list_closest_bar.append(list(bar_list)[min_distance_bar]["Cells"]["Name"])
    list_closest_bar.append(min_distance)
    return list_closest_bar


def get_version():
    url_version = "http://api.data.mos.ru/version"
    version = urlopen(url_version)
    version = json.loads(version.read().decode("utf-8"))["Version"]
    return version


def get_id():
    url_bars_id = "http://api.data.mos.ru/v{version}/datasets".format(
        version = str(get_version()))
    json_bars_id = urlopen(url_bars_id)
    bars_id = json.loads(json_bars_id.read().decode("utf-8"))
    for bars in bars_id:
        bars_dataset = list(bars.values())
        for names in bars_dataset:
            if names == "Бары":
                return bars["Id"]
    return None


if __name__ == '__main__':
    url_bars_list = "http://api.data.mos.ru/"+\
    "v{0}/datasets/{1}/rows?$orderby=SeatsCount".format(
        str(get_version()), 
        str(get_id()))
    bar_list = load_data(url_bars_list)
    biggest_bars = get_biggest_bar(bar_list)
    smallest_bars = get_smallest_bar(bar_list)
    longitude = 32
    #float(input("Input longitude"))
    latitude = 55
    #float(input("Input latitude"))
    closest_bar = get_closest_bar(bar_list, longitude, latitude)
    print()
    print()
    print("Biggest bar")
    print("-------------------------------")
    for bars in biggest_bars:
        print(bars)
    print("-------------------------------")
    print()
    print()
    print("Smallest bar")
    print("-------------------------------")
    for bars in smallest_bars:
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
