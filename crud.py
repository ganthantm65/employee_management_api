import models
from validation import Validation
from database import engine,base

class AdminCrud:
    def register_admin(self,db,admin:models.Admin):
        admin.password=Validation().hash_password(admin.password)
        db.add(admin)
        db.commit()
        db.refresh(admin)
    def login_admin(self,db,username:str,password:str):
        admin=db.query(models.Admin).filter(models.Admin.username==username).first()
        if admin and Validation().verify_password(password,admin.password):
            return admin
        return None

class EmployeeCrud:
    def add_employee(self,db,employee:models.Employee):
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    def get_all_employee(self,db):
        return (
            db.query(models.Employee, models.Department)
            .join(models.Department, models.Employee.dep_id == models.Department.dep_id)
            .all()
        )
    def get_employee_by_name(self,db,name:str):
        return (
            db.query(models.Employee, models.Department)
            .join(models.Department, models.Employee.dep_id == models.Department.dep_id)
            .filter(models.Employee.emp_name == name)
            .first()
            )
    def update_employee(self,db,emp_id,employee:models.Employee):
        existing_emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
        if not existing_emp:
            return None   

        existing_emp.emp_name = employee.emp_name
        existing_emp.emp_salary = employee.emp_salary
        existing_emp.dep_id = employee.dep_id
        existing_emp.emp_email = employee.emp_email
        existing_emp.emp_phone = employee.emp_phone
        existing_emp.emp_age = employee.emp_age

        db.commit()
        db.refresh(existing_emp)
        return existing_emp
    def delete_employee(self,db,id:int):
        emp=db.query(models.Employee).filter(models.Employee.id==id).first()
        if emp:
            db.delete(emp)
            db.commit()
        return (
            db.query(models.Employee, models.Department)
            .join(models.Department, models.Employee.dep_id == models.Department.dep_id)
            .all()
        )
class DeparmentCrud:
    def add_department(self,db,department:models.Department):
        db.add(department)
        db.commit()
        db.refresh(department)
        return department
class BaseCrud(EmployeeCrud,DeparmentCrud,AdminCrud):
    def __init__(self):
        base.metadata.create_all(bind=engine)