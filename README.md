<h1 align="center">Привет, меня зовут <a href="https://t.me/Taeray" target="_blank">Артем</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>
<h3 align="center">Начинающий Python Developer, прошел курсы Яндекс.Практикума</h3>
<h3 align="center">Пример работы с Google-Sheets-API и PostgreSQL</h3>

### Описание: ###

Скрипт получает данные из документа (Google Sheets) с помощью Google API.
Полученные данные сохраняются в базе данных PostgreSQL с некоторыми изменениями.
Добавляется столбец цены в рублях (курс доллара берется из API ЦБ РФ).
Обновление таблицы происходит методом pooling'a (раз в 5 секунд).
Скрипт распаковывается с помощью Docker-compose.
#### Отдельно прикрепляю ссылку на таблицу в Google Sheets - `ссылка на тестовую таблицу скрыта` ####

## Установка: ##

### Клонируйте репозиторий: ###

    git clone git@github.com:KitKat-ru/testcase_kanal.git

### Подготовка скрипта к работе: ###

#### В папку `infra` необходимо добавить два файла `.env` и `creads.json`:
1. #### Пример файла `.env`:

        SPREADSHEET_ID=1zY4uUSXqL027hM5oPGBKYbyPD-Y0e7Es5_DUM4L5iis (ID таблицы из моего Google Sheets, Вам необходимо указать свой)
        DB_NAME=... (имя базы данных)
        POSTGRES_USER=... (логин для подключения к базе данных)
        POSTGRES_PASSWORD=... (пароль для подключения к БД (установите свой)
        DB_HOST=db (название сервиса (контейнера))
        DB_PORT=5432 (порт для подключения к БД)

2. #### Файл `creads.json` необходимо получить при создании своего сервисного аккаунта (файл будет предложено скачать, его необходимо переименовать в `creads.json`), более подробный гайд по [ссылке оф. документации](https://support.google.com/a/answer/7378726?hl=ru) или из [видео Диджитализируй](https://support.google.com/a/answer/7378726?hl=ru).
### Запуск скрипта: ###
#### Для запуска скрипта перейдите в папку `/infra` и запустите команду `sudo docker-compose up -d --build` после чего развернется два контейнера `infra_app_1`и `infra_db_1` контейнер скрипта и базы данных соответственно. ####
#### В контейнере скрипта в `stdout` каждые 5 секунд выбрасывается кортеж с полной таблицей и кортеж с таблицей просроченных заказов. Данную информацию можно парсить и использовать. Для проверки введите команду `sudo docker logs --follow infra_app_1`. ########

*Планирую добавить контейнер бота который будет делать к базе данных запросы и забирать информацию об актуальных и просроченных заказах и отдавать в чат телеграмма (при нажатии соответствующей кнопки) в меню бота.*
