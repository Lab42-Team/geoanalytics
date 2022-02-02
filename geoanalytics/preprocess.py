import os
import math
import fnmatch
import pandas as pd
from pathlib import Path

# Каталоги с исходными данными
DATA_DIR_NAME = "data"
WEATHER_DIR_NAME = "weather_data"
# Названия исходных csv-файлов
FIRE_CSV_FILE = "data-2020.csv"  # "fires_in_region_2017.csv"
CAR_ROADS_CSV_FILE = "gis_bogdanov.dorogiavtomobiln.csv"
RAILWAYS_CSV_FILE = "gis_bogdanov.dorogizheleznyeb.csv"
RIVERS_CSV_FILE = "gis_bogdanov.rekibakalskiregi.csv"
LAKES_CSV_FILE = "gis_bogdanov.ozerabakalskireg.csv"
POPULATION_DENSITY_CSV_FILE = "gis_bogdanov.plotnostselskogo.csv"
FORESTRY_CSV_FILE = "user_schema.lestniche_3036.csv"
WEATHER_STATIONS_CSV_FILE = "user_schema.gidromed_3075.csv"
FOREST_DISTRICTS_CSV_FILE = "user_schema.lesnye_kv_3051.csv"
FOREST_HAZARD_CLASSES_CSV_FILE = "forest_hazard_classes.csv"
NOT_FIRES_CSV_FILE = "not_fires.csv"  # Данные по не пожарам
LOCALITIES_CSV_FILE = "localities.csv"  # Данные по населенным пунктам
# Название целевого (выходного) csv-файла
OUTPUT_FILE_NAME = "data.csv"


def get_csv_data(csv_file_name, subdir=None):
    """
    Получение данных из csv-файла электронной таблицы.
    :param csv_file_name: название csv-файла электронной таблицы с расширением
    :param subdir: название дополнительного каталога
    :return: набор данных
    """
    file_data = None
    # Формирование полного пути к csv-файлу электронной таблицы
    if subdir is None:
        csv_file = Path(Path.cwd().parent, DATA_DIR_NAME, csv_file_name)
    else:
        csv_file = Path(Path.cwd().parent, DATA_DIR_NAME, subdir, csv_file_name)
    # Если указанный csv-файл существует
    if csv_file.exists():
        try:
            file_data = pd.DataFrame(pd.read_csv(csv_file, sep=";", header=0, index_col=False))
        except pd.errors.EmptyDataError:
            print("Файл электронной таблицы пуст!")
    else:
        print("Файла электронной таблицы не существует!")

    return file_data


def get_csv_file_list(subdir):
    """
    Получение списка файлов из заданного каталога.
    :param subdir: название дополнительного каталога
    :return: список файлов с информацией по погоде
    """
    return [f for f in os.listdir(Path(Path.cwd().parent, DATA_DIR_NAME, subdir)) if fnmatch.fnmatch(f, "*.csv")]


def save_new_csv_file(target_dict):
    """
    Сохранение целевого словаря в формате CSV.
    :param target_dict: целевой словарь
    """
    df = pd.DataFrame.from_dict(target_dict, orient="index")
    df.to_csv(OUTPUT_FILE_NAME, sep=";", index_label="id")


def get_fires_dict(fires_csv_data):
    """
    Получение словаря с необходимой информацией по пожарам из данных csv-файла электронной таблицы.
    :param fires_csv_data: данные csv-файла электронной таблицы по пажарам
    :return: словарь с информацией по пожарам
    """
    result = dict()
    result_id = 1
    for index, row in fires_csv_data.iterrows():
        item = dict()
        item["id"] = row["id"]
        item["fire_id"] = row["fire_id"]
        # item["new_fire_id"] = ""  # Для обработки старого файла пожаров
        item["new_fire_id"] = row["new_fire_id"]
        item["dt"] = row["dt"]
        item["since"] = row["since"]
        item["lat"] = row["lat"]
        item["lon"] = row["lon"]
        item["poly"] = row["poly"]
        item["geometry"] = row["geometry"]
        result[result_id] = item
        result_id += 1

    return result


