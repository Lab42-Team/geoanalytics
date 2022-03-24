import re
import pyproj
import shapely
import shapely.wkb
import shapely.wkt
from pyproj import Geod
from shapely import ops
from shapely.geometry import Point
from shapely.ops import cascaded_union
from shapely.errors import WKBReadingError
from datetime import datetime
from Levenshtein._levenshtein import distance
import geoanalytics.utility as utl
import geoanalytics.preprocess as gp


def reproject(geom):
    """
    Препроекция геометрических данных в геодезические величины.
    :param geom: геометрическая фигура в радианах
    :return: геометрическая фигура в метрах
    """
    wgs84 = pyproj.CRS("EPSG:4326")
    utm = pyproj.CRS("EPSG:3857")
    project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform

    return ops.transform(project, geom)


def get_area(polygon):
    """
    Получение площади полигона в квадратных киллометрах.
    :param polygon: полигон
    :return: площадь полигона в квадратных киллометрах
    """
    geodesic_measure = Geod(ellps="WGS84")
    area_in_square_meters = abs(geodesic_measure.geometry_area_perimeter(polygon)[0])
    area_in_square_kilometers = area_in_square_meters / 1e6

    return area_in_square_kilometers


def get_distance(fires_shape, second_shape):
    """
    Получение расстояния между двумя геометрическими фигурами (полигонами).
    :param fires_shape: первая геометрическая фигура
    :param second_shape: вторая геометрическая фигура
    :return: расстояние в километрах
    """
    first_shape_in_meters = reproject(fires_shape)
    second_shape_in_meters = reproject(second_shape)
    distance_in_meters = first_shape_in_meters.distance(second_shape_in_meters)
    distance_in_kilometers = distance_in_meters / 1e6

    return distance_in_kilometers


def get_min_distance(fire_polygon, geom_dict):
    """
    Получение минимального расстояния от текущего полигона с пожаром до некоторого географическим объекта.
    :param fire_polygon: полигон с пожаром
    :param geom_dict: словарь с географическим объектом в WKB
    :return: минимальное расстояния от пожара до географического объекта
    """
    min_distance = 99999
    for geom_item in geom_dict.values():
        try:
            geom_polygon = shapely.wkb.loads(geom_item["geom"], hex=True)
            current_distance = get_distance(fire_polygon, geom_polygon)
            if min_distance > current_distance:
                min_distance = current_distance
        except WKBReadingError:
            print("Не удалось создать геометрию из-за ошибок при чтении.")

    return "{:.3f}".format(min_distance)


