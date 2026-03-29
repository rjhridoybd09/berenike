"""
OCR Web Application
Backend: Flask + Google Gemini Vision API
"""

import os
import base64
import json
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import google.generativeai as genai
from PIL import Image
import io

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
GEMINI_API_KEY = "AIzaSyDyPxpK7DT5q-jYwgbnKEihY-IuBR9Mhnc"
UPLOAD_FOLDER  = Path("uploads")
ALLOWED_EXT    = {"png", "jpg", "jpeg", "gif", "bmp", "webp", "tiff", "pdf"}
MAX_FILE_MB    = 10

UPLOAD_FOLDER.mkdir(exist_ok=True)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_MB * 1024 * 1024
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def extract_text_with_gemini(image_path: str) -> dict:
    """Send image to Gemini Vision and extract all text."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        img = Image.open(image_path)

        prompt = """You are an expert OCR system. Your task is to extract ALL text from this image with perfect accuracy.

Instructions:
- Extract every single word, number, and character visible in the image
- Preserve the original layout and line breaks as much as possible
- Keep the original formatting (tables, lists, paragraphs)
- Do NOT add any commentary, explanation, or extra text
- If the image contains multiple languages, extract all of them
- If there is no text in the image, respond with: [No text found in image]

Return ONLY the extracted text, nothing else."""

        response = model.generate_content([prompt, img])

        extracted = response.text.strip()

        return {
            "success": True,
            "text": extracted,
            "word_count": len(extracted.split()) if extracted != "[No text found in image]" else 0,
            "char_count": len(extracted),
            "line_count": len(extracted.splitlines()),
        }

    except Exception as e:
        return {
            "success": False,
            "text": "",
            "error": str(e),
            "word_count": 0,
            "char_count": 0,
            "line_count": 0,
        }


# ══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════════════════════
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/extract", methods=["POST"])
def extract():
    """Main OCR endpoint — receives uploaded image, returns extracted text."""

    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image file received."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": f"File type not supported. Allowed: {', '.join(ALLOWED_EXT).upper()}"
        }), 400

    # Save file with unique name
    ext      = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = UPLOAD_FOLDER / filename
    file.save(str(filepath))

    # Run OCR
    result = extract_text_with_gemini(str(filepath))

    # Clean up uploaded file after processing
    try:
        filepath.unlink()
    except Exception:
        pass

    return jsonify(result)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": "gemini-1.5-flash"})


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 50)
    print("  OCR Web App — Powered by Google Gemini")
    print("  Open: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
