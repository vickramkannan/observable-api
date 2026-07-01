from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

API_KEY = "ak_45rln8w59kkg9sgnszl8ogsj"
EMAIL = "22f3000616@ds.study.iitm.ac.in"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.post("/analytics")
def analytics(
    data: AnalyticsRequest,
    x_api_key: str = Header(None)
):

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401)

    total_events = len(data.events)

    users = set()
    revenue = 0
    totals = {}

    for e in data.events:
        users.add(e.user)

        if e.amount > 0:
            revenue += e.amount
            totals[e.user] = totals.get(e.user, 0) + e.amount

    top_user = max(totals, key=totals.get)

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user
    }