def determine_area_and_distances(fires_dict, car_roads_dict, railways_dict, rivers_dict, lakes_dict):
    """
    Определение площади полигонов с пожарами, а также расстояний от пожаров до
    автомобильных и железных дорог, рек и озер.
    :param fires_dict: словарь с данными по пожарам
    :param car_roads_dict: словарь с данными по автомобильным дорогам
    :param railways_dict: словарь с данными по железным дорогам
    :param rivers_dict: словарь с данными по рекам
    :param lakes_dict: словарь с данными по озерам
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    for fire_item in fires_dict.values():
        start_time = datetime.now()
        # Получение полигона пожара
        fire_polygon = shapely.wkt.loads(fire_item["geometry"])
        # Получение площади полигона пожара
        fire_polygon_area = get_area(fire_polygon)
        fire_item["area"] = "{:.3f}".format(fire_polygon_area)
        # Получение минимального расстояния текущего полигона с пожаром до автомобильной дороги
        fire_item["distance_to_car_road"] = get_min_distance(fire_polygon, car_roads_dict)
        # Получение минимального расстояния текущего полигона с пожаром до железной дороги
        fire_item["distance_to_railway"] = get_min_distance(fire_polygon, railways_dict)
        # # Получение минимального расстояния текущего полигона с пожаром до реки
        # fire_item["distance_to_river"] = get_min_distance(fire_polygon, rivers_dict)
        # Получение минимального расстояния текущего полигона с пожаром до озера
        fire_item["distance_to_lake"] = get_min_distance(fire_polygon, lakes_dict)
        print(str(fire_item["new_fire_id"]) + ": " + str(datetime.now() - start_time))
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def determine_average_population_density(fires_dict, population_density_dict):
    """
    Определение средней плотности населения попадающих в область (полигон) пожара,
    а также муниципальные образования, затронутые пожарами.
    :param fires_dict: словарь с данными по пожарам
    :param population_density_dict: словарь с данными по плотности населения
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    for fire_item in fires_dict.values():
        # Получение полигона пожара
        fire_polygon = shapely.wkb.loads(fire_item["poly"], hex=True)
        municipalities = ""
        average_population_density = 0
        full_population_density = 0
        counter = 0
        for population_density_item in population_density_dict.values():
            try:
                # Получение полигона муниципального образования
                population_density_polygon = shapely.wkb.loads(population_density_item["geom"], hex=True)
                # Если есть пересечение полигона пожара с полигоном муниципального образования
                if fire_polygon.intersects(population_density_polygon):
                    if municipalities == "":
                        municipalities = population_density_item["name"]
                    else:
                        municipalities += ", " + population_density_item["name"]
                    try:
                        full_population_density += float(population_density_item["population_density_2016"])
                    except ValueError:
                        print("Не удалось преобразовать строку в число с плавающей запятой.")
                    counter += 1
            except WKBReadingError:
                print("Не удалось создать геометрию из-за ошибок при чтении.")
        # Вычисление средней плотности населения
        if counter != 0:
            average_population_density = full_population_density / counter
        # Формирование данных по муниципальным образованиям и средней плотности населения
        fire_item["municipalities"] = municipalities
        fire_item["average_population_density"] = average_population_density
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def determine_intersection_with_forestry(fires_dict, forestry_dict):
    """
    Определение лесничеств, которые были затронуты пожарами.
    :param fires_dict: словарь с данными по пожарам
    :param forestry_dict: словарь с данными по лесничествам
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    for fire_item in fires_dict.values():
        # Получение полигона пожара
        fire_polygon = shapely.wkb.loads(fire_item["poly"], hex=True)
        forestry = ""
        for forestry_item in forestry_dict.values():
            try:
                # Получение полигона лесничества
                forestry_polygon = shapely.wkb.loads(forestry_item["geom"], hex=True)
                # Если есть пересечение полигона пожара с полигоном лесничества
                if fire_polygon.intersects(forestry_polygon):
                    if forestry == "":
                        forestry = forestry_item["frname"]
                    else:
                        forestry += ", " + forestry_item["frname"]
            except WKBReadingError:
                print("Не удалось создать геометрию из-за ошибок при чтении.")
        # Формирование данных по лесничествам
        fire_item["forestry"] = forestry
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def determine_nearest_weather_station(fires_dict, weather_stations_dict):
    """
    Определение ближайших к пожарам метеостанций.
    :param fires_dict: словарь с данными по пожарам
    :param weather_stations_dict: словарь с данными по метеостанциям
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    for fire_item in fires_dict.values():
        weather_stations = dict()
        # Получение точки пожара по координатам
        fire_point = Point(float(fire_item["lat"]), float(fire_item["lon"]))
        # Определение расстояния от метеостанции к текущему пожару по координатам
        for geom_item in weather_stations_dict.values():
            try:
                # Получение точки метеостанции по координатам
                weather_station_point = Point(float(geom_item["latitude"]), float(geom_item["longitude"]))
                # Формирование словаря расстояний до метеостанций
                weather_stations[fire_point.distance(weather_station_point)] = [int(geom_item["weather_station_id"]),
                                                                                geom_item["weather_station_name"]]
            except WKBReadingError:
                print("Не удалось создать геометрию из-за ошибок при чтении.")
        # Сортировка метеостанций по расстояниям
        weather_stations = dict(sorted(weather_stations.items(), key=lambda item: item[0]))
        # Обход метеостанций
        for weather_station in weather_stations.values():
            exist_weather_station = False
            # Получение списка csv-файлов с информацией о погоде из каталога "weather_data"
            weather_file_list = gp.get_csv_file_list(gp.WEATHER_DIR_NAME)
            # Обход списка csv-файлов с информацией о погоде
            for weather_file_name in weather_file_list:
                # Если csv-файл относится к искомой метеостанции
                if weather_file_name.find(str(weather_station[0])) != -1:
                    exist_weather_station = True
            exist_weather_conditions_station = False
            # Получение списка csv-файлов с информацией о погоде из каталога "kp_po_forcast"
            weather_conditions_file_list = gp.get_csv_file_list(gp.WEATHER_CONDITIONS_DIR_NAME)
            # Обход списка csv-файлов с информацией о погоде
            for weather_conditions_file_name in weather_conditions_file_list:
                # Если csv-файл относится к искомой метеостанции
                if weather_conditions_file_name.find(str(weather_station[0])) != -1:
                    exist_weather_conditions_station = True
            if exist_weather_station and exist_weather_conditions_station:
                # Формирование данных по метеостанции
                fire_item["weather_station_id"] = int(weather_station[0])
                fire_item["weather_station_name"] = weather_station[1]
                break

    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def determine_forest_hazard_classes(fires_dict, forest_districts_dict, forest_hazard_classes_dict):
    """
    Определение классов опасности лесов на основе лесных кварталов, которые были затронуты пожарами.
    :param fires_dict: словарь с данными по пожарам
    :param forest_districts_dict: словарь с данными по лесным кварталам
    :param forest_hazard_classes_dict: словарь с данными по классам опасностей лесов
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    defined_hazard_class_number = 0
    fire_number = 0
    for fire_item in fires_dict.values():
        start_time = datetime.now()
        fire_number += 1
        # Получение полигона пожара
        fire_polygon = shapely.wkb.loads(fire_item["poly"], hex=True)
        forest_districts = ""
        forest_hazard_classes = []
        flag = []
        for forest_district_item in forest_districts_dict.values():
            try:
                # Получение полигона лесного квартала
                forest_district_polygon = shapely.wkb.loads(forest_district_item["geom"], hex=True)
                # Если есть пересечение полигона пожара с полигоном лесного квартала
                if fire_polygon.intersects(forest_district_polygon):
                    fd_municipality = forest_district_item["name_in"]
                    fd_forest_plot = forest_district_item["uch_l_ru"]
                    fd_dacha = forest_district_item["dacha_ru"]
                    fd_kv = forest_district_item["kv"]

                    # Формирование строки с лесными кварталами затронутых пожарами
                    if forest_districts == "":
                        forest_districts = str([fd_municipality, fd_forest_plot, fd_dacha, fd_kv])
                    else:
                        forest_districts += ", " + str([fd_municipality, fd_forest_plot, fd_dacha, fd_kv])

                    #
                    if str(fd_municipality) != "nan":
                        fd_municipality = re.sub(r"[-']", "", fd_municipality)
                        fd_municipality = fd_municipality.lower()
                    else:
                        flag.append(3)
                    if str(fd_forest_plot) != "nan":
                        fd_forest_plot = re.sub(r"[-']", "", fd_forest_plot)
                        fd_forest_plot = fd_forest_plot.lower()
                    else:
                        flag.append(5)
                    if str(fd_dacha) != "nan":
                        fd_dacha = re.sub(r"[-']", "", fd_dacha)
                        fd_dacha = fd_dacha.lower()
                    else:
                        flag.append(7)

                    if str(fd_municipality) != "nan" and str(fd_forest_plot) != "nan" and str(fd_dacha) != "nan":
                        exist_municipality = False
                        exist_forest_plot = False
                        exist_dacha = False
                        exist_kv = False

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

                            if fhc_municipality == fd_municipality:
                                exist_municipality = True
                            if fhc_forest_plot == fd_forest_plot:
                                exist_forest_plot = True
                            if fhc_dacha == fd_dacha:
                                exist_dacha = True

                            # Вычисление расстояния Левенштейна
                            levenshtein_distance_for_municipality = distance(fhc_municipality, fd_municipality)
                            # Вычисление расстояния Левенштейна
                            levenshtein_distance_for_forest_plot = distance(fhc_forest_plot, fd_forest_plot)
                            # Вычисление расстояния Левенштейна
                            levenshtein_distance_for_dacha = distance(fhc_dacha, fd_dacha)
                            total_levenshtein_distance = levenshtein_distance_for_municipality + \
                                                         levenshtein_distance_for_forest_plot + \
                                                         levenshtein_distance_for_dacha
                            if total_levenshtein_distance < 4:
                                for forest_district_number in forest_hazard_classes_item["forest_districts"]:
                                    if str(fd_kv) and str(forest_district_number):
                                        if int(forest_district_number) == int(fd_kv):
                                            # Формирование списка определенных классов опасности лесов
                                            forest_hazard_classes.append(str(forest_hazard_classes_item["hazard_class"]))
                                            flag.append(0)
                                            exist_kv = True

                        if not exist_kv:
                            flag.append(1)
                        if not exist_municipality:
                            flag.append(2)
                        if not exist_forest_plot:
                            flag.append(4)
                        if not exist_dacha:
                            flag.append(6)
            except WKBReadingError:
                print("Не удалось создать геометрию из-за ошибок при чтении.")
            except UnicodeEncodeError:
                print("Проблема с кодировкой.")

        # Формирование данных по лесным кварталам
        fire_item["kv"] = forest_districts
        # Формирование данных по классам опасности лесов
        if forest_hazard_classes:
            fire_item["forest_hazard_classes"] = str(forest_hazard_classes)
            defined_hazard_class_number += 1
            print("Классы опасности: " + fire_item["forest_hazard_classes"])

        fire_item["flag"] = str(flag)

        print(str(fire_item["fire_id"]) + ": " + str(datetime.now() - start_time))

    # Вычисление точности определения класса опасности
    accuracy = defined_hazard_class_number / fire_number
    print("Accuracy: " + str(accuracy))

    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def determine_hazard_classes_by_weather(fires_dict):
    """
    Определение класса пожарной опасности по условиям погоды.
    :param fires_dict: словарь с данными по пожарам
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    for fire_item in fires_dict.values():
        start_time = datetime.now()
        weather_conditions_dict = dict()
        # Получение списка csv-файлов с информацией по погодным условиям (прогноз погоды)
        weather_conditions_list = gp.get_csv_file_list(gp.WEATHER_CONDITIONS_DIR_NAME)
        # Обход списка csv-файлов с информацией по погодным условиям (прогноз погоды)
        for weather_conditions_file_name in weather_conditions_list:
            # Если csv-файл относится к искомой метеостанции
            if weather_conditions_file_name.find(str(fire_item["weather_station_id"])) != -1:
                # Получение данных по погодным условиям (прогноз погоды)
                weather_conditions_csv_data = gp.get_csv_data(weather_conditions_file_name,
                                                              gp.WEATHER_CONDITIONS_DIR_NAME)
                weather_conditions_dict = gp.get_weather_conditions_dict(weather_conditions_csv_data)
        if weather_conditions_dict:
            weather_datetime = []
            for weather_conditions_item in weather_conditions_dict.values():
                weather_datetime.append(datetime.strptime(str(weather_conditions_item["datetime"]),
                                                          "%Y-%m-%d %H:%M:%S"))
            nearest_datetime = utl.nearest(weather_datetime, datetime.strptime(fire_item["dt"], "%d.%m.%Y %H:%M"))
            for weather_conditions_item in weather_conditions_dict.values():
                if datetime.strptime(weather_conditions_item["datetime"], "%Y-%m-%d %H:%M:%S") == nearest_datetime:
                    # Определение класса опасности
                    fire_item["weather_hazard_class"] = ""
                    if float(weather_conditions_item["kp"]) <= 300:
                        fire_item["weather_hazard_class"] = "I"
                    if 301 <= float(weather_conditions_item["kp"]) <= 1000:
                        fire_item["weather_hazard_class"] = "II"
                    if 1001 <= float(weather_conditions_item["kp"]) <= 4000:
                        fire_item["weather_hazard_class"] = "III"
                    if 4001 <= float(weather_conditions_item["kp"]) <= 10000:
                        fire_item["weather_hazard_class"] = "IV"
                    if float(weather_conditions_item["kp"]) > 10000:
                        fire_item["weather_hazard_class"] = "V"
                    print("Класс опасности: " + fire_item["weather_hazard_class"])
        else:
            print("Класс опасности не определен!")
        print(str(fire_item["new_fire_id"]) + ": " + str(datetime.now() - start_time))
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def determine_forest_types(fires_dict, forest_districts_dict, forest_types_dict):
    """
    Определение классов опасности лесов на основе лесных кварталов, которые были затронуты пожарами.
    :param fires_dict: словарь с данными по пожарам
    :param forest_districts_dict: словарь с данными по лесным кварталам
    :param forest_types_dict: словарь с данными по типам лесов
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    defined_type_number = 0
    fire_number = 0
    for fire_item in fires_dict.values():
        start_time = datetime.now()
        fire_number += 1
        # Получение полигона пожара
        fire_polygon = shapely.wkb.loads(fire_item["poly"], hex=True)
        forest_districts = ""
        forest_zones = []
        forest_seed_zoning_zones = []
        for forest_district_item in forest_districts_dict.values():
            try:
                # Получение полигона лесного квартала
                forest_district_polygon = shapely.wkb.loads(forest_district_item["geom"], hex=True)
                # Если есть пересечение полигона пожара с полигоном лесного квартала
                if fire_polygon.intersects(forest_district_polygon):
                    fd_municipality = forest_district_item["name_in"]
                    fd_forest_plot = forest_district_item["uch_l_ru"]
                    fd_dacha = forest_district_item["dacha_ru"]
                    fd_kv = forest_district_item["kv"]

                    # Формирование строки с лесными кварталами затронутых пожарами
                    if forest_districts == "":
                        forest_districts = str([fd_municipality, fd_forest_plot, fd_dacha, fd_kv])
                    else:
                        forest_districts += ", " + str([fd_municipality, fd_forest_plot, fd_dacha, fd_kv])

                    if str(fd_municipality) != "nan":
                        fd_municipality = re.sub(r"[-']", "", fd_municipality)
                        fd_municipality = fd_municipality.lower()
                    if str(fd_forest_plot) != "nan":
                        fd_forest_plot = re.sub(r"[-']", "", fd_forest_plot)
                        fd_forest_plot = fd_forest_plot.lower()
                    if str(fd_dacha) != "nan":
                        fd_dacha = re.sub(r"[-']", "", fd_dacha)
                        fd_dacha = fd_dacha.lower()

                    if str(fd_municipality) != "nan" and str(fd_forest_plot) != "nan" and str(fd_dacha) != "nan" and \
                            str(fd_kv) != "nan":
                        # Обход данных по типам лесов
                        for forest_types_item in forest_types_dict.values():
                            fhc_municipality = forest_types_item["name_in"]
                            fhc_forest_plot = forest_types_item["uch_l_ru"]
                            fhc_dacha = forest_types_item["dacha_ru"]

                            if str(fhc_municipality) != "nan":
                                fhc_municipality = forest_types_item["name_in"]
                                fhc_municipality = re.sub(r"[-']", "", fhc_municipality)
                                fhc_municipality = fhc_municipality.lower()

                            if str(fhc_forest_plot) != "nan":
                                fhc_forest_plot = forest_types_item["uch_l_ru"]
                                fhc_forest_plot = re.sub(r"[-']", "", fhc_forest_plot)
                                fhc_forest_plot = fhc_forest_plot.lower()

                            if str(fhc_dacha) != "nan":
                                fhc_dacha = forest_types_item["dacha_ru"]
                                fhc_dacha = re.sub(r"[-']", "", fhc_dacha)
                                fhc_dacha = fhc_dacha.lower()

                            if str(fhc_municipality) != "nan" and str(fhc_forest_plot) != "nan" and \
                                    str(fhc_dacha) != "nan":
                                # Вычисление расстояния Левенштейна
                                levenshtein_distance_for_municipality = distance(fhc_municipality, fd_municipality)
                                # Вычисление расстояния Левенштейна
                                levenshtein_distance_for_forest_plot = distance(fhc_forest_plot, fd_forest_plot)
                                # Вычисление расстояния Левенштейна
                                levenshtein_distance_for_dacha = distance(fhc_dacha, fd_dacha)
                                total_levenshtein_distance = levenshtein_distance_for_municipality + \
                                                             levenshtein_distance_for_forest_plot + \
                                                             levenshtein_distance_for_dacha
                                if total_levenshtein_distance < 4:
                                    for forest_type_number in forest_types_item["kv"]:
                                        if str(fd_kv) and str(forest_type_number) and str(forest_type_number) != "nan":
                                            if int(forest_type_number) == int(fd_kv):
                                                # Формирование списка определенных типов лесов
                                                forest_zones.append(str(forest_types_item["forest_zone"]))
                                                forest_seed_zoning_zones.append(str(
                                                    forest_types_item["forest_seed_zoning_zone"]))
            except WKBReadingError:
                print("Не удалось создать геометрию из-за ошибок при чтении.")
            except UnicodeEncodeError:
                print("Проблема с кодировкой в строке.")

        # Формирование данных по типам лесов
        if forest_zones:
            fire_item["forest_zone"] = str(forest_zones)
            defined_type_number += 1
            print("forest_zone: " + fire_item["forest_zone"])
        if forest_seed_zoning_zones:
            fire_item["forest_seed_zoning_zones"] = str(forest_seed_zoning_zones)
            defined_type_number += 1
            print("forest_seed_zoning_zones: " + fire_item["forest_seed_zoning_zones"])

        print(str(fire_item["fire_id"]) + ": " + str(datetime.now() - start_time))

    # Вычисление точности определения
    accuracy = defined_type_number / fire_number
    print("Accuracy: " + str(accuracy))

    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def determine_snowiness(fires_dict, snowiness_dict):
    """
    Определение снежности зимы по метеостанции.
    :param fires_dict: словарь с данными по пожарам
    :param snowiness_dict: словарь с данными по снегу
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    for fire_item in fires_dict.values():
        start_time = datetime.now()
        # Получение даты и времени пожара
        fire_datetime = datetime.strptime(fire_item["dt"], "%d.%m.%Y %H:%M")
        # Обход данных по снегу
        for snowiness_item in snowiness_dict.values():
            # Если сходятся номера метеостанций
            if int(fire_item["weather_station_id"]) == int(snowiness_item["station_id"]):
                # Получение даты и времени окончания зимы
                end_datetime = datetime.strptime(snowiness_item["end"], "%Y-%m-%d")
                # Если дата и время пожара попадает за определенный год
                if fire_datetime.year == end_datetime.year:
                    # Определение снежности зимы в зависимости от процентов
                    fire_item["snowiness"] = ""
                    if float(snowiness_item["percent"]) < -25:
                        fire_item["snowiness"] = "малоснежная"
                    if -25 <= float(snowiness_item["percent"]) <= 25:
                        fire_item["snowiness"] = "норма"
                    if float(snowiness_item["percent"]) > 25:
                        fire_item["snowiness"] = "многоснежная"
                    if 90 <= float(snowiness_item["percent"]) <= 100:
                        fire_item["snowiness"] = "норма"
                    print("Снежность зимы: " + fire_item["snowiness"])
        print(str(fire_item["new_fire_id"]) + ": " + str(datetime.now() - start_time))
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def determine_dry_thunderstorm(fires_dict):
    """
    Определение сухой грозы по погодным условиям для каждого пожара.
    :param fires_dict: словарь с данными по пожарам
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    for fire_item in fires_dict.values():
        start_time = datetime.now()
        weather_dict = dict()
        # Получение списка csv-файлов с информацией по метеостанциям (погоде)
        weather_file_list = gp.get_csv_file_list(gp.WEATHER_DIR_NAME)
        # Обход списка csv-файлов с информацией по метеостанциям (погоде)
        for weather_file_name in weather_file_list:
            # Если csv-файл относится к искомой метеостанции
            if weather_file_name.find(str(fire_item["weather_station_id"])) != -1:
                # Получение данных по метеостанции (погоде)
                weather_csv_data = gp.get_csv_data(weather_file_name, gp.WEATHER_DIR_NAME)
                weather_dict = gp.get_weather_dict(weather_csv_data)
        fire_item["thunderstorm"] = ""
        # Получение даты и времени пожара
        fire_datetime = datetime.strptime(fire_item["dt"], "%d.%m.%Y %H:%M")
        # Обход по данным метеостанции (погоде)
        for weather_item in weather_dict.values():
            # Получение даты и времени замера погоды
            weather_datetime = datetime.strptime(weather_item["datetime"], "%d.%m.%Y %H:%M")
            # Если дата пожара совпадает с датой замера погоды
            if fire_datetime.date() == weather_datetime.date():
                # Объединение условий погоды в одну строку
                weather_string = str(weather_item["WW"]).lower() + str(weather_item["W1"]).lower() + \
                                 str(weather_item["W2"]).lower()
                # Поиск слова "гроза" без частей "дожд" и "ливень" в строке
                if weather_string.find("гроза") != -1 and weather_string.find("дожд") == -1 and \
                        weather_string.find("ливень") == -1:
                    # Формирование значения "сухая гроза" если нет осадков
                    if str(weather_item["RRR"]).lower().find("осадков нет") != -1 or str(weather_item["RRR"]) == "nan":
                        fire_item["thunderstorm"] = "сухая гроза"
        print(str(fire_item["new_fire_id"]) + ": " + str(datetime.now() - start_time))
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def identify_fire(fires_dict):
    """
    Идентификация пожаров на основе пересечения их полигонов.
    :param fires_dict: словарь с данными по пожарам (со старыми fire_id)
    :return: новый словарь с данными по пожарам (с новыми new_fire_id)
    """
    start_full_time = datetime.now()
    index = 1
    for current_key, current_item in fires_dict.items():
        start_time = datetime.now()
        shape1 = shapely.wkb.loads(current_item["poly"], hex=True)
        intersection = list()
        for key, item in fires_dict.items():
            if key > current_key:
                shape2 = shapely.wkb.loads(item["poly"], hex=True)
                if shape1.intersects(shape2):
                    if current_item["new_fire_id"] == "":
                        intersection.append(key)
                    if current_item["new_fire_id"] != "" and item["new_fire_id"] == "":
                        item["new_fire_id"] = current_item["new_fire_id"]
        number = index
        for key, item in fires_dict.items():
            if key > current_key:
                for value in intersection:
                    if key == value and item["new_fire_id"] != "":
                        if number != index and number != item["new_fire_id"]:
                            print("Обнаружены разные индексы")
                        number = item["new_fire_id"]
        for key, item in fires_dict.items():
            if key > current_key:
                for value in intersection:
                    if key == value:
                        item["new_fire_id"] = number
        if current_item["new_fire_id"] == "":
            current_item["new_fire_id"] = number
            index += 1
        print(str(current_item["new_fire_id"]) + ": " + str(datetime.now() - start_time))
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def delete_fire_by_technogenic_object(fires_dict, not_fires_dict):
    """
    Удаление пожаров пересекающихся с полигонами не пожаров (техногенными объектами).
    :param fires_dict: словарь с данными по пожарам
    :param not_fires_dict: словарь с данными по не пожарам (техногенным объектам)
    :return: новый словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    # Вычисление пожаров, полигоны которых пересекаются с полигонами не пожаров
    intersection = list()
    for fire_key, fire_item in fires_dict.items():
        start_time = datetime.now()
        shape1 = shapely.wkb.loads(fire_item["poly"], hex=True)
        for not_fire_key, not_fire_item in not_fires_dict.items():
            shape2 = shapely.wkb.loads(not_fire_item["WKB"], hex=True)
            if shape1.intersects(shape2):
                for key, item in fires_dict.items():
                    if item["new_fire_id"] == fire_item["new_fire_id"]:
                        if key not in intersection:
                            intersection.append(key)
                break
        print(str(fire_item["id"]) + ": " + str(datetime.now() - start_time))
    # Удаление пожаров
    for key in intersection:
        fires_dict.pop(key)
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def delete_fire_by_locality(fires_dict, locality_dict):
    """
    Удаление пожаров пересекающихся с полигонами населенных пунктов.
    :param fires_dict: словарь с данными по пожарам
    :param locality_dict: словарь с данными по населенным пунктам
    :return: новый словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    # Вычисление пожаров, полигоны которых пересекаются с полигонами населенных пунктов
    intersection = list()
    for fire_key, fire_item in fires_dict.items():
        start_time = datetime.now()
        shape1 = shapely.wkt.loads(fire_item["geometry"])
        for locality_key, locality_item in locality_dict.items():
            if int(locality_item["locality"]) == 1:
                shape2 = shapely.wkt.loads(locality_item["poly_wkt"])
                if shape1.intersects(shape2):
                    for key, item in fires_dict.items():
                        if item["new_fire_id"] == fire_item["new_fire_id"]:
                            if key not in intersection:
                                intersection.append(key)
                    break
        print(str(fire_item["id"]) + ": " + str(datetime.now() - start_time))
    # Удаление пожаров
    for key in intersection:
        fires_dict.pop(key)
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def delete_fire_by_forest_district(fires_dict, forest_districts_dict):
    """
    Удаление пожаров не пересекающихся с полигонами лесных кварталов.
    :param fires_dict: словарь с данными по пожарам
    :param forest_districts_dict: словарь с данными по лесным кварталам
    :return: новый словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    # Вычисление пожаров не пересекающихся с лесными кварталами
    not_intersection = list()
    for fire_key, fire_item in fires_dict.items():
        start_time = datetime.now()
        shape1 = shapely.wkb.loads(fire_item["poly"], hex=True)
        intersection = False
        for forest_district_key, forest_district_item in forest_districts_dict.items():
            try:
                shape2 = shapely.wkb.loads(forest_district_item["geom"], hex=True)
                if shape1.intersects(shape2):
                    intersection = True
                    break
            except WKBReadingError:
                print("Не удалось создать геометрию из-за ошибок при чтении.")
            except UnicodeEncodeError:
                print("Проблема с кодировкой в строке: " + str(forest_district_key))
        if not intersection:
            for key, item in fires_dict.items():
                if item["new_fire_id"] == fire_item["new_fire_id"]:
                    if key not in not_intersection:
                        not_intersection.append(key)
        print(str(fire_item["id"]) + ": " + str(datetime.now() - start_time))
    # Удаление пожаров
    for key in not_intersection:
        fires_dict.pop(key)
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def delete_fire(fires_dict):
    """
    Отбор пожаров по первой дате их появления (все остальные записи пожаров кроме первой удалаются).
    :param fires_dict: словарь с данными по пожарам
    :return: новый словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    # Вычисление лишних пожаров
    saved_fires = dict()
    deleted_fires = []
    for key, item in fires_dict.items():
        if item["new_fire_id"] in saved_fires:
            deleted_fires.append(key)
        else:
            saved_fires[item["new_fire_id"]] = key
    # Удаление пожаров
    for key in deleted_fires:
        fires_dict.pop(key)
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def delete_winter_fires(fires_dict):
    """
    Удаление пожаров не входящих в пожароопасный период (зимний период).
    :param fires_dict: словарь с данными по пожарам
    :return: новый словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    deleted_fires = []
    for current_key, current_item in fires_dict.items():
        start_time = datetime.now()
        current_date_str = current_item["dt"].split(" ")[0]
        current_date_obj = datetime.strptime(current_date_str, "%d.%m.%Y")
        if current_date_obj < datetime.strptime("01.04.2019", "%d.%m.%Y"):
            exist_intersection = False
            for key, item in fires_dict.items():
                date_str = item["dt"].split(" ")[0]
                date_obj = datetime.strptime(date_str, "%d.%m.%Y")
                if date_obj >= datetime.strptime("01.04.2019", "%d.%m.%Y"):
                    shape1 = shapely.wkt.loads(current_item["geometry"])
                    shape2 = shapely.wkt.loads(item["geometry"])
                    if shape1.intersects(shape2):
                        exist_intersection = True
            if not exist_intersection:
                deleted_fires.append(current_key)
            print(str(current_item["new_fire_id"]) + ": " + str(datetime.now() - start_time))
    # Удаление пожаров
    for key in deleted_fires:
        fires_dict.pop(key)
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def identify_fire_by_dates(fires_dict):
    start_full_time = datetime.now()
    index = 1
    for current_key, current_item in fires_dict.items():
        start_time = datetime.now()
        for key, item in fires_dict.items():
            if key > current_key:
                current_date_str = current_item["dt"].split(" ")[0]
                current_date_obj = datetime.strptime(current_date_str, "%d.%m.%Y")
                date_str = item["dt"].split(" ")[0]
                date_obj = datetime.strptime(date_str, "%d.%m.%Y")
                days = abs((date_obj - current_date_obj).days)
                if days <= 1 or (2 < days < 10):
                    shape1 = shapely.wkb.loads(current_item["poly"], hex=True)
                    shape2 = shapely.wkb.loads(item["poly"], hex=True)
                    if shape1.intersects(shape2):
                        if current_item["new_fire_id"] == "":
                            item["new_fire_id"] = index
                        else:
                            item["new_fire_id"] = current_item["new_fire_id"]
                else:
                    break
        if current_item["new_fire_id"] == "":
            current_item["new_fire_id"] = index
            index += 1
        print(str(current_item["new_fire_id"]) + ": " + str(datetime.now() - start_time))
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict


