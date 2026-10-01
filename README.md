# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. It provides:

- Q&A at `/qa`
- Simple concept explanation at `/explain`
- Three-question MCQ generation at `/quiz`
- Summarization at `/summarize`
- Beginner-to-advanced learning recommendations at `/learn/recommendations`
- A responsive HTML/CSS/JavaScript frontend served by FastAPI

## Architecture

```text
Browser
   |
   v
FastAPI (main.py)
   |
   +--> qna.py ----------------------+
   +--> explanation_module.py        |
   +--> quiz_module.py              |
   +--> summary_module.py           |--> gemini_client.py --> Gemini API
   +--> learning_path.py -----------+
   |
   +--> templates/index.html + static/
```

The supplied documentation describes Gemini 1.5 Pro and LaMini-Flan-T5-783M. Gemini 1.5 Pro is no longer a good default for a new build, so this implementation uses the configurable `GEMINI_MODEL`, defaulting to `gemini-2.5-flash`. The explanation module keeps the documented LaMini model as an optional local path, disabled by default so the standard installation stays lightweight.

## 1. VS Code setup

Install Python 3.10+ and VS Code.

Open the project folder in VS Code.

Create a virtual environment:

### Windows PowerShell

```powershell
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Configure Gemini

Copy `.env.example` to `.env`:

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS/Linux

```bash
cp .env.example .env
```

Open `.env` and set:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
ENABLE_LOCAL_EXPLAINER=false
```

Do not commit `.env` to Git.

## 3. Run

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 4. Test

Run automated tests:

```bash
pytest
```

Test the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

For Windows PowerShell, you can also open the URL in a browser.

## 5. Test each feature

### Q&A

```json
POST /qa
{
  "question": "Which is the largest ocean?"
}
```

### Explain

```json
POST /explain
{
  "text": "Pythagoras theorem"
}
```

### Quiz

```json
POST /quiz
{
  "text": "Water covers most of Earth's surface and is found in oceans, rivers, lakes and glaciers."
}
```

The response contains exactly three questions, four options per question, and the correct answer.

### Summarize

```json
POST /summarize
{
  "text": "Paste a long educational passage here..."
}
```

### Learning path

```json
POST /learn/recommendations
{
  "topic": "SQL"
}
```

## Optional: local LaMini explanation model

The supplied documentation identifies `MBZUAI/LaMini-Flan-T5-783M` for concept explanation. To enable that path, install the optional packages:

```bash
pip install "transformers>=4.45,<5.0" "torch>=2.4,<3.0"
```

Then set:

```env
ENABLE_LOCAL_EXPLAINER=true
LOCAL_EXPLAINER_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

The model is downloaded on first use and can require substantial disk space/RAM. If local loading fails, EduGenie automatically falls back to Gemini.

## Project files

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_api.py
```

## Troubleshooting

### "GEMINI_API_KEY is not configured"

Check that `.env` exists in the project root and contains a valid key. Restart Uvicorn after changing environment settings.

### Gemini request failed

Check your API key, internet connection, API quota, and selected model. You can change `GEMINI_MODEL` to another model supported by your Gemini API account.

### Quiz JSON error

The quiz module validates the generated response with Pydantic. If a model returns malformed JSON, the endpoint returns a clear error instead of silently producing incorrect quiz data.

### Port already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Security notes

- Keep the Gemini API key on the backend only.
- Never place the key in `static/app.js` or HTML.
- `.env` is ignored by Git.
- Validate request sizes before sending content to an LLM.
- For a production deployment, add authentication, rate limiting, structured logging, HTTPS, and stronger abuse controls.

## Scope and future extensions

The source documentation lists future possibilities such as voice interaction, multilingual support, mobile apps, progress dashboards, gamification, adaptive learning, group study, LMS integration, and image/PDF input. Those are intentionally not enabled in this baseline build so the documented core application remains small and easy to run.
