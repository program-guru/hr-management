from sqlmodel import Session, select
from app.db.database import engine
from app.models.employee import Employee, Role
from app.core.security import get_password_hash

def seed_admin():
    with Session(engine) as session:
        # Check if an admin already exists to avoid duplicates
        statement = select(Employee).where(Employee.role == Role.ADMIN)
        existing_admin = session.exec(statement).first()
        
        if existing_admin:
            print(f"Admin already exists: {existing_admin.email}")
            return

        # Create the initial admin user
        admin_user = Employee(
            name="Super Admin",
            email="admin@hrconnect.com",
            role=Role.ADMIN,
            hashed_password=get_password_hash("123456789")
        )
        
        session.add(admin_user)
        session.commit()
        session.refresh(admin_user)
        print(f"Successfully created admin user: {admin_user.email}")

if __name__ == "__main__":
    print("Seeding database...")
    seed_admin()