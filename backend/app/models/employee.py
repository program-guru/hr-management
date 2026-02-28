from sqlmodel import Field, SQLModel
from enum import Enum
from pydantic import EmailStr

# Define user roles for Authorization
class Role(str, Enum):
  ADMIN = "admin"
  EMPLOYEE = "employee"

# Base model for Employee with common fields
class EmployeeBase(SQLModel):
  name: str = Field(
      min_length=2,
      max_length=100,
      index=True,
      title="Employee Name",
      description="Full name of the employee",
  )
  email: EmailStr = Field(
      unique=True,
      index=True,
      title="Email Address",
      description="Unique email address for the employee",
  )
  role: Role = Field(
      default=Role.EMPLOYEE,
      title="User Role",
      description="Role assigned to the employee (admin or employee)",
  )


# Actual database table
class Employee(EmployeeBase, table=True):
  id: int | None = Field(default=None, primary_key=True, title="Employee ID")
  hashed_password: str = Field(
      title="Hashed Password",
      description="Securely hashed password for authentication"
  )


# Public model for reading
class EmployeeRead(EmployeeBase):
  id: int = Field(title="Employee ID", description="Unique identifier")


# Model for creating a new employee
class EmployeeCreate(EmployeeBase):
  password: str = Field(
      min_length=8,
      max_length=128,
      title="Password",
      description="Password for authentication (min 8 characters)",
  )

# Model for updating an existing employee
class EmployeeUpdate(SQLModel):
  id: int = Field(title="Employee ID", description="ID of employee to update")
  name: str | None = Field(
      default=None,
      min_length=2,
      max_length=100,
      index=True,
      title="Employee Name",
      description="Full name of the employee",
  )
  email: EmailStr | None = Field(
      default=None,
      unique=True,
      index=True,
      title="Email Address",
      description="Email address of the employee",
  )
  role: Role | None = Field(
      default=None,
      title="User Role",
      description="Role to assign (admin or employee)",
  )