"""Analytics endpoint API

Run with
```
uvicorn api:app --reload
```

Automated generated docs
```
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

OpenAPI json
```
http://127.0.0.1:8000/openapi.json
```

"""

from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend import Sql_conn

from sqlalchemy.exc import ProgrammingError


class Query(BaseModel):
    """Definition of the query schema

    Args:
        BaseModel (obj): Enforce the defined schema
    """
    select: str
    where: Optional[str] = None
    order_by: Optional[str] = None
    group_by: Optional[str] = None
    sort_by: Optional[str] = None


app = FastAPI()


@app.post("/analytics")
async def query_data(query: Query):
    try:
        return Sql_conn().request_query(query.dict())
    except ProgrammingError as err:
        raise HTTPException(status_code = 400, detail =  err.__repr__())
