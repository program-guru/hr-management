import jwt
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.crud.employee import get_employee_by_email
from app.db.database import get_session
from app.models.employee import Employee, Role
from app.core.config import settings

# OAuth2 scheme (points to your login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency to get the current user based on the JWT token
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)],
) -> Employee:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        # Extract subject (email)
        username = payload.get("sub")

        if not isinstance(username, str):
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    # Query database
    employee = get_employee_by_email(session=session, email=username)

    if employee is None:
        raise credentials_exception

    return employee

# Dependency to ensure the current user is an admin
def get_current_admin(
    current_user: Annotated[Employee, Depends(get_current_user)]
) -> Employee:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action. Admins only."
        )
    return current_user