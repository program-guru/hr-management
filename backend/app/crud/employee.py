from sqlmodel import Session, select

from app.models.employee import Employee, EmployeeCreate
from app.core.security import get_password_hash

def get_employee_by_email(*, session: Session, email: str) -> Employee | None:
    statement = select(Employee).where(Employee.email == email)
    return session.exec(statement).first()

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