from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.crud.employee import get_employee_by_email
from app.db.database import get_session
from app.models.dto import DTO
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=DTO[dict])
def login_access_token(
    session: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    # Query the user
    user = get_employee_by_email(session=session, email=form_data.username)
    
    # Verify the user exists and the password matches
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect email or password"
        )
    
    # Generate the JWT token
    # We include the role in the token payload to make authorization easier later
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    
    return DTO(
        success=True,
        message="Login successful",
        data={"access_token": access_token, "token_type": "bearer"}
    )