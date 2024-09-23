from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from main import Student, Grade, Group, Subject, Teacher
from main import engine

Session = sessionmaker(bind=engine)
session = Session()

# 1.  5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    return session.query(
        Student.name, 
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

# 2.  студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    return session.query(
        Student.name, 
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Grade).join(Subject).filter(Subject.name == subject_name)\
    .group_by(Student.id).order_by(desc('avg_grade')).first()

# 3.  середній бал у групах з певного предмета.
def select_3(subject_name):
    return session.query(
        Group.name,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Student).join(Grade).join(Subject)\
    .filter(Subject.name == subject_name).group_by(Group.id).all()

# 4. середній бал на потоці (по всій таблиці оцінок).
def select_4():
    return session.query(
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).all()

# 5. які курси читає певний викладач.
def select_5(teacher_name):
    return session.query(Subject.name).join(Teacher)\
    .filter(Teacher.name == teacher_name).all()

# 6.  список студентів у певній групі.
def select_6(group_name):
    return session.query(Student.name).join(Group)\
    .filter(Group.name == group_name).all()

# 7.  оцінки студентів у окремій групі з певного предмета.
def select_7(group_name, subject_name):
    return session.query(
        Student.name, Grade.grade
    ).join(Group).join(Grade).join(Subject)\
    .filter(Group.name == group_name, Subject.name == subject_name).all()

# 8. середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_name):
    return session.query(
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Subject).join(Teacher)\
    .filter(Teacher.name == teacher_name).all()

# 9.  список курсів, які відвідує певний студент.
def select_9(student_name):
    return session.query(Subject.name).join(Grade).join(Student)\
    .filter(Student.name == student_name).all()

# 10. cписок курсів, які певному студенту читає певний викладач.
def select_10(student_name, teacher_name):
    return session.query(Subject.name).join(Grade).join(Student).join(Teacher)\
    .filter(Student.name == student_name, Teacher.name == teacher_name).all()
