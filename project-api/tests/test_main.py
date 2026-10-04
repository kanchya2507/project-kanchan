from fastapi.testclient import TestClient
# Updated this line to look inside the app folder
from app.main import app 

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
