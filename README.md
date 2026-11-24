# AASHRAY — Phase 1 starter
Educational simulation only. No real emergencies, personal information, dispatch or live hazard monitoring.

Windows PowerShell, Python 3.11:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local address printed in the terminal. Submit a synthetic report, switch to Officer dashboard, manually classify and save a review. Restart the app to verify SQLite persistence. Unicode Odia text is accepted, but not translated. The next phase adds AI extraction with schema validation and human review. No authentication yet: keep the app local, never expose publicly. Delete incidents.db when the app is stopped to reset synthetic data.
