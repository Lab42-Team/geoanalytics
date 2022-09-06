import os
import math
import fnmatch
import pandas as pd
from pathlib import Path


# Каталоги с исходными данными
DATA_DIR_NAME = "data"
WEATHER_DIR_NAME = "weather_data"
WEATHER_CONDITIONS_DIR_NAME = "kp_po_forcast"
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
FOREST_DISTRICTS_PROCESSED_CSV_FILE = "user_schema.lesnye_kv_3051_processed.csv"  # Обработанные данные по кварталам
FOREST_HAZARD_CLASSES_CSV_FILE = "forest_hazard_classes.csv"
NOT_FIRES_CSV_FILE = "not_fires.csv"  # Данные по не пожарам
LOCALITIES_CSV_FILE = "localities.csv"  # Данные по населенным пунктам
FOREST_TYPES_PROCESSED_CSV_FILE = "forest_types_processed.csv"  # Данные по видам лесов
SNOWINESS_CSV_FILE = "snowiness.csv"  # Данные по снегу
# Название целевого (выходного) csv-файла
OUTPUT_FILE_NAME = "data.csv"

DATA_2019_V2 = "data-2019-v2.csv"
DATA_2020_V2 = "data-2020-v2.csv"


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
        item["fire_id"] = row["fire_id"]
        # item["new_fire_id"] = ""  # Для обработки старого файла пожаров
        item["new_fire_id"] = row["new_fire_id"]
        item["dt"] = row["dt"]
        item["since"] = row["since"]
        item["lat"] = row["lat"]
        item["lon"] = row["lon"]
        item["poly"] = row["poly"]
        item["geometry"] = row["geometry"]
        # Поля для получения расширенной информации по пожарам
        item["municipalities"] = row["municipalities"]
        item["average_population_density"] = row["average_population_density"]
        item["forestry"] = row["forestry"]
        item["kv"] = row["kv"]
        item["forest_hazard_classes"] = row["forest_hazard_classes"]
        item["flag"] = row["flag"]
        item["forest_zone"] = row["forest_zone"]
        item["forest_seed_zoning_zones"] = row["forest_seed_zoning_zones"]
        item["weather_hazard_class"] = row["weather_hazard_class"]
        item["snowiness"] = row["snowiness"]
        item["snowiness-uncertainty"] = row["snowiness-uncertainty"]
        item["thunderstorm"] = row["thunderstorm"]
        item["distance_to_car_road"] = row["distance_to_car_road"]
        item["distance_to_lake"] = row["distance_to_lake"]
        item["area"] = row["area"]
        item["distance_to_railway"] = row["distance_to_railway"]
        # item["distance_to_river"] = row["distance_to_river"]  # Необходимо отключить, т.к. время подсчета очень большое
        item["weather_station_id"] = row["weather_station_id"]
        item["weather_station_name"] = row["weather_station_name"]
        item["RRR"] = row["RRR"]
        item["Ff"] = row["Ff"]
        item["U"] = row["U"]
        item["T"] = row["T"]
        item["Td"] = row["Td"]
        item["DD"] = row["DD"]
        item["WW"] = row["WW"]
        item["W1"] = row["W1"]
        item["W2"] = row["W2"]
        item["Po"] = row["Po"]
        # item["name_locality"] = row["name_locality"]
        # item["name_MO_locality"] = row["name_MO_locality"]
        # item["municipalities_locality"] = row["municipalities_locality"]
        # item["distance_to_locality"] = row["distance_to_locality"]
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
        item["DD"] = row["DD"]
        item["WW"] = row["WW"]
        item["W1"] = row["W1"]
        item["W2"] = row["W2"]
        item["Po"] = row["Po"]
        item["Tn"] = row["Tn"]
        item["Tx"] = row["Tx"]
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
        # Для исходного файла кварталов из ГИС
        item["name_in"] = row[0]
        item["dacha_ru"] = row[4]
        item["uch_l_ru"] = row[5]
        item["kv"] = row[11]
        item["geom"] = row[20]
        result[result_id] = item
        result_id += 1

    return result


