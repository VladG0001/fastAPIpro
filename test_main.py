from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_infourl():
    url = "https://jsonplaceholder.typicode.com/"
    resp = client.get("/info-url/", params={"url": url})
    assert resp.status_code == 200
    assert "title" in resp.json()
    assert "urls" in resp.json()

def test_error_infourl():
    url = "htts://jsonplaceholder.typicode.com/"
    resp = client.get("/info-url/", params={"url": url})
    assert resp.status_code == 422


def test_wiki_data_python():
    resp = client.get("/wiki/data_program", params={"language": "Python"})
    assert resp.status_code == 200
    json_data = resp.json()
    assert "description" in json_data
    assert "First_appeared" in json_data
    assert "Developer" in json_data

def test_wiki_data_go():
    resp = client.get("/wiki/data_program", params={"language": "Go"})
    assert resp.status_code == 200
    json_data = resp.json()
    assert "description" in json_data
    assert "First_appeared" in json_data
    assert "Developer" in json_data

def test_wiki_data_unknown_language():
    resp = client.get("/wiki/data_program", params={"language": "UnknownLanguage"})
    assert resp.status_code == 200
    json_data = resp.json()
    assert "error" in json_data
