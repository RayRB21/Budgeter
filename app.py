
# Budgeter

#------IMPORTS------------

from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON
from flask_migrate import Migrate
import calendar as Calendar
from datetime import datetime
import re
import json
import ast
import os

#-------------------------

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///budget.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ucrv8929bmjsel:pcf7dc1e3ecbeb5299ba7d9428b1ce65ad704bb2451191fd5b1028c18118926e1@cd7f19r8oktbkp.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1qnb8nfjahc86"
#-------------^^HAD TO MAKE THE PREFIX "postgresql" INSTEAD OF "postgres" TO FIX ISSUE^^------------------
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = "test"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    income = db.Column(db.Integer, default=0)
    spending = db.Column(db.Integer, default=0)
    goal = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(20), nullable=False)
    events = db.Column(JSON, default=dict)

    def __repr__(self):
        return f'<Task {self.id}>'
    


def is_money_format(s):
    pattern = r"^-?\d+(\.\d{1,2})?$"
    return bool(re.match(pattern, s))






@app.route('/', methods= ["GET"])
def menu():
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))
    else:
        return redirect(url_for("info"))




@app.route('/login/', methods = ["POST","GET"])
def login():
    if request.method == 'POST':
        userContent = request.form["username"].lower()
        curUser = Users.query.filter_by(username=userContent).first()
        if curUser and request.form["password"] == curUser.password:
            session["id"] = curUser.id
            session["user"] = curUser.username
            session["income"] = curUser.income
            session["spending"] = curUser.spending
            session["goal"] = curUser.goal
            session["date_created"] = curUser.date_created
            session["events"] = curUser.events
            return redirect(url_for("info"))
        flash("Login failed, please try again", "error")
        return redirect(url_for("login"))
    else:
        return render_template("login.html")




@app.route('/logout/', methods= ["GET"])
def logout():
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))
    session.clear()
    flash("You have logged out", "info")
    return redirect(url_for("login"))



@app.route('/calendar/', methods= ["GET"])
def calendar():
    '''events = {"15-8-2025": [["Party", "leisure", "-50", "Jake's birthday party"], ["Monthly Salary", "work", "+2000", "Monthly paycheque from my job"]]}
    curUser = Users.query.get(session["id"])
    curUser.events = events
    db.session.commit()'''
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))

    else:
        year = request.args.get('year', default=datetime.now().year, type=int)
        month = request.args.get('month', default=datetime.now().month, type=int)

    cal = Calendar.monthcalendar(year, month)
    month_name = Calendar.month_name[month]

    years = list(range(2020, 2031))
    months = [(i, Calendar.month_name[i]) for i in range(1, 13)]

    return render_template('calendar.html',calendar=cal,month=month,year=year,month_name=month_name,months=months,years=years,
                           show_modal=False,
                           addEvent=False)



@app.route('/calendar/add-event/<cell_id>/', methods=["GET","POST"])
def addEvent(cell_id):
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))

    cell_values = cell_id.split("-")
    year = int(cell_values[2])
    month = int(cell_values[1])

    cal = Calendar.monthcalendar(year, month)
    month_name = Calendar.month_name[month]

    years = list(range(2020, 2031))
    months = [(i, Calendar.month_name[i]) for i in range(1, 13)]

    if request.method == "POST":
        event_name = request.form.get('event-name')
        event_type = request.form.get('event-type')
        event_trans = request.form.get('event-transaction')
        event_descr = request.form.get('event-description')
        if not all([event_name, event_type, event_trans, event_descr]):
            flash ("All fields are required!","error")
            return redirect(url_for('calendar', year=year,month=month,)) 
        if cell_id not in session["events"]:
            session["events"][cell_id] = []
        _events = session["events"][cell_id]
        _events.append([event_name,event_type,event_trans,event_descr])
        try:
            curUser = Users.query.get(session["id"])
            session["events"][cell_id] = _events
            session.modified = True
            curUser.events = session["events"]
            db.session.commit()
        except:
            flash("Issue adding event","error")
        return redirect(url_for('calendar', year=year,month=month,))
    else:
     #   if cell_id in session["events"]:
      #      modal_events = session["events"][cell_id]
      #  else:
     #       modal_events = "" 
        return render_template('calendar.html',calendar=cal,month=month,year=year,month_name=month_name,months=months,years=years,
                            #modal_events=modal_events,
                            modal_title=cell_id,
                            cell_id=cell_id,
                            add_event=True,
                            show_modal=True)

    


