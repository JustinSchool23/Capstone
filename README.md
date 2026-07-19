# Text Summarizer

A Flask web app that uploads `.txt` files and generates summaries using the Groq API.

See [Instructions.md](Instructions.md) for the full product requirements.

## Quick Start

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and add your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   FLASK_DEBUG=1
   ```

4. Run the app:

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000`, upload a `.txt` file, and click **Summarize**.
