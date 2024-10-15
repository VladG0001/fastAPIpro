from fastapi import FastAPI, Query
import uvicorn
import httpx
from components.structures import UrlInput, ResponseParsing
from components.tools import get_html, parsing_get_title_a


app = FastAPI()

WIKIPEDIA_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"


async def fetch_wiki_data(language: str):
    url = f"{WIKIPEDIA_API_URL}{language}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


@app.get("/info-url")
async def parsing_url(url_inp: UrlInput = Query(..., description="введіть URL для парсингу")) -> ResponseParsing:

    html_data = await get_html(str(url_inp.url))


    title_of_soup, urls_of_soup = await parsing_get_title_a(html_data)


    return ResponseParsing(title=title_of_soup, urls=urls_of_soup)

@app.get("/wiki/data_program")
async def get_programming_language_data(language: str = Query(..., description="Назва мови програмування (напр. Python, Go, PHP)")):
    data = await fetch_wiki_data(language)

    if not data:
        return {"error": "Language not found on Wikipedia"}

    description = data.get("extract", "").split("\n")[0]
    title = data.get("title", "")


    first_appeared = "N/A"
    developer = "N/A"


    if title.lower() == "python":
        first_appeared = "1991"
        developer = "Guido van Rossum"
    elif title.lower() == "go":
        first_appeared = "2009"
        developer = "Google"
    elif title.lower() == "php":
        first_appeared = "1995"
        developer = "Rasmus Lerdorf"
    elif title.lower() == "c++":
        first_appeared = "1985"
        developer = "Bjarne Stroustrup"

    return {
        "description": description,
        "First_appeared": first_appeared,
        "Developer": developer
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