@app.route('/calendar/<cell_id>/<event>', methods=["GET","POST"])
def viewEvent(cell_id,event):
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))
    
    cell_values = cell_id.split("-")
    year = int(cell_values[2])
    month = int(cell_values[1])

    cal = Calendar.monthcalendar(year, month)
    month_name = Calendar.month_name[month]

    years = list(range(2020, 2031))
    months = [(i, Calendar.month_name[i]) for i in range(1, 13)]

    if request.method == "POST":
        _events = session["events"][cell_id]
        print(_events)
        event_arr = ast.literal_eval(event)
        print(event)
        _events.remove(event_arr)
        session["events"][cell_id] = _events
        session["events"] = {k: v for k, v in session["events"].items() if v}
        curUser = Users.query.get(session["id"])
        curUser.events = session["events"]
        try:
            db.session.commit()
            flash("Event Deleted","info")
        except:
            flash("Issue deleting event","error")
        return redirect(url_for('calendar', year=year,month=month,))
    else:
        event_arr = ast.literal_eval(event)

        event_name = event_arr[0]
        event_details = event_arr[3]
        event_transaction = event_arr[2]
    return render_template('calendar.html',calendar=cal,month=month,year=year,month_name=month_name,months=months,years=years,
                           event_details=event_details,
                           modal_title=event_name,
                           event_transaction=event_transaction,
                           cell_id=cell_id,
                           event=event,
                           add_event=False,
                           show_modal=True)


@app.route('/information/', methods= ["GET"])
def info():
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))
    

    year = request.args.get('year', default=datetime.now().year, type=int)
    month = request.args.get('month', default=datetime.now().month, type=int)
    cal = Calendar.monthcalendar(year, month)
    month_name = Calendar.month_name[month]
    years = list(range(2020, 2031))
    months = [(i, Calendar.month_name[i]) for i in range(1, 13)]

#Pie Chart Logic-----------------------------
    def PieChartSpend(m_or_y,param):
        spending = {}
        income = {}
        for date in session["events"]:
            if m_or_y == "m":
                check = "-" + str(param[0]) + "-" + str(param[1]) in date
            elif m_or_y == "y":
                check = "-" + str(param) in date
            else:
                flash("There was an error loading Graphs")
                break
            if check:
                for event in session["events"][date]:
                    if int(event[2]) < 0:
                        if event[1] not in spending:
                            spending[event[1]] = 0
                        spending[event[1]] += int(event[2])
                    elif int(event[2]) > 0:
                        if event[1] not in income:
                            income[event[1]] = 0
                        income[event[1]] += int(event[2])
        return spending, income
    
    month_spending, month_income = PieChartSpend("m",[month,year])
    year_spending, year_income = PieChartSpend("y",year)

#---------------------------------------------------------------

#Income vs Spending Bar Chart Logic-------------------------
    weekSpend= [0,0,0,0,0]
    weekIncome=[0,0,0,0,0]
    for date in session["events"]:
        cell_values = date.split("-")
        cell_values = [int(x) for x in cell_values]
        if cell_values[1]== month and cell_values[2] == year:

            for event in session["events"][date]:
                if int(event[2]) < 0:
                    if cell_values[0] in cal[0]:
                        weekSpend[0] -= int(event[2])
                    elif cell_values[0] in cal[1]:
                        weekSpend[1] -= int(event[2])
                    elif cell_values[0] in cal[2]:
                        weekSpend[2] -= int(event[2])
                    elif cell_values[0] in cal[3]:
                        weekSpend[3] -= int(event[2])
                    elif cell_values[0] in cal[4]:
                        weekSpend[4] -= int(event[2])


                elif int(event[2]) > 0:
                    if cell_values[0] in cal[0]:
                        weekIncome[0] += int(event[2])
                    elif cell_values[0] in cal[1]:
                        weekIncome[1] += int(event[2])
                    elif cell_values[0] in cal[2]:
                        weekIncome[2] += int(event[2])
                    elif cell_values[0] in cal[3]:
                        weekIncome[3] += int(event[2])
                    elif cell_values[0] in cal[4]:
                        weekIncome[4] += int(event[2])

    monthSpend = []
    monthIncome = []
    for i in range(1,13):
        spend,income = PieChartSpend("m",[i,year])
        monthSpend.append(abs(sum(spend.values())))
        monthIncome.append(sum(income.values()))
    
    #print(f"monthSpend === {monthSpend}")
    #print(f"monthIncome === {monthIncome}")
#---------------------------------------------------------------

