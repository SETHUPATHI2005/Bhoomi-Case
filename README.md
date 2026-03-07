Land Cases Search — MVP

This scaffold provides a minimal, runnable prototype for searching court cases by `village` + `survey number`.

Quick start (Windows, PowerShell):

1. Build and run with Docker Compose:

```powershell
make build
make up
```

2. Open the UI: http://localhost:8000/

3. To stop:

```powershell
make down
```

Notes:
- Backend is a small FastAPI app in `backend/app` serving a static search UI and a `/api/v1/search` endpoint.
- Sample data is in `backend/app/data/sample_parcels.json`.
- CI workflow is in `.github/workflows/ci.yml`.

Next steps:
- Add ETL to ingest court records and OCRed documents.
- Add admin UI for human-in-the-loop verification.
- Add authentication, logging, and monitoring for production.
