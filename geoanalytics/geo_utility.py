import pyproj
import shapely
import shapely.wkb
import shapely.wkt
from pyproj import Geod
from shapely import ops
from shapely.ops import cascaded_union
from shapely.errors import WKBReadingError


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
    for fire_item in fires_dict.values():
        # Получение полигона пожара
        fire_polygon = shapely.wkb.loads(fire_item["poly"], hex=True)
        # Получение площади полигона пожара
        fire_polygon_area = get_area(fire_polygon)
        fire_item["area"] = "{:.3f}".format(fire_polygon_area)
        # Получение минимального расстояния текущего полигона с пожаром до автомобильной дороги
        fire_item["distance_to_car_road"] = get_min_distance(fire_polygon, car_roads_dict)
        # Получение минимального расстояния текущего полигона с пожаром до железной дороги
        fire_item["distance_to_railway"] = get_min_distance(fire_polygon, railways_dict)
        # Получение минимального расстояния текущего полигона с пожаром до реки
        fire_item["distance_to_river"] = get_min_distance(fire_polygon, rivers_dict)
        # Получение минимального расстояния текущего полигона с пожаром до озера
        fire_item["distance_to_lake"] = get_min_distance(fire_polygon, lakes_dict)

    return fires_dict


def determine_average_population_density(fires_dict, population_density_dict):
    """
    Определение средней плотности населения попадающих в область (полигон) пожара,
    а также муниципальные образования, затронутые пожарами.
    :param fires_dict: словарь с данными по пожарам
    :param population_density_dict: словарь с данными по плотности населения
    :return: дополненный словарь с данными по пожарам
    """
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
                    full_population_density += float(population_density_item["population_density_2016"])
                    counter += 1
            except WKBReadingError:
                print("Не удалось создать геометрию из-за ошибок при чтении.")
        # Вычисление средней плотности населения
        if counter != 0:
            average_population_density = full_population_density / counter
        # Формирование данных по муниципальным образованиям и средней плотности населения
        fire_item["municipalities"] = municipalities
        fire_item["average_population_density"] = average_population_density

    return fires_dict


def get_polygon_intersection(fires_dict):
    for item1 in fires_dict.values():
        if item1["fire_id"] == 24:
            for item2 in fires_dict.values():
                if item2["fire_id"] == 24:
                    shape1 = shapely.wkb.loads(item1["poly"], hex=True)
                    shape2 = shapely.wkb.loads(item2["poly"], hex=True)
                    print(shape1.intersects(shape2))


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
