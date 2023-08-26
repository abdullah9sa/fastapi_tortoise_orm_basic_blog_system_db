from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel
import datetime
from app.models.user import User

UserInCreate = pydantic_model_creator(User, name="UserInCreate", exclude_readonly=True)

user_pydantic_out = pydantic_model_creator(User,name="UserOut",exclude=("password",))

# Custom Pydantic models for output
class UserOutResponse(BaseModel):
    id: int
    username: str
    email: str
    join_date: datetime.datetime

