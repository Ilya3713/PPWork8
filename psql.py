import psycopg2
from datetime import datetime

conn = psycopg2.connect("dbname=ODS user=io.mikhailutca")

cur = conn.cursor()

now = datetime.now()

s1 = {
    'name': 'Василий Пупкин',
    'gpa': 4.7,
    'birth': now
}


def create_db():  # создает таблицы
    cur.execute("""CREATE TABLE Student (
    id serial PRIMARY KEY,
    name varchar(100),
    gpa numeric(10,2),
    birth timestamp with time zone);
    """)
    cur.execute("""CREATE TABLE Course (
    id serial PRIMARY KEY,
    name varchar(100));
    """)
    cur.execute("""CREATE TABLE Student_Course (
    id serial PRIMARY KEY,
    student_id INTEGER REFERENCES Student(id),
    course_id INTEGER REFERENCES Course(id));
    """)
    conn.commit()


def get_students(course_id):  # возвращает студентов определенного курса
    cur.execute(f'select student_id from Student_Course where course_id={course_id}')
    return cur.fetchall()

def add_students(course_id, students):  # создает студентов и записывает их на курс
    cur.execute('insert into Student (name, gpa, birth) values (%s, %s, %s)', (s1['name'], s1['gpa'],
                                                                               s1['birth']))
    conn.commit()
    cur.execute('insert into Student_Course (student_id, course_id) values (%s, %s)', (students, course_id))
    conn.commit()


def add_student(student):
    # просто создает студента
    cur.execute(""" INSERT INTO student (name, gpa, birth)
        VALUES (%s, %s, %s);
        """, (student["name"], student["gpa"], student["birth"], ))
    cur.execute("""SELECT * FROM student ORDER BY id DESC LIMIT 1;""")
    conn.commit()
    last_added_student = cur.fetchone()
    # возвращает id только что созданного студента
    return last_added_student[0]


def get_student(student_id):
    cur.execute(f'select name from Student where student_id={student_id}')
    return cur.fetchall()


create_db()
add_student(s1)
get_students(1)
