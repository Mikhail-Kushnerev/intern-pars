# Парсер интеренет-магазина "Детский мир" по категориям

## Описание

Парсер, собирающий с сайта информацию:  
- ID товара;
- название товара;
- цену со скидкой и без;
- страну-производителя;
- **url** товара.

## Содержание

- [Технологии](#технологии)
- <a href="#t1">Структура проекта</a>
- [Запуск](#запуск)
- [Автор](#автор)

## Технологии

- Python
- Selenium
- Redis

<details>
  <summary>
    <h2 id="t1">Структура проект</h2>
  </summary>

    ```cmd
    itern-pars
    |   .gitignore
    |   configs.py  <-- Конфигуратор парсера и логов
    |   constants.py  <-- Дефолтные ссылки, форматы, пути и т.д.
    |   LICENSE
    |   main.py  <-- исполняемый файл
    |   outputs.py  <-- представление в CSV-файле
    |   README.md
    |   requirements.txt
    |   utils.py  <-- обработчик ошибок
    |
    +---driver  <-- Директория драйвера браузера
    |       chromedriver.exe  <-- Сам драйвер
    |       __init__.py
    |
    +---redis_dir  <-- Директория с Redis
    |   |   redis-cli.exe
    |   |   redis-server.exe
    |   |   __init__.py
    |   |   
    |   \---__pycache__
    |
    +---results  <-- Директория с таблицами csv
    |   \---csv  <-- Одноименная директория
    ```

</details>

[⬆️Содержание](#содержание)

## Запуск
- Активируйте вирт. окружение, установите зависимости:
  ```python
  py -m venv venv
  (win) source venv/Scripts/activate
  (linux) source venv/bin/activate
  pip install -r requirements.txt
  ```
- Запустите **redis**
  ```python
  docker-compose up
  ```
- Запустите **redis-cli** внутри контейнера **redis**
- В файле `constants.py` задайте переменной `URL` любую категорию для парсинга по примеру:
    ```python
    - https://www.detmir.ru/catalog/index/name/lego/
    - https://www.detmir.ru/catalog/index/name/transport/
    и т.д.
    ```

- Из директории **src** запустите файл `main.py`
- Дождитесь завершения работы

**Замечание**:
1. по умолчанию парсится весь каталог с первой страницы. Для ускорения работы уберите блок `while` (67 - 81 строки, 82 удалить) в файле `main.py`, сдивнув при этом содержимое цикла влево на одну табуляцию
  ```python
  while True:
      site: str = URL + "page/{}/".format(page)
      ...
      write_csv(part_result)
  ```
  Задайте в переменную `page` нужную страницу.  
2. Если во время работы парсера произойдет разрыв с сайтом, продолжите парсинг со страницы (см. замечание 1), на котором произошёл сбой.  
[⬆️Содержание](#содержание)


## Автор

[Mikhail Kushnerev](https://github.com/Mikhail-Kushnerev/)  
[⬆️В начало](#описание)