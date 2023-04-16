import pytest
import allure
from .base_get_cag_statistics import CagStatistics


@allure.feature("tests")
class TestContent:
    cag_statistics_object = CagStatistics()
    get_json_all_content = cag_statistics_object.get_all_content()
    cag_statistics_object.get_pages(get_json_all_content)
    bad_films_list = cag_statistics_object.list_films_id_bad
    ok_films_list = cag_statistics_object.list_films_id_ok

    @allure.story("TestContent")
    @pytest.mark.parametrize("bad_film", bad_films_list)
    def test_content_bad(self, bad_film):
        with allure.step(f"Проверка нерабочего контента: {bad_film}"):
            assert False, f"Нерабочий контент: {bad_film}. Проверьте папку results"

    @allure.story("TestContent")
    @pytest.mark.parametrize("ok_film", ok_films_list)
    def test_content_ok(self, ok_film):
        with allure.step(f"Проверка рабочего контента: {ok_film}"):
            assert True, f"Pабочий контент: {ok_film}. Проверьте папку results"




