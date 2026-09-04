import sqlite3

connection = sqlite3.connect("calculator.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expression TEXT NOT NULL,
    result REAL NOT NULL
)
""")

cursor.execute("SELECT COUNT(*) FROM calculations")
count = cursor.fetchone()[0]

if count == 0:
    calculations = [
        ("10 + 20", 30),
        ("50 - 15", 35),
        ("6 * 7", 42),
        ("100 / 4", 25)
    ]

    cursor.executemany(
        "INSERT INTO calculations (expression, result) VALUES (?, ?)",
        calculations
    )

    connection.commit()
    print("Sample calculations inserted successfully!")
else:
    print("Sample data already exists. Nothing inserted.")

connection.close()