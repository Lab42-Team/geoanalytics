import pyproj
import shapely
import shapely.wkb
from pyproj import Geod
from shapely import ops
from shapely.errors import WKBReadingError


def nearest(items, pivot):
    """
    Определение ближайшего элемента из items к элементу pivot.
    :param items: список элементов (например, datetime)
    :param pivot: элемент с которым сравнивается список
    :return: ближайший элемент из items к элементу pivot
    """
    return min(items, key=lambda x: abs(x - pivot))


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


def get_min_distance(polygon, geom_dict):
    """
    Получение минимального расстояния от полигона до некоторого географическим объекта.
    :param polygon: полигон
    :param geom_dict: словарь с географическим объектом в WKB
    :return: минимальное расстояния от полигона до географического объекта
    """
    min_distance = 99999
    for geom_item in geom_dict.values():
        try:
            geom_polygon = shapely.wkb.loads(geom_item["geom"], hex=True)
            current_distance = get_distance(polygon, geom_polygon)
            if min_distance > current_distance:
                min_distance = current_distance
        except WKBReadingError:
            print("Не удалось создать геометрию из-за ошибок при чтении.")

    return "{:.3f}".format(min_distance)
