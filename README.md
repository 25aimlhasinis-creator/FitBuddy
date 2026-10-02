# FitBuddy – AI Fitness Plan Generator

A FastAPI + Jinja2 + SQLite + SQLAlchemy web app that uses Google's Gemini API to create personalized 7-day workout plans, nutrition/recovery guidance, and feedback-based plan revisions.

## What is included

- Premium responsive UI for Home, Result, Feedback, and Admin pages
- Personalized 7-day workout plan generation
- Nutrition/recovery tip with protein-focused guidance
- Dedicated Feedback page
- Feedback updates the **latest version of the plan** and shows the complete revised 7-day plan
- Original plan remains saved for comparison
- Admin dashboard showing user details, original plan, latest updated plan, and feedback
- SQLite database created automatically
- FastAPI Swagger docs

## 1. Requirements

- Python 3.10+
- VS Code
- A Gemini API key

## 2. Install

Open the project folder in VS Code, then open **Terminal → New Terminal**.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Configure Gemini

Open `.env` and add your own API key:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_WORKOUT_MODEL=gemini-3.1-pro-preview
GEMINI_FAST_MODEL=gemini-3.8-flash
APP_HOST=127.0.0.1
APP_PORT=8000
```

Do not share the `.env` file or commit it to Git. `.gitignore` already excludes it.

## 4. Run

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000` — Home
- `http://127.0.0.1:8000/feedback` — Feedback page
- `http://127.0.0.1:8000/view-all-users` — Admin dashboard
- `http://127.0.0.1:8000/docs` — FastAPI API docs
- `http://127.0.0.1:8000/api/health` — Health check

## 5. Main user flow

1. Enter name, User ID, age, weight, goal, and intensity.
2. Click **Generate My 7-Day Plan**.
3. Review the complete workout plan and Nutrition Tip.
4. Click **Give Feedback**.
5. Enter the same User ID and feedback such as:
   - `Add more cardio`
   - `Include one extra rest day`
   - `Make the strength workouts easier`
   - `Add more mobility work`
6. Click **Update Plan with AI**.
7. FitBuddy generates and displays the **complete updated 7-day plan** and a confirmation message.
8. The original plan remains stored, so the Admin Dashboard can show original vs updated.

### Important feedback behavior

If a user gives feedback more than once, the next revision starts from the **latest updated plan**, not the old original plan. The original plan is kept unchanged for comparison.

## 6. API endpoints

### Generate

`POST /api/generate-workout`

```json
{
  "name": "Arun",
  "user_id": "FB001",
  "age": 25,
  "weight": 65,
  "goal": "muscle gain",
  "intensity": "medium"
}
```

### Feedback update

`POST /api/submit-feedback`

```json
{
  "user_id": "FB001",
  "feedback": "Add more cardio and include one extra recovery day."
}
```

The response contains the complete `updated_plan`, the nutrition tip, and a success message.

## 7. Database

`fitbuddy.db` is created automatically in the project root when the app starts. It is intentionally excluded from the distributable ZIP so every fresh installation starts clean.

## 8. Project structure

```text
FitBuddy/
├── app/
│   ├── api.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── gemini_client.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
├── static/
│   └── style.css
├── templates/
│   ├── all_users.html
│   ├── feedback.html
│   ├── index.html
│   └── result.html
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## 9. Troubleshooting

### `No module named uvicorn`

Activate the virtual environment first:

```powershell
.venv\Scripts\activate
```

Then run:

```powershell
python -m uvicorn app.main:app --reload
```

### `API_KEY_INVALID`

Check that `.env` contains exactly one key assignment:

```env
GEMINI_API_KEY=your_real_key_here
```

Do not write `API_KEY=GEMINI_API_KEY=...`.

### Gemini model unavailable

Change `GEMINI_WORKOUT_MODEL` or `GEMINI_FAST_MODEL` in `.env` to a model currently available to your Gemini API project.

### Port already in use

Run on another port:

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.
