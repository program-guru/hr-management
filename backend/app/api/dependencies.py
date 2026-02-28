from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select

from db.database import get_session
from models.employee import Employee
from app.core.config import settings


# OAuth2 scheme (points to your login endpoint)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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
    employee = session.exec(
        select(Employee).where(Employee.email == username)
    ).first()

    if employee is None:
        raise credentials_exception

    return employee