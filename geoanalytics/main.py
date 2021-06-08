import geoanalytics.preprocess as gp
import geoanalytics.geo_utility as ggu


FIRE_CSV_FILE = "fires_avh_3076_for_test.csv"
CAR_ROADS_CSV_FILE = "gis_bogdanov.dorogiavtomobiln.csv"
RAILWAYS_CSV_FILE = "gis_bogdanov.dorogizheleznyeb.csv"
RIVERS_CSV_FILE = "gis_bogdanov.rekibakalskiregi.csv"
LAKES_CSV_FILE = "gis_bogdanov.ozerabakalskireg.csv"
POPULATION_DENSITY_CSV_FILE = "gis_bogdanov.plotnostselskogo.csv"
FORESTRY_CSV_FILE = "user_schema.lestniche_3036.csv"


# Получение данных по пожарам
fires_csv_data = gp.get_csv_data(FIRE_CSV_FILE)
fires_dict = gp.get_fires_list(fires_csv_data)

# Получение данных по автомобильным дорогам
car_roads_csv_data = gp.get_csv_data(CAR_ROADS_CSV_FILE)
car_roads_dict = gp.get_car_roads_list(car_roads_csv_data)

# Получение данных по железным дорогам
railways_csv_data = gp.get_csv_data(RAILWAYS_CSV_FILE)
railways_dict = gp.get_railways_list(railways_csv_data)

# Получение данных по рекам
rivers_csv_data = gp.get_csv_data(RIVERS_CSV_FILE)
rivers_dict = gp.get_rivers_list(rivers_csv_data)

# Получение данных по озерам
lakes_csv_data = gp.get_csv_data(LAKES_CSV_FILE)
lakes_dict = gp.get_lakes_list(lakes_csv_data)

# Получение данных по плотности населения
population_density_csv_data = gp.get_csv_data(POPULATION_DENSITY_CSV_FILE)
population_density_dict = gp.get_population_density_list(population_density_csv_data)

# Получение данных по лесничествам
forestry_csv_data = gp.get_csv_data(FORESTRY_CSV_FILE)
forestry_dict = gp.get_forestry_list(forestry_csv_data)

# Определение недостающих характеристик (площади и расстояний)
# result = ggu.determine_area_and_distances(fires_dict, car_roads_dict, railways_dict, rivers_dict, lakes_dict)

# Определение средней плотности населения
# result = ggu.determine_average_population_density(fires_dict, population_density_dict)

# Определение затронутых пожарами лесничеств
result = ggu.determine_forestry(fires_dict, forestry_dict)
for item in result.values():
    print(item)

# Сохранение результатов в новом CSV-файле
gp.save_new_csv_file(result)

# ggu.get_polygon_intersection(fires_csv_data)
# ggu.testing(fires_csv_data)
