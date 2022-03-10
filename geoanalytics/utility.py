from datetime import datetime
import geoanalytics.preprocess as gp


def nearest(items, pivot):
    """
    Определение ближайшего элемента из items к элементу pivot.
    :param items: список элементов (например, datetime)
    :param pivot: элемент с которым сравнивается список
    :return: ближайший элемент из items к элементу pivot
    """
    return min(items, key=lambda x: abs(x - pivot))


def determine_weather_characteristics(fires_dict):
    """
    Определение характеристик погоды по метеостанциям.
    :param fires_dict: словарь с данными по пожарам
    :return: дополненный словарь с данными по пожарам
    """
    start_full_time = datetime.now()
    # Получение списка csv-файлов с информацией о погоде из каталога "weather_data"
    weather_file_list = gp.get_csv_file_list(gp.WEATHER_DIR_NAME)
    # Обход словаря с пожарами
    for fire_item in fires_dict.values():
        start_time = datetime.now()
        # Обход списка csv-файлов с информацией о погоде
        for weather_file_name in weather_file_list:
            # Поиск подстроки (номера метеостанции) в названии csv-файла электронной таблицы
            index = weather_file_name.find(str(fire_item["weather_station_id"]))
            # Если csv-файл относится к искомой метеостанции
            if index != -1:
                print(weather_file_name)
                # Определение строки с характеристиками погоды по ближайшей дате и времени с пожаром
                weather_csv_data = gp.get_csv_data(weather_file_name, gp.WEATHER_DIR_NAME)
                weather_dict = gp.get_weather_dict(weather_csv_data)
                weather_datetime = []
                for weather_item in weather_dict.values():
                    weather_datetime.append(datetime.strptime(str(weather_item["datetime"]), '%d.%m.%Y %H:%M'))
                nearest_datetime = nearest(weather_datetime, datetime.strptime(fire_item["dt"], '%d.%m.%Y %H:%M'))
                for weather_item in weather_dict.values():
                    if datetime.strptime(weather_item["datetime"], '%d.%m.%Y %H:%M') == nearest_datetime:
                        # Формирование характеристик по погоде
                        fire_item["RRR"] = weather_item["RRR"]
                        fire_item["Ff"] = weather_item["Ff"]
                        fire_item["U"] = weather_item["U"]
                        fire_item["T"] = weather_item["T"]
                        fire_item["Td"] = weather_item["Td"]
                        fire_item["DD"] = weather_item["DD"]
                        fire_item["WW"] = weather_item["WW"]
                        fire_item["W1"] = weather_item["W1"]
                        fire_item["W2"] = weather_item["W2"]
                        fire_item["Po"] = weather_item["Po"]
        print(str(fire_item["new_fire_id"]) + ": " + str(datetime.now() - start_time))
    print("***************************************************")
    print("Full time: " + str(datetime.now() - start_full_time))

    return fires_dict
