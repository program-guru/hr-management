from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.crud.employee import create_employee, get_employee_by_email
from app.db.database import get_session
from app.models.employee import Employee, EmployeeCreate, EmployeeRead
from app.api.dependencies import get_current_admin

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_new_employee(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Employee, Depends(get_current_admin)],
    employee_in: EmployeeCreate
):
    # Use CRUD function to check for duplicates
    existing_employee = get_employee_by_email(session=session, email=employee_in.email)
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The employee with this email already exists in the system."
        )
    
    # Use CRUD function to create the employee
    new_employee = create_employee(session=session, employee_in=employee_in)
    
    return new_employee