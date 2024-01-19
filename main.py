from hashlib import md5
from typing import Dict

from pydantic import BaseModel, HttpUrl
from fastapi import FastAPI, HTTPException


app = FastAPI()


class URLModel(BaseModel):
    long_url: HttpUrl
    short_url: str = None


class DatabaseModel(BaseModel):
    dictionary: Dict[str, URLModel]


database = DatabaseModel(dictionary={})


@app.post("/shorten")
async def shorten_url(url: URLModel):
    key = md5(str(url.long_url).encode("utf-8")).hexdigest()[:6]
    if key in database.dictionary.keys():
        return database.dictionary[key]

    url.short_url = f"https://example.com/{key}"
    database.dictionary[key] = url
    return {"short_url": url.short_url}


@app.get("/elongate/{key}")
async def redirect_to_long_url(key: str):
    if key in database.dictionary.keys():
        return {"long_url": database.dictionary[key].long_url}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
