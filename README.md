Задача:
Из определенного количества одинаковых цифр и набора математических знаков найти варианты получения определенного целочисленного значения.

Сейчас в настройках 7 "двоек" и знаки (+ - * /). Также выставлено ограничение на минимум и максимум искомого сначения.

Для генерации вариантов применены итераторы из itertools. 

Из вариантов удалены дубликаты. Например, такие:

222/2+22*2

22*2+222/2 - дубликат

2*22+222/2 - дубликат

Для замера времени выполнения применены два метода библиотеки time: perf_counter и process_time.
По идее, дельта perf_counter должна быть меньше, но в данном случае наоборот.
