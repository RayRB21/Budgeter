# 💰 Budgeting Web App

A simple budgeting web application built with **Flask**, **SQLite**, and **Bootstrap**, designed to show i can **DEPLOY, MAINTAIN and CODE a FULL STACK web application with a functional database**. 
Users can record income and expenses, set savings goals, and track spending trends through a clean dashboard.

https://budgeterapp-e0fa271274bb.herokuapp.com/

Dummy Account: Username = test, Password = 123

---

## 🛠 Tech Stack
- **Backend:** Python (Flask) , Java
- **Frontend:** HTML, CSS (Bootstrap)
- **Database:** SQLite (SQLAlchemy ORM)
- **Deployment:** Heroku
- **CI/CD:** GitHub Actions (tests + auto-deploy)

---

## 🚀 Features
- Add, edit, and delete income and expenses
- View total balance and monthly breakdown
- View charts and data of spending analytics
- Dashboard with spending summaries
- Authentication (login & register users)

---

## 🧪 Tests

- Implemented testing using PyTest
- Implemented CI/CD using GitHub Actions
- Tests automatically run on pull or push to GitHub
  
Run tests locally with:
   ```bash
   pytest
   ```

---

## 📸 Screenshots

Login Page
<img width="1920" height="911" alt="image" src="https://github.com/user-attachments/assets/70190f3f-d6ff-4d1f-ab1b-5fe94d2bb1b3" />

Information Charts
<img width="1897" height="899" alt="image" src="https://github.com/user-attachments/assets/5be0a8a9-cbcc-4a6f-abcb-2e7769ff8718" />
<img width="1870" height="908" alt="image" src="https://github.com/user-attachments/assets/dc3ccf59-20b2-445b-99eb-9312d2f2d96f" />

Past and Future Transactions
<img width="1916" height="909" alt="image" src="https://github.com/user-attachments/assets/dc9c9e92-a23b-4764-8d6c-c6c55fac9ab5" />

---

## ⚙️ Installation & Setup

1. Clone the repository
   ```bash
   git clone https://github.com/rayrb21/budgeter.git
   cd budgeter
   
2. Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate #For Linux/Mac
   venv\Scripts\activate  #For Windows
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Initialise database
   ```bash
   flask db upgrade
   ```

5. Run the app
   ```bash
   flask run
   ```
The app should now run at http://127.0.0.1:5000/

---
## 🔑 Usage

- Register for an account
- Log in to your dashboard
- Add income/expenses
- Track savings goals

---


## 📌 Future Improvements

- Export data as csv
- Make website more user friendly
- Add more features
- Implement predictions on future earnings

---

## 👤 Author
**Rayan Butt**

[Linkedin](www.linkedin.com/in/rayan-butt-cs) | [Github](https://github.com/RayRB21?tab=overview&from=2025-07-01&to=2025-07-31)
