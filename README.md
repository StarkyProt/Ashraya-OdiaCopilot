# AASHRAY — Phase 2 modular foundation
Educational simulation only. No real emergencies, personal information, dispatch or live hazard monitoring. No authentication: keep local.

Windows PowerShell (Python 3.12):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address localhost
```

`app.py` handles navigation; `ashray/citizen.py` and `ashray/dashboard.py` render pages; `ashray/incidents.py` validates and coordinates operations; `ashray/database.py` owns SQL. Tests use a separate temporary database. Existing Phase 1 `incidents.db` and its schema are preserved. Report submissions and manual reviews are logged. Odia is stored as Unicode; translation and AI are not implemented. Future modules should call the service layer, not directly modify the UI or database. Keep the existing `.gitignore` and never commit local databases, credentials or virtual environments.
