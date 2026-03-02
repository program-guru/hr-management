from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from pydantic import EmailStr
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.payroll import Payroll
  from app.models.leaves import Leave

# Define user roles for Authorization
class Role(str, Enum):
  ADMIN = "admin"
  EMPLOYEE = "employee"

class Department(str, Enum):
  HR = "HR"
  ENGINEERING = "Engineering"
  SALES = "Sales"
  MARKETING = "Marketing"
  FINANCE = "Finance"

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
  leave_balance: int = Field(
        default=20,
        title="Leave Balance",
        description="Number of available leave days"
  )
  department: Department = Field(
      default=Department.HR,
      title="Department",
      description="Department the employee belongs to"
  )

# Actual database table
class Employee(EmployeeBase, table=True):
  id: int | None = Field(default=None, primary_key=True, title="Employee ID")
  hashed_password: str = Field(
      title="Hashed Password",
      description="Securely hashed password for authentication"
  )
  leaves: list["Leave"] = Relationship(back_populates="employee")
  payrolls: list["Payroll"] = Relationship(back_populates="employee")

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
  department: Department | None = Field(
      default=None,
      title="Department",
      description="Department the employee belongs to",
  )