from datetime import datetime

import geoanalytics.preprocess as gp
import geoanalytics.fire_processor as fp
import geoanalytics.forest_district_processor as fdp


if __name__ == '__main__':
    # Получение данных по пожарам
    fires_csv_data = gp.get_csv_data(gp.FIRE_CSV_FILE)
    fires_dict = gp.get_fires_dict(fires_csv_data)

    # # Определение новых идентификаторов для пожаров
    # result = fp.identify_fire(fires_dict)
    # gp.save_new_csv_file(result)
    # # Получение данных по не пожарам (техногенные объекты)
    # not_fires_csv_data = gp.get_csv_data(gp.NOT_FIRES_CSV_FILE)
    # not_fires_dict = gp.get_not_fires_dict(not_fires_csv_data)
    # # Удаление пожаров пересекающихся с полигонами не пожаров (техногенные объекты)
    # result = fp.delete_fire_by_technogenic_object(fires_dict, not_fires_dict)
    # gp.save_new_csv_file(result)
    # # Получение данных по населенным пунктам
    # locality_csv_data = gp.get_csv_data(gp.LOCALITIES_CSV_FILE)
    # locality_dict = gp.get_locality_dict(locality_csv_data)
    # # Удаление пожаров пересекающихся с полигонами населенных пунктов
    # result = fp.delete_fire_by_locality(fires_dict, locality_dict)

    # # Получение данных по лесным кварталам
    # forest_districts_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_CSV_FILE)
    # forest_districts_dict = gp.get_forest_districts_dict(forest_districts_csv_data)
    # # Удаление пожаров не пересекающихся с полигонами лесных кварталов
    # result = fp.delete_fire_by_forest_district(fires_dict, forest_districts_dict)

    # # Удаление всех записей одного пожара кроме первой
    # result = fp.delete_fire(fires_dict)

    # # Удаление пожаров не входящих в пожароопасный период (зимний период)
    # result = fp.delete_winter_fires(fires_dict)


    # # Получение данных по плотности населения
    # population_density_csv_data = gp.get_csv_data(gp.POPULATION_DENSITY_CSV_FILE)
    # population_density_dict = gp.get_population_density_dict(population_density_csv_data)
    # # Определение средней плотности населения
    # result = fp.determine_average_population_density(fires_dict, population_density_dict)

    # # Получение данных по лесничествам
    # forestry_csv_data = gp.get_csv_data(gp.FORESTRY_CSV_FILE)
    # forestry_dict = gp.get_forestry_dict(forestry_csv_data)
    # # Определение затронутых пожарами лесничеств
    # result = fp.determine_intersection_with_forestry(fires_dict, forestry_dict)

    # Получение данных по автомобильным дорогам
    car_roads_csv_data = gp.get_csv_data(gp.CAR_ROADS_CSV_FILE)
    car_roads_dict = gp.get_car_roads_dict(car_roads_csv_data)
    # Получение данных по железным дорогам
    railways_csv_data = gp.get_csv_data(gp.RAILWAYS_CSV_FILE)
    railways_dict = gp.get_railways_dict(railways_csv_data)
    # Получение данных по рекам
    rivers_csv_data = gp.get_csv_data(gp.RIVERS_CSV_FILE)
    rivers_dict = gp.get_rivers_dict(rivers_csv_data)
    # Получение данных по озерам
    lakes_csv_data = gp.get_csv_data(gp.LAKES_CSV_FILE)
    lakes_dict = gp.get_lakes_dict(lakes_csv_data)
    # # Определение недостающих характеристик (площади и расстояний)
    result = fp.determine_area_and_distances(fires_dict, car_roads_dict, railways_dict, rivers_dict, lakes_dict)

    # # Получение данных по метеостанциям
    # weather_stations_csv_data = gp.get_csv_data(gp.WEATHER_STATIONS_CSV_FILE)
    # weather_stations_dict = gp.get_weather_stations_dict(weather_stations_csv_data)
    # # Определение ближайших к пожарам метеостанций
    # fires_dict = fp.determine_nearest_weather_station_to_fire(fires_dict, weather_stations_dict)
    # # Определение характеристик погоды по метеостанции
    # result = fp.determine_weather_characteristics(fires_dict)

    # # Определение класса пожарной опасности по условиям погоды
    # result = fp.determine_hazard_classes_by_weather(fires_dict)

    # # Получение данных по лесным кварталам
    # forest_districts_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_CSV_FILE)
    # forest_districts_dict = gp.get_forest_districts_dict(forest_districts_csv_data)
    # # Получение данных по классам опасности лесов
    # forest_hazard_classes_csv_data = gp.get_csv_data(gp.FOREST_HAZARD_CLASSES_CSV_FILE)
    # forest_hazard_classes_dict = gp.get_forest_hazard_classes_dict(forest_hazard_classes_csv_data)
    # # Определение класса опасности лесов по лесным кварталам
    # result = fp.determine_hazard_classes_by_forest_districts(fires_dict, forest_districts_dict,
    #                                                          forest_hazard_classes_dict)

    # # Получение данных по лесным кварталам
    # forest_districts_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_CSV_FILE)
    # forest_districts_dict = gp.get_forest_districts_dict(forest_districts_csv_data)
    # # Получение данных по типам лесов
    # forest_types_csv_data = gp.get_csv_data(gp.FOREST_TYPES_PROCESSED_CSV_FILE)
    # forest_types_dict = gp.get_forest_types_dict(forest_types_csv_data)
    # # Определение типа лесов по лесным кварталам
    # result = fp.determine_forest_types(fires_dict, forest_districts_dict, forest_types_dict)

    # # Получение данных по снегу
    # snowiness_csv_data = gp.get_csv_data(gp.SNOWINESS_CSV_FILE)
    # snowiness_dict = gp.get_snowiness_dict(snowiness_csv_data)
    # # Определение снежности зимы по метеостанции
    # result = fp.determine_snowiness(fires_dict, snowiness_dict)

    # # Определение сухой грозы по погодным условиям
    # result = fp.determine_dry_thunderstorm(fires_dict)


    # # Получение данных по лесным кварталам
    # forest_districts_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_CSV_FILE)
    # forest_districts_dict = gp.get_forest_districts_dict(forest_districts_csv_data)
    # # Получение данных по классам опасности лесов
    # forest_hazard_classes_csv_data = gp.get_csv_data(gp.FOREST_HAZARD_CLASSES_CSV_FILE)
    # forest_hazard_classes_dict = gp.get_forest_hazard_classes_dict(forest_hazard_classes_csv_data)
    # # Определение класса опасности для лесных кварталов
    # result = ggu.determine_hazard_classes_for_forest_districts(forest_districts_dict, forest_hazard_classes_dict)

    # # Получение обработанных данных по лесным кварталам
    # forest_districts_processed_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_PROCESSED_CSV_FILE)
    # forest_districts_processed_dict = gp.get_forest_districts_processed_dict(forest_districts_processed_csv_data)
    # # Получение данных по метеостанциям
    # weather_stations_csv_data = gp.get_csv_data(gp.WEATHER_STATIONS_CSV_FILE)
    # weather_stations_dict = gp.get_weather_stations_dict(weather_stations_csv_data)
    # # Определение списка ближайших метеостанций к лесному кварталу
    # result = fdp.determine_nearest_weather_station_to_forest_district(forest_districts_processed_dict,
    #                                                                   weather_stations_dict)

    # # Получение обработанных данных по лесным кварталам
    # forest_districts_processed_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_PROCESSED_CSV_FILE)
    # forest_districts_processed_dict = gp.get_forest_districts_processed_dict(forest_districts_processed_csv_data)
    # # Задание целевой даты для поиска погоды
    # target_date = datetime.strptime("10.08.2020", "%d.%m.%Y").date()
    # # Определение характеристик погоды по метеостанции для лесных кварталов
    # result = fdp.determine_weather_characteristics_for_forest_district(forest_districts_processed_dict, target_date)

    # # Получение обработанных данных по лесным кварталам
    # forest_districts_processed_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_PROCESSED_CSV_FILE)
    # forest_districts_processed_dict = gp.get_forest_districts_processed_dict(forest_districts_processed_csv_data)
    # # Задание целевой даты для поиска погоды
    # target_date = datetime.strptime("10.08.2020", "%d.%m.%Y").date()
    # # Определение класса пожарной опасности по условиям погоды для лесных кварталов
    # result = fdp.determine_hazard_classes_by_weather_for_forest_district(forest_districts_processed_dict, target_date)

    # # Получение обработанных данных по лесным кварталам
    # forest_districts_processed_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_PROCESSED_CSV_FILE)
    # forest_districts_processed_dict = gp.get_forest_districts_processed_dict(forest_districts_processed_csv_data)
    # # Получение данных по снегу
    # snowiness_csv_data = gp.get_csv_data(gp.SNOWINESS_CSV_FILE)
    # snowiness_dict = gp.get_snowiness_dict(snowiness_csv_data)
    # # Задание целевого года для определения снежности зимы
    # target_year = datetime.strptime("10.08.2020", "%d.%m.%Y").year
    # # Определение снежности зимы по метеостанции для лесных кварталов
    # result = fdp.determine_snowiness_for_forest_district(forest_districts_processed_dict, snowiness_dict, target_year)

    # # Получение обработанных данных по лесным кварталам
    # forest_districts_processed_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_PROCESSED_CSV_FILE)
    # forest_districts_processed_dict = gp.get_forest_districts_processed_dict(forest_districts_processed_csv_data)
    # # Получение данных по типам лесов
    # forest_types_csv_data = gp.get_csv_data(gp.FOREST_TYPES_PROCESSED_CSV_FILE)
    # forest_types_dict = gp.get_forest_types_dict(forest_types_csv_data)
    # # Определение типа лесов для лесных кварталов
    # result = fdp.determine_forest_types_for_forest_district(forest_districts_processed_dict, forest_types_dict)

    # # Получение обработанных данных по лесным кварталам
    # forest_districts_processed_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_PROCESSED_CSV_FILE)
    # forest_districts_processed_dict = gp.get_forest_districts_processed_dict(forest_districts_processed_csv_data)
    # # Задание целевой даты для поиска погоды
    # target_date = datetime.strptime("10.08.2020", "%d.%m.%Y").date()
    # # Определение сухой грозы по погодным условиям для лесных кварталов
    # result = fdp.determine_dry_thunderstorm_for_forest_district(forest_districts_processed_dict, target_date)

    # loc_csv_data = gp.get_csv_data(gp.DATA_2020_V2)
    # loc_dict = gp.get_loc_dict(loc_csv_data)
    # result = fp.determine_loc(fires_dict, loc_dict)

    # Сохранение результатов в новом CSV-файле
    gp.save_new_csv_file(result)

    # # Тестирование
    # ggu.union_polygons(fires_dict)
    # ggu.get_polygon_intersection(fires_csv_data)
    # ggu.testing(fires_csv_data)
