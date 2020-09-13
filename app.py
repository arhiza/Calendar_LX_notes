import json
from datetime import datetime, timedelta
import os

from flask import Flask, request, render_template, redirect, session
from update_data import data_to_cash


def load_data():
    with open(f"cash.json", "r") as f:
        res = json.load(f)
    return res


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") #
API_TOKEN = os.environ.get("API_TOKEN") # 
SECRET_CODE = os.environ.get("SECRET_CODE") #


def check_filters(event, date_from, date_to, opt_location, options_locations, isfree, opt_tag, options_tags): # ...
    if (date_from != "") and (event["startdate"] < date_from):
        return False
    if (date_to != "") and (event["startdate"] > date_to):
        return False
    if (opt_location != options_locations[0]) and (opt_location != event["location"]):
        return False
    if (isfree == "on") and (event["isfree"] == "0"):
        return False
    if (options_tags[0] not in opt_tag) and (len(set(opt_tag) & set(event["tags"])) == 0): # множественный выбор
        return False
    return True

@app.route("/<secret>")
def update_data(secret):
    if secret == SECRET_CODE and API_TOKEN:
        data_to_cash(API_TOKEN)
        session["message"] = "Данные о мероприятиях обновлены."
    return redirect("/") # редирект, чтоб при обновлении страницы данные из гугль-таблицы не запрашивались еще раз

@app.route("/", methods=["GET", "POST"])
def render_main():
    cash_data = load_data()
    min_date = cash_data.get("min_date", "") # ограничители в полях фильтра
    max_date = cash_data.get("max_date", "")
    meetings = cash_data.get("meetings", []) # перед отправкой в рендер отфильтровать по датам/полям
    options_locations = ["Везде"]
    options_locations.extend({meeting["location"] for meeting in meetings})
    tags = []
    for meeting in meetings:
        tags.extend(meeting["tags"])
    options_tags = ["На любую тему"] + sorted(set(tags))

    if request.method == "GET": # изначальные фильтры
        now = datetime.now()
        monday = now - timedelta(days=now.weekday())
        date_from = monday.strftime("%Y-%m-%d") # даты с понедельника по воскресенье текущей недели
        if date_from < min_date:
            min_date = date_from
        date_to = (monday + timedelta(days=7)).strftime("%Y-%m-%d")
        if date_to > max_date:
            max_date = date_to
        opt_location = options_locations[0] # везде
        opt_tag = [options_tags[0]] # на любую тему
        isfree = None # непоставленная галочка бесплатности
    else:
        date_from = request.form.get("date_from")
        date_to = request.form.get("date_to")
        if date_from != '' and date_from < min_date:
            min_date = date_from
        if date_to != '' and date_to > max_date:
            max_date = date_to
        opt_location = request.form.get("opt_location")
        opt_tag = request.form.getlist("opt_tag") # мультиселект
        isfree = request.form.get("isfree")

    filtered_meetings = []
    for meeting in meetings:
        if check_filters(meeting, date_from, date_to, opt_location, options_locations, 
                         isfree, opt_tag, options_tags):
            filtered_meetings.append(meeting)

    return render_template("index.html", meetings=filtered_meetings, min_date=min_date, \
                           max_date=max_date, date_from=date_from, date_to=date_to, \
                           opt_location=opt_location, options_locations=options_locations, \
                           isfree=isfree, opt_tag=opt_tag, options_tags=options_tags)



if __name__ == "__main__":
    app.run() #debug=True)
