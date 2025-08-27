from sqlalchemy import Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship as relationship
from database import base

class Employee(base):
    __tablename__="Employee"
    id=Column(Integer,primary_key=True,index=True)
    emp_name=Column(String(200))
    emp_salary=Column(Float)
    dep_id=Column(Integer, ForeignKey("Department.dep_id")) 
    emp_email=Column(String(200),unique=True,index=True)
    emp_phone=Column(String(10),unique=True,index=True)
    emp_age=Column(Integer)

    department=relationship("Department", back_populates="employees")

class Department(base):
    __tablename__="Department"
    dep_id=Column(Integer,primary_key=True,index=True)
    dept_name=Column(String(200),unique=True,index=True)
    dept_manager=Column(String(200))
    dept_location=Column(String(200))

    employees = relationship("Employee", back_populates="department")