def get_not_fires_dict(not_fires_csv_data):
    """
    Получение словаря с необходимой информацией по не пожарам из данных csv-файла электронной таблицы.
    :param not_fires_csv_data: данные csv-файла электронной таблицы по не пажарам
    :return: словарь с информацией по не пожарам
    """
    result = dict()
    result_id = 1
    for index, row in not_fires_csv_data.iterrows():
        item = dict()
        item["id"] = row["id"]
        item["WKT"] = row["WKT"]
        item["WKB"] = row["WKB"]
        result[result_id] = item
        result_id += 1

    return result


def get_locality_dict(locality_csv_data):
    """
    Получение словаря с необходимой информацией по населенным пунктам из данных csv-файла электронной таблицы.
    :param locality_csv_data: данные csv-файла электронной таблицы по населенным пунктам
    :return: словарь с информацией по населенным пунктам
    """
    result = dict()
    result_id = 1
    for index, row in locality_csv_data.iterrows():
        item = dict()
        item["name"] = row["name"]
        item["type"] = row["type"]
        item["name_MO"] = row["name_MO"]
        item["code"] = row["code"]
        item["distance"] = row["distance"]
        item["ado"] = row["ado"]
        item["id"] = row["id"]
        item["query"] = row["query"]
        item["address"] = row["address"]
        item["geometry"] = row["geometry"]
        item["poly_wkt"] = row["poly_wkt"]
        item["poly"] = row["poly"]
        item["valid"] = row["valid"]
        item["locality"] = row["locality"]
        result[result_id] = item
        result_id += 1

    return result


def get_car_roads_dict(car_roads_csv_data):
    """
    Получение словаря с необходимой информацией по автомобильным дорогам из данных csv-файла электронной таблицы.
    :param car_roads_csv_data: данные csv-файла электронной таблицы по автомобильным дорогам
    :return: словарь с информацией по автомобильным дорогам
    """
    result = dict()
    for index, row in car_roads_csv_data.iterrows():
        item = dict()
        item["type"] = row["type"]
        item["geom"] = row["geom"]
        result[row["id"]] = item

    return result


def get_railways_dict(railways_csv_data):
    """
    Получение словаря с необходимой информацией по железным дорогам из данных csv-файла электронной таблицы.
    :param railways_csv_data: данные csv-файла электронной таблицы по железным дорогам
    :return: словарь с информацией по железным дорогам
    """
    result = dict()
    for index, row in railways_csv_data.iterrows():
        item = dict()
        item["geom"] = row["geom"]
        result[row["id"]] = item

    return result


def get_rivers_dict(rivers_csv_data):
    """
    Получение словаря с необходимой информацией по рекам из данных csv-файла электронной таблицы.
    :param rivers_csv_data: данные csv-файла электронной таблицы по рекам
    :return: словарь с информацией по рекам
    """
    result = dict()
    for index, row in rivers_csv_data.iterrows():
        item = dict()
        item["name"] = row["name"]
        item["geom"] = row["geom"]
        result[row["id"]] = item

    return result


def get_lakes_dict(lakes_csv_data):
    """
    Получение словаря с необходимой информацией по озерам из данных csv-файла электронной таблицы.
    :param lakes_csv_data: данные csv-файла электронной таблицы по озерам
    :return: словарь с информацией по озерам
    """
    result = dict()
    for index, row in lakes_csv_data.iterrows():
        item = dict()
        item["name"] = row["name"]
        item["geom"] = row["geom"]
        result[row["id"]] = item

    return result


