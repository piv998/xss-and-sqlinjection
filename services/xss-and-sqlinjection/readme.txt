https://hub.docker.com/_/microsoft-mssql-server

ok. Сервис должен подниматься docker'ом
ok. Должен быть checker - скрипт, который кладёт флаги и проверяет
ok. Написать скрипты, которые воруют 10 последних флагов
ok. Вместо наведения мышкой сделать явно при нажатии на кнопку
5. Добавить в функцию check чекера "просмотр флагов" так,
    чтобы он стал уязвим и XSS отработало.
    Если так не получается, то вероятно такая уязвимость неэксплатируема


Запуск программы, которую можно взломать:

docker-compose up --build
При этом создаётся volume

Доступ к программе с хоста через http://localhost/ .

Работа с checker'ом:
1. python checker.py info
2. python checker.py check localhost - делает проверку работоспособности системы
3. python checker.py put localhost id flag - помещает флаг по ключу id
4. python checker.py get localhost id flag - проверяет, что по ключу id можно найти флаг flag

Exploiting sql-injection vulnerability:
1. Сгенерируем 100 флагов и сохраним данные о сгенерированных флагах в файл flags_were_put.txt:
python checker.py gen localhost >flags_were_put.txt

2. Достаём последние 10 добавленных флагов через уязвимость SQL Injection:
python crackme.py localhost


Exploiting xss vulnerability:
1. Запустим атакующую программу, которая создаст флаг с ID=a и таким значением, что
    эксплуатируется уязвимость XSS; а затем эта программа открывает прослушку на порту 5002,
    ожидая входящую от жертвы информацию.
.\attack\attack.exe

2. Запускаем скрипт жертвы, который сгенерирует и сохранит 30 секретных флагов,
    после чего просмотрит флаг с ID=a, полученный от злоумышленника, нажмёт на появившуюся
    кнопку, и затем просмотрит свои секретные флаги (чтобы убедиться, что они никуда не исчезли):
python xss_victim.py >victim_flags.txt

3. Там, где был запущен сервер будут появляться id и флаги, которые просматривает жертва



python3 check.py list
python3 check.py up
python3 check.py check
python3 sploits\crackme.py localhost
.\sploits\attack\attack.exe
Во втором шеле:
python3 sploits\xss_victim.py >victim_flags.txt
В первом шеле:
Ctrl+C
Удаляем файл victim_flags.txt
python3 check.py down
