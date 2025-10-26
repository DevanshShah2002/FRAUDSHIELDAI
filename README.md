# FraudShield AI - Prototype (MVP)

**What this is**
- A minimal prototype (Flask) that demonstrates core features:
  - Upload invoice (PDF/text) — runs simple rule checks and ML-based spam/fraud detection on invoice text.
  - Vendor domain trust check (detects lookalike domains).
  - Email phishing classifier (toy model).
  - Simple dashboard to view recent uploads and vendor trust scores.

**Structure**
```
FraudShieldAI/
├── app.py                 # Flask app (APIs + simple UI)
├── fraud_detector.py      # Toy NLP classifier + helper
├── vendor_check.py        # Domain similarity and trust scoring
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── sample_data/
│   └── sample_invoice.txt
└── README.md
```

**Quick setup (Linux / macOS / WSL)**
1. Create virtualenv:
   ```
   python -m venv venv
   source venv/bin/activate
   ```
   (Windows PowerShell: `venv\Scripts\Activate.ps1`)
2. Install:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   flask run --host=0.0.0.0 --port=5000
   ```
   (Windows PowerShell use `set` instead of `export`.)
4. Open `http://localhost:5000` in your browser.

**Notes & Next steps**
- This is a functional prototype with toy data and simple heuristics. For production:
  - Replace the toy ML model with a real trained model on labeled invoice/phishing datasets.
  - Add authentication, role-based access, database (Postgres), and secure file storage (S3).
  - Add logging, unit tests, and CI/CD.
