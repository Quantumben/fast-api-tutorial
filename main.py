from fastapi import FastAPI

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

data = [
    {
        "campaign_id": 1,
        "name": "Campaign 1",
        "due_date": "2024-12-31T23:59:59",
        "created_at": "2024-01-01T12:00:00"
    },
    {
        "campaign_id": 2,
        "name": "Campaign 2",
        "due_date": "2024-11-30T23:59:59",
        "created_at": "2024-02-01T12:00:00"
    }
    ,{
        "campaign_id": 3,
        "name": "Campaign 3",
        "due_date": "2024-10-31T23:59:59",
        "created_at": "2024-03-01T12:00:00"
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