def get_forest_districts_processed_dict(forest_districts_processed_csv_data):
    """
    Получение словаря с необходимой информацией по лесным кварталам из обработанных данных
    csv-файла электронной таблицы.
    :param forest_districts_processed_csv_data: обработанные данные csv-файла электронной таблицы по лесным кварталам
    :return: словарь с информацией по лесным кварталам (обработанные)
    """
    result = dict()
    result_id = 1
    for index, row in forest_districts_processed_csv_data.iterrows():
        item = dict()
        # Для обработанного файла кварталов
        item["name_in"] = row[1]
        item["dacha_ru"] = row[2]
        item["uch_l_ru"] = row[3]
        item["kv"] = row[4]
        item["geom"] = row[5]
        item["hazard_classes"] = row[6]

        string = str(row[7]).replace(" ", "")
        string = string.replace("'", "")
        string = string.replace("[", "")
        res_string = string.replace("]", "")
        item["weather_stations"] = res_string.split(",")

        item["RRR"] = row[8]
        item["Ff"] = row[9]
        item["U"] = row[10]
        item["Td"] = row[11]
        item["DD"] = row[12]
        item["WW"] = row[13]
        item["W1"] = row[14]
        item["W2"] = row[15]
        item["Po"] = row[16]
        item["Tn"] = row[17]
        item["Tx"] = row[18]
        item["Tx"] = row[18]
        item["weather_hazard_class"] = row[19]
        item["snowiness"] = row[20]
        item["forest_zone"] = row[21]
        item["forest_seed_zoning_zones"] = row[22]
        result[result_id] = item
        result_id += 1

    return result


def get_forest_types_dict(forest_types_csv_data):
    """
    Получение словаря с необходимой информацией по типам лесов из данных csv-файла электронной таблицы.
    :param forest_types_csv_data: данные csv-файла электронной таблицы по типам лесов
    :return: словарь с информацией по типам лесов
    """
    result = dict()
    result_id = 1
    for index, row in forest_types_csv_data.iterrows():
        item = dict()
        item["name_in"] = row[0]
        item["uch_l_ru"] = row[2]
        item["dacha_ru"] = row[3]
        item["forest_zone"] = row[4]
        item["forest_seed_zoning_zone"] = row[5]
        item["kv"] = str(row[6]).split(",")
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


def get_weather_conditions_dict(weather_conditions_csv_data):
    """
    Получение словаря с необходимой информацией по погодным условиям (прогнозу погоды).
    :param weather_conditions_csv_data: данные csv-файла электронной таблицы по погодным условиям (прогнозу погоды)
    :return: словарь с информацией по погодным условиям (прогнозу погоды)
    """
    result = dict()
    result_id = 1
    for index, row in weather_conditions_csv_data.iterrows():
        item = dict()
        item["datetime"] = row[3]
        item["kp"] = row[10]
        result[result_id] = item
        result_id += 1

    return result


def get_snowiness_dict(snowiness_csv_data):
    """
    Получение словаря с необходимой информацией по снегу.
    :param snowiness_csv_data: данные csv-файла электронной таблицы по снегу
    :return: словарь с информацией по снегу
    """
    result = dict()
    result_id = 1
    for index, row in snowiness_csv_data.iterrows():
        item = dict()
        item["station_id"] = row[0]
        item["start"] = row[2]
        item["end"] = row[3]
        item["percent"] = row[17]
        result[result_id] = item
        result_id += 1

    return result


def get_loc_dict(loc_csv_data):
    result = dict()
    result_id = 1
    for index, row in loc_csv_data.iterrows():
        item = dict()
        item["name_locality"] = row["name"]
        item["municipalities_locality"] = row["ado"]
        item["distance_to_locality"] = row["distance"]
        item["name_MO_locality"] = row["name_MO"]
        result[result_id] = item
        result_id += 1

    return result
