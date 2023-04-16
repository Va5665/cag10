import csv
from datetime import datetime
from json.decoder import JSONDecodeError

import requests
from tqdm import tqdm


class CagStatistics:
    """Базовый класс для работы с API CAG"""

    HEADERS = {
        "Authorization-Client": " Тут токен"
        "Content-Type": "application/json",
    }

    CAG_URL = "https://mediapi.mediatech.by"

    def __init__(self, page=0, size=20):
        self.page = page
        self.size = size

    all_content_url = CAG_URL + "/api/v1/services/1/contents-with-meta-info"
    local_content_url = CAG_URL + "/api/v1/stream/services/1/local/"

    json_response_all_content = {}
    current_date_time = datetime.now().strftime("%Y_%m_%d-%Hh%Mm%Ss")

    list_films_id_ok = []  # Список OK фильмов
    list_films_id_bad = []  # Список BAD фильмов

    list_episodes_id_ok = []  # Список OK серий
    list_episodes_id_bad = []  # Список BAD серий

    list_seasons_id_ok = []  # Список OK сезонов
    list_seasons_id_bad = []  # Список BAD сезонов

    list_serials_id_ok = []  # Список OK сериалов
    list_serials_id_bad = []  # Список BAD сериалов

    def get_all_content(self, page=None):
        if page is not None:
            data = {"number": page, "size": self.size}
        else:
            data = {"number": self.page, "size": self.size}

        response_all_content = requests.get(
            url=self.all_content_url, headers=self.HEADERS, params=data
        )
        status_code_response_all_content = response_all_content.status_code

        try:
            json_response_all_content = response_all_content.json()
            return json_response_all_content
        except JSONDecodeError:
            print(f"JSONDecodeError: code: {status_code_response_all_content}")

    def _get_serials(self, elements, type_content, name_content):
        # цикл по сериалам
        if type_content == "serial":
            id_series = elements["id"]  # id сериала
            seasons = elements["seasons"]

            # количество нерабочих сезонов в сериале
            list_season_id_bad_in_series = []
            for s in range(len(seasons)):
                season = seasons[s]
                series_in_season = season["episodes"]

                # количество нерабочих серий в СЕЗОНЕ
                list_episodes_id_bad_in_season = []
                for ser in range(len(season["episodes"])):
                    series = series_in_season[ser]
                    episode_name = series["name"]
                    episode_id = str(series["id"])
                    data = {"accountId": "1", "manifest": "all"}
                    response_local_content = requests.get(
                        url=self.local_content_url + episode_id,
                        headers=self.HEADERS,
                        params=data,
                    )
                    response_local_content_status_code = (
                        response_local_content.status_code
                    )

                    # кортеж с данными по серии
                    id_and_name_content_and_episode_name_and_code_response = (
                        episode_id,
                        name_content,
                        episode_name,
                        response_local_content_status_code,
                    )

                    # список рабочих серий ОБЩИЙ
                    if response_local_content_status_code == 200:
                        self.list_episodes_id_ok.append(
                            id_and_name_content_and_episode_name_and_code_response
                        )
                    else:
                        # список нерабочих серий в ОДНОМ СЕЗОНЕ
                        list_episodes_id_bad_in_season.append(
                            id_and_name_content_and_episode_name_and_code_response
                        )

                        # список нерабочих серий ОБЩИЙ
                        self.list_episodes_id_bad.append(
                            id_and_name_content_and_episode_name_and_code_response
                        )

                        # количество нерабочих СЕЗОНОВ В ОДНОМ СЕРИАЛЕ
                        list_season_id_bad_in_series.append(id_series)

                if len(list_episodes_id_bad_in_season):
                    # список нерабочих сезонов ОБЩИЙ
                    self.list_seasons_id_bad.append(season["id"])
                else:
                    self.list_seasons_id_ok.append(season["id"])

            if len(list_season_id_bad_in_series):
                # список нерабочих сериалов
                self.list_serials_id_bad.append((id_series, name_content))
            else:
                # список рабочих сериалов
                self.list_serials_id_ok.append(id_series)
                # print(f"рабочие сериалы{self.list_serials_id_ok}")

    def _get_films(self, elements, type_content, name_content):

        # цикл по фильмам
        if type_content == "film":
            content_id = elements["id"]
            data = {"accountId": "1", "manifest": "all"}
            response_local_content = requests.get(
                url=self.local_content_url + content_id,
                headers=self.HEADERS,
                params=data,
            )
            response_local_content_status_code = response_local_content.status_code
            id_and_name_content_and_episode_name_and_code_response = (
                content_id,
                name_content,
                response_local_content_status_code,
            )

            # список рабочих фильмов
            if response_local_content_status_code == 200:
                self.list_films_id_ok.append(
                    id_and_name_content_and_episode_name_and_code_response
                )

            else:
                # список нерабочих фильмов
                self.list_films_id_bad.append(
                    id_and_name_content_and_episode_name_and_code_response
                )



    def get_pages(self, json_all_content):
        # в этом методе происходит итерация по страницам общего списка контента
        total_pages = json_all_content["totalPages"]
        # total_pages = 1 для быстрого тестирования

        # tqdm задаёт шкалу прогресса
        for iter_page in tqdm(
                range(total_pages - self.page),
                desc=f"Всего страниц: {total_pages}. Начали с: {self.page} страницы. Осталось страниц",
        ):
            json_response_all_content = self.get_all_content(page=iter_page + self.page)
            len_list_content = len((json_response_all_content["elements"]))

            if len_list_content:
                for i in range(len_list_content):
                    elements = (json_response_all_content["elements"])[i]

                    if elements is not None:
                        type_content = elements["type"]
                        name_content = elements["name"]
                        self._get_films(elements, type_content, name_content)

            # запись результатов в csv файл
            with open(
                    "tests/results/" + str(self.current_date_time) + "-" + "statistics.csv",
                    mode="w",
                    encoding="utf-8",
            ) as w_file:
                file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r\n")
                file_writer.writerow(["Вид контента", "Количество"])
                file_writer.writerow(["Всего фильмов", len(self.list_films_id_ok + self.list_films_id_bad)])
                file_writer.writerow(["Всего фильмов с проблемами", len(self.list_films_id_bad)])
                file_writer.writerow(["Всего фильмов  без проблем", len(self.list_films_id_ok)])
                file_writer.writerow(["Всего сериалов", len(self.list_serials_id_ok + self.list_serials_id_bad)])
                file_writer.writerow(["Всего сериалов с проблемами", len(self.list_serials_id_bad)])
                file_writer.writerow(["Всего сериалов  без проблем", len(self.list_serials_id_ok)])
                file_writer.writerow(["Всего сезонов", len(self.list_seasons_id_ok + self.list_seasons_id_bad)])
                file_writer.writerow(["Всего сезонов с проблемами", len(self.list_seasons_id_bad)])
                file_writer.writerow(["Всего сезонов без проблем", len(self.list_seasons_id_ok)])
                file_writer.writerow(["Всего эпизодов", len(self.list_episodes_id_ok + self.list_episodes_id_bad)])
                file_writer.writerow(["Всего эпизодов с проблемами", len(self.list_episodes_id_bad)])
                file_writer.writerow(["Всего эпизодов без проблемам", len(self.list_episodes_id_bad)])


            with open(
                    "tests/results/" + str(self.current_date_time) + "-" + "result_films_bad.csv",
                    mode="w",
                    encoding="utf-8",
            ) as w_file:
                file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r\n")
                file_writer.writerow(["id", "Название фильма", "Код ответа"])
                for i in self.list_films_id_bad:
                    file_writer.writerow(
                        [
                            i[0],
                            i[1],
                            i[2],
                        ]
                    ),
            with open(
                    "tests/results/" + str(self.current_date_time) + "-" + "result_serials_bad.csv",
                    mode="w",
                    encoding="utf-8",
            ) as w_file:
                file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r\n")
                file_writer.writerow(
                    ["id", "Название сериала", "Название серии", "Код ответа"]
                )
                for i in self.list_episodes_id_bad:
                    file_writer.writerow(
                        [
                            i[0],
                            i[1],
                            i[2],
                            i[3],
                        ]
                    ),