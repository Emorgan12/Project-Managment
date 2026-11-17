from sqlmodel import SQLModel, Field, create_engine, select, Session
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID, uuid4
from typing import Annotated
from datetime import datetime, timezone
from enum import Enum

class ClientBase(SQLModel):
    first_name: str = Field(default="")
    middle_name: str = Field(default="")
    last_name: str = Field(default="")
    company: str = Field(default="")
    client_email: str = Field(default="")

class Client(ClientBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

class TenderStatus(str, Enum):
    IN_PROGRESS = "In Progress"
    NOT_STARTED = "Not Started"
    COMPLETED = "Completed"

class TenderBase(SQLModel):
    client_id: UUID | None = Field(default= None, nullable=True)
    tender_name: str = Field(default="")
    log_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deadline: datetime | None = Field(default= None, nullable=True)
    status: TenderStatus = Field(default=TenderStatus.NOT_STARTED)
    hours_spent: float = Field(default=0)

class Tender(TenderBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

engine = create_engine("sqlite:///database.db")

def get_session():
    with Session(engine) as session:
        yield session

session_dep  = Annotated[Session, Depends(get_session)]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get-clients/", response_model=list[Client])
def get_clients(session: session_dep):
    clients = session.exec(select(Client)).all()
    return clients

@app.get("/get-client-by-id/", response_model=Client)
def get_client_by_id(client_id : UUID, session: session_dep):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client Not Found")
    return client


@app.post("/create-clients/", response_model=Client)
def create_client(client_in: ClientBase, session: session_dep):
    db_client = Client.model_validate(client_in)
    session.add(db_client)
    session.commit()
    session.refresh(db_client)
    return db_client

@app.post("/create-tender/", response_model=Tender)
def create_tender(tender_in: TenderBase, session:session_dep):
    if tender_in.client_id != None:
        get_client_by_id(tender_in.client_id, session)

    db_tender = Tender.model_validate(tender_in)
    session.add(db_tender)
    session.commit()
    session.refresh(db_tender)
    return db_tender

@app.get("/get-tenders/", response_model= list[Tender])
def get_tenders(session: session_dep):
    tenders = session.exec(select(Tender)).all()
    return tenders