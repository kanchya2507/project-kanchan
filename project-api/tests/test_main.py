from fastapi.testclient import TestClient
# Import your FastAPI app instance (adjust the import path based on your file structure)
from main import app 

client = TestClient(app)

def test_read_root():
    # Make a request to your API's root path
    response = client.get("/")
    
    # Assert that the API responds with a successful HTTP 200 status code
    assert response.status_code == 200
