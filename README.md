# Calendar_LX_notes

Календарь событий от https://t.me/lxnotes
(до деплоя не дошло)

макеты отсюда: https://github.com/gkatejka/Stepik-Academy-LX-Notes

Проект на Flask'е.

Сервис представляет из себя страницу, которая отображает данные, закешированные в json-файле. 
Для обновления информации модератор заходит по секретной ссылке, и 
сервис загружает себе информацию из гуглевской таблицы с помощью https://sheetdb.io/. 
(https://github.com/arhiza/Calendar_LX_notes/blob/main/update_data.py#L19)

Актуальные данные хранятся (и обновляются модератором вручную) в гуглевской таблице.

Пользователю изначально показываются данные с фильтром на текущую неделю. 
Можно настроить фильтры на другие даты, определенные категории, параметры и т.д. 
(html-код - https://github.com/arhiza/Calendar_LX_notes/blob/main/templates/index.html#L165),
(код в питоне - https://github.com/arhiza/Calendar_LX_notes/blob/main/app.py#L26). 

И можно создать запись в гугль-календаре для выбранного мероприятия. 
(html-код - https://github.com/arhiza/Calendar_LX_notes/blob/main/templates/index.html#L262), 
(код в питоне с преобразованием дат в нужный формат - https://github.com/arhiza/Calendar_LX_notes/blob/main/update_data.py#L55)
