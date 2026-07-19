import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from groq import Groq

load_dotenv()

app = Flask(__name__)

MAX_CHARS = 120_000
GROQ_MODEL = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes text clearly and concisely."
)


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)


def summarize_text(text):
    client = get_groq_client()
    if client is None:
        raise RuntimeError("Groq API key is not configured.")

    truncated = False
    document = text
    if len(document) > MAX_CHARS:
        document = document[:MAX_CHARS]
        truncated = True

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": document},
        ],
    )

    summary = response.choices[0].message.content.strip()
    if truncated:
        summary = (
            "[Note: The document was truncated before summarization due to length limits.]\n\n"
            + summary
        )
    return summary


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "No file selected."}), 400

    if not file.filename.lower().endswith(".txt"):
        return jsonify({"error": "Only .txt files are supported."}), 400

    content = file.read().decode("utf-8", errors="replace")
    if not content.strip():
        return jsonify({"error": "The file is empty."}), 400

    return jsonify({"text": content, "filename": file.filename})


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Please upload a .txt file first."}), 400

    try:
        summary = summarize_text(text)
    except RuntimeError:
        app.logger.error("GROQ_API_KEY is missing.")
        return jsonify({"error": "Summarization is unavailable. Check server configuration."}), 500
    except Exception:
        app.logger.exception("Groq API request failed.")
        return jsonify({"error": "Unable to generate a summary. Please try again."}), 502

    return jsonify({"summary": summary})


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
