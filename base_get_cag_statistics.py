import csv
from datetime import datetime
from json.decoder import JSONDecodeError

import requests
from tqdm import tqdm



class CagStatistics:
    """Базовый класс для работы с API CAG"""

    HEADERS = {
        "Authorization-Client": "LDtddNer9eiTEIPVQJ6Qt4mM0hkWmlglWnPNLCHNJKE7WRtLeff51YVqUlNlco0ozWipp4hJGk6kFgYuzZH78iq7JeFVemnUXJWH2OIyQnsT4qdYyKnRJ6TsjlKcXFgdOmjjB0VRorhZ35BuFEzYCB3xabJkaR3zMTreflktk6eseqvYCnqHmrjXSrWCkN4WhpEX3X1o024Vmd659dDvc87JzZ6sF0y18e8LOGmwwetVvIWXwpHVyVG2VBUNaic",
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
        total_pages = 1

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
                file_writer.writerow(["Argument", "Value"])
                file_writer.writerow(["Всего фильмов", len(self.list_films_id_ok + self.list_films_id_bad)])
                file_writer.writerow(["Всего фильмов с проблемами", len(self.list_films_id_bad)])
                file_writer.writerow(["Всего фильмов  без проблем", len(self.list_films_id_ok)])

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
