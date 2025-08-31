from pydantic import BaseModel

class AdminBase(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class AdminResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    name: str
    age: int
    phone: str
    email: str
    dep_id: int
    salary: float

    class Config:
        orm_mode = True
class DepBase(BaseModel):
    dep_name:str
    dep_location:str
    dep_manager:str
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
class DepResponse(BaseModel):
    dep_id: int
    dep_name:str
    dep_location:str
    dep_manager:str

    class Config:
        orm_mode = True
