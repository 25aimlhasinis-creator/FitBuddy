from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .crud import get_latest_plan, get_user, save_plan, save_user, update_plan
from .database import get_db
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter(prefix="/api", tags=["FitBuddy API"])


@router.post("/generate-workout")
def api_generate_workout(payload: UserInput, db: Session = Depends(get_db)):
    user = save_user(db, payload)
    workout = generate_workout_gemini(
        user.name, user.age, user.weight, user.goal, user.intensity
    )
    tip = generate_nutrition_tip_with_flash(user.goal)
    plan = save_plan(db, user, workout, tip)
    return {
        "user_id": user.user_id,
        "plan_id": plan.id,
        "workout_plan": workout,
        "nutrition_tip": tip,
    }


@router.post("/submit-feedback")
def api_submit_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    user = get_user(db, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plan = get_latest_plan(db, user)
    if not plan:
        raise HTTPException(status_code=404, detail="No plan found")

    base_plan = plan.updated_plan or plan.original_plan
    updated = update_workout_plan(
        base_plan,
        payload.feedback,
        user.goal,
        user.intensity,
    )
    tip = generate_nutrition_tip_with_flash(user.goal, payload.feedback)
    update_plan(db, plan, updated, payload.feedback, nutrition_tip=tip)

    return {
        "user_id": user.user_id,
        "plan_id": plan.id,
        "feedback": payload.feedback,
        "updated_plan": updated,
        "nutrition_tip": tip,
        "message": "Plan updated successfully.",
    }
