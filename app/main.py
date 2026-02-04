from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User, JobOffer, JobApplication
from pydantic import BaseModel
from auth import create_access_token, generate_otp
from passlib.hash import bcrypt

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tanzania Job Portal Backend")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------
# Schemas
# -----------------------
class UserRegister(BaseModel):
    role: str
    phone: str
    email: str
    password: str = None
    nida: str = None
    firstName: str
    middleName: str
    lastName: str
    dob: str
    gender: str
    region: str
    district: str
    ward: str
    street: str
    house: str
    jobCategory: str
    eduLevel: str = None
    institution: str = None
    chairman: str
    baloozi: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

class JobOfferSchema(BaseModel):
    employer_id: int
    job_title: str
    description: str
    region: str
    district: str
    ward: str

class JobApplicationSchema(BaseModel):
    applicant_id: int
    offer_id: int

# -----------------------
# Register User
# -----------------------
@app.post("/api/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter((User.email==user.email)|(User.nida==user.nida)|(User.phone==user.phone)).first():
        raise HTTPException(status_code=400, detail="Email/NIDA/Phone already registered")
    otp_code = generate_otp()
    db_user = User(
        role=user.role,
        phone=user.phone,
        email=user.email,
        password_hash=bcrypt.hash(user.password) if user.password else None,
        nida=user.nida,
        firstName=user.firstName,
        middleName=user.middleName,
        lastName=user.lastName,
        dob=user.dob,
        gender=user.gender,
        region=user.region,
        district=user.district,
        ward=user.ward,
        street=user.street,
        house=user.house,
        jobCategory=user.jobCategory,
        eduLevel=user.eduLevel,
        institution=user.institution,
        chairman=user.chairman,
        baloozi=user.baloozi,
        otp=otp_code,
        verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"Simulated OTP for {user.phone}: {otp_code}")  # console for prototype
    return {"message": "User registered. OTP sent.", "user_id": db_user.id}

# -----------------------
# Verify OTP
# -----------------------
@app.post("/api/verify-otp")
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.phone==data.phone).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    db_user.verified = True
    db_user.otp = None
    db.commit()
    token = create_access_token({"sub": db_user.phone, "role": db_user.role})
    return {"message": "OTP verified", "access_token": token}

# -----------------------
# Create Job Offer
# -----------------------
@app.post("/api/job-offer")
def create_job_offer(offer: JobOfferSchema, db: Session = Depends(get_db)):
    job_offer = JobOffer(
        employer_id=offer.employer_id,
        job_title=offer.job_title,
        description=offer.description,
        region=offer.region,
        district=offer.district,
        ward=offer.ward
    )
    db.add(job_offer)
    db.commit()
    db.refresh(job_offer)
    return {"message": "Job offer created", "offer_id": job_offer.id}

# -----------------------
# Apply for Job
# -----------------------
@app.post("/api/apply-job")
def apply_job(application: JobApplicationSchema, db: Session = Depends(get_db)):
    db_application = JobApplication(
        applicant_id=application.applicant_id,
        offer_id=application.offer_id
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return {"message": "Applied successfully", "application_id": db_application.id}

# -----------------------
# List Users (admin)
# -----------------------
@app.get("/api/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# -----------------------
# List Job Offers
# -----------------------
@app.get("/api/job-offers")
def list_offers(db: Session = Depends(get_db)):
    return db.query(JobOffer).all()

# -----------------------
# List Applications (admin)
# -----------------------
@app.get("/api/applications")
def list_applications(db: Session = Depends(get_db)):
    return db.query(JobApplication).all()
