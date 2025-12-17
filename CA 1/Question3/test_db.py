import sqlite3, uuid

def create_database():
    connection = sqlite3.connect('dbs_applications.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_number TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            qualifications TEXT NOT NULL,
            course TEXT NOT NULL,
            start_year INTEGER NOT NULL,
            start_month INTEGER NOT NULL,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    connection.close()

def generate_application_number():
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"APP-{unique_id}"

def save_application(data):
    connection = sqlite3.connect('dbs_applications.db')
    cursor = connection.cursor()
    app_number = generate_application_number()

    cursor.execute('''
        INSERT INTO applications (
            application_number,
            name,
            address,
            qualifications,
            course,
            start_year,
            start_month
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        app_number,
        data['name'],
        data['address'],
        data['qualifications'],
        data['course'],
        data['start_year'],
        data['start_month']
    ))

    connection.commit()
    connection.close()
    print("Inserted:", app_number)

create_database()
save_application({
    'name': 'Test Student',
    'address': 'Dublin',
    'qualifications': 'Bachelor',
    'course': 'MSc Cybersecurity',
    'start_year': 2025,
    'start_month': 9
})
