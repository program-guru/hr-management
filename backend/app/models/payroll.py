from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.employee import Employee

class PayrollBase(SQLModel):
    basic_pay: float = Field(
        title="Basic Pay", 
        description="Base salary amount"
    )
    deductions: float = Field(
        default=0.0, 
        title="Deductions", 
        description="Total deductions (taxes, insurance, etc.)"
    )
    payment_date: date = Field(
        title="Payment Date", 
        description="Date the salary was processed"
    )

# The actual database table
class Payroll(PayrollBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    # Foreign key linking to the employee table
    employee_id: int = Field(foreign_key="employee.id", index=True)

    # Relationship back to the Employee model
    employee: "Employee" = Relationship(back_populates="payrolls")

# Model for admins to create a payroll record
class PayrollCreate(PayrollBase):
    pass

# Model for securely reading payroll data
class PayrollRead(PayrollBase):
    id: int
    employee_id: int