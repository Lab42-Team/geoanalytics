import geoanalytics.utility as utl
import geoanalytics.preprocess as gp
import geoanalytics.geo_utility as ggu


# Получение данных по пожарам
fires_csv_data = gp.get_csv_data(gp.FIRE_CSV_FILE)
fires_dict = gp.get_fires_dict(fires_csv_data)

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

# Получение данных по плотности населения
population_density_csv_data = gp.get_csv_data(gp.POPULATION_DENSITY_CSV_FILE)
population_density_dict = gp.get_population_density_dict(population_density_csv_data)

# Получение данных по лесничествам
forestry_csv_data = gp.get_csv_data(gp.FORESTRY_CSV_FILE)
forestry_dict = gp.get_forestry_dict(forestry_csv_data)

# Получение данных по метеостанциям
weather_stations_csv_data = gp.get_csv_data(gp.WEATHER_STATIONS_CSV_FILE)
weather_stations_dict = gp.get_weather_stations_dict(weather_stations_csv_data)

# Получение данных по лесным кварталам
forest_districts_csv_data = gp.get_csv_data(gp.FOREST_DISTRICTS_CSV_FILE)
forest_districts_dict = gp.get_forest_districts_dict(forest_districts_csv_data)

# Получение данных по классам опасности лесов
forest_hazard_classes_csv_data = gp.get_csv_data(gp.FOREST_HAZARD_CLASSES_CSV_FILE)
forest_hazard_classes_dict = gp.get_forest_hazard_classes_dict(forest_hazard_classes_csv_data)

# Определение недостающих характеристик (площади и расстояний)
# result = ggu.determine_area_and_distances(fires_dict, car_roads_dict, railways_dict, rivers_dict, lakes_dict)

# Определение средней плотности населения
# result = ggu.determine_average_population_density(fires_dict, population_density_dict)

# Определение затронутых пожарами лесничеств
# result = ggu.determine_intersection_with_forestry(fires_dict, forestry_dict)

# Определение ближайших к пожарам метеостанций
# fires_dict = ggu.determine_nearest_weather_station(fires_dict, weather_stations_dict)
# Определение характеристик погоды по метеостанциям
# result = utl.determine_weather_characteristics(fires_dict)

# Определение класса опасности лесов
result = ggu.determine_forest_hazard_classes(fires_dict, forest_districts_dict, forest_hazard_classes_dict)

# Сохранение результатов в новом CSV-файле
gp.save_new_csv_file(result)

# ggu.union_polygons(fires_dict)

# ggu.get_polygon_intersection(fires_csv_data)
# ggu.testing(fires_csv_data)
