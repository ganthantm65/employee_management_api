import models
from database import engine,base

class EmployeeCrud:
    def __init__(self):
        base.metadata.create_all(bind=engine)
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
        return db.query(models.Employee).filter(models.Employee.emp_name==name).first()
    def update_employee(self,db,employee:models.Employee):
        db.merge(employee)
        db.commit()
        return db.query(models.Employee).all()
    def delete_employee(self,db,id:int):
        emp=db.query(models.Employee).filter(models.Employee.id==id).first()
        if emp:
            db.delete(emp)
            db.commit()
        return db.query(models.Employee).all()
