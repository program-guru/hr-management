from sqlmodel import Session, select

from app.models.employee import Employee, EmployeeCreate, EmployeeUpdate
from app.core.security import get_password_hash

def get_employee_by_email(*, session: Session, email: str) -> Employee | None:
    statement = select(Employee).where(Employee.email == email)
    return session.exec(statement).first()

def get_employee_by_id(*, session: Session, employee_id: int) -> Employee | None:
    return session.get(Employee, employee_id)

def get_multi_employees(*, session: Session, skip: int = 0, limit: int = 100) -> list[Employee]:
    statement = select(Employee).offset(skip).limit(limit)
    return list(session.exec(statement).all())

def create_employee(*, session: Session, employee_in: EmployeeCreate) -> Employee:
    # 1. Hash the password
    hashed_password = get_password_hash(employee_in.password)
    
    # 2. Create the database model
    db_employee = Employee.model_validate(
        employee_in, 
        update={"hashed_password": hashed_password}
    )
    
    # 3. Save to database
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    
    return db_employee

def update_employee(*, session: Session, db_employee: Employee, employee_in: EmployeeUpdate) -> Employee:
    # Extract only the fields that were actually provided in the update request
    update_data = employee_in.model_dump(exclude_unset=True)
    
    # Apply the updated fields to our database model object
    for key, value in update_data.items():
        setattr(db_employee, key, value)
        
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee

def delete_employee(*, session: Session, db_employee: Employee) -> Employee:
    session.delete(db_employee)
    session.commit()
    return db_employee