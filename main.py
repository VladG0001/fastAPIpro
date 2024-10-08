from fastapi import FastAPI, HTTPException
from pydantic import HttpUrl
from bs4 import BeautifulSoup
import httpx

app = FastAPI()

@app.get("/")
async def home():
    return "Welcome to the Web Scraper API! Use /parse endpoint to parse URLs."

@app.get("/parse")
async def parse_url(url: HttpUrl, extract: str = "titles"):

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="URL not found")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Unable to complete the request")


    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch the URL")


    soup = BeautifulSoup(response.text, 'html.parser')

    if extract == "titles":
        headings = [tag.get_text(strip=True) for tag in soup.find_all(["h1", "h2", "h3"])]
        return "\n".join(headings)

    elif extract == "links":
        links = [a['href'] for a in soup.find_all("a", href=True)]
        return "\n".join(links)

    else:
        raise HTTPException(status_code=400, detail="Invalid extract parameter. Use 'titles' or 'links'.")
