# backend/app/api/routers/payroll.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

import app.crud.payroll as crud
from app.db.database import get_session
from app.models.employee import Employee, Role
from app.models.payroll import PayrollCreate, PayrollRead
from app.api.dependencies import get_current_user, get_current_admin
from app.models.dto import DTO

router = APIRouter(prefix="/payroll", tags=["Payroll"])

@router.post("/{employee_id}", response_model=DTO[PayrollRead], status_code=status.HTTP_201_CREATED)
def create_payroll_for_employee(
    employee_id: int,
    payroll_in: PayrollCreate,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Employee, Depends(get_current_admin)]
):
    payroll = crud.create_payroll(
        session=session, payroll_in=payroll_in, employee_id=employee_id
    )
    return DTO[PayrollRead](
        success=True,
        message="Payroll created successfully",
        data=PayrollRead.model_validate(payroll)
    )

@router.get("/", response_model=DTO[list[PayrollRead]])
def get_payrolls(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[Employee, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
):
    assert current_user.id is not None
    
    if current_user.role == Role.ADMIN:
        payrolls = crud.get_all_payrolls(session=session, skip=skip, limit=limit)
    else:
        payrolls = crud.get_employee_payroll(
            session=session, employee_id=current_user.id, skip=skip, limit=limit
        )
    return DTO[list[PayrollRead]](
        success=True,
        message="Payrolls retrieved successfully",
        data=[PayrollRead.model_validate(p) for p in payrolls]
    )