#Balance Line Graph Logic------------------------------

    last_day = max(cal[-1])
    days= [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    for i in range(29,last_day+1):
        days.append(i)

    balance= [0] * len(days)
    relCells = []
    for date in session["events"]:
        cell_values = date.split("-")
        cell_values = [int(x) for x in cell_values]
        if cell_values[1]== month and cell_values[2] == year:
            relCells.append([cell_values,date])
    curBalance = session["income"]  
    relCells = sorted(relCells)
    
    cnt = 1
    for date in relCells:
        for event in session["events"][date[1]]:
            while cnt < date[0][0]:
                balance[cnt-1] = curBalance
                cnt += 1
            curBalance += int(event[2])
            balance[cnt-1] = curBalance
    while cnt <= days[-1]:
        balance[cnt-1] = curBalance
        cnt += 1

    monthBalance = []
    for i,j in zip(monthIncome,monthSpend):
        curBalance += i-j
        monthBalance.append(curBalance)
    #print(f"monthBalance ==== {monthBalance}")


#---------------------------------------------------------------
    return render_template('information.html',
                            month_spending_labels=list(month_spending.keys()), 
                            month_spending_values=list(month_spending.values()), 
                            month_income_labels=list(month_income.keys()), 
                            month_income_values=list(month_income.values()),
                            year_spending_labels=list(year_spending.keys()), 
                            year_spending_values=list(year_spending.values()), 
                            year_income_labels=list(year_income.keys()), 
                            year_income_values=list(year_income.values()),

                            weekSpend = weekSpend,
                            weekIncome = weekIncome,
                            monthSpend = monthSpend,
                            monthIncome = monthIncome,

                            balance=balance,
                            monthBalance = monthBalance,

                            month_name=month_name,
                            year=year,
                            days=days,
                            years=years,
                            months=months,
                            month=month,

                            )




@app.route('/transactions/', methods=['POST','GET'])
def transactions():
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))
    user_info = Users.query.get_or_404(session["id"])

    if request.method == 'POST':
        user_info.income = str(int(request.form['income']) + int(user_info.income))

        try:
            db.session.commit()
            session["income"] = user_info.income
            return redirect('/transactions')
        except:
            return 'There was an issue with updating your income'
    else:
        day = request.args.get('day',default=datetime.now().day, type=int)
        year = request.args.get('year', default=datetime.now().year, type=int)
        month = request.args.get('month', default=datetime.now().month, type=int)
        past_events = []
        future_events = []

        for date in session["events"]:
            cell_values = date.split("-")
            cell_values = [int(x) for x in cell_values]
            if cell_values[2] <= year and cell_values[1] <= month and cell_values[0] < day:
                past_events.append([cell_values,date])
            else:
                future_events.append([cell_values,date])
    if past_events:
        past_events = sorted(past_events,key=lambda x: (x[0][2], x[0][1], x[0][0]),reverse=True)
    if future_events:
        future_events = sorted(future_events,key=lambda x: (x[0][2], x[0][1], x[0][0]))



    return render_template('transactions.html', past_events=past_events,future_events=future_events)





@app.route('/signup/',methods=["POST","GET"])
def signup():
    if request.method == "POST":
        signUpError = False
        curUsername = request.form['username'].lower()
        curPassword = request.form['password']
        curIncome = request.form['income']
        curGoal = request.form['goal']
        if not curUsername or not curUsername.isalnum() or len(curUsername) > 20:
            flash("Username must be alphanumeric and less than 20 characters!", "error")
            signUpError = True
        if Users.query.filter_by(username=curUsername).first():
            flash("Username is already taken try a different Username", "error")
            signUpError = True
        if not curPassword or not isinstance(curPassword,str) or len(curPassword) > 20:
            flash("Password must be a string of characters that is less than 20 characters!", "error")
            signUpError = True
        if not is_money_format(curIncome):
            flash("Income must be a valid currency input!", "error")
            signUpError = True
        if not is_money_format(curGoal):
            flash("Goal must be a valid currency input!", "error")
            signUpError = True
        if signUpError:
            return redirect(url_for("signup"))
        newUser = Users(username = curUsername, password=curPassword, income= curIncome, goal= curGoal)

        try:
            db.session.add(newUser)
            db.session.commit()
            flash("Account successfully created!","info")
            return redirect(url_for('login'))
        except:
            flash("There was an issue creating your account please try again","warning")
            return redirect(url_for('signup'))
        
    else:
        return render_template('signup.html')



@app.route('/delete/<int:id>/', methods= ["GET"])
def delete(id):
    username_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(username_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a failure to delete"    



if __name__ == "__main__":
    app.run(debug=True)
