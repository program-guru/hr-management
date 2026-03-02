from datetime import date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.employee import Employee

# Define the states for admin approval workflow
class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# Base model with shared fields
class LeaveBase(SQLModel):
    start_date: date = Field(
        title="Start Date",
        description="First day of leave"
    )
    end_date: date = Field(
        title="End Date",
        description="Last day of leave"
    )
    reason: str = Field(
        title="Reason",
        description="Reason for the leave request"
    )
    status: LeaveStatus = Field(
        default=LeaveStatus.PENDING, 
        title="Leave Status",
        description="Current status of the request"
    )

# The actual database table
class Leave(LeaveBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    # Foreign key linking to the employee table
    employee_id: int = Field(foreign_key="employee.id", index=True)

    # Relationship back to the Employee model
    employee: Optional["Employee"] = Relationship(back_populates="leaves")

# Model for when an employee applies for leave
class LeaveCreate(SQLModel):
    start_date: date
    end_date: date
    reason: str

# Model for reading leave data
class LeaveRead(LeaveBase):
    id: int
    employee_id: int

# Model for admins to approve/reject leaves
class LeaveUpdate(SQLModel):
    status: LeaveStatus