from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

import app.crud.employee as crud
from app.db.database import get_session
from app.models.employee import Employee, EmployeeCreate, EmployeeRead, EmployeeUpdate, Role
from app.api.dependencies import get_current_admin, get_current_user
from app.models.dto import DTO

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=DTO[EmployeeRead], status_code=status.HTTP_201_CREATED)
def create_new_employee(
    *,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Employee, Depends(get_current_admin)],
    employee_in: EmployeeCreate
):
    # Use CRUD function to check for duplicates
    existing_employee = crud.get_employee_by_email(session=session, email=employee_in.email)
    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The employee with this email already exists in the system."
        )
    
    # Use CRUD function to create the employee
    new_employee = crud.create_employee(session=session, employee_in=employee_in)
    
    return DTO(
        success=True,
        message="Employee created successfully",
        data=new_employee
    )

@router.get("/", response_model=DTO[list[EmployeeRead] | EmployeeRead])
def read_employees(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[Employee, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100,
):
    if current_user.role != Role.ADMIN:
        # Non-admin users can only see their own record
        return DTO(
            success=True,
            message="Employee retrieved successfully",
            data=current_user
        )

    employees = crud.get_multi_employees(session=session, skip=skip, limit=limit)
    return DTO(
        success=True,
        message="Employees retrieved successfully",
        data=employees
    )

@router.get("/{employee_id}", response_model=DTO[EmployeeRead])
def read_employee_by_id(
    employee_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Employee, Depends(get_current_admin)]
):
    employee = crud.get_employee_by_id(session=session, employee_id=employee_id)
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return DTO(
        success=True,
        message="Employee retrieved successfully",
        data=employee
    )

@router.patch("/{employee_id}", response_model=DTO[EmployeeRead])
def update_employee(
    employee_id: int,
    employee_in: EmployeeUpdate,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Employee, Depends(get_current_admin)]
):
    db_employee = crud.get_employee_by_id(session=session, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    updated_employee = crud.update_employee(
        session=session, db_employee=db_employee, employee_in=employee_in
    )
    return DTO(
        success=True,
        message="Employee updated successfully",
        data=updated_employee
    )

@router.delete("/{employee_id}", response_model=DTO[None])
def delete_employee(
    employee_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Employee, Depends(get_current_admin)]
):
    db_employee = crud.get_employee_by_id(session=session, employee_id=employee_id)
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    crud.delete_employee(session=session, db_employee=db_employee)
    return DTO(
        success=True,
        message="Employee deleted successfully",
        data=None
    )