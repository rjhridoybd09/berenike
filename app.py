import os
import uuid
import base64
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import google.generativeai as genai
from PIL import Image

# ── Config ─────────────────────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyDyPxpK7DT5q-jYwgbnKEihY-IuBR9Mhnc"
UPLOAD_FOLDER  = Path(os.path.dirname(__file__)) / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024   # 10 MB limit

ALLOWED = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

# ── Routes ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image uploaded."}), 400

    f = request.files["image"]
    if f.filename == "" or not allowed(f.filename):
        return jsonify({"success": False, "error": "Invalid file type. Use PNG, JPG, WEBP, etc."}), 400

    ext      = f.filename.rsplit(".", 1)[1].lower()
    savepath = UPLOAD_FOLDER / f"{uuid.uuid4().hex}.{ext}"
    f.save(str(savepath))

    try:
        model  = genai.GenerativeModel("gemini-1.5-flash")
        img    = Image.open(str(savepath))
        prompt = (
            "Extract ALL text from this image exactly as it appears. "
            "Preserve original line breaks and formatting. "
            "Return ONLY the extracted text — no commentary, no explanation. "
            "If there is no text, respond with: [No text found in image]"
        )
        response  = model.generate_content([prompt, img])
        extracted = response.text.strip()

        return jsonify({
            "success":    True,
            "text":       extracted,
            "word_count": len(extracted.split()),
            "char_count": len(extracted),
            "line_count": len(extracted.splitlines()),
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    finally:
        try: savepath.unlink()
        except: pass

# ── Entry point (for local testing only) ────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
