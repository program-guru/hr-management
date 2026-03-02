from fastapi import HTTPException, status
from sqlmodel import Session, desc, select

from app.models.payroll import Payroll, PayrollCreate
from app.models.employee import Employee

def create_payroll(*, session: Session, payroll_in: PayrollCreate, employee_id: int) -> Payroll:
    # Verify the employee exists before generating payroll
    employee = session.get(Employee, employee_id)

    if not employee:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    # Create the database model, merging the input data with our secure calculations
    db_payroll = Payroll.model_validate(
        payroll_in, 
        update={
            "employee_id": employee_id,
        }
    )
    
    # Save to the database
    session.add(db_payroll)
    session.commit()
    session.refresh(db_payroll)
    
    return db_payroll

def get_employee_payroll(*, session: Session, employee_id: int, skip: int = 0, limit: int = 100) -> list[Payroll]:
    statement = select(Payroll).where(Payroll.employee_id == employee_id).order_by(desc(Payroll.payment_date)).offset(skip).limit(limit)
    return list(session.exec(statement).all())

def get_all_payrolls(*, session: Session, skip: int = 0, limit: int = 100) -> list[Payroll]:
    statement = select(Payroll).order_by(desc(Payroll.payment_date)).offset(skip).limit(limit)
    return list(session.exec(statement).all())