def get_population_density_dict(population_density_csv_data):
    """
    Получение словаря с необходимой информацией по плотности населения из данных csv-файла электронной таблицы.
    :param population_density_csv_data: данные csv-файла электронной таблицы по плотности населения
    :return: словарь с информацией по плотности населения
    """
    result = dict()
    for index, row in population_density_csv_data.iterrows():
        item = dict()
        item["name"] = row["name"]
        item["population_density_2016"] = row["population_density_2016"]
        item["geom"] = row["geom"]
        result[row["id"]] = item

    return result


def get_forestry_dict(forestry_csv_data):
    """
    Получение словаря с необходимой информацией по лесничествам из данных csv-файла электронной таблицы.
    :param forestry_csv_data: данные csv-файла электронной таблицы по лесничествам
    :return: словарь с информацией по лесничествам
    """
    result = dict()
    for index, row in forestry_csv_data.iterrows():
        item = dict()
        item["oblname"] = row["oblname"]
        item["frname"] = row["frname"]
        item["geom"] = row["geom"]
        result[row["id"]] = item

    return result


def get_weather_stations_dict(weather_stations_csv_data):
    """
    Получение словаря с необходимой информацией по метеостанциям из данных csv-файла электронной таблицы.
    :param weather_stations_csv_data: данные csv-файла электронной таблицы по метеостанциям
    :return: словарь с информацией по метеостанциям
    """
    results = dict()
    for index, row in weather_stations_csv_data.iterrows():
        item = dict()
        number = float(row["sinopticheski_in"])
        if not math.isnan(number):
            weather_station_id_exist = False
            for result in results.values():
                if result["weather_station_id"] == row["sinopticheski_in"]:
                    weather_station_id_exist = True
            if weather_station_id_exist is False:
                item["weather_station_id"] = row["sinopticheski_in"]
                item["weather_station_name"] = row["imya_stancii"]
                item["latitude"] = row["shirota"]
                item["longitude"] = row["dolgota"]
                results[row["id"]] = item

    return results


def get_weather_dict(weather_csv_data):
    """
    Получение словаря с необходимой информацией по погоде из данных csv-файла электронной таблицы.
    :param weather_csv_data: данные csv-файла электронной таблицы по погоде
    :return: словарь с информацией по погоде
    """
    result = dict()
    result_id = 1
    for index, row in weather_csv_data.iterrows():
        item = dict()
        item["datetime"] = row[0]
        item["RRR"] = row["RRR"]
        item["Ff"] = row["Ff"]
        item["U"] = row["U"]
        item["T"] = row["T"]
        item["Td"] = row["Td"]
        result[result_id] = item
        result_id += 1

    return result


def get_forest_districts_dict(forest_districts_csv_data):
    """
    Получение словаря с необходимой информацией по лесным кварталам из данных csv-файла электронной таблицы.
    :param forest_districts_csv_data: данные csv-файла электронной таблицы по лесным кварталам
    :return: словарь с информацией по лесным кварталам
    """
    result = dict()
    result_id = 1
    for index, row in forest_districts_csv_data.iterrows():
        item = dict()
        item["name_in"] = row[0]
        item["dacha_ru"] = row[4]
        item["uch_l_ru"] = row[5]
        item["kv"] = row[11]
        item["geom"] = row[20]
        result[result_id] = item
        result_id += 1

    return result


def get_forest_hazard_classes_dict(forest_hazard_classes_csv_data):
    """
    Получение словаря с необходимой информацией по классам опасности лесов из данных csv-файла электронной таблицы.
    :param forest_hazard_classes_csv_data: данные csv-файла электронной таблицы по классам опасности лесов
    :return: словарь с информацией по классам опасности лесов
    """
    result = dict()
    result_id = 1
    for index, row in forest_hazard_classes_csv_data.iterrows():
        item = dict()
        item["municipality"] = row[0]
        item["forest_plot"] = row[1]
        item["dacha"] = row[2]
        item["forest_districts"] = str(row[3]).split(",")
        item["hazard_class"] = row[4]
        result[result_id] = item
        result_id += 1

    return result
