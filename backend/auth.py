from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from pocketbase_service import pb

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    confirmPassword: str


@router.post("/login")
async def login(login_data: LoginRequest):

    try:

        auth = pb.collection("users").auth_with_password(
            login_data.email,
            login_data.password
        )

        return {
            "status": "success",
            "message": "Login Successful",

            "token": auth.token,
        "user": {
            "id": auth.record.id,
            "username": auth.record.username,
            "email": auth.record.email,
            "roles": auth.record.roles
        }
        }

    except Exception as e:
        print("LOGIN ERROR:", e)

        raise HTTPException(
            status_code=401,
            detail=str(e)
    )

@router.post("/signup")
async def signup(data: SignupRequest):

    # Password validation
    if data.password != data.confirmPassword:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match."
        )

    try:

        pb.collection("users").create({

            "username": data.username,

            "email": data.email,

            "password": data.password,

            "passwordConfirm": data.confirmPassword,

            # Every new user becomes an Operator
            "roles": "OPERATOR"

        })

        return {
            "status": "success",
            "message": "Account created successfully."
        }


    except Exception as e:

        error_message = str(e)

        if "Failed to authenticate" in error_message:

            raise HTTPException(
                status_code=401,
                detail="No account found with this email or the password is incorrect."
            )

        raise HTTPException(
            status_code=500,
            detail="Something went wrong. Please try again."
        )