from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_create_approve_fund_repay():
    r = client.post("/loans", json={"id":1,"amount":1000,"rate":0.05,"term":12,"balance":1000})
    assert r.status_code == 200 and r.json()["status"] == "pending"
    r = client.post("/loans/1/approve"); assert r.json()["status"] == "approved"
    r = client.post("/loans/1/fund");    assert r.json()["status"] == "funded"
    r = client.post("/loans/1/repay", params={"amount": 1000})
    j = r.json(); assert j["status"] == "closed" and j["balance"] == 0
