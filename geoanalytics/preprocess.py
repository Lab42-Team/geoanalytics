import pandas as pd
from pathlib import Path


def save_new_csv_file(target_dict):
    """
    Сохранение целевого словаря в формате CSV.
    :param target_dict: целевой словарь
    """
    df = pd.DataFrame.from_dict(target_dict, orient="index")
    df.to_csv("data.csv", sep=";", index_label="id")


def get_csv_data(csv_file_name):
    """
    Получение данных из csv-файла электронной таблицы.
    :param csv_file_name: название csv-файла электронной таблицы с расширением
    :return: набор данных
    """
    file_data = None
    # Формирование полного пути к csv-файлу электронной таблицы
    csv_file = Path(Path.cwd().parent, "examples", csv_file_name)
    # Если указанный csv-файл существует
    if csv_file.exists():
        try:
            file_data = pd.DataFrame(pd.read_csv(csv_file, sep=";", header=0, index_col=False))
        except pd.errors.EmptyDataError:
            print("Файл электронной таблицы пуст!")
    else:
        print("Файла электронной таблицы не существует!")

    return file_data


def get_fires_list(fires_csv_data):
    """
    Получение словаря с необходимой информацией по пожарам из данных csv-файла электронной таблицы.
    :param fires_csv_data: данные csv-файла электронной таблицы по пажарам
    :return: словарь с информацией по пожарам
    """
    result = dict()
    for index, row in fires_csv_data.iterrows():
        item = dict()
        item["fire_id"] = row["fire_id"]
        item["dt"] = row["dt"]
        item["lat"] = row["lat"]
        item["lon"] = row["lon"]
        item["poly"] = row["poly"]
        result[row["id"]] = item

    return result


def get_car_roads_list(car_roads_csv_data):
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


def get_railways_list(railways_csv_data):
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


def get_rivers_list(rivers_csv_data):
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


def get_lakes_list(lakes_csv_data):
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


def get_population_density_list(population_density_csv_data):
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
