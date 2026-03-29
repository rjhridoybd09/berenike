# OCR Studio — Image to Text Web App
**Powered by:** Google Gemini Vision API  
**Stack:** Python (Flask) + HTML/CSS/JS

---

## What it does

Upload any image → Gemini AI reads the text → Clean result displayed instantly.

Supports: PNG, JPG, JPEG, WEBP, BMP, TIFF (max 10 MB)

---

## Run Locally (for testing)

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Run the app
```bash
python app.py
```

### Step 3 — Open in browser
```
http://localhost:5000
```

---

## Deploy to Hosting (cPanel / Shared Hosting)

If your hosting supports **Python/Flask** (most cPanel hosts do):

### Option A — cPanel Python App
1. Login to cPanel → go to **"Setup Python App"**
2. Create new app:
   - Python version: `3.10` or higher
   - Application root: `ocr_webapp/`
   - Application startup file: `app.py`
   - Application entry point: `app`
3. Upload all files via **File Manager**
4. In cPanel terminal, run: `pip install -r requirements.txt`
5. Click **Restart** — your app is live!

### Option B — VPS / Cloud Server (DigitalOcean, AWS, etc.)
```bash
# Install
pip install -r requirements.txt

# Run with gunicorn (production server)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option C — PythonAnywhere (Free tier available)
1. Sign up at pythonanywhere.com
2. Upload files to `/home/yourusername/ocr_webapp/`
3. Go to **Web** tab → Add new web app → Flask
4. Set source code path and WSGI file
5. In **Bash console**: `pip install -r requirements.txt`
6. Reload the app

---

## Project Structure

```
ocr_webapp/
├── app.py               ← Flask backend (main server)
├── requirements.txt     ← Python dependencies
├── README.md            ← This file
├── uploads/             ← Temp folder (auto-cleaned after each request)
└── templates/
    └── index.html       ← Frontend UI
```

---

## API Endpoint

The app exposes one endpoint:

**POST /extract**
- Form field: `image` (file)
- Returns JSON:
```json
{
  "success": true,
  "text": "Extracted text here...",
  "word_count": 42,
  "char_count": 215,
  "line_count": 6
}
```

---

*Gemini API key is set in app.py line 16. Keep this file private — do not share publicly.*
