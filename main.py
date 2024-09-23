from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from faker import Faker
import random


engine = create_engine('postgresql://Alexey:Alessio@localhost:5432/universityGoIt')
Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="students")

Group.students = relationship("Student", order_by=Student.id, back_populates="group")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher", back_populates="subjects")

Teacher.subjects = relationship("Subject", order_by=Subject.id, back_populates="teacher")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Float, nullable=False)
    date_received = Column(Date, nullable=False)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

Student.grades = relationship("Grade", order_by=Grade.id, back_populates="student")
Subject.grades = relationship("Grade", order_by=Grade.id, back_populates="subject")


Base.metadata.create_all(engine)

# Заповнення таблиці
faker = Faker()
Session = sessionmaker(bind=engine)
session = Session()

# групп
groups = [Group(name=f'Group {i}') for i in range(1, 4)]
session.add_all(groups)
session.commit()

# вчителів
teachers = [Teacher(name=faker.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# предмети
subjects = [Subject(name=f'Subject {i}', teacher=random.choice(teachers)) for i in range(1, 9)]
session.add_all(subjects)
session.commit()

# студентів
students = [Student(name=faker.name(), group=random.choice(groups)) for _ in range(50)]
session.add_all(students)
session.commit()

# оцінки
for student in students:
    for subject in subjects:
        for _ in range(random.randint(10, 20)):
            grade = Grade(student=student, subject=subject, grade=random.uniform(60, 100), date_received=faker.date_this_year())
            session.add(grade)

session.commit()
