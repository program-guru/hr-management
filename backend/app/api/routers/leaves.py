from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

import app.crud.leaves as crud
from app.db.database import get_session
from app.models.employee import Employee, Role
from app.models.leaves import LeaveCreate, LeaveRead, LeaveUpdate
from app.api.dependencies import get_current_user, get_current_admin
from app.models.dto import DTO

router = APIRouter(prefix="/leaves", tags=["Leaves"])

@router.post("/", response_model=DTO[LeaveRead], status_code=status.HTTP_201_CREATED)
def apply_for_leave(
    leave_in: LeaveCreate,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[Employee, Depends(get_current_user)]
):
    if current_user.id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is invalid")
    
    leave = crud.create_leave_request(
        session=session, leave_in=leave_in, employee_id=current_user.id
    )
    return DTO(success=True, message="Leave request created successfully", data=leave)

@router.get("/", response_model=DTO[list[LeaveRead]])
def get_leaves(
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[Employee, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 100
):
    if current_user.id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is invalid")

    if current_user.role == Role.ADMIN:
        leaves = crud.get_all_leaves(session=session, skip=skip, limit=limit)
    else:
        leaves = crud.get_employee_leaves(
            session=session, employee_id=current_user.id, skip=skip, limit=limit
        )

    return DTO(success=True, message="Leaves retrieved successfully", data=leaves)

@router.patch("/{leave_id}", response_model=DTO[LeaveRead])
def update_leave_status_admin(
    leave_id: int,
    leave_update: LeaveUpdate,
    session: Annotated[Session, Depends(get_session)],
    current_admin: Annotated[Employee, Depends(get_current_admin)]
):
    if current_admin.id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin ID is invalid")
    
    db_leave = crud.get_leave_by_id(session=session, leave_id=leave_id)

    if not db_leave:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")
    
    updated_leave = crud.update_leave_status(
        session=session, db_leave=db_leave, leave_update=leave_update
    )
    return DTO(success=True, message="Leave status updated successfully", data=updated_leave)