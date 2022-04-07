import re
import shapely
import shapely.wkb
import shapely.wkt
import haversine as hs
from shapely.errors import WKBReadingError
from datetime import datetime
from Levenshtein._levenshtein import distance


def determine_hazard_classes_for_forest_districts(forest_districts_dict, forest_hazard_classes_dict):
    """
    Определение классов опасности лесов для лесных кварталов.
    :param forest_districts_dict: словарь с данными по лесным кварталам
    :param forest_hazard_classes_dict: словарь с данными по классам опасностей лесов
    :return: дополненный словарь с данными по лесным кварталам
    """
    start_full_time = datetime.now()
    forest_district_index = 0
    defined_hazard_class_number = 0
    # Обход лесных кварталов
    for forest_district_item in forest_districts_dict.values():
        start_time = datetime.now()
        forest_hazard_classes = []
        forest_district_index += 1
        fd_municipality = forest_district_item["name_in"]
        fd_forest_plot = forest_district_item["uch_l_ru"]
        fd_dacha = forest_district_item["dacha_ru"]
        fd_kv = forest_district_item["kv"]
        if str(fd_municipality) != "nan":
            fd_municipality = re.sub(r"[-']", "", fd_municipality)
            fd_municipality = fd_municipality.lower()
        if str(fd_forest_plot) != "nan":
            fd_forest_plot = re.sub(r"[-']", "", fd_forest_plot)
            fd_forest_plot = fd_forest_plot.lower()
        if str(fd_dacha) != "nan":
            fd_dacha = re.sub(r"[-']", "", fd_dacha)
            fd_dacha = fd_dacha.lower()
        if str(fd_municipality) != "nan" and str(fd_forest_plot) != "nan" and str(fd_dacha) != "nan":
            # Обход данных по классам опасностей лесов
            for forest_hazard_classes_item in forest_hazard_classes_dict.values():
                fhc_municipality = forest_hazard_classes_item["municipality"]
                fhc_municipality = re.sub(r"[-']", "", fhc_municipality)
                fhc_municipality = fhc_municipality.lower()
                fhc_forest_plot = forest_hazard_classes_item["forest_plot"]
                fhc_forest_plot = re.sub(r"[-']", "", fhc_forest_plot)
                fhc_forest_plot = fhc_forest_plot.lower()
                fhc_dacha = forest_hazard_classes_item["dacha"]
                fhc_dacha = re.sub(r"[-']", "", fhc_dacha)
                fhc_dacha = fhc_dacha.lower()
                # Вычисление расстояния Левенштейна
                levenshtein_distance_for_municipality = distance(fhc_municipality, fd_municipality)
                # Вычисление расстояния Левенштейна
                levenshtein_distance_for_forest_plot = distance(fhc_forest_plot, fd_forest_plot)
                # Вычисление расстояния Левенштейна
                levenshtein_distance_for_dacha = distance(fhc_dacha, fd_dacha)
                total_levenshtein_distance = levenshtein_distance_for_municipality + \
                                             levenshtein_distance_for_forest_plot + levenshtein_distance_for_dacha
                if total_levenshtein_distance < 4:
                    for forest_district_number in forest_hazard_classes_item["forest_districts"]:
                        if str(fd_kv) and str(forest_district_number):
                            if int(forest_district_number) == int(fd_kv):
                                # Формирование списка определенных классов опасности лесов
                                forest_hazard_classes.append(str(forest_hazard_classes_item["hazard_class"]))

        # Формирование данных по классам опасности лесов
        if forest_hazard_classes:
            forest_district_item["hazard_classes"] = str(forest_hazard_classes)
            defined_hazard_class_number += 1
            print("Классы опасности: " + forest_district_item["hazard_classes"])

        print("Строка " + str(forest_district_index) + ": " + str(datetime.now() - start_time))

    # Вычисление точности определения класса опасности
    accuracy = defined_hazard_class_number / forest_district_index
    print("Accuracy: " + str(accuracy))

    print("Full time: " + str(datetime.now() - start_full_time))

    return forest_districts_dict


def determine_nearest_weather_station_to_forest_district(forest_districts_processed_dict, weather_stations_dict):
    """
    Определение списка ближайших метеостанций к лесному кварталу.
    :param forest_districts_processed_dict: словарь с обработанными данными по лесным кварталам
    :param weather_stations_dict: словарь с данными по метеостанциям
    :return: дополненный словарь с обработанными данными по лесным кварталам
    """
    start_full_time = datetime.now()
    for forest_districts_item in forest_districts_processed_dict.values():
        weather_stations = dict()
        try:
            # Получение полигона лесного квартала
            shape = shapely.wkb.loads(forest_districts_item["geom"], hex=True)
            # Получение координат центра полигона
            shape_center = shape.centroid
            point1 = (shape_center.y, shape_center.x)
            # Обход данных по метеостанциям
            for weather_station_item in weather_stations_dict.values():
                # Получение точки метеостанции по координатам
                point2 = (float(weather_station_item["latitude"]), float(weather_station_item["longitude"]))
                # Формирование словаря расстояний до метеостанций в киллометрах
                weather_stations[int(weather_station_item["weather_station_id"])] = hs.haversine(point1, point2)
        except WKBReadingError:
            print("Не удалось создать геометрию из-за ошибок при чтении.")
        except UnicodeEncodeError:
            print("Проблема с кодировкой.")
        # Сортировка метеостанций по расстояниям
        weather_stations = dict(sorted(weather_stations.items(), key=lambda item: item[1]))
        print(weather_stations)
        # Формирование списка метеостанций строкой через запятую
        forest_districts_item["weather_stations"] = ",".join(map(str, list(weather_stations.keys())))
    print("Full time: " + str(datetime.now() - start_full_time))

    return forest_districts_processed_dict
