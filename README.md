# Logictap Backend Intern Assignment – Call Records Service

A small backend web service built using Python and FastAPI for handling call-ended webhook events.

The service accepts call records, prevents duplicate records for the same `call_id`, and allows stored call information to be retrieved through an API.

---

## Assignment Objective

The objective of this project is to build a small web service that:

1. Accepts a `POST /call-ended` request containing call information.
2. Stores the call record.
3. Prevents the same `call_id` from being stored more than once.
4. Returns a successful response even when a duplicate request is received.
5. Provides `GET /calls/{call_id}` to retrieve a stored call.
6. Rejects invalid requests such as a missing `call_id`.
7. Includes an automated test for duplicate request handling.

These requirements are based on Part 3 of the Logictap Backend Intern Assignment. 

---

## Technology Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTTPX
- SQLite
- Git
- GitHub
- Swagger / OpenAPI

---

## Project Structure

```text
logictap-assignment/
│
├── final/
│   └── main.py
│
├── tests/
│   └── test_calls.py
│
├── version1/
│   └── main.py
│
├── .gitignore
│
└── README.md


Version 1
The version1/main.py file contains the first version of the service generated with AI.
The initial implementation was kept separately and was not modified after generation, as required by the assignment.
Version 1 demonstrates:
- FastAPI application
- Request validation
- POST /call-ended
- GET /calls/{call_id}
- Duplicate detection
- In-memory record storage
The Version 1 code is preserved separately from the final implementation.
Final Version
The final/main.py file contains the improved implementation.
The final version improves the initial implementation by:
- Using SQLite for persistent record storage.
- Handling duplicate call_id values safely.
- Preserving the original record when a duplicate webhook is received.
- Returning clear responses for new and duplicate requests.
- Providing validation for call_id.
- Providing clear 404 Not Found responses.
- Supporting automated testing.
API Endpoints
1. POST /call-ended
This endpoint receives a call-ended webhook event.
Request
POST /call-ended

Example JSON
{
  "call_id": "abc123",
  "status": "answered",
  "duration_secs": 42
}

Fields
Field	Type	Description
call_id	string	Unique identifier of the call
status	string	Status of the call
duration_secs	integer	Call duration in seconds


First Request
When a new call_id is received, the record is stored.
Example response:
{
  "message": "Call record stored",
  "duplicate": false,
  "call": {
    "call_id": "abc123",
    "status": "answered",
    "duration_secs": 42
  }
}

The first request is treated as a new call record.
Duplicate Request
If the same call_id is sent again, the service does not create another record.
Instead, it returns a successful response indicating that the call was already recorded.
Example response:
{
  "message": "Call already recorded",
  "duplicate": true,
  "call": {
    "call_id": "abc123",
    "status": "answered",
    "duration_secs": 42
  }
}

This makes the endpoint safe against repeated webhook delivery.
2. GET /calls/{call_id}
This endpoint retrieves a stored call record.
Request
GET /calls/abc123

Example Response
{
  "call_id": "abc123",
  "status": "answered",
  "duration_secs": 42
}

If the requested call does not exist, the service returns a 404 Not Found response.
Request Validation
The service validates incoming request data.
A valid request must contain:
- call_id
- status
- duration_secs
The call_id must not be empty.
The duration must be zero or greater.
Invalid requests are rejected with a clear validation error.
Duplicate Handling
Duplicate webhook requests are an important part of this assignment.
The service uses call_id to identify a call.
The logic is:
Request received
       │
       ▼
Read call_id
       │
       ▼
Does call_id already exist?
       │
   ┌───┴────┐
   │        │
  No       Yes
   │        │
   ▼        ▼
Store     Do not
record    store again
   │        │
   └───┬────┘
       ▼
Return successful response

Therefore, sending the same call-ended event multiple times does not create multiple records for the same call.
Running the Project
1. Install Dependencies
Open the terminal in the project directory and run:
python -m pip install fastapi uvicorn pytest httpx

2. Run the Final Application
Run:
python -m uvicorn final.main:app --reload

The server starts at:
http://127.0.0.1:8000

Swagger API Documentation
FastAPI automatically provides interactive API documentation.
Open:
http://127.0.0.1:8000/docs

The Swagger interface can be used to test:
POST /call-ended
GET /calls/{call_id}

Testing the API
First Request
Send:
{
  "call_id": "abc123",
  "status": "answered",
  "duration_secs": 42
}

Expected result:
201 Created
duplicate: false

The record is stored.
Second Request
Send the exact same request again.
Expected result:
200 OK
duplicate: true

The service recognizes the request as a duplicate and does not create another record.
GET Request
After sending the POST request, retrieve the record using:
GET /calls/abc123

Expected result:
{
  "call_id": "abc123",
  "status": "answered",
  "duration_secs": 42
}

Expected status:
200 OK

Automated Testing
The project includes an automated test:
tests/test_calls.py

The test verifies that sending the same call_id twice does not create a second record.
The test checks:
1. The first request succeeds.
2. The second request is identified as a duplicate.
3. The duplicate flag is true.
4. Only one record exists for the given call_id.
Run the test with:
python -m pytest tests/test_calls.py -v

Expected result:
1 passed

Test Result
The automated test was successfully executed.
Actual result:
1 passed, 1 warning

The test passed successfully. The warning did not cause the test to fail.
Proof of API Execution
The API was tested locally using FastAPI Swagger UI.
The following flow was verified:
POST /call-ended
       │
       ▼
Call record stored
       │
       ▼
Same POST request again
       │
       ▼
Duplicate detected
       │
       ▼
GET /calls/abc123
       │
       ▼
Stored call returned

The Swagger testing demonstrated:
- First POST request → 201
- Repeated POST request → 200
- Duplicate response → "duplicate": true
- GET request → 200
Version 1 vs Final Version
The main changes between Version 1 and the Final Version were:
1. Version 1 used an in-memory dictionary, while the final version uses SQLite for persistent record storage.
2. Duplicate handling was implemented using call_id so that repeated webhook requests do not create a second record.
3. Automated testing was added to verify that duplicate requests result in only one stored record.
AI Prompt Used for Version 1
The first prompt used to generate Version 1 was:
Build a small Python web service using FastAPI for this requirement:

1. POST /call-ended accepts JSON:
   {
     "call_id": "abc123",
     "status": "answered",
     "duration_secs": 42
   }

2. Store the call record.

3. If the same call_id is sent again, do not store a second record, but still return a successful response.

4. GET /calls/{call_id} should return the stored record, or a not found response if it does not exist.

5. A request without call_id must be rejected with a clear error message.

Keep the implementation simple and suitable for running locally.
Please provide the complete code and the commands needed to run it.

AI Usage
AI tools were used during development to:
- Understand the assignment requirements.
- Generate the initial FastAPI implementation.
- Review and improve the initial implementation.
- Implement SQLite-based storage.
- Improve duplicate request handling.
- Add request validation.
- Create the automated test.
- Debug installation and runtime issues.
- Improve project documentation.
The Version 1 implementation has been preserved separately in:
version1/main.py

The final implementation is available in:
final/main.py

Tools Used
The following tools were used while completing the assignment:
- ChatGPT – AI assistance, code generation, debugging and explanation
- Visual Studio Code – Development environment
- Python – Programming language
- FastAPI – Web framework
- Uvicorn – ASGI server
- Pydantic – Data validation
- Pytest – Automated testing
- HTTPX – Testing support
- Swagger UI – API testing
- webhook.site – Webhook and HTTP request inspection
- Git – Version control
- GitHub – Code repository
- Windows Terminal / PowerShell – Command execution
GitHub Repository
Repository:
https://github.com/Udaynemade/logictap-backend-assignment
The repository contains:
final/main.py
version1/main.py
tests/test_calls.py
.gitignore
README.md

Author
Uday Nemade
Logictap Backend Intern Assignment