from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .config import BASE_DIR
from .crud import (
    delete_user,
    get_all_users,
    get_latest_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from .database import get_db
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


def page_context(request: Request, **kwargs):
    return {"request": request, **kwargs}


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=page_context(request),
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user_data = UserInput(
            name=name,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        user = save_user(db, user_data)
        workout_plan = generate_workout_gemini(
            user.name, user.age, user.weight, user.goal, user.intensity
        )
        nutrition_tip = generate_nutrition_tip_with_flash(user.goal)
        plan = save_plan(db, user, workout_plan, nutrition_tip)
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context=page_context(
                request,
                user=user,
                plan=plan,
                displayed_plan=workout_plan,
                message="Your personalized 7-day plan is ready.",
                error=None,
                is_updated=False,
            ),
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context=page_context(request, error=str(exc)),
            status_code=400,
        )


@router.get("/feedback", response_class=HTMLResponse)
def feedback_page(
    request: Request,
    user_id: str | None = None,
):
    return templates.TemplateResponse(
        request=request,
        name="feedback.html",
        context=page_context(request, user_id=user_id or "", error=None),
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        feedback_data = FeedbackRequest(user_id=user_id, feedback=feedback)
        user = get_user(db, feedback_data.user_id)
        if not user:
            raise ValueError("User ID was not found. Generate a plan first.")

        plan = get_latest_plan(db, user)
        if not plan:
            raise ValueError("No workout plan was found for this user.")

        # Important: subsequent feedback updates the latest version, while
        # original_plan remains unchanged for admin comparison.
        base_plan = plan.updated_plan or plan.original_plan
        updated = update_workout_plan(
            base_plan,
            feedback_data.feedback,
            user.goal,
            user.intensity,
        )
        updated_tip = generate_nutrition_tip_with_flash(user.goal, feedback_data.feedback)
        plan = update_plan(
            db,
            plan,
            updated,
            feedback_data.feedback,
            nutrition_tip=updated_tip,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context=page_context(
                request,
                user=user,
                plan=plan,
                displayed_plan=updated,
                message="Your plan has been updated using your feedback.",
                error=None,
                is_updated=True,
            ),
        )
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="feedback.html",
            context=page_context(
                request,
                user_id=user_id,
                error=str(exc),
            ),
            status_code=400,
        )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context=page_context(request, users=users),
    )


@router.post("/delete-user/{user_id}")
def remove_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user)
    return RedirectResponse(url="/view-all-users", status_code=303)


@router.get("/api/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}
