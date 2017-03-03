import json
import math
from urllib.request import urlopen

km_in_longtitude = 63
km_in_latitude = 111

def load_data(filepath):
    bars_from_url = urlopen(filepath)
    bar_json = json.loads(bars_from_url.read().decode("utf-8"))
    return list(bar_json)


def get_biggest_bar(bar_list):
    return max(bar_list, 
    key = lambda bar: bar["Cells"]["SeatsCount"])


def get_smallest_bar(bar_list):
    return min(bar_list, 
    key = lambda bar: bar["Cells"]["SeatsCount"])


def get_distance_to_bar(bar, longitude, latitude):
    x_diff = (longitude-bar["Cells"]["geoData"]["coordinates"][0])*km_in_longtitude
    y_diff = (latitude-bar["Cells"]["geoData"]["coordinates"][1])*km_in_latitude
    return (math.sqrt((x_diff**2)+(y_diff**2)))

def get_closest_bar(bar_list, longitude, latitude):
    return min(bar_list, 
    key = lambda bar: get_distance_to_bar(bar, longitude, latitude))



def get_version():
    url_version = "http://api.data.mos.ru/version"
    version = urlopen(url_version)
    version = json.loads(version.read().decode("utf-8"))["Version"]
    return version


def get_id():
    url_datasets = "http://api.data.mos.ru/v{version}/datasets".format(
        version = str(get_version()))
    raw_datasets = urlopen(url_datasets)
    all_datasets = json.loads(raw_datasets.read().decode("utf-8"))
    for company_id in all_datasets:
        for company_type in company_id.values():
            if company_type == "Бары":
                return company_id["Id"]
    return None


if __name__ == '__main__':
    url_bars_list = "{0}v{1}/datasets/{2}/{3}".format(
        "http://api.data.mos.ru/",
        str(get_version()), 
        str(get_id()),
        "rows?$orderby=SeatsCount")
    bar_list = load_data(url_bars_list)
    biggest_bar = get_biggest_bar(bar_list)
    smallest_bar = get_smallest_bar(bar_list)
    longitude = float(input("Input longitude  "))
    latitude = float(input("Input latitude  "))
    closest_bar = get_closest_bar(bar_list, longitude, latitude)
    print()
    print()
    print("Biggest bar")
    print("-------------------------------")
    print(biggest_bar["Cells"]["Name"])
    print("-------------------------------")
    print()
    print()
    print("Smallest bar")
    print("-------------------------------")
    print(smallest_bar["Cells"]["Name"])
    print("-------------------------------")
    print()
    print()
    print("Closest bar")
    print("-------------------------------")
    print(closest_bar["Cells"]["Name"])
    print()
    print()
