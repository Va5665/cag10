# Запуск в качестве теста: вставляем токен
python -m pytest --verbose test_amediateka_stream_links.py -s
затем      pytest --alluredir=allure-results 
 и затем   allure serve allure-results  

# Запуск в качестве скрипта: 
запустить файл: script_get_statistics.py
<br>
<br>
Прогресс выполнения выводится в командную строку

#Результаты прогона теста хранятся в папке results в виде:

#yyyy_mm_dd-hhmmss-statistics.csv:
Всего сериалов/с проблемами,Всего сезонов/с проблемами,Всего серий/с проблемами,Всего фильмов/с проблемами

#yyyy_mm_dd-hhmmss-result_serials_bad.csv:
id,Название сериала,Название серии,Код ответа

#yyyy_mm_dd-hhmmss-result_films_bad.csv:
id,Название фильма,Код ответа
