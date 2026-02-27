import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# Create teacher table

cursor.execute("""

CREATE TABLE IF NOT EXISTS teachers(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT UNIQUE,

password TEXT

)

""")


# Insert teacher login

cursor.execute("""

INSERT OR IGNORE INTO teachers

(username,password)

VALUES

('teacher','admin123')

""")


conn.commit()
conn.close()

print("✅ Teacher login created")