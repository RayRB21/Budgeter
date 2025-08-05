
# Budgeter

#------IMPORTS------------

from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#-------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///budget.db"
db = SQLAlchemy(app)
app.secret_key = "test"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    income = db.Column(db.Integer, default=0)
    spending = db.Column(db.Integer, default=0)
    goal = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'
    



@app.route('/')
def menu():
    if "user" not in session:
        return redirect(url_for("login"))
    else:
        return render_template('menu.html')




@app.route('/login', methods = ["POST","GET"])
def login():
    if request.method == 'POST':
        userContent = request.form["username"].lower()
        curUser = Users.query.filter_by(username=userContent).first()
        if curUser:
            session["id"] = curUser.id
            session["user"] = curUser.username
            session["income"] = curUser.income
            session["spending"] = curUser.spending
            session["goal"] = curUser.goal
            session["date_created"] = curUser.date_created
            return redirect(url_for("menu")) 
        flash("Username not found, please try again", "error")
        return redirect(url_for("login"))
    else:
        return render_template("login.html")




@app.route('/logout')
def logout():
    if "user" not in session:
        return redirect(url_for("login"))
    session.pop("user",None)
    flash("You have logged out", "info")
    return redirect(url_for("login"))




@app.route('/calendar', methods=['POST','GET'])
def calendar():
    if "user" not in session:
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
        return render_template('calendar.html', usernames = usernames)




@app.route('/information')
def info():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template('information.html')




@app.route('/transactions', methods=['POST','GET'])
def transactions():
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




@app.route('/delete/<int:id>')
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

