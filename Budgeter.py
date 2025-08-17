
# Budgeter

#------IMPORTS------------

from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import JSON
from flask_migrate import Migrate
import calendar as Calendar
from datetime import datetime
import re

#-------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///budget.db"   
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
    events = db.Column(JSON)

    def __repr__(self):
        return f'<Task {self.id}>'
    


def is_money_format(s):
    pattern = r"^-?\d+(\.\d{1,2})?$"
    return bool(re.match(pattern, s))






@app.route('/')
def menu():
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))
    else:
        return render_template('menu.html')




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




@app.route('/logout/')
def logout():
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))
    session.clear()
    flash("You have logged out", "info")
    return redirect(url_for("login"))



@app.route('/calendar/')
def calendar():
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

    return render_template('calendar.html',calendar=cal,month=month,year=year,month_name=month_name,months=months,years=years,show_modal=False)



@app.route('/calendar/add-event/<cell_id>/')
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
    if cell_id in session["events"]:
        modal_events = session["events"][cell_id]
    else:
        modal_events = ""
    modal_title = cell_id
    return render_template('calendar.html',calendar=cal,month=month,year=year,month_name=month_name,months=months,years=years,
                           modal_events=modal_events,
                           modal_title=modal_title,
                           show_modal=True,
                           add_event=True)

    


@app.route('/calendar/<cell_id>/<event>', methods=["POST","GET"])
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
        print(event)
        _events.remove(event)
        session["events"][cell_id] = _events
        curUser = Users.query.get(session["id"])
        curUser.events = session["events"]
        return redirect(url_for("calendar"))
    else:
        print(event)
        print(type(event))
        event = event.replace("'","")
        event_arr = event[1:-1].split(",")
        print(event_arr)
        print(type(event_arr))

        event_name = event_arr[0]
        event_details = event_arr[3]
        event_transaction = event_arr[2]
        return render_template('calendar.html',calendar=cal,month=month,year=year,month_name=month_name,months=months,years=years,
                           event_details=event_details,
                           modal_title=event_name,
                           event_transaction=event_transaction,
                           add_event=False,
                           show_modal=True)


@app.route('/information/')
def info():
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))

    return render_template('information.html')




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
        return render_template('transactions.html')





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



@app.route('/delete/<int:id>/')
def delete(id):
    username_to_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(username_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a failure to delete"    



@app.route('/oldCal/', methods=['POST','GET'])
def oldCal():
    if "user" not in session:
        flash("Please login or sign up","info")
        return redirect(url_for("login"))
    if request.method == 'POST':
        calendar_content = request.form['content']
        test = Users(username=calendar_content)

        try:
            db.session.add(test)
            db.session.commit()
            return redirect('/')
    
        except:
            return 'There was an issue with the test'
        
    else:
        usernames = Users.query.order_by(Users.date_created).all()
        return render_template('oldCal.html', usernames = usernames)
    


if __name__ == "__main__":
    app.run(debug=True)
