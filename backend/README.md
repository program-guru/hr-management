backend/
├── app/
│   ├── main.py              # The entry point of the FastAPI application
│   ├── api/
│   │   ├── dependencies.py  # Reusable dependencies (like checking current_user)
│   │   └── routers/         # API endpoints grouped by feature
│   │       ├── auth.py      
│   │       ├── employees.py 
│   │       ├── leaves.py    
│   │       └── payroll.py   
│   ├── core/                # App-wide settings and configurations
│   │   ├── config.py        # Environment variables (.env parsing)
│   │   └── security.py      # Password hashing, JWT token generation
│   ├── db/                  # Database setup
│   │   ├── database.py      # MySQL connection and session creation
│   │   └── redis.py         # Redis connection for caching
│   ├── models/              # SQLAlchemy Database Models (How data is stored in MySQL)
│   │   ├── employee.py
│   │   ├── leave.py
│   │   └── payroll.py
│   ├── schemas/             # Pydantic Models (How data is validated from the client)
│   │   ├── employee.py
│   │   ├── leave.py
│   │   └── payroll.py
│   ├── crud/                # Create, Read, Update, Delete functions (DB interactions)
│   │   ├── crud_employee.py
│   │   ├── crud_leave.py
│   │   └── crud_payroll.py
│   └── services/            # Core business logic and background tasks
│       ├── payroll_calc.py  # E.g., Complex salary calculations
│       └── email_service.py # E.g., Background task to send leave approval emails
├── alembic/                 # Database migration folder (tracks changes to your tables)
├── .env                     # Your secret keys, database URL, etc. (Never commit this!)
└── requirements.txt         # Project dependencies (FastAPI, SQLAlchemy, PyMySQL, etc.)