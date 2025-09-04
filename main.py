from fastapi import FastAPI

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}


"""
Campaign
- campaign_id: int
- name: str
- due_date: datetime
- created_at: datetime
"""

@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": "example"}