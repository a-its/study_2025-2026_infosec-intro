# Приложение для однократного гаммирования

Запуск: Python 3.8 или новее, только стандартная библиотека.
Выполнять команды из этого каталога. Кодировка текста по умолчанию cp1251.

```bash
python3 gamma.py --help
python3 gamma.py encrypt --text 'Штирлиц - Вы Герой!!' --key-file input/center-key.hex
python3 gamma.py decrypt --data-file output/task-cipher.hex --key-file output/greeting-key.hex
python3 gamma.py derive --data-file output/task-cipher.hex --text 'С Новым Годом, друзья!'
```

Существующие результаты с --out программа не перезаписывает.
Демонстрационные ключи и шифротексты не предназначены для секретной переписки.
Исходник идентичен файлу в записи по SHA-256, показанному после py_compile.
HEX-файлы восстановлены по значениям, видимым в записи выполнения 12.10.2026.
Журнал session.log и гостевой архив не перенесены из ВМ и здесь не воспроизводятся.
Полная таблица greeting-table.txt сохранена в evidence; её байты сверены с записью.
