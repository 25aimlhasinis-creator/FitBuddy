from .config import GEMINI_FAST_MODEL
from .gemini_client import generate_text


def _fallback_nutrition_tip(goal: str, feedback: str | None = None) -> str:
    if goal == "weight loss":
        tip = "Build meals around a protein source such as chicken, fish, beans, eggs, or Greek yogurt, add vegetables and a sensible carbohydrate portion, and keep water nearby. Protein can support fullness and muscle maintenance while you work toward fat loss."
    elif goal == "muscle gain":
        tip = "Prioritize a protein source at every meal—such as chicken, fish, eggs, beans, paneer, or Greek yogurt—and include carbohydrates around training for energy. Consistent sleep and hydration support recovery and muscle-building efforts."
    elif goal == "flexibility":
        tip = "Choose balanced meals with protein, colorful fruits and vegetables, and enough fluids to support tissue recovery. Pair your nutrition habits with short daily mobility sessions and consistent sleep."
    else:
        tip = "Keep meals balanced with protein, fiber-rich foods, colorful produce, and regular hydration. Protein sources such as chicken, fish, beans, eggs, or Greek yogurt can support recovery and help you stay satisfied between meals."

    if feedback:
        tip += " Keep the nutrition routine simple and sustainable while you adjust your training plan."
    return tip


def generate_nutrition_tip_with_flash(goal: str, feedback: str | None = None) -> str:
    feedback_instruction = (
        f"The user also requested this training change: {feedback}. Reflect recovery or nutrition considerations where useful."
        if feedback
        else ""
    )
    prompt = f"""
Give one concise, practical nutrition or recovery tip for a person whose fitness goal is: {goal}.
{feedback_instruction}
Emphasize building meals around a protein source such as chicken, fish, beans, eggs, paneer, or Greek yogurt when appropriate.
Briefly explain that protein can support muscle repair/building and fullness, while balanced food, hydration, and sleep support recovery.
Keep it under 100 words. Focus on normal food and realistic habits.
Do not prescribe supplements, medication, or extreme diets.
"""
    try:
        return generate_text(prompt, GEMINI_FAST_MODEL)
    except Exception:
        return _fallback_nutrition_tip(goal, feedback)
