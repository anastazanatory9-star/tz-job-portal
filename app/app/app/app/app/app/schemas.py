from pydantic import BaseModel

# -----------------------------
# User registration schema
# -----------------------------
class UserRegister(BaseModel):
    role: str
    phone: str
    email: str
    password: str | None = None
    nida: str | None = None
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
    eduLevel: str | None = None
    institution: str | None = None
    chairman: str
    balozi: str


# -----------------------------
# OTP verification schema
# -----------------------------
class OTPVerify(BaseModel):
    phone: str
    otp: str


# -----------------------------
# Job offer schema
# -----------------------------
class JobOfferSchema(BaseModel):
    employer_id: int
    job_title: str
    description: str
    region: str
    district: str
    ward: str


# -----------------------------
# Job application schema
# -----------------------------
class JobApplicationSchema(BaseModel):
    applicant_id: int
    offer_id: int
