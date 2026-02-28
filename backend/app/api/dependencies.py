from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

# Import your database session maker and models
from db.database import get_session 
from models.employee import Employee
from core.security import SECRET_KEY, ALGORITHM

# This tells FastAPI where the login endpoint is (we'll build it next)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)]
) -> Employee:
  
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
  )
  
  try:
      # Decode the token
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      username: str = payload.get("sub")
      
      if username is None:
          raise credentials_exception
  except InvalidTokenError:
      raise credentials_exception
      
  # Query your database using SQLModel
  # Adjust this query based on how you look up employees (e.g., by email or ID)
  employee = session.query(Employee).filter(Employee.email == username).first()
  
  if employee is None:
      raise credentials_exception
      
  return employee