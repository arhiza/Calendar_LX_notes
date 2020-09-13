from datetime import datetime, timedelta
import json
import urllib.request


def date_short(date_str): # "2020-08-25" to "25 авг"
    months = {"01": "янв", "02": "фев", "03": "мар", "04": "апр",\
              "05": "май", "06": "июн", "07": "июл", "08": "авг",\
              "09": "сен", "10": "окт", "11": "ноя", "12": "дек"}
    return "{} {}".format(date_str[8:10], months[date_str[5:7]])


API_URL = "https://sheetdb.io/api/v1/{}/?sheet=Data"

def data_to_cash(API_TOKEN):
    start_url = API_URL.format(API_TOKEN)
    response = urllib.request.urlopen(start_url)
    meetings = json.loads(response.read())

    for meeting in meetings:
        meeting["tags"] = [tag.strip() for tag in meeting["tags"].split(",")]
        start_date = datetime.strptime(meeting["startdate"], "%d.%m.%Y")
        end_date = datetime.strptime(meeting["enddate"], "%d.%m.%Y")
        meeting["startdate"] = start_date.strftime("%Y-%m-%d") # для фильтра по датам
        meeting["startdate_short"] = date_short(meeting["startdate"]) # для отображения на карточке мероприятия
        if meeting["allday"] == "FALSE":
            start_time = datetime.strptime(meeting["starttime"], "%I:%M %p")
            end_time = datetime.strptime(meeting["endtime"], "%I:%M %p")
            meeting["dates_to_calendar"] = start_date.strftime("%Y%m%d")+"T"+\
                 start_time.strftime("%H%M%S")+"/"+end_date.strftime("%Y%m%d")+"T"+\
                 end_time.strftime("%H%M%S") # для создания мероприятия в гуглевском календаре "20140127THHMM00/20140320THHMM00"
            meeting["starttime"] = start_time.strftime("%H:%M") # для отображения на карточке мероприятия
        else:
            end_date = end_date + timedelta(days=1)
            meeting["dates_to_calendar"] = start_date.strftime("%Y%m%d")+"/"+\
                 end_date.strftime("%Y%m%d") # для создания мероприятия в гуглевском календаре "20140127/20140320"

    dates = {meeting["startdate"] for meeting in meetings}

    cash_data = {"min_date": min(dates), "max_date": max(dates), "meetings": meetings}
    with open("cash.json", "w") as f:
        json.dump(cash_data, f)
    
    return cash_data

