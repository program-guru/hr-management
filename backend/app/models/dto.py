from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

# Define a generic type variable
T = TypeVar('T')

class DTO(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
