from datetime import datetime, timedelta
import json
import urllib.request


def date_short(date_str): # "2020-08-25" to "25 авг"
    months = {"01": "янв", "02": "фев", "03": "мар", "04": "апр",\
              "05": "май", "06": "июн", "07": "июл", "08": "авг",\
              "09": "сен", "10": "окт", "11": "ноя", "12": "дек"}
    return "{} {}".format(date_str[8:10], months[date_str[5:7]])


API_URL = "https://sheetdb.io/api/v1/{}/?sheet=Data"


def err_mes(col_name, value):
    return "'{}' в колонке {}".format(value, col_name)

def data_to_cash(API_TOKEN):
    start_url = API_URL.format(API_TOKEN)
    response = urllib.request.urlopen(start_url)
    meetings = json.loads(response.read())
    meetings_res = []
    errors = []

    for meeting in meetings:
        is_ok = True
        meeting["tags"] = [tag.strip() for tag in meeting["tags"].split(",")]
        try: # на случай человеческого фактора, от которого робот не понимает данные в таблице
            end_date = datetime.strptime(meeting["enddate"], "%d.%m.%Y")
        except:
            errors.append(err_mes("enddate", meeting["enddate"]))
            is_ok = False

        try:
            start_date = datetime.strptime(meeting["startdate"], "%d.%m.%Y")
            meeting["startdate"] = start_date.strftime("%Y-%m-%d") # для фильтра по датам
            meeting["startdate_short"] = date_short(meeting["startdate"]) # для отображения на карточке мероприятия
        except:
            errors.append(err_mes("startdate", meeting["startdate"]))
            is_ok = False

        if meeting["allday"] == "FALSE":
            try:
                start_time = datetime.strptime(meeting["starttime"], "%I:%M %p")
            except:
                errors.append(err_mes("starttime", meeting["starttime"]))
                is_ok = False
            try:
                end_time = datetime.strptime(meeting["endtime"], "%I:%M %p")
            except:
                errors.append(err_mes("endtime", meeting["endtime"]))
                is_ok = False
            if is_ok:
                meeting["dates_to_calendar"] = start_date.strftime("%Y%m%d")+"T"+\
                     start_time.strftime("%H%M%S")+"/"+end_date.strftime("%Y%m%d")+"T"+\
                     end_time.strftime("%H%M%S") # для создания мероприятия в гуглевском календаре "20140127THHMM00/20140320THHMM00"
                meeting["starttime"] = start_time.strftime("%H:%M") # для отображения на карточке мероприятия
        else:
            if is_ok:
                end_date = end_date + timedelta(days=1)
                meeting["dates_to_calendar"] = start_date.strftime("%Y%m%d")+"/"+\
                     end_date.strftime("%Y%m%d") # для создания мероприятия в гуглевском календаре "20140127/20140320"
        if is_ok:
            meetings_res.append(meeting)

    dates = {meeting["startdate"] for meeting in meetings_res}

    cash_data = {"min_date": min(dates), "max_date": max(dates), "meetings": meetings_res}
    with open("json/cash.json", "w") as f:
        json.dump(cash_data, f)

    return errors

