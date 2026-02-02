import os
import sys
import random
from faker import Faker
from datetime import datetime, timezone
from decimal import Decimal

# Add the project root to sys.path to allow imports from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.database.connection import SessionLocal, engine, Base
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.doctor_model import DoctorModel
from src.infrastructure.database.models.hospital_model import HospitalModel
from src.infrastructure.database.models.production_model import ProductionModel, ProductionType
from src.infrastructure.database.models.repasse_model import RepasseModel
from src.infrastructure.database.models.doctor_hospital_model import DoctorHospitalModel
from src.domain.enums.repasse_status import RepasseStatus
from passlib.context import CryptContext

fake = Faker('pt_BR')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    print("Ensuring database tables exist...")
    # Base.metadata.drop_all(bind=engine) # Don't drop for this script, we might want to append
    Base.metadata.create_all(bind=engine)

def create_demo_data():
    db = SessionLocal()
    try:
        print("Starting demo data creation process...")

        # 1. Check or Create Demo User
        email = "admin@seiwa.com"
        demo_user = db.query(UserModel).filter(UserModel.email == email).first()

        if not demo_user:
            print("Creating demo user...")
            demo_user = UserModel(
                name="Admin Usuario",
                email=email,
                password=pwd_context.hash("123456"),
                created_at=datetime.now(timezone.utc)
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print(f"User created: {demo_user.email} (pass: 123456)")
        else:
             print(f"User {email} already exists. Using existing user.")

        # 2. Create 5 Hospitals
        hospitals = []
        for _ in range(5):
            hospital = HospitalModel(
                name=f"{fake.company()} Hospital",
                address=fake.address(),
                created_at=datetime.now(timezone.utc),
                user_id=demo_user.id
            )
            hospitals.append(hospital)
        db.add_all(hospitals)
        db.commit()
        for h in hospitals: db.refresh(h)
        print(f"Created {len(hospitals)} hospitals.")

        # 3. Create 5 Doctors
        doctors = []
        for _ in range(5):
            doctor = DoctorModel(
                name=fake.name(),
                crm=f"{random.randint(1000, 99999)}/{fake.state_abbr()}",
                specialty=fake.job(),
                phone=fake.phone_number(),
                email=fake.unique.email(),
                created_at=datetime.now(timezone.utc),
                user_id=demo_user.id
            )
            doctors.append(doctor)
        db.add_all(doctors)
        db.commit()
        for d in doctors: db.refresh(d)
        print(f"Created {len(doctors)} doctors.")

        # 4. Associate Doctors with Hospitals
        doctor_hospital_relations = []
        for doctor in doctors:
            # Assign to 2 random hospitals
            assigned_hospitals = random.sample(hospitals, k=2)
            for hospital in assigned_hospitals:
                relation = DoctorHospitalModel(
                    doctor_id=doctor.id,
                    hospital_id=hospital.id,
                    created_at=datetime.now(timezone.utc)
                )
                doctor_hospital_relations.append(relation)
        db.add_all(doctor_hospital_relations)
        db.commit()
        print(f"Associated doctors with hospitals.")

        # 5. Create 5 Productions
        productions = []
        for i in range(5):
            doc = doctors[i]
            hosp = hospitals[i]

            prod_type = random.choice(list(ProductionType))

            production = ProductionModel(
                doctor_id=doc.id,
                hospital_id=hosp.id,
                type=prod_type,
                date=fake.date_between(start_date='-3m', end_date='today'),
                description=f"Produção Ref. {fake.month_name()}",
                created_at=datetime.now(timezone.utc),
                user_id=demo_user.id
            )
            productions.append(production)

        db.add_all(productions)
        db.commit()
        for p in productions: db.refresh(p)
        print(f"Created {len(productions)} productions.")

        # 6. Create 5 Repasses
        repasses = []
        for prod in productions:
            repasse = RepasseModel(
                production_id=prod.id,
                amount=Decimal(random.uniform(1000.0, 5000.0)),
                status=random.choice(list(RepasseStatus)),
                created_at=datetime.now(timezone.utc),
                user_id=demo_user.id
            )
            repasses.append(repasse)

        db.add_all(repasses)
        db.commit()
        print(f"Created {len(repasses)} repasses.")

        print("\n=== DEMO DATA CREATED SUCCESSFULLY ===")
        print(f"Login: {demo_user.email}")
        print(f"Password: 123456")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    create_demo_data()
