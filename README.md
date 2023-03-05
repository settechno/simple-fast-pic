Simple Fast Pic - простой проект на питоне с целью получению опыта в работе на python.

Проект представляет из себя хранилку изображений на удалённом webdav-сервере. 
Сам проект изображений не хранит. В качестве webdav-сервера может выступать любой публичный 
(н.р. Облако mail.ru или Яндекс.Диск) или приватный. Настройки подключения к webdav, как и вся конфигурация, находятся в .env файле.
Загружать изображения можно либо через web-интерфейс, либо отправлять telegram-боту.

Используемый стек:
- python 3.10
- poetry
- FastAPI
- uvicorn
- pytelegrambotapi
- jinja2

Для удобавства создан Makefile с командами.