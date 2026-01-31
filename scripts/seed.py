import os
import sys
import random
from faker import Faker
from datetime import datetime
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
    print("Recreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    try:
        print("Creating seed data...")

        # 1. Create Users
        users = []
        for _ in range(10):
            user = UserModel(
                name=fake.name(),
                email=fake.unique.email(),
                password=pwd_context.hash("123456"), # Default password
                created_at=datetime.utcnow()
            )
            users.append(user)
        db.add_all(users)
        db.commit() # Commit to get IDs
        print(f"Created {len(users)} users.")

        # 2. Create Hospitals
        hospitals = []
        for _ in range(10):
            hospital = HospitalModel(
                name=fake.company() + " Hospital",
                address=fake.address(),
                created_at=datetime.utcnow()
            )
            hospitals.append(hospital)
        db.add_all(hospitals)
        db.commit()
        print(f"Created {len(hospitals)} hospitals.")

        # 3. Create Doctors
        doctors = []
        for _ in range(10):
            doctor = DoctorModel(
                name=fake.name(),
                crm=f"{random.randint(1000, 99999)}/{fake.state_abbr()}",
                specialty=fake.job(),
                phone=fake.phone_number(),
                email=fake.unique.email(),
                created_at=datetime.utcnow()
            )
            doctors.append(doctor)
        db.add_all(doctors)
        db.commit()
        print(f"Created {len(doctors)} doctors.")

        # 4. Associate Doctors with Hospitals
        doctor_hospital_relations = []
        for doctor in doctors:
            # Assign each doctor to 1-3 random hospitals
            assigned_hospitals = random.sample(hospitals, k=random.randint(1, 3))
            for hospital in assigned_hospitals:
                # Check if relation already exists (unlikely given the logic but good practice)
                relation = DoctorHospitalModel(
                    doctor_id=doctor.id,
                    hospital_id=hospital.id,
                    created_at=datetime.utcnow()
                )
                doctor_hospital_relations.append(relation)
        db.add_all(doctor_hospital_relations)
        db.commit()
        print(f"Associated doctors with hospitals.")

        # 5. Create Productions
        productions = []
        for _ in range(10):
            doc = random.choice(doctors)
            hosp = random.choice(hospitals)

            prod_type = random.choice(list(ProductionType))

            production = ProductionModel(
                doctor_id=doc.id,
                hospital_id=hosp.id,
                type=prod_type,
                date=fake.date_between(start_date='-1y', end_date='today'),
                description=fake.sentence(),
                created_at=datetime.utcnow()
            )
            productions.append(production)

        db.add_all(productions)
        db.commit()
        print(f"Created {len(productions)} productions.")

        # 6. Create Repasses
        repasses = []
        for prod in productions:
            # Randomly decide if a repasse exists or multiple? Assuming 1 for now based on model usually being 1-to-many or 1-to-1.
            # Production - Repasse seems to be 1 production -> 1 or many repasses?
            # Model Repasse has production_id.

            repasse = RepasseModel(
                production_id=prod.id,
                valor=Decimal(random.uniform(100.0, 5000.0)),
                status=random.choice(list(RepasseStatus)),
                created_at=datetime.utcnow()
            )
            repasses.append(repasse)

        db.add_all(repasses)
        db.commit()
        print(f"Created {len(repasses)} repasses.")

        print("Seeding completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed()
