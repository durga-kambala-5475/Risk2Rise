from flask import Flask, render_template, request, redirect, session
import sqlite3
import joblib
import smtplib
from email.mime.text import MIMEText


# =========================
# Flask App
# =========================

app = Flask(__name__)
app.secret_key = "risk2rise_secret"


# =========================
# Load ML Model
# =========================

model = joblib.load("risk_model.pkl")


# =========================
# Explainable AI Function
# =========================

def generate_explanation(attendance, internal1, internal2, assignment, study_hours, risk):

    reasons = []
    suggestions = []

    avg_internal = (internal1 + internal2) / 2


    # =========================
    # HIGH RISK
    # =========================

    if risk == "High":

        if attendance < 75:
            reasons.append("Very low attendance affecting academic performance")

        if avg_internal < 15:
            reasons.append("Poor internal exam marks")

        if assignment < 3:
            reasons.append("Assignments not properly completed")

        if study_hours < 2:
            reasons.append("Extremely low study hours")

        while len(reasons) < 4:
            reasons.append("Overall performance is critically low")

        suggestions = [

            "Attend all classes regularly",

            "Meet teachers and seek academic guidance",

            "Increase study time to minimum 4 hours daily",

            "Follow strict study plan and complete assignments"

        ]


    # =========================
    # MEDIUM RISK
    # =========================

    elif risk == "Medium":

        if attendance < 80:
            reasons.append("Attendance is below recommended level")

        if avg_internal < 18:
            reasons.append("Internal marks need improvement")

        if assignment < 4:
            reasons.append("Assignment performance is average")

        if study_hours < 3:
            reasons.append("Study hours are not sufficient")

        while len(reasons) < 4:
            reasons.append("Academic performance can be improved")

        suggestions = [

            "Improve attendance above 85%",

            "Practice previous question papers",

            "Increase study hours gradually",

            "Focus on weak subjects"

        ]


    # =========================
    # LOW RISK
    # =========================

    else:

        reasons = [

            "Good attendance and academic consistency",

            "Good internal marks performance",

            "Assignments completed properly",

            "Maintaining good study habits"

        ]

        suggestions = [

            "Continue maintaining current performance",

            "Aim for higher academic excellence",

            "Participate in group study",

            "Prepare for advanced learning"

        ]


    return reasons[:4], suggestions[:4]


# =========================
# Login Page
# =========================

@app.route("/")
def home():

    return render_template("login.html")


# =========================
# Teacher Login
# =========================

@app.route("/teacher_login", methods=["POST"])
def teacher_login():

    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM teachers WHERE username=? AND password=?",

        (username, password)

    )

    teacher = cursor.fetchone()
    conn.close()

    if teacher:

        session["teacher"] = username
        return redirect("/teacher_dashboard")

    else:

        return "<h2>Invalid Teacher Login</h2>"


# =========================
# Student Login
# =========================

@app.route("/student_login", methods=["POST"])
def student_login():

    student_id = request.form["student_id"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(

        """SELECT attendance, internal1, internal2, assignment, study_hours
           FROM students
           WHERE student_id=? AND password=?""",

        (student_id, password)

    )

    student = cursor.fetchone()
    conn.close()

    if student:

        attendance, internal1, internal2, assignment, study_hours = student

        internal1_25 = (internal1 / 40) * 25
        internal2_25 = (internal2 / 40) * 25
        assignment_5 = (assignment / 10) * 5

        total = ((internal1_25 + internal2_25) / 2) + assignment_5

        # =========================
        # ML Prediction
        # =========================

        risk = model.predict([[

            attendance,
            internal1_25,
            internal2_25,
            assignment_5,
            total,
            study_hours

        ]])[0]


        # =========================
        # Explainable AI
        # =========================

        reasons, suggestions = generate_explanation(

            attendance,
            internal1_25,
            internal2_25,
            assignment_5,
            study_hours,
            risk

        )


        return render_template(

            "student_dashboard.html",

            risk=risk,

            attendance=attendance,

            internal1=internal1_25,

            internal2=internal2_25,

            assignment=assignment_5,

            study_hours=study_hours,

            reasons=reasons,

            suggestions=suggestions

        )

    else:

        return "<h2>Invalid Student Login</h2>"


# =========================
# Teacher Dashboard
# =========================

@app.route("/teacher_dashboard")
def teacher_dashboard():

    if "teacher" not in session:

        return redirect("/")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(

        "SELECT student_id, attendance, email, risk FROM students"

    )

    students = cursor.fetchall()
    conn.close()

    student_list = []

    low = medium = high = 0

    for sid, att, email, risk in students:

        if risk == "High":
            high += 1

        elif risk == "Medium":
            medium += 1

        else:
            low += 1

        student_list.append({

            "id": sid,
            "attendance": att,
            "risk": risk,
            "email": email

        })

    return render_template(

        "teacher_dashboard.html",

        students=student_list,

        low=low,
        medium=medium,
        high=high

    )


# =========================
# SEND EMAIL
# =========================

@app.route("/send_mail/<email>/<risk>/<id>")
def send_mail(email, risk, id):

    sender = "durgakambala5475@gmail.com"

    password = "icgmdyhdjqvigpdn"


    message = MIMEText(f"""

Risk2Rise AI Alert

Student ID: {id}

Risk Level: {risk}

Please take action immediately.

""")

    message["Subject"] = "Risk2Rise Alert"

    message["From"] = sender

    message["To"] = email


    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(sender, password)

    server.send_message(message)

    server.quit()


    return "Mail Sent Successfully"


# =========================
# Run App
# =========================

if __name__ == "__main__":

    app.run(debug=True)




