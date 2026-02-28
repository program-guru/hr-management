from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.leaves import Leave, LeaveCreate, LeaveUpdate, LeaveStatus
from app.models.employee import Employee

def create_leave_request(*, session: Session, leave_in: LeaveCreate, employee_id: int) -> Leave:
    # We force the employee_id from the logged-in user's token, not from their input
    db_leave = Leave.model_validate(leave_in, update={"employee_id": employee_id})
    session.add(db_leave)
    session.commit()
    session.refresh(db_leave)
    return db_leave

def get_employee_leaves(*, session: Session, employee_id: int, skip: int = 0, limit: int = 100) -> list[Leave]:
    statement = select(Leave).where(Leave.employee_id == employee_id).offset(skip).limit(limit)
    return list(session.exec(statement).all())

def get_all_leaves(*, session: Session, skip: int = 0, limit: int = 100) -> list[Leave]:
    statement = select(Leave).offset(skip).limit(limit)
    return list(session.exec(statement).all())

def get_leave_by_id(*, session: Session, leave_id: int) -> Leave | None:
    return session.get(Leave, leave_id)

def update_leave_status(*, session: Session, db_leave: Leave, leave_update: LeaveUpdate) -> Leave:
    # If the admin is approving the leave, we need to update the employee's balance
    if leave_update.status == LeaveStatus.APPROVED and db_leave.status == LeaveStatus.PENDING:
        # Calculate the number of days requested (inclusive)
        leave_days = (db_leave.end_date - db_leave.start_date).days + 1
        
        # Fetch the employee to check and update their balance
        employee = session.get(Employee, db_leave.employee_id)
        
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
            
        if employee.leave_balance < leave_days:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Insufficient leave balance. Employee has {employee.leave_balance} days, but requested {leave_days}."
            )
        
        # Deduct the balance
        employee.leave_balance -= leave_days
        session.add(employee)

    # Update the leave status
    db_leave.status = leave_update.status
    session.add(db_leave)
    session.commit()
    session.refresh(db_leave)
    
    return db_leave