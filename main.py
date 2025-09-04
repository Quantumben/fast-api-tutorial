from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timezone
from typing import Annotated, Generic, TypeVar
from sqlmodel import SQLModel, create_engine, Session, select, Field
from contextlib import asynccontextmanager
from pydantic import BaseModel

class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True, index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="Summer Launch", due_date=datetime.now()),
                Campaign(name="Black Friday", due_date=datetime.now())
            ])
            session.commit()
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(root_path="/api/v1", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    data: T

class CampaignCreate(SQLModel):
    name: str
    due_date: datetime | None = None

@app.get("/campaigns", response_model=Response[list[Campaign]])
async def read_campaigns(session: SessionDep):
    data = session.exec(select(Campaign)).all()
    return {"data": data}

@app.get("/campaigns/{campaign_id}", response_model=Response[Campaign])
async def read_campaign(campaign_id: int, session: SessionDep):
    data = session.get(Campaign, campaign_id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"data": data}

@app.post("/campaigns", response_model=Response[Campaign], status_code=201)
async def create_campaign(body: CampaignCreate, session: SessionDep):
    new_campaign = Campaign(name=body.name, due_date=body.due_date)
    db_campaign = Campaign.model_validate(new_campaign)
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"data": db_campaign}

@app.put("/campaigns/{campaign_id}", response_model=Response[Campaign])
async def update_campaign(campaign_id: int, body: CampaignCreate, session: SessionDep):
    data = session.get(Campaign, campaign_id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    data.name = body.name
    data.due_date = body.due_date
    session.add(data)
    session.commit()
    session.refresh(data)
    return {"data": data}

@app.delete("/campaigns/{campaign_id}", status_code=204)
async def delete_campaign(campaign_id: int, session: SessionDep):
    data = session.get(Campaign, campaign_id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    session.delete(data)
    session.commit()