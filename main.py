from fastapi import FastAPI, HTTPException, Request, Response
from datetime import datetime
from typing import Any
from random import randint
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

@app.post("/campaigns", status_code=201)
async def create_campaign(body: dict[str, Any]):
    new : Any = {
        "campaign_id": randint(100, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }

    data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{campaign_id}")
async def update_campaign(campaign_id: int, body: dict[str, Any]):
    for index, campaign in enumerate(data):
        if campaign["campaign_id"] == campaign_id:
                    updated : Any = {
                        "campaign_id": campaign_id,
                        "name": body.get("name"),
                        "due_date": body.get("due_date"),
                        "created_at": campaign.get("created_at")
                    }
                    data[index] = updated
                    return {"campaign": updated}
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.delete("/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: int):
    for index, campaign in enumerate(data):
        if campaign["campaign_id"] == campaign_id:
                    updated : Any = data.pop(index)
                    return Response(status_code=204, content=None)
    raise HTTPException(status_code=404, detail="Campaign not found")