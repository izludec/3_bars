import json
import math
from urllib.request import urlopen


def load_data(filepath):
    bars_from_url = urlopen(filepath)
    bar_json = json.loads(bars_from_url.read().decode("utf-8"))
    return list(bar_json)


def get_biggest_bar(bar_list):
    return max(bar_list, 
    key = lambda bar: bar["Cells"]["SeatsCount"])["Cells"]["Name"]


def get_smallest_bar(bar_list):
    return min(bar_list, 
    key = lambda bar: bar["Cells"]["SeatsCount"])["Cells"]["Name"]


def get_closest_bar(bar_list, longitude, latitude):
    min_distance = float(50000)
    distance = 0
    min_distance_bar = 0
    list_closest_bar = []
    for i, bars in enumerate(bar_list):
        x_diff = (longitude-bars["Cells"]["geoData"]["coordinates"][0])*63
        y_diff = (latitude-bars["Cells"]["geoData"]["coordinates"][1])*111
        distance = (math.sqrt((x_diff**2)+(y_diff**2)))
        if distance < min_distance and distance != 0:
            min_distance = distance
            min_distance_bar = i
    list_closest_bar.append(bar_list[min_distance_bar]["Cells"]["Name"])
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
    longitude = float(input("Input longitude"))
    latitude = float(input("Input latitude"))
    closest_bar = get_closest_bar(bar_list, longitude, latitude)
    print()
    print()
    print("Biggest bar")
    print("-------------------------------")
    print(biggest_bars)
    print("-------------------------------")
    print()
    print()
    print("Smallest bar")
    print("-------------------------------")
    print(smallest_bars)
    print("-------------------------------")
    print()
    print()
    print("Closest bar")
    print("-------------------------------")
    km = "%.3f" % closest_bar[1]
    print(closest_bar[0]+"  ---  "+km+" км.")
    print()
    print()
