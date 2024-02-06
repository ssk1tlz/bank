from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import re

def init_db():
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bank
        (username TEXT PRIMARY KEY, password TEXT, surname TEXT, patronymic TEXT, birth_date TEXT, gender TEXt, passport_series TEXT, passport_number TEXT UNIQUE, passport_issued_by TEXT, passport_issue_date TEXT, id_number TEXT UNIQUE, registration_city TEXT, current_address TEXT, phone_home TEXT, phone_mobile TEXT, email TEXT, residencecity TEXT, citizenship TEXT, residenceaddress TEXT, marital_status TEXT, citizenship TEXT, disability TEXT, pensioner TEXT)
    ''')
    conn.close()

def add_account(username, password, surname, patronymic, birth_date, gender, passport_series, passport_number, passport_issued_by, passport_issue_date, id_number, birth_place, registration_city, current_address, phone_home, phone_mobile, email, residencecity, residenceaddress, marital_status, citizenship, disability, pensioner):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    hashed_password = generate_password_hash(password)
    c.execute('INSERT INTO bank (username, password, surname, patronymic, birth_date, gender, passport_series, passport_number, passport_issued_by, passport_issue_date, id_number, birth_place, registration_city, current_address, phone_home, phone_mobile, email, residencecity, residenceaddress, marital_status, citizenship, disability, pensioner) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (username, password, surname, patronymic, birth_date, gender, passport_series, passport_number, passport_issued_by, passport_issue_date, id_number, birth_place, registration_city, current_address, phone_home, phone_mobile, email, residencecity, residenceaddress, marital_status, citizenship, disability, pensioner))
    conn.commit()
    conn.close()

def check_account(username, password):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute('SELECT password FROM bank WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    if data is None:
        return False
    return check_password_hash(data[0], password)

def get_account(username):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bank WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    return data

def check_username_exists(username):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute('SELECT username FROM bank WHERE username = ?', (username,))
    data = c.fetchone()
    conn.close()
    return data is not None

def check_passport_number_exists(passport_number):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute('SELECT passport_number FROM bank WHERE passport_number = ?', (passport_number,))
    data = c.fetchone()
    conn.close()
    return data is not None

def check_id_number_exists(id_number):
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute('SELECT id_number FROM bank WHERE id_number = ?', (id_number,))
    data = c.fetchone()
    conn.close()
    return data is not None

def get_all_accounts():
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()
    c.execute('SELECT username FROM bank')
    data = c.fetchall()
    conn.close()
    return data
