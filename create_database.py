import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# Drop old table (IMPORTANT for clean fix)

cursor.execute("DROP TABLE IF EXISTS students")


# Create table WITH risk column

cursor.execute("""

CREATE TABLE students (

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT,

student_id TEXT UNIQUE,

password TEXT,

attendance REAL,

internal1 REAL,

internal2 REAL,

assignment REAL,

study_hours REAL,

email TEXT,

risk TEXT

)

""")


# Insert students WITH risk

students = [

# LOW RISK

('Low1','S201','1234',96,38,39,9,6,'durgaai@mailinator.com','Low'),

('Low2','S202','1234',94,37,38,9,5,'low2@mailinator.com','Low'),

('Low3','S203','1234',92,36,37,8,5,'low3@mailinator.com','Low'),

('Low4','S204','1234',95,39,38,9,6,'low4@mailinator.com','Low'),

('Low5','S205','1234',93,37,36,8,5,'low5@mailinator.com','Low'),

# MEDIUM RISK

('Med1','S206','1234',82,26,28,6,3,'med1@gmail.com','Medium'),

('Med2','S207','1234',80,25,27,6,3,'med2@gmail.com','Medium'),

('Med3','S208','1234',78,24,26,5,2,'med3@gmail.com','Medium'),

('Med4','S209','1234',79,27,25,6,3,'med4@gmail.com','Medium'),

('Med5','S210','1234',81,26,27,5,2,'med5@gmail.com','Medium'),



# HIGH RISK

('High1','S211','1234',60,10,12,2,1,'high1@gmail.com','High'),

('High2','S212','1234',65,12,13,3,1,'high2@gmail.com','High'),

('High3','S213','1234',58,9,11,2,1,'high3@gmail.com','High'),

('High4','S214','1234',62,11,12,3,1,'high4@gmail.com','High'),

('High5','S215','1234',67,13,14,3,1,'high5@gmail.com','High')

]


cursor.executemany("""

INSERT INTO students

(name, student_id, password, attendance, internal1, internal2, assignment, study_hours, email, risk)

VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

""", students)


conn.commit()

conn.close()

print("✅ Database created with correct risk labels")