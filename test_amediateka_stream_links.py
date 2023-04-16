import pytest
import allure
from .base_get_cag_statistics import CagStatistics


@allure.story("All_TestContent")
class TestContent:
    cag_statistics_object = CagStatistics()
    get_json_all_content = cag_statistics_object.get_all_content()
    cag_statistics_object.get_pages(get_json_all_content)

    bad_films_list = cag_statistics_object.list_films_id_bad
    ok_films_list = cag_statistics_object.list_films_id_ok

    bad_serials_list = cag_statistics_object.list_serials_id_bad
    ok_serials_list = cag_statistics_object.list_serials_id_ok

    bad_episodes_list = cag_statistics_object.list_episodes_id_bad
    ok_episodes_list = cag_statistics_object.list_episodes_id_ok

    bad_seasons_list = cag_statistics_object.list_seasons_id_bad
    ok_seasons_list = cag_statistics_object.list_seasons_id_ok



    @allure.story("TestContent_films")
    @pytest.mark.parametrize("bad_film", bad_films_list)
    def test_content_bad_film(self, bad_film):
        with allure.step(f"Проверка нерабочего контента: {bad_film}"):
            assert False, f"Нерабочий контент: {bad_film}. Проверьте папку results"

    @allure.story("TestContent_films")
    @pytest.mark.parametrize("ok_film", ok_films_list)
    def test_content_ok_film(self, ok_film):
        with allure.step(f"Проверка рабочего контента: {ok_film}"):
            assert True, f"Pабочий контент: {ok_film}. Проверьте папку results"




    @allure.story("TestContent_serials")
    @pytest.mark.parametrize("bad_serials", bad_serials_list)
    def test_content_bad_serials(self, bad_serials):
        with allure.step(f"Проверка рабочего контента: {bad_serials}"):
            assert False, f"Pабочий контент: {bad_serials}. Проверьте папку results"

    @allure.story("TestContent_serials")
    @pytest.mark.parametrize("ok_serials", ok_serials_list)
    def test_content_ok_serials(self, ok_serials):
        with allure.step(f"Проверка рабочего контента: {ok_serials}"):
            assert True, f"Pабочий контент: {ok_serials}. Проверьте папку results"



    @allure.story("TestContent_seasons")
    @pytest.mark.parametrize("bad_seasons", bad_seasons_list)
    def test_content_bad_seasons(self, bad_seasons):
        with allure.step(f"Проверка рабочего контента: {bad_seasons}"):
            assert False, f"Pабочий контент: {bad_seasons}. Проверьте папку results"

    @allure.story("TestContent_seasons")
    @pytest.mark.parametrize("ok_seasons", ok_seasons_list)
    def test_content_ok_seasons(self, ok_seasons):
        with allure.step(f"Проверка рабочего контента: {ok_seasons}"):
            assert True, f"Pабочий контент: {ok_seasons}. Проверьте папку results"



    @allure.story("TestContent_episodes")
    @pytest.mark.parametrize("bad_episodes", bad_episodes_list)
    def test_content_bad_episodes(self, bad_episodes):
        with allure.step(f"Проверка рабочего контента: {bad_episodes}"):
            assert False, f"Pабочий контент: {bad_episodes}. Проверьте папку results"

    @allure.story("TestContent_episodes")
    @pytest.mark.parametrize("ok_episodes", ok_episodes_list)
    def test_content_ok_episodes(self, ok_episodes):
        with allure.step(f"Проверка рабочего контента: {ok_episodes}"):
            assert True, f"Pабочий контент: {ok_episodes}. Проверьте папку results"
    #








