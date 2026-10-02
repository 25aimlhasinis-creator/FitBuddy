from .config import GEMINI_WORKOUT_MODEL
from .gemini_client import generate_text


def _fallback_workout_plan(name: str, age: int, weight: float, goal: str, intensity: str) -> str:
    intensity_label = intensity.lower()
    if intensity_label == "low":
        cardio_minutes = 15
        sets = 2
    elif intensity_label == "high":
        cardio_minutes = 25
        sets = 4
    else:
        cardio_minutes = 20
        sets = 3

    if goal == "weight loss":
        focus = "fat loss, conditioning, and consistency"
    elif goal == "muscle gain":
        focus = "strength work, progressive overload, and recovery"
    elif goal == "flexibility":
        focus = "mobility, posture, and controlled movement"
    else:
        focus = "general fitness, stamina, and balanced movement"

    return f"""Day 1
Focus: {focus}
Warm-up: 5 minutes brisk walking or marching, then 10 arm circles and leg swings.
Main Workout: Squats 3 x 10 reps, Push-ups 3 x 8 reps (modify on knees if needed), Dumbbell rows 3 x 10 reps, Plank 3 x 30 seconds.
Cool-down/Recovery: 5 minutes of light stretching and breathing.

Day 2
Focus: Cardio + core
Warm-up: 5 minutes easy cycling or brisk walking.
Main Workout: Incline walk or bike {cardio_minutes} minutes, Dead bug 3 x 10 reps per side, Russian twists 3 x 12 reps, Light lunges 2 x 10 reps per leg.
Cool-down/Recovery: Gentle hamstring and hip flexor stretch.

Day 3
Focus: Strength and posture
Warm-up: 5 minutes dynamic mobility, then band pull-aparts and shoulder rolls.
Main Workout: Hip hinges 3 x 10 reps, Overhead press 3 x 8 reps, Goblet squats 3 x 10 reps, Seated rows 3 x 10 reps, Side planks 2 x 20 seconds per side.
Cool-down/Recovery: Cat-cow and chest-opening stretches.

Day 4
Focus: Recovery and mobility
Warm-up: 5 minutes easy walk and ankle circles.
Main Workout: Mobility circuit: walking lunges 2 x 8 reps, glute bridges 2 x 12 reps, thoracic rotations 2 x 10 reps, easy yoga flow 15 minutes.
Cool-down/Recovery: Full-body stretch and 10 minutes of relaxed breathing.

Day 5
Focus: Lower-body strength
Warm-up: 5 minutes marching and leg swings.
Main Workout: Romanian deadlifts 3 x 10 reps, Reverse lunges 3 x 8 reps each leg, Step-ups 3 x 10 reps each leg, Calf raises 3 x 15 reps.
Cool-down/Recovery: Stretch calves, quads, and hamstrings.

Day 6
Focus: Cardio + upper-body conditioning
Warm-up: 5 minutes light rowing or brisk walk.
Main Workout: Fast-paced interval walk or bike 20 minutes total, Push-ups 3 x 8-12 reps, Lat pulldowns or band rows {sets} x 10 reps, Farmer carry 3 x 20 seconds.
Cool-down/Recovery: Light shoulder and chest stretch.

Day 7
Focus: Recovery and consistency
Warm-up: 5 minutes easy movement and mobility.
Main Workout: Light walk or cycle 20-30 minutes, core routine 10 minutes, gentle stretching.
Cool-down/Recovery: Relaxation walk, hydration, and a short recovery routine.

Safety Note: {name}, if you feel sharp pain, dizziness, or unusual fatigue, stop the workout and consult a qualified fitness professional. Progress gradually, stay hydrated, and prioritize form over intensity.
"""


def generate_workout_gemini(name: str, age: int, weight: float, goal: str, intensity: str) -> str:
    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.
Create a safe, practical, personalized 7-day beginner-to-intermediate workout plan.

User:
- Name: {name}
- Age: {age}
- Weight: {weight} kg
- Goal: {goal}
- Preferred intensity: {intensity}

Requirements:
1. Return exactly 7 days, Day 1 through Day 7.
2. Each day must include Focus, Warm-up, Main Workout, and Cool-down/Recovery.
3. For each main exercise include sets/reps or duration and rest time where appropriate.
4. Match the selected goal and intensity.
5. Include at least one sensible recovery/rest-focused day.
6. Do not prescribe medication, supplements, extreme calorie restriction, or dangerous exercises.
7. Keep the plan practical for a normal gym/home setting.
8. Add a short Safety Note at the end advising the user to stop if they experience pain or unusual symptoms and to consult a qualified professional when appropriate.
9. Use clean plain text headings; do not use JSON or markdown tables.
"""
    try:
        return generate_text(prompt, GEMINI_WORKOUT_MODEL)
    except Exception:
        return _fallback_workout_plan(name, age, weight, goal, intensity)
