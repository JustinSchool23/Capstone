# Product Requirements Document (PRD)
## Text Summarizer Web Application

---

## 1. Overview

Build a single-page web application that lets users upload `.txt` files, view the original content, and generate an AI-powered summary using the **Groq API**. The app uses **Flask** for the backend and server-rendered HTML/CSS for the frontend.

**Primary goal:** Provide a simple, local tool for quickly summarizing plain-text documents without leaving the browser.

---

## 3. Core Features

### 3.1 File Upload

- Provide a **drop zone** that accepts `.txt` files via:
  - Drag and drop, or
  - Click-to-browse file picker
- Only accept files with a `.txt` extension.
- Read and display the file contents in the **original text** panel immediately after upload.
- Track the **most recently uploaded file** as the active document for summarization.

**Acceptance criteria:**
- [ ] Dropping a valid `.txt` file populates the left text box with its contents
- [ ] Clicking the drop zone opens a file picker filtered to `.txt` files
- [ ] Uploading a non-`.txt` file shows a clear error message (no crash)
- [ ] Uploading a new file replaces the previous content in the original text box

### 3.2 Summarize

- Provide a **Summarize** button that sends the active document text to the Groq API.
- If no file has been loaded, the button does nothing (or shows a brief inline message such as "Please upload a .txt file first").
- While the request is in progress, disable the button and show a loading indicator.
- On success, display the Groq response in the **summary** panel (right text box).
- On failure, show a user-friendly error message in or near the summary panel.

**Acceptance criteria:**
- [ ] Clicking **Summarize** with loaded text calls the Groq API and fills the right text box
- [ ] Clicking **Summarize** with no loaded text produces no API call
- [ ] API errors (network, invalid key, rate limit) are surfaced to the user without exposing stack traces
- [ ] The original text panel is never modified by the summarize action

### 3.3 Display

- **Left panel:** Read-only (or editable optional) text area showing the uploaded file content.
- **Right panel:** Read-only text area showing the AI-generated summary.
- Layout should work on desktop; responsive behavior on smaller screens is a nice-to-have.

**Acceptance criteria:**
- [ ] Both panels are visible on the same page without navigation
- [ ] Long documents scroll within each panel independently
- [ ] Summary panel is empty until the first successful summarize

---

## 4. UI Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    Text Summarizer                          │
├─────────────────────────────────────────────────────────────┤
│   ┌─────────────────────────────────────────────────────┐   │
│   │  Drop .txt file here  (or click to browse)          │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│                     [ Summarize ]                           │
│                                                             │
│      ┌──────────────────────┐  ┌──────────────────────┐     │
│      │  Original Text       │  │  Summary             │     │
│      │                      │  │                      │     │
│      │  (left text box)     │  │  (right text box)    │     │
│      │                      │  │                      │     │
│      └──────────────────────┘  └──────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

**Visual guidelines:**
- Clear labels for each region (drop zone, buttons, panels)
- Visible disabled/loading state on the Summarize button during API calls
- Minimal, clean styling with HTML5 + CSS3 (no frontend framework required)

---

## 5. Technical Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask (Python) |
| Frontend | HTML5, CSS3, minimal JavaScript (for drag-drop and fetch if using AJAX) |
| AI | Groq API (chat completions) |
| Config | Environment variables via `.env` (see Setup) |

---

## 6. API Integration (Groq)

- **Endpoint:** Groq Chat Completions API (`https://api.groq.com/openai/v1/chat/completions`)
- **Authentication:** Bearer token from environment variable `GROQ_API_KEY`
- **Suggested model:** `llama-3.3-70b-versatile` (or latest Groq-supported chat model)
- **Prompt pattern:** System message instructs the model to summarize concisely; user message contains the full document text.
- **Constraints:** Handle empty input, very long documents (truncate or warn if over token limits), and timeouts gracefully.

**Example request shape (conceptual):**

```python
{
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant that summarizes text clearly and concisely."},
        {"role": "user", "content": "<document text>"}
    ]
}
```

**Security:** Never hardcode API keys in source code or commit them to version control. Use a `.env` file listed in `.gitignore`.

---

## 7. Project Structure

```
Capstone/
├── app.py                 # Flask app, routes, Groq client logic
├── requirements.txt       # Python dependencies
├── .env.example           # Template for GROQ_API_KEY (no real key)
├── .gitignore             # Ignore .env, __pycache__, venv/
├── Instructions.md        # This PRD
├── README.md              # Quick start for developers
├── static/
│   └── css/
│       └── style.css      # Page layout and styling
└── templates/
    └── index.html         # Main page (drop zone, buttons, text areas)
```

**Suggested routes:**

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/` | Render main page |
| `POST` | `/upload` | Accept `.txt` upload, return or render original text |
| `POST` | `/summarize` | Send text to Groq, return summary JSON or render updated page |

Implementation may use a single-page form with standard POST or separate JSON endpoints with `fetch`—either approach is acceptable if acceptance criteria are met.

---

## 8. Setup Instructions

### Prerequisites

- Python 3.10+ installed
- Groq API key ([Groq Console](https://console.groq.com/))

### Local development

1. **Clone or open the project** and create a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Expected packages (minimum):
   - `flask`
   - `python-dotenv`
   - `groq` (official Groq Python SDK) or `requests`

3. **Configure environment variables:**

   Copy `.env.example` to `.env` and set your key:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   FLASK_DEBUG=1
   ```

   > **Note:** Do not commit `.env`. If a key was previously shared in documentation, rotate it in the Groq console and use the new key only in `.env`.

4. **Run the application:**

   ```bash
   python app.py
   ```

   Default URL: `http://127.0.0.1:5000`

5. **Verify:** Upload a sample `.txt` file, click **Summarize**, and confirm the summary appears in the right panel.

---

## 9. Error Handling & Edge Cases

| Scenario | Expected behavior |
|----------|-------------------|
| No file uploaded before Summarize | No API call; optional message to upload first |
| Empty `.txt` file | Show message that file is empty; do not call API |
| Invalid file type | Reject with clear error; do not update text panels |
| Missing `GROQ_API_KEY` | Server logs error; user sees generic failure message |
| Groq API failure | Display friendly error; re-enable Summarize button |
| Very large file | Summarize if within limits; otherwise show truncation/limit message |

---

## 10. Non-Functional Requirements

- **Performance:** Summary response within reasonable time for typical documents (< 10k words); show loading state for slow requests.
- **Security:** API key server-side only; never exposed to the client or repository.
- **Usability:** All primary actions achievable in two steps: upload → summarize.
- **Maintainability:** Keep logic in `app.py` modular (upload parsing, Groq call, error mapping) for easy testing.

---

## 11. Definition of Done

The project is complete when:

1. All acceptance criteria in Sections 3.1–3.3 are satisfied.
2. The app runs locally following Section 8 without manual code edits beyond `.env`.
3. `.gitignore` excludes `.env` and virtual environment artifacts.
4. `README.md` includes a short quick-start pointing to this document.

---

## 12. Future Enhancements (Optional)

- Download summary as `.txt`
- Adjustable summary length (short / medium / long)
- Dark mode
- Support for `.md` or `.pdf` files
- Summary history per session
