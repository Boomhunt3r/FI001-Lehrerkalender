import sqlite3
import datatime

def get_db_connection():
    conn = sqlite3.connect('lehrerkalender.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_login_data(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Login WHERE Email = ?',
                        (email,)).fetchone()
    return user

def get_all_classes():
    conn = get_db_connection()
    classes = conn.execute('SELECT * FROM Klasse ').fetchall()
    conn.close()
    return classes

def get_class(id):
    conn = get_db_connection()
    sclass = conn.execute('SELECT * FROM Klasse WHERE Klassenid = ?', (id,)).fetchone()
    return sclass

def get_all_students_in_class(id):
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM Schueler WHERE Klasse = ?', (id,)).fetchall()
    return students

def get_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM Schueler WHERE SchuelerID = ?', (id,)).fetchone()
    return student

def get_all_appointments():
    conn = get_db_connection()
    appointments = conn.execute('SELECT * FROM Termin ORDER BY Wochentag').fetchall()
    return appointments

def get_appointment(id):
    conn = get_db_connection()
    appointment = conn.execute('SELECT * FROM Termine WHERE TerminId = ?', (id,)).fetchone()
    return appointment

def get_all_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM Schueler').fetchall()
    return students

def set_student(Vorname, Nachname, Klasse, Klassenlehrer, PLZ, Straße, Hausnummer):
    conn = get_db_connection()
    conn.execute('INSERT INTO Schueler(Vorname, Nachname, Klasse, Klassenlehrer, PLZ, Straße, Hausnummer) VALUES (?,?,?,?,?,?, ?)',
                 (Vorname, Nachname, Klasse, Klassenlehrer, PLZ, Straße, Hausnummer))
    conn.commit()
    conn.close()

def set_class(Klassenname, Klassenlehrer):
    conn = get_db_connection()
    conn.execute('INSERT INTO Klasse(Klassenname, Klassenlehrer) VALUES (?, ?)',
                 (Klassenname, Klassenlehrer))
    conn.commit()
    conn.close()

def set_appointment(Titel, Zeitraum, Wochentag, Teilnehmer, Ort, Notiz):
    conn = get_db_connection()
    conn.execute('INSERT INTO Termin(Titel, erstelltAM, Zeitraum, Wochentag, Teilnehmer, Ort, Notiz) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (Titel, datatime.get_time(), Zeitraum, Wochentag, Teilnehmer, Ort, Notiz))
    conn.commit()
    conn.close()

def set_login_data(Email, Password):
    conn = get_db_connection()
    conn.execute('INSERT INTO Login(Email, Password) VALUES(?, ?)',
                 (Email, Password))
    conn.commit()
    conn.close()