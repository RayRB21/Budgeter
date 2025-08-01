
# Budgeter

#------IMPORTS------------

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#-------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///budget.db"
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    income = db.Column(db.Integer, default=0)
    spending = db.Column(db.Integer, default=0)
    goal = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'
    


@app.route('/', methods=['POST','GET'])
def index():
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

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/information')
def info():
    user_info = Users.query.get_or_404(1)

    return render_template('information.html',user_info = user_info)

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

'''class Person: #User class
    def __init__(self, username, income, spending, goal):
        self._username = username.lower()
        self._income = income
        self._spending = spending
        self._goal = goal.lower()
    
    def set_username(self,username):
        if isinstance(username,str):
            self._username = username.lower()
        else:
            print("username is not a string")
            
    def set_income(self,income):
        if isinstance(income,(int,float)):
            self._income = income
        else:
            print("please enter a valid number")
            
    def set_spending(self,spending):
        if isinstance(spending,(int,float)):
            self._spending = spending
        else:
            print("please enter a valid number")
        
    
    def set_goal(self,goal):
        if isinstance(goal,str):
            self._goal = goal
        else:
            print("please enter a valid percentage")
        
    def username(self):
        return(self._username)
    def income(self):
        return(self._income)
    def spending(self):
        return(self._spending)
    def goal(self):
        return(self._goal)
        
    def __str__(self):
        return f"username: {self._username}, income: £{self._income}"
        
def writeAccount(user):
    with open("users.txt","r") as file:
        content = file.read()
        print (content)
        print(f"username: {user.username()}")
    with open("users.txt","a") as file:
        if f"username: {user.username()}" in content: #checks if username is in file already
            print("test1")
            return "username taken"
        else:
            print("test2")
            file.write(f"username: {user.username()}\nincome: {str(user.income())}\nspending: {str(user.spending())}\ngoal: {user.goal()}\n\n") #writes info to users.txt
    
def findAccount(user):
    with open("users.txt","r") as file:
        content = file.read()
        try:
            userIndex = content.index(f"username: {user.username()}") #checks users.txt for username
            print(f"Substring found at index {userIndex}")
            print(content.index("income: ", userIndex))
            user.set_income(int(content[content.index("income: ", userIndex) +8:content.index("\n", content.index("income: ", userIndex))])) #sets income to value indexed in users.txt
            print("yrdsduih")
            user.set_spending(int(content[content.index("spending: ", userIndex) +10:content.index("\n")])) #sets spending to value indexed in users.txt
            user.set_goal(content[content.index("goal: ", userIndex) +6:content.index("\n")]) #sets goal to value indexed in users.txt
            print(f"user = {user.username()}, income = {user.income()}, spending = {user.spending()}, goal = {user.goal()}")
        except ValueError:
            print("error finding values")
            


#Mat = Person("Mat",1000,500,"40%")
#Mat.set_income(int(input("Set a income")))
#writeAccount(Mat)

#print (Mat.goal())
#print (Mat)

#Sal = Person("sally",200,100,"30%")
#findAccount(Sal)

'''