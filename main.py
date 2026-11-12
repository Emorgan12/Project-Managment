from sqlmodel import SQLModel, Field
from fastapi import FastAPI
from uuid import UUID
app = FastAPI()

class Client(SQLModel):
    id: UUID
    first_name: str = Field(default="")
    middle_name: str = Field(default="")
    last_name: str = Field(default="")
