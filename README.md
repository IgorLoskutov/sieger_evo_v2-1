На главной странице формаза грузки файлов и поле ввода времени жизни файла 
(в минутах для ускорения тестирования) По сабмиту формы файл грузится на сервер. 
По истечению срока жизни файла он удаляется с сервера, вместо файла пользователь получает страницу 404.

Доп. задания:
1. Форма работает через AJAX
  -реализована форма загрузки и страница выдачи загруженных пользователем файлов.
  последняя реализована через AJAX. При отсутствии у пользователя файлов выдается
  страница 404
2. Сохранение файлов в персистентное хранилище. 
  - Postgresql. проект содержит миграции alembic
        $ psql postgres
         postgres=# create database fileshare owner <username>;
         postgres=# \q
        $ flask db upgrade
  -  в базу (в миграцию) вставлена процедура удаления старых файлов и триггер
    ON INSERT, её запускающий
  - на случай работы с низкой загрузкой (частота  INSERT'ов мала) в приложении предусмотрена
    функция, запускающая апдейт базы если между запросом файла и прошлым инсеhтом прошло больше минуты
    (вроде, дублирование функций, но думаю, что доверить апдейт базы самой базе, более правильно. 
    Если приложени будет записывать файлы достаточно часто, достаточно в коде закоментить одну строку, 
    чтобы не вызывать лишний раз апдейт)
3. Авторизация, можно получить список файлов созданых авторизованым пользователем.
  - задачи на форму регистрации не стояло Ж:)
    для тестирования:
      username: one
      password: pass
 4. Отдельная страница для файла, на котором видно сколько жить осталось этому файлу.
  - переход со стр п.п 3
  - там же и Download 
   
