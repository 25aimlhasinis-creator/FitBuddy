from .config import GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text


def _fallback_updated_plan(original_plan: str, feedback: str, goal: str, intensity: str) -> str:
    feedback_text = feedback.lower()
    additions = []
    if "cardio" in feedback_text:
        additions.append("Add 15-20 minutes of steady cardio on two days and keep one day lighter for recovery.")
    if "recovery" in feedback_text or "rest" in feedback_text:
        additions.append("Include one active recovery day with mobility work, walking, and light stretching.")
    if "strength" in feedback_text or "muscle" in feedback_text or goal == "muscle gain":
        additions.append("Increase lower-body and upper-body strength work with controlled progressive overload.")
    if "weight loss" in goal or "fat" in feedback_text:
        additions.append("Keep total weekly movement consistent by adding short brisk walks between strength sessions.")
    if not additions:
        additions.append("Keep the structure of the original plan and make the workouts more consistent, safe, and sustainable.")

    update_note = "\n".join(f"- {item}" for item in additions)
    summary = f"Updated based on feedback: {feedback}\n\n{update_note}\n\n"
    return f"{summary}{original_plan.strip()}\n\nSafety Note: Progress gradually and keep recovery in the plan. If you feel pain or unusual fatigue, stop and consult a qualified professional."


def update_workout_plan(original_plan: str, feedback: str, goal: str, intensity: str) -> str:
    prompt = f"""
You are FitBuddy. Revise the existing 7-day workout plan according to the user's feedback.

Fitness goal: {goal}
Intensity: {intensity}

Original plan:
---
{original_plan}
---

User feedback:
---
{feedback}
---

Return a complete revised 7-day plan, not only the changed day.
Preserve useful parts of the original plan while applying reasonable feedback.
Include Focus, Warm-up, Main Workout, and Cool-down/Recovery for each day.
Keep the plan safe and practical. Do not prescribe medication, supplements, extreme calorie restriction, or dangerous exercises.
Finish with a short Safety Note.
Use plain text headings and no JSON.
"""
    try:
        return generate_text(prompt, GEMINI_WORKOUT_MODEL)
    except Exception:
        return _fallback_updated_plan(original_plan, feedback, goal, intensity)
