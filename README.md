## Setup and Usage

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Configure Django settings accordingly, especially the API endpoint URL and authentication token.
4. Run the Django server using `python manage.py runserver`.
5. Make POST requests to the `/generate_pdf` endpoint with the required data to generate reports.

### Usage Example

```python
import requests
import json

data = {
    "Kit_code": "your_kit_code_here"
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_auth_token_here"
}

response = requests.post("http://localhost:8000/generate_pdf", headers=headers, data=json.dumps(data))

print(response.json())
