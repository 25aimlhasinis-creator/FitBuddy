from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Plan, User


def get_user(db: Session, user_id: str) -> User | None:
    return db.scalar(select(User).where(User.user_id == user_id))


def save_user(db: Session, user_data) -> User:
    user = get_user(db, user_data.user_id)
    if user is None:
        user = User(**user_data.model_dump())
        db.add(user)
    else:
        user.name = user_data.name
        user.age = user_data.age
        user.weight = user_data.weight
        user.goal = user_data.goal
        user.intensity = user_data.intensity
    db.commit()
    db.refresh(user)
    return user


def save_plan(db: Session, user: User, original_plan: str, nutrition_tip: str) -> Plan:
    plan = Plan(user_id=user.id, original_plan=original_plan, nutrition_tip=nutrition_tip)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_latest_plan(db: Session, user: User) -> Plan | None:
    return db.scalar(select(Plan).where(Plan.user_id == user.id).order_by(Plan.created_at.desc()))


def update_plan(db: Session, plan: Plan, updated_plan: str, feedback: str, nutrition_tip: str | None = None) -> Plan:
    plan.updated_plan = updated_plan
    plan.feedback = feedback
    if nutrition_tip:
        plan.nutrition_tip = nutrition_tip
    db.commit()
    db.refresh(plan)
    return plan


def get_all_users(db: Session) -> list[User]:
    return list(db.scalars(select(User).order_by(User.created_at.desc())).all())


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
