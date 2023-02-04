from flask import Flask, render_template, request
from flask import jsonify
import datetime
app = Flask(__name__)

def get_passed_days(year, month, day):
    month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    cnt = 0
    for i in range(1, 12+1):
        cnt += month_days[i]
    assert cnt==365

    passed_days = 0
    for i in range(1, month):
        month_day = month_days[i]
        if i==2 and year%4==0:
            month_day+=1
        passed_days += month_day
    passed_days += day
    return passed_days

def get_days_gap(year1, month1, day1, year2, month2, day2):
    year1_passed_days = get_passed_days(year1, month1, day1)
    year2_passed_days = get_passed_days(year2, month2, day2)

    days_gap = -year1_passed_days
    for i in range(year1, year2):
        days_gap += 365
        if i%4==0:
            days_gap += 1
    days_gap += year2_passed_days
    return days_gap

def checkweekday(tgt_year, tgt_month, tgt_day):
    cur_date = datetime.datetime.now()
    cur_year = cur_date.year
    cur_month = cur_date.month
    cur_day = cur_date.day
    cur_weekday = datetime.date.today().weekday()+1
    print("Current date:", cur_year, cur_month, cur_day)
    print("Target date:", tgt_year, tgt_month, tgt_day)

    d1 = datetime.datetime(cur_year, cur_month, cur_day)
    d2 = datetime.datetime(tgt_year, tgt_month, tgt_day)
    if d1==d2:
        res = 0
        res = (cur_weekday+res)%7
    elif d1<d2:
        days_gap = get_days_gap(cur_year, cur_month, cur_day, tgt_year, tgt_month, tgt_day)
        res = days_gap%7
        res = (cur_weekday+res)%7
    elif d1>d2:
        days_gap = get_days_gap(tgt_year, tgt_month, tgt_day, cur_year, cur_month, cur_day)
        res = days_gap%7
        res = (cur_weekday-res)%7
    print("Weekday of target date:", res)
    return res

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/check/<tgt_year>/<tgt_month>/<tgt_day>')
def route(tgt_year, tgt_month, tgt_day):
    month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if int(tgt_month)>12 or int(tgt_month)<1:
        result_str = f"Date out of range."
        return jsonify(result_str)
    if int(tgt_day)<1 or int(tgt_day)>month_days[int(tgt_month)]:
        result_str = f"Date out of range."
        return jsonify(result_str)

    print(f"Check the weekday of {tgt_year}-{tgt_month}-{tgt_day}")
    result = checkweekday(int(tgt_year), int(tgt_month), int(tgt_day))

    my_dict = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 0: "Sunday"}
    result_str = f"{tgt_year}-{tgt_month}-{tgt_day} is {my_dict[result]}."
    return jsonify(result_str)

@app.route('/checkapi', methods=['POST'])
def send():
    month_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    important_dates = {"christmas": [12, 25], "new year's day": [1,1], "Halloween": [10, 31]}

    if request.method == 'POST':
        tgt_year = request.form['year']
        tgt_month = request.form['month']
        tgt_day = request.form['day']
        tgt_holiday = request.form['holiday']
        if tgt_holiday != "":
            try:
                tgt_holiday = tgt_holiday.lower()
                tgt_month, tgt_day = important_dates[tgt_holiday]
            except:
                return render_template('index.html', results="Invalid Input.")

        if tgt_year == "" or tgt_month=="" or tgt_day=="":
            pass
        else:
            try:
                tgt_year = int(tgt_year)
                tgt_month = int(tgt_month)
                tgt_day = int(tgt_day)
            except:
                return render_template('index.html', results="Invalid Input.")
        if int(tgt_month)>12 or int(tgt_month)<1:
            return render_template('index.html', results="Date out of range.")
        if int(tgt_day)<1 or int(tgt_day)>month_days[int(tgt_month)]:
            return render_template('index.html', results="Date out of range.")
        
        result = checkweekday(int(tgt_year), int(tgt_month), int(tgt_day))
        my_dict = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 0: "Sunday"}
        result_str = f"{tgt_year}-{tgt_month}-{tgt_day} is {my_dict[result]}."
        return render_template('index.html', results=result_str)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)