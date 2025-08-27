from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from database import sessionLocal
from sqlalchemy.orm import Session
import models
from crud import EmployeeCrud

app = FastAPI()
employee_card = EmployeeCrud()

class EmployeeBase(BaseModel):
    name: str
    age: int
    phone: str
    email: str
    dep_id: int
    salary: float

    class Config:
        orm_mode = True

class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    email: str
    dep_name: str
    dep_location: str
    salary: float

    class Config:
        orm_mode = True

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/employee/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def add_employee(emp: EmployeeBase, db: Session = Depends(get_db)):
    emp_model = models.Employee(
        emp_name=emp.name,
        emp_age=emp.age,
        emp_phone=emp.phone,
        dep_id=emp.dep_id,
        emp_email=emp.email,
        emp_salary=emp.salary,
    )
    saved_emp = employee_card.add_employee(db, emp_model)
    return EmployeeResponse(
        id=saved_emp.id,
        name=saved_emp.emp_name,
        age=saved_emp.emp_age,
        phone=saved_emp.emp_phone,
        email=saved_emp.emp_email,
        dep_id=saved_emp.dep_id,
        salary=saved_emp.emp_salary,
    )

@app.get("/employee/", response_model=List[EmployeeResponse])
async def get_all_employee(db: Session = Depends(get_db)):
    results = employee_card.get_all_employee(db)

    for emp, dep in results:
        emp_dict = {c.name: getattr(emp, c.name) for c in emp.__table__.columns}
        dep_dict = {c.name: getattr(dep, c.name) for c in dep.__table__.columns}
        combined = {**emp_dict, "department": dep_dict}
        print(combined)

    return [
        EmployeeResponse(
            id=emp.id,
            name=emp.emp_name,
            age=emp.emp_age,
            phone=emp.emp_phone,
            email=emp.emp_email,
            dep_name=dep.dept_name,
            dep_location=dep.dept_location,
            salary=emp.emp_salary,
        )
        for emp, dep in results  
    ]

@app.get("/employee/{name}", response_model=EmployeeResponse)
async def get_employee_by_name(name: str, db: Session = Depends(get_db)):
    emp = employee_card.get_employee_by_name(db, name)
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with name {name} not found")
    return EmployeeResponse(
        id=emp.id,
        name=emp.emp_name,
        age=emp.emp_age,
        phone=emp.emp_phone,
        email=emp.emp_email,
        dep_id=emp.dep_id,
        salary=emp.emp_salary,
    )
