# Job-genie

## API

Install dependencies:

```powershell
cd c:\Users\LOQ\React-Projects\Job-genie-backend
.\.venv\Scripts\python.exe -m pip install -e .
```

Run the API server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn job_genie_backend.app:app --reload
```

Signup endpoint:

- `POST /signup`
- JSON body:
  - `email` (string)
  - `full_name` (string)
  - `password` (string)

Example payload:

```json
{
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "password": "secret123"
}
```

Health check:

- `GET /health`
