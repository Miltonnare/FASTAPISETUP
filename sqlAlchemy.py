from fastapi import FastAPI, Depends,HTTPException
from typing import Annotated
from sqlmodel import Field,Session,SQLModel,create_engine,select


class Hero(SQLModel,table=True):
    id: int = Field(default=None,primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
    

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url,echo=True)