def define_gaps_in_days(fires_dict):
    for key1, item1 in fires_dict.items():
        for key2, item2 in fires_dict.items():
            if key2 > key1:
                date1_str = item1["dt"].split(" ")[0]
                date1_obj = datetime.strptime(date1_str, "%d.%m.%Y")
                date2_str = item2["dt"].split(" ")[0]
                date2_obj = datetime.strptime(date2_str, "%d.%m.%Y")
                days = abs((date2_obj - date1_obj).days)
                if days > 2:
                    print("Days: " + str(days) + " Dates: " + item1["dt"] + " - " + item2["dt"])
                break


def get_polygon_intersection(fires_dict):
    for item1 in fires_dict.values():
        if item1["fire_id"] == 24:
            for item2 in fires_dict.values():
                if item2["fire_id"] == 24:
                    shape1 = shapely.wkb.loads(item1["poly"], hex=True)
                    shape2 = shapely.wkb.loads(item2["poly"], hex=True)
                    print(shape1.intersects(shape2))


def union_polygons(fires_dict):
    polygons = []
    for item1 in fires_dict.values():
        if item1["fire_id"] == 24:
            shape = shapely.wkb.loads(item1["poly"], hex=True)
            shape_area = get_area(shape)
            print("Geodesic area: {:.3f} km^2".format(shape_area))
            polygons.append(shape)
    combined_polygon = cascaded_union(polygons)
    combined_area = get_area(combined_polygon)
    print("Geodesic combined area: {:.3f} km^2".format(combined_area))


def testing(file_data):
    geometry1 = None
    geometry2 = None
    for index, row in file_data.iterrows():
        if row["fire_id"] == 2:
            print(row["id"])
            if geometry1 is None:
                geometry1 = row["poly"]
        if row["fire_id"] == 8:
            print(row["id"])
            if geometry2 is None:
                geometry2 = row["poly"]
    shape1 = shapely.wkb.loads(geometry1, hex=True)
    shape2 = shapely.wkb.loads(geometry2, hex=True)
    print(shape1.intersects(shape2))

    area1 = get_area(shape1)
    print("Geodesic area 1: {:.3f} km^2".format(area1))
    area2 = get_area(shape2)
    print("Geodesic area 2: {:.3f} km^2".format(area2))

    polygons = [shape1, shape2]
    combined_polygon = cascaded_union(polygons)
    combined_area = get_area(combined_polygon)
    print("Geodesic combined area: {:.3f} km^2".format(combined_area))

    distance = get_distance(shape1, shape2)
    print("Geodesic distance: {:.3f} km".format(distance))
