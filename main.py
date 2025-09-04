from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Any
app = FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

data : Any = [
    {
        "campaign_id": 1,
        "name": "Summer Launch",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    },
    {
        "campaign_id": 2,
        "name": "Black Friday",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    }
    ,{
        "campaign_id": 3,
        "name": "Campaign 3",
        "due_date": datetime.now(),
        "created_at": datetime.now()
    }
]

"""
Campaign
- campaign_id: int
- name: str
- due_date: datetime
- created_at: datetime
"""

@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}


@app.get("/campaigns/{campaign_id}")
async def read_campaign(campaign_id: int):
    for campaign in data:
        if campaign["campaign_id"] == campaign_id:
            return {"campaign": data[campaign_id - 1]}
    raise HTTPException(status_code=404, detail="Campaign not found")