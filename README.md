### Описание работы сервиса

Сервис предназначен для формирования ситемных статусов (полезная работа и простои техники).
Сервис получает сообщения, парсит их и разбивает на структуры. Определяется событие сообщения. Далее сообщение записывается в Базу Данных.


### Список системных статусов

    1. `DB_CYCLE_CODE_UNLOADING`: Разгрузка;
    2. `DB_CYCLE_CODE_STOPPING_EMPTY`: Стоянка/остановка без груза;
    3. `DB_CYCLE_CODE_MOVEMENT_EMPTY`: Движение без груза;
    4. `DB_CYCLE_CODE_LOADING`: Погрузка;
    5. `DB_CYCLE_CODE_STOPPING_LOAD`: Стоянка/остановка с грузом;
    6. `DB_CYCLE_CODE_MOVEMENT_LOAD`: Движение с грузом;
