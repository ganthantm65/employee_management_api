from fastapi import FastAPI, Depends, HTTPException, status
from request_models import EmployeeBase, EmployeeResponse, DepBase, DepResponse,AdminBase
from typing import List
from database import sessionLocal
from sqlalchemy.orm import Session
import models
from crud import BaseCrud

app = FastAPI()
employee_card = BaseCrud()
        
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/admin/register", status_code=status.HTTP_201_CREATED)
async def register_admin(admin: AdminBase, db: Session = Depends(get_db)):
    existing_admin = db.query(models.Admin).filter(models.Admin.username == admin.username).first()
    if existing_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    added_admin = models.Admin(
        username=admin.username,
        password=admin.password
    )
    employee_card.register_admin(db, added_admin)
    return {"message": "Admin registered successfully"}

@app.post("/admin/login", status_code=status.HTTP_200_OK)
async def login_admin(admin:AdminBase,db:Session=Depends(get_db)):
    logged_in_admin=employee_card.login_admin(db,admin.username,admin.password)
    if not logged_in_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username or password")
    return {"message":"Login successful"}

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

@app.post("/department/",response_model=DepResponse,status_code=status.HTTP_201_CREATED)
async def add_department(department:DepBase,db:Session=Depends(get_db)):
    dep_model=models.Department(
        dept_name=department.dep_name,
        dept_location=department.dep_location,
        dept_manager=department.dep_manager
    )
    saved_dep=employee_card.add_department(db,dep_model)
    return DepResponse(
        dep_id=saved_dep.dep_id,
        dep_name=saved_dep.dept_name,
        dep_location=saved_dep.dept_location,
        dep_manager=saved_dep.dept_manager
    )

@app.put("/employee/{emp_id}", response_model=EmployeeResponse)
async def update_employee(emp_id: int, emp: EmployeeBase, db: Session = Depends(get_db)):
    emp_model = models.Employee(
        id=emp_id,
        emp_name=emp.name,
        emp_age=emp.age,
        emp_phone=emp.phone,
        emp_email=emp.email,
        dep_id=emp.dep_id,
        emp_salary=emp.salary,
    )
    updated_emp = employee_card.update_employee(db, emp_id, emp_model)
    if not updated_emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    dep = db.query(models.Department).filter(models.Department.dep_id == updated_emp.dep_id).first()

    return EmployeeResponse(
        id=updated_emp.id,
        name=updated_emp.emp_name,
        age=updated_emp.emp_age,
        phone=updated_emp.emp_phone,
        email=updated_emp.emp_email,
        dep_name=dep.dept_name if dep else None,
        dep_location=dep.dept_location if dep else None,
        salary=updated_emp.emp_salary,
    )

@app.delete("/employee/{emp_id}",response_model=List[EmployeeResponse],status_code=status.HTTP_200_OK)
async def delete_employee(emp_id:int,db:Session=Depends(get_db)):
    employee=employee_card.delete_employee(db,emp_id)
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
        for emp,dep in employee
    ]
@app.get("/employee/", response_model=List[EmployeeResponse])
async def get_all_employee(db: Session = Depends(get_db)):
    results = employee_card.get_all_employee(db)

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
    result = employee_card.get_employee_by_name(db, name)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with name {name} not found"
        )

    emp, dep = result  
    return EmployeeResponse(
        id=emp.id,
        name=emp.emp_name,
        age=emp.emp_age,
        phone=emp.emp_phone,
        email=emp.emp_email,
        dep_name=dep.dept_name,
        dep_location=dep.dept_location,
        salary=emp.emp_salary,
    )

