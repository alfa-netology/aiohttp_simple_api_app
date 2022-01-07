from pydantic import BaseModel, EmailStr, constr


class UserSerializer(BaseModel):
    username: constr(min_length=5, max_length=25)
    email: EmailStr
    password: constr(min_length=8, max_length=30)
    
class AdvertisingSerializer(BaseModel):
    title: str
    text: str
    user_id: int
