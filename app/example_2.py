"""
uvicorn example_2:app --reload

http://localhost:8000/

http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc

http://127.0.0.1:8000/openapi.json
"""

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Query(BaseModel):
    select: str
    where: Optional[str] = None
    order_by: Optional[str] = None
    sort_by: Optional[str] = None


app = FastAPI()


@app.post("/analytics")
async def query_data(query: Query):
    return query