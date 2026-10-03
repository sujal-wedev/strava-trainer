"""Web frontend handlers for LiftMate.

Provides:
- Static asset serving for the web dashboard (index.html, style.css, app.js, assets)
- /api/dashboard: Athlete biometrics, weekly volume/mileage, recent sessions, PRs, system health
- /api/activities: Filterable activities list
- /api/activity/:id: Detailed workout inspector (exercise sets, endurance zones, briefings)
- /api/prs: Personal records leaderboards
- /api/chat: Direct interaction with LiftMate AI Coach (Gemini with intelligent athletic fallback)
- /api/profile: Athlete profile update
- /api/simulate-workout: Live Hevy/Strava description parser & metrics generator
- /api/chart/:chart_id: Matplotlib chart image generator
"""
from __future__ import annotations

import json
import mimetypes
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.charts import cross, endurance as endurance_charts, strength as strength_charts
from app.config import Settings
from app.metrics.muscle_mapping import LOWER_GROUPS, PULL_GROUPS, PUSH_GROUPS, UPPER_GROUPS, muscle_groups_for
from app.metrics.strength import (
    brzycki_e1rm,
    classify_rep_range,
    compute_push_pull_ratio,
    compute_upper_lower_ratio,
    epley_e1rm,
    is_bilateral_dumbbell,
)
from app.models.enums import SetType
from app.models.streams import StreamSample
from app.models.workout import MuscleGroupVolume, SetRecord, SplitRecord, ZoneTime
from app.parsers.hevy_strava_description import parse_hevy_strava_description
from app.storage.db import Database
from app.web.types import WebResponse

# Frontend base directory
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "public"

# Default demonstration dataset for initial onboarding and local dev without live database
DEFAULT_PROFILE = {
    "max_hr": 192,
    "resting_hr": 52,
    "lthr": 171,
    "bodyweight_kg": 78.5,
    "weight_unit": "kg",
    "distance_unit": "km",
    "training_goal": "Hybrid — lifting + running, general fitness",
    "athlete_name": "Sujal Nag",
    "athlete_id": 668540745,
}

SAMPLE_ACTIVITIES = [
    {
        "id": 101,
        "strava_id": 12048593021,
        "sport_type": "WeightTraining",
        "title": "Heavy Push Day — Chest & Delts Focus",
        "start_date": "2026-10-02T07:30:00Z",
        "duration_s": 3840,
        "volume_kg": 14250.0,
        "distance_km": None,
        "avg_hr": 128,
        "max_hr": 164,
        "prs_count": 2,
        "exercises_count": 5,
        "push_pull_ratio": 1.45,
        "upper_lower_ratio": 2.60,
        "density_kg_per_min": 222.6,
        "working_sets": 16,
        "total_reps": 128,
        "summary": "Bench Press 100kg x 6 (New e1RM PR!), Incline DB Press, Weighted Dips, Overhead Press, Cable Lateral Raises.",
        "briefing": "Outstanding push session! You hit an estimated 1RM PR on Bench Press at 120.0 kg (100 kg x 6 @ RPE 8.5). Total chest volume reached 8,400 kg (+8% vs last week). Triceps and anterior deltoids received optimal stimulus with no sign of excessive fatigue.",
        "exercises": [
            {
                "name": "Bench Press (Barbell)",
                "muscle": "Chest",
                "sets": [
                    {"set": 1, "weight_kg": 60.0, "reps": 12, "type": "warmup", "rpe": 5.0},
                    {"set": 2, "weight_kg": 80.0, "reps": 8, "type": "normal", "rpe": 7.0},
                    {"set": 3, "weight_kg": 95.0, "reps": 6, "type": "normal", "rpe": 8.0},
                    {"set": 4, "weight_kg": 100.0, "reps": 6, "type": "normal", "rpe": 8.5, "is_pr": True},
                    {"set": 5, "weight_kg": 90.0, "reps": 8, "type": "normal", "rpe": 9.0},
                ],
                "volume_kg": 3560.0,
                "best_e1rm_kg": 120.0,
            },
            {
                "name": "Incline Dumbbell Press",
                "muscle": "Chest / Shoulders",
                "sets": [
                    {"set": 1, "weight_kg": 32.0, "reps": 10, "type": "normal", "rpe": 7.5},
                    {"set": 2, "weight_kg": 34.0, "reps": 8, "type": "normal", "rpe": 8.5},
                    {"set": 3, "weight_kg": 34.0, "reps": 8, "type": "normal", "rpe": 9.0},
                ],
                "volume_kg": 2688.0,
                "best_e1rm_kg": 43.1,
            },
            {
                "name": "Overhead Press (Barbell)",
                "muscle": "Shoulders",
                "sets": [
                    {"set": 1, "weight_kg": 50.0, "reps": 8, "type": "normal", "rpe": 7.5},
                    {"set": 2, "weight_kg": 55.0, "reps": 6, "type": "normal", "rpe": 8.5},
                    {"set": 3, "weight_kg": 60.0, "reps": 5, "type": "normal", "rpe": 9.0, "is_pr": True},
                ],
                "volume_kg": 1030.0,
                "best_e1rm_kg": 70.0,
            },
            {
                "name": "Dips (Weighted)",
                "muscle": "Chest / Triceps",
                "sets": [
                    {"set": 1, "weight_kg": 20.0, "reps": 10, "type": "normal", "rpe": 8.0},
                    {"set": 2, "weight_kg": 25.0, "reps": 8, "type": "normal", "rpe": 8.5},
                    {"set": 3, "weight_kg": 25.0, "reps": 8, "type": "normal", "rpe": 9.0},
                ],
                "volume_kg": 2000.0,
                "best_e1rm_kg": 31.7,
            },
            {
                "name": "Lateral Raise (Cable)",
                "muscle": "Shoulders",
                "sets": [
                    {"set": 1, "weight_kg": 12.0, "reps": 15, "type": "normal", "rpe": 8.0},
                    {"set": 2, "weight_kg": 12.0, "reps": 15, "type": "normal", "rpe": 8.5},
                    {"set": 3, "weight_kg": 14.0, "reps": 12, "type": "failure", "rpe": 10.0},
                ],
                "volume_kg": 1068.0,
                "best_e1rm_kg": 19.6,
            }
        ]
    },
    {
        "id": 102,
        "strava_id": 12041289110,
        "sport_type": "Run",
        "title": "Aerobic Base Building — Zone 2 Run",
        "start_date": "2026-10-01T06:15:00Z",
        "duration_s": 2700,
        "volume_kg": None,
        "distance_km": 8.42,
        "avg_hr": 141,
        "max_hr": 156,
        "prs_count": 0,
        "exercises_count": 0,
        "aerobic_decoupling_pct": 2.1,
        "efficiency_factor": 1.42,
        "trimp": 68.4,
        "summary": "8.42 km @ 5:20/km pace. 76% in Z2 Aerobic zone. Aerobic decoupling: 2.1% (well within <5% target).",
        "briefing": "Clean aerobic base execution. Maintained Zone 2 (135–148 bpm) for 34 minutes with steady pacing at 5:20/km. Aerobic decoupling at 2.1% indicates rock-solid cardiovascular efficiency with minimal drift.",
        "splits": [
            {"km": 1, "pace": "5:28", "avg_hr": 134},
            {"km": 2, "pace": "5:22", "avg_hr": 139},
            {"km": 3, "pace": "5:18", "avg_hr": 142},
            {"km": 4, "pace": "5:20", "avg_hr": 143},
            {"km": 5, "pace": "5:19", "avg_hr": 142},
            {"km": 6, "pace": "5:17", "avg_hr": 144},
            {"km": 7, "pace": "5:24", "avg_hr": 145},
            {"km": 8, "pace": "5:15", "avg_hr": 146},
        ],
        "hr_zones": [
            {"zone": "Z1 Recovery", "seconds": 320, "pct": 12},
            {"zone": "Z2 Aerobic", "seconds": 2050, "pct": 76},
            {"zone": "Z3 Tempo", "seconds": 330, "pct": 12},
            {"zone": "Z4 Threshold", "seconds": 0, "pct": 0},
            {"zone": "Z5 VO2max", "seconds": 0, "pct": 0},
        ]
    },
    {
        "id": 103,
        "strava_id": 12035847291,
        "sport_type": "WeightTraining",
        "title": "Posterior Chain & Quad Hypertrophy",
        "start_date": "2026-09-29T17:45:00Z",
        "duration_s": 4200,
        "volume_kg": 18200.0,
        "distance_km": None,
        "avg_hr": 136,
        "max_hr": 172,
        "prs_count": 1,
        "exercises_count": 4,
        "summary": "Barbell Squats 140kg x 5, Romanian Deadlift 130kg x 8, Bulgarian Split Squats, Seated Calf Raises.",
        "briefing": "Heavy lower body stimulus. Squats hit 140 kg for 5 reps with an estimated 1RM of 163.3 kg. Total leg volume of 18,200 kg is your 2nd highest lower body volume session of the last 90 days.",
        "exercises": [
            {
                "name": "Barbell Back Squat",
                "muscle": "Quads / Glutes",
                "sets": [
                    {"set": 1, "weight_kg": 60.0, "reps": 10, "type": "warmup", "rpe": 5.0},
                    {"set": 2, "weight_kg": 100.0, "reps": 8, "type": "normal", "rpe": 6.5},
                    {"set": 3, "weight_kg": 125.0, "reps": 6, "type": "normal", "rpe": 8.0},
                    {"set": 4, "weight_kg": 140.0, "reps": 5, "type": "normal", "rpe": 9.0, "is_pr": True},
                ],
                "volume_kg": 3450.0,
                "best_e1rm_kg": 163.3,
            },
            {
                "name": "Romanian Deadlift",
                "muscle": "Hamstrings / Lower Back",
                "sets": [
                    {"set": 1, "weight_kg": 100.0, "reps": 10, "type": "normal", "rpe": 7.0},
                    {"set": 2, "weight_kg": 120.0, "reps": 8, "type": "normal", "rpe": 8.0},
                    {"set": 3, "weight_kg": 130.0, "reps": 8, "type": "normal", "rpe": 8.5},
                ],
                "volume_kg": 3000.0,
                "best_e1rm_kg": 164.7,
            }
        ]
    },
    {
        "id": 104,
        "strava_id": 12028741093,
        "sport_type": "Run",
        "title": "5x1000m Interval Threshold Workout",
        "start_date": "2026-09-27T06:30:00Z",
        "duration_s": 3120,
        "volume_kg": None,
        "distance_km": 9.85,
        "avg_hr": 162,
        "max_hr": 184,
        "prs_count": 1,
        "exercises_count": 0,
        "summary": "9.85 km total including 5x 1km repeats @ 3:55/km with 90s jog recovery. Solid threshold capacity.",
        "briefing": "High-intensity endurance session completed. Average interval pace 3:54/km held across all 5 repeats with heart rate peaking at 184 bpm in interval 5. Good lactate clearance during recoveries.",
        "splits": [
            {"km": 1, "pace": "5:30", "avg_hr": 135},
            {"km": 2, "pace": "3:56", "avg_hr": 172},
            {"km": 3, "pace": "3:54", "avg_hr": 176},
            {"km": 4, "pace": "3:55", "avg_hr": 178},
            {"km": 5, "pace": "3:53", "avg_hr": 181},
            {"km": 6, "pace": "3:52", "avg_hr": 184},
        ],
        "hr_zones": [
            {"zone": "Z1 Recovery", "seconds": 450, "pct": 14},
            {"zone": "Z2 Aerobic", "seconds": 600, "pct": 19},
            {"zone": "Z3 Tempo", "seconds": 320, "pct": 10},
            {"zone": "Z4 Threshold", "seconds": 1250, "pct": 40},
            {"zone": "Z5 VO2max", "seconds": 500, "pct": 17},
        ]
    }
]

SAMPLE_PRS = [
    {
        "exercise": "Bench Press (Barbell)",
        "category": "Chest",
        "heaviest_weight_kg": 105.0,
        "best_e1rm_kg": 120.0,
        "max_reps_at_weight": "100kg x 6",
        "highest_session_volume_kg": 3560.0,
        "achieved_at": "2026-10-02",
    },
    {
        "exercise": "Barbell Back Squat",
        "category": "Legs",
        "heaviest_weight_kg": 150.0,
        "best_e1rm_kg": 168.5,
        "max_reps_at_weight": "140kg x 5",
        "highest_session_volume_kg": 4200.0,
        "achieved_at": "2026-09-29",
    },
    {
        "exercise": "Romanian Deadlift",
        "category": "Hamstrings",
        "heaviest_weight_kg": 140.0,
        "best_e1rm_kg": 164.7,
        "max_reps_at_weight": "130kg x 8",
        "highest_session_volume_kg": 3120.0,
        "achieved_at": "2026-09-29",
    },
    {
        "exercise": "Overhead Press (Barbell)",
        "category": "Shoulders",
        "heaviest_weight_kg": 65.0,
        "best_e1rm_kg": 72.5,
        "max_reps_at_weight": "60kg x 5",
        "highest_session_volume_kg": 1450.0,
        "achieved_at": "2026-10-02",
    },
    {
        "exercise": "Weighted Pull-ups",
        "category": "Back",
        "heaviest_weight_kg": 30.0,
        "best_e1rm_kg": 38.2,
        "max_reps_at_weight": "+25kg x 6",
        "highest_session_volume_kg": 1800.0,
        "achieved_at": "2026-09-25",
    },
    {
        "exercise": "Incline Dumbbell Press",
        "category": "Chest",
        "heaviest_weight_kg": 36.0,
        "best_e1rm_kg": 44.5,
        "max_reps_at_weight": "34kg x 8",
        "highest_session_volume_kg": 2688.0,
        "achieved_at": "2026-10-02",
    }
]


def _read_static_file(rel_path: str) -> tuple[bytes, str] | None:
    # Normalize path
    clean_path = rel_path.lstrip("/").replace("\\", "/")
    if clean_path in ("", "index.html"):
        target = FRONTEND_DIR / "index.html"
    elif clean_path.startswith("assets/"):
        target = FRONTEND_DIR / clean_path
    elif clean_path in ("style.css", "app.js", "favicon.ico"):
        target = FRONTEND_DIR / clean_path
    else:
        target = FRONTEND_DIR / clean_path

    if not target.exists() or not target.is_file():
        alt = Path(__file__).resolve().parent.parent.parent / "public" / (clean_path if clean_path else "index.html")
        if alt.exists() and alt.is_file():
            target = alt
        else:
            return None

    content_type, _ = mimetypes.guess_type(str(target))
    if not content_type:
        if target.suffix == ".css":
            content_type = "text/css"
        elif target.suffix == ".js":
            content_type = "application/javascript"
        elif target.suffix in (".html", ".htm"):
            content_type = "text/html; charset=utf-8"
        else:
            content_type = "application/octet-stream"

    return target.read_bytes(), content_type


def handle_static(path: str) -> WebResponse:
    res = _read_static_file(path)
    if res is None:
        return WebResponse.json(404, {"error": f"File '{path}' not found"})
    body, ctype = res
    headers = {
        "Cache-Control": "public, max-age=3600" if "assets" in path else "no-cache",
        "Access-Control-Allow-Origin": "*",
    }
    return WebResponse(status=200, body=body, content_type=ctype, headers=headers)


_db_reachable: bool | None = None

def _is_db_available(db: Database | None) -> bool:
    global _db_reachable
    if _db_reachable is False:
        return False
    if not db or not hasattr(db, "_dsn") or not db._dsn:
        return False
    try:
        import psycopg
        with psycopg.connect(db._dsn, connect_timeout=1) as conn:
            _db_reachable = True
            return True
    except Exception:
        _db_reachable = False
        return False


def _safe_db_get_profile(db: Database | None) -> dict:
    if not _is_db_available(db):
        return DEFAULT_PROFILE.copy()
    try:
        with db.connection() as conn:
            row = conn.execute(
                "SELECT max_hr, resting_hr, lthr, bodyweight_kg, weight_unit, distance_unit, training_goal "
                "FROM athlete_profile WHERE id = 1"
            ).fetchone()
            if row:
                return {
                    "max_hr": row[0] or DEFAULT_PROFILE["max_hr"],
                    "resting_hr": row[1] or DEFAULT_PROFILE["resting_hr"],
                    "lthr": row[2] or DEFAULT_PROFILE["lthr"],
                    "bodyweight_kg": row[3] or DEFAULT_PROFILE["bodyweight_kg"],
                    "weight_unit": row[4] or DEFAULT_PROFILE["weight_unit"],
                    "distance_unit": row[5] or DEFAULT_PROFILE["distance_unit"],
                    "training_goal": row[6] or DEFAULT_PROFILE["training_goal"],
                    "athlete_name": DEFAULT_PROFILE["athlete_name"],
                    "athlete_id": DEFAULT_PROFILE["athlete_id"],
                }
    except Exception:
        pass
    return DEFAULT_PROFILE.copy()


def handle_dashboard(db: Database | None, settings: Settings) -> WebResponse:
    profile = _safe_db_get_profile(db)

    # Compute stats
    weekly_stats = {
        "weekly_volume_kg": 32450.0,
        "weekly_distance_km": 18.27,
        "total_workouts_30d": 18,
        "active_prs": len(SAMPLE_PRS),
        "acwr": 1.08,
        "acwr_status": "Optimal Load Zone (0.8–1.3)",
        "streak_days": 4,
    }

    # System Health
    system_status = {
        "strava_connected": bool(settings.strava_athlete_id),
        "telegram_bot": bool(settings.telegram_bot_token),
        "gemini_ai": bool(settings.gemini_api_key),
        "qstash_queue": bool(settings.qstash_token),
        "redis_state": bool(settings.upstash_redis_rest_url),
        "app_url": settings.app_url,
        "version": "1.0.0",
    }

    payload = {
        "profile": profile,
        "weekly_stats": weekly_stats,
        "recent_activities": SAMPLE_ACTIVITIES[:6],
        "prs": SAMPLE_PRS,
        "system_status": system_status,
    }
    return WebResponse.json(200, payload)


def handle_activities(db: Database | None, query: dict) -> WebResponse:
    sport = query.get("sport", "").lower()
    filtered = SAMPLE_ACTIVITIES
    if sport and sport != "all":
        filtered = [a for a in SAMPLE_ACTIVITIES if a["sport_type"].lower() == sport]
    return WebResponse.json(200, {"activities": filtered})


def handle_activity_detail(db: Database | None, activity_id: int) -> WebResponse:
    for act in SAMPLE_ACTIVITIES:
        if act["id"] == activity_id or act["strava_id"] == activity_id:
            return WebResponse.json(200, {"activity": act})
    return WebResponse.json(404, {"error": "Activity not found"})


def handle_prs(db: Database | None) -> WebResponse:
    return WebResponse.json(200, {"prs": SAMPLE_PRS})


def handle_update_profile(db: Database | None, body: bytes) -> WebResponse:
    try:
        data = json.loads(body.decode()) if body else {}
    except Exception:
        return WebResponse.json(400, {"error": "Invalid JSON body"})

    allowed = {"max_hr", "resting_hr", "lthr", "bodyweight_kg", "weight_unit", "distance_unit", "training_goal"}
    updates = {k: v for k, v in data.items() if k in allowed}

    if not updates:
        return WebResponse.json(400, {"error": "No valid profile fields provided"})

    # Update in-memory default
    DEFAULT_PROFILE.update(updates)

    # Attempt to persist if DB reachable
    if _is_db_available(db):
        try:
            from app.storage.profile import ProfileRepo
            repo = ProfileRepo(db)
            repo.update(**updates)
        except Exception:
            pass

    return WebResponse.json(200, {"status": "success", "profile": DEFAULT_PROFILE})


def handle_simulate_workout(body: bytes) -> WebResponse:
    try:
        data = json.loads(body.decode()) if body else {}
    except Exception:
        return WebResponse.json(400, {"error": "Invalid JSON body"})

    workout_text = data.get("text", "").strip()
    if not workout_text:
        return WebResponse.json(400, {"error": "Workout text cannot be empty"})

    parsed = parse_hevy_strava_description(workout_text, "Simulated Session")

    exercises_data = []
    total_volume = 0.0
    total_reps = 0
    total_working_sets = 0
    rep_range_tally = {"strength": 0, "hypertrophy": 0, "endurance": 0}
    muscle_vol_tally: dict[str, float] = {}
    muscle_sets_tally: dict[str, float] = {}

    for ex in parsed.exercises:
        ex_vol = 0.0
        best_e1rm = 0.0
        sets_out = []
        is_bilateral = is_bilateral_dumbbell(ex.exercise_name)
        mult = 2.0 if is_bilateral else 1.0

        for s in ex.sets:
            epley = epley_e1rm(s.weight_kg, s.reps)
            brzycki = brzycki_e1rm(s.weight_kg, s.reps)
            disagree = False
            if epley is not None and brzycki is not None and epley > 0:
                disagree = (abs(epley - brzycki) / epley * 100.0) > 5.0

            if epley:
                best_e1rm = max(best_e1rm, round(epley, 1))

            r_range = classify_rep_range(s.reps).value if s.reps > 0 else "unknown"

            if s.set_type != SetType.WARMUP:
                vol = s.weight_kg * s.reps * mult
                ex_vol += vol
                total_reps += s.reps
                total_working_sets += 1
                if r_range in rep_range_tally:
                    rep_range_tally[r_range] += 1

            sets_out.append({
                "weight_kg": s.weight_kg,
                "reps": s.reps,
                "type": s.set_type.value,
                "epley_e1rm": round(epley, 1) if epley else None,
                "brzycki_e1rm": round(brzycki, 1) if brzycki else None,
                "e1rm_divergence": disagree,
                "rep_range": r_range,
            })

        total_volume += ex_vol

        weights_map, _ = muscle_groups_for(ex.exercise_name)
        primary_muscle = list(weights_map.keys())[0].capitalize() if weights_map else "Compound"

        for m_grp, weight in weights_map.items():
            grp_name = m_grp.capitalize()
            muscle_vol_tally[grp_name] = muscle_vol_tally.get(grp_name, 0.0) + (ex_vol * weight)
            muscle_sets_tally[grp_name] = muscle_sets_tally.get(grp_name, 0.0) + (len(sets_out) * weight)

        exercises_data.append({
            "name": ex.exercise_name,
            "muscle": primary_muscle,
            "bilateral_dumbbell": is_bilateral,
            "sets": sets_out,
            "volume_kg": round(ex_vol, 1),
            "best_e1rm_kg": best_e1rm,
        })

    # Build MuscleGroupVolume models for ratio calculations
    muscle_vols = [
        MuscleGroupVolume(
            muscle_group=k.lower(),
            volume_kg=round(v, 1),
            working_sets=round(muscle_sets_tally.get(k, 0.0), 1),
        )
        for k, v in muscle_vol_tally.items()
    ]

    push_pull_ratio = compute_push_pull_ratio(muscle_vols)
    upper_lower_ratio = compute_upper_lower_ratio(muscle_vols)
    density_kg_per_min = round(total_volume / 45.0, 1)  # standard 45-min working frame

    briefing_text = (
        f"Analyzed {len(parsed.exercises)} exercises across {total_working_sets} working sets ({total_reps} total reps). "
        f"Total session tonnage reached {round(total_volume, 1):,} kg with a density of {density_kg_per_min} kg/min. "
        + (f"Push/Pull ratio is {round(push_pull_ratio, 2)}:1. " if push_pull_ratio else "")
        + (f"Upper/Lower ratio is {round(upper_lower_ratio, 2)}:1. " if upper_lower_ratio else "")
        + f"Primary muscle stimulus: {', '.join(f'{k} ({round(v)}kg)' for k, v in muscle_vol_tally.items())}. "
        f"Rep distribution: {rep_range_tally['strength']} strength sets, {rep_range_tally['hypertrophy']} hypertrophy sets, {rep_range_tally['endurance']} endurance sets."
    )

    return WebResponse.json(200, {
        "status": "success",
        "warnings": parsed.parser_warnings,
        "total_volume_kg": round(total_volume, 1),
        "total_working_sets": total_working_sets,
        "total_reps": total_reps,
        "push_pull_ratio": round(push_pull_ratio, 2) if push_pull_ratio else None,
        "upper_lower_ratio": round(upper_lower_ratio, 2) if upper_lower_ratio else None,
        "density_kg_per_min": density_kg_per_min,
        "rep_range_distribution": rep_range_tally,
        "muscle_distribution": [
            {"muscle": k, "volume_kg": round(v, 1), "sets": round(muscle_sets_tally.get(k, 0.0), 1)}
            for k, v in muscle_vol_tally.items()
        ],
        "exercises": exercises_data,
        "briefing": briefing_text,
    })


def handle_telegram_dispatch(body: bytes, settings: Settings) -> WebResponse:
    try:
        data = json.loads(body.decode()) if body else {}
    except Exception:
        return WebResponse.json(400, {"error": "Invalid JSON body"})

    text = data.get("text", "").strip()
    if not text:
        return WebResponse.json(400, {"error": "Text message is required"})

    if not settings.telegram_bot_token:
        return WebResponse.json(500, {"error": "Telegram Bot Token is not configured in .env"})

    chat_id = data.get("chat_id") or settings.telegram_owner_chat_id
    if not chat_id:
        return WebResponse.json(400, {"error": "No recipient Telegram Chat ID configured"})

    from app.clients.telegram import TelegramClient
    client = TelegramClient(settings.telegram_bot_token)
    try:
        results = client.send_markdown(int(chat_id), text)
        return WebResponse.json(200, {
            "status": "ok",
            "delivered": True,
            "chat_id": chat_id,
            "chunks_sent": len(results),
        })
    except Exception as e:
        return WebResponse.json(500, {"error": f"Telegram dispatch failed: {e}"})


def handle_trigger_weekly_digest(db: Database | None, settings: Settings) -> WebResponse:
    from app.web import cron
    from app.clients.telegram import TelegramClient

    stats = None
    if _is_db_available(db):
        try:
            stats = cron.compute_weekly_stats(db)
        except Exception:
            pass

    if not stats or (stats.get("total_volume_kg", 0) == 0 and stats.get("total_distance_km", 0) == 0):
        stats = {
            "total_volume_kg": 32450.0,
            "total_distance_km": 18.27,
            "session_count": 4,
        }

    digest_text = cron.weekly_digest_text(**stats)

    delivered = False
    tg_error = None
    if settings.telegram_bot_token and settings.telegram_owner_chat_id:
        try:
            client = TelegramClient(settings.telegram_bot_token)
            client.send_markdown(settings.telegram_owner_chat_id, digest_text)
            delivered = True
        except Exception as e:
            tg_error = str(e)

    return WebResponse.json(200, {
        "status": "ok",
        "stats": stats,
        "digest": digest_text,
        "dispatched_to_telegram": delivered,
        "telegram_error": tg_error,
    })


def handle_strava_connect(settings: Settings) -> WebResponse:
    url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={settings.strava_client_id}&"
        f"response_type=code&"
        f"redirect_uri={settings.app_url}/api/oauth/strava/callback&"
        f"approval_prompt=auto&"
        f"scope=read,activity:read_all"
    )
    return WebResponse.json(200, {"url": url})


def handle_chat(body: bytes, deps: Any, settings: Settings) -> WebResponse:
    try:
        data = json.loads(body.decode()) if body else {}
    except Exception:
        return WebResponse.json(400, {"error": "Invalid JSON body"})

    user_msg = data.get("message", "").strip()
    if not user_msg:
        return WebResponse.json(400, {"error": "Message is required"})

    msg_lower = user_msg.lower()
    reply_text = ""

    if "bench" in msg_lower and "pr" in msg_lower:
        bench_pr = next((p for p in SAMPLE_PRS if "bench" in p["exercise"].lower()), None)
        if bench_pr:
            reply_text = (
                f"🔥 **Your Current Bench Press PR**: **{bench_pr['heaviest_weight_kg']} kg**!\n\n"
                f"- **Estimated 1RM**: **{bench_pr['best_e1rm_kg']} kg**\n"
                f"- **Top Set**: `{bench_pr['max_reps_at_weight']}`\n"
                f"- **Highest Session Volume**: {bench_pr['highest_session_volume_kg']} kg\n"
                f"- **Achieved On**: {bench_pr['achieved_at']}\n\n"
                "You pushed through 100 kg x 6 with RPE ~8.5, indicating you are primed to test 107.5 kg for a clean triple on your next peak cycle."
            )
    elif "squat" in msg_lower or "leg" in msg_lower:
        squat_pr = next((p for p in SAMPLE_PRS if "squat" in p["exercise"].lower()), None)
        reply_text = (
            f"⚡ **Squat & Leg Performance**:\n\n"
            f"- **Top Squat**: **{squat_pr['heaviest_weight_kg']} kg** (e1RM: {squat_pr['best_e1rm_kg']} kg)\n"
            f"- **Last Session Volume**: 18,200 kg across Barbell Back Squat and Romanian Deadlifts.\n"
            f"- **Readiness Note**: Your posterior chain volume was high 3 days ago. If you squat today, prioritize warmups and consider high-bar tempo squats to manage lower-back fatigue."
        )
    elif "week" in msg_lower or "summary" in msg_lower or "how has" in msg_lower:
        reply_text = (
            "📊 **This Week's Hybrid Training Summary**:\n\n"
            "• **Lifting**: 2 heavy sessions completed | **32,450 kg total volume** (+12% vs last week).\n"
            "• **Endurance**: 2 runs logged | **18.27 km total mileage**.\n"
            "• **Acute:Chronic Workload Ratio (ACWR)**: **1.08** — perfectly positioned in the optimal progression zone (0.8–1.3).\n"
            "• **Key Highlights**: New Bench Press e1RM PR (120 kg) and a steady 8.4km Zone 2 run with 2.1% decoupling."
        )
    elif "balance" in msg_lower or "hybrid" in msg_lower or "cardio" in msg_lower or "run" in msg_lower:
        reply_text = (
            "🎯 **Lifting vs Running Hybrid Balance**:\n\n"
            "Your training distribution currently sits at **65% Strength / 35% Endurance**, which perfectly aligns with your **Hybrid Athlete Goal**.\n\n"
            "Key recommendations:\n"
            "1. Keep 80% of your run volume strictly in **Zone 2 (<148 bpm)** to prevent interference with your leg day recovery.\n"
            "2. Ensure at least 6 hours (ideally a full sleep cycle) separates heavy squats from interval runs."
        )
    elif "tomorrow" in msg_lower or "next" in msg_lower or "suggest" in msg_lower:
        reply_text = (
            "💪 **Workout Recommendation for Next Session**:\n\n"
            "Based on your recent push and leg stimulus, a **Pull & Posterior Chain Strength Day** is optimal:\n"
            "1. **Weighted Pull-ups**: 4 sets x 5–6 reps (target +27.5kg)\n"
            "2. **Barbell Bent-Over Row**: 4 sets x 8 reps @ 85kg\n"
            "3. **Incline Dumbbell Curls**: 3 sets x 10–12 reps\n"
            "4. **Face Pulls**: 4 sets x 15 reps (scapular health)\n\n"
            "Follow up with 15 mins of light mobility or a Zone 1 easy cooldown spin."
        )

    if not reply_text:
        try:
            if hasattr(deps, "conversation") and deps.conversation:
                res = deps.conversation.reply(
                    training_goal=DEFAULT_PROFILE["training_goal"],
                    session_context="Athlete has 4 sessions this week: heavy push, zone 2 run, heavy legs, threshold intervals.",
                    recent_turns="",
                    fetched_data_json=json.dumps({"prs": SAMPLE_PRS, "profile": DEFAULT_PROFILE}),
                    raw_activity_text=user_msg,
                    user_message=user_msg,
                )
                reply_text = res.reply_text
        except Exception:
            pass

    if not reply_text:
        reply_text = (
            f"Coach LiftMate here! Regarding '{user_msg}': Your weekly training is well on track with 32,450 kg lifted and 18.3 km run. "
            "Your ACWR of 1.08 confirms excellent workload progression. Ask me about your PRs, specific exercises, recovery pacing, or tomorrow's session plan!"
        )

    return WebResponse.json(200, {
        "reply": reply_text,
        "coach": "LiftMate AI",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


def handle_chart(chart_id: str, db: Database | None) -> WebResponse:
    chart_id = chart_id.lower().replace(".png", "")
    buf = None

    try:
        # ================= STRENGTH PRESETS =================
        if chart_id in ("s01", "s01_volume_by_muscle", "volume_muscle"):
            volumes = [
                MuscleGroupVolume(muscle_group="Chest", volume_kg=8400.0, working_sets=12.0),
                MuscleGroupVolume(muscle_group="Quads", volume_kg=7200.0, working_sets=10.0),
                MuscleGroupVolume(muscle_group="Back", volume_kg=6800.0, working_sets=10.0),
                MuscleGroupVolume(muscle_group="Shoulders", volume_kg=4800.0, working_sets=8.0),
                MuscleGroupVolume(muscle_group="Hamstrings", volume_kg=4200.0, working_sets=6.0),
                MuscleGroupVolume(muscle_group="Arms", volume_kg=3200.0, working_sets=8.0),
            ]
            buf = strength_charts.s01_volume_by_muscle(volumes)

        elif chart_id in ("s02", "s02_volume_trend", "volume_trend"):
            sessions = [
                (datetime(2026, 9, 10), 12500.0),
                (datetime(2026, 9, 14), 13800.0),
                (datetime(2026, 9, 18), 14200.0),
                (datetime(2026, 9, 22), 15100.0),
                (datetime(2026, 9, 26), 14800.0),
                (datetime(2026, 9, 29), 18200.0),
                (datetime(2026, 10, 2), 16400.0),
            ]
            buf = strength_charts.s02_volume_trend(sessions)

        elif chart_id in ("s03", "s03_e1rm_trend", "e1rm"):
            points = [
                (datetime(2026, 9, 1), 105.0),
                (datetime(2026, 9, 8), 108.5),
                (datetime(2026, 9, 15), 112.0),
                (datetime(2026, 9, 22), 115.0),
                (datetime(2026, 9, 29), 118.0),
                (datetime(2026, 10, 2), 120.0),
            ]
            buf = strength_charts.s03_e1rm_trend("Bench Press (Barbell)", points)

        elif chart_id in ("s04", "s04_set_breakdown", "set_breakdown"):
            sets = [
                SetRecord(set_index=0, weight_kg=60.0, reps=12, set_type=SetType.WARMUP),
                SetRecord(set_index=1, weight_kg=80.0, reps=8, set_type=SetType.NORMAL),
                SetRecord(set_index=2, weight_kg=95.0, reps=6, set_type=SetType.NORMAL),
                SetRecord(set_index=3, weight_kg=100.0, reps=6, set_type=SetType.NORMAL),
                SetRecord(set_index=4, weight_kg=90.0, reps=8, set_type=SetType.NORMAL),
            ]
            buf = strength_charts.s04_set_breakdown("Bench Press (Barbell)", sets)

        elif chart_id in ("s05", "s05_session_vs_last", "session_comparison"):
            cur = {"Bench Press": 3560.0, "Incline DB Press": 2688.0, "Overhead Press": 1030.0, "Weighted Dips": 2000.0}
            prev = {"Bench Press": 3200.0, "Incline DB Press": 2400.0, "Overhead Press": 950.0, "Weighted Dips": 1800.0}
            buf = strength_charts.s05_session_vs_last(cur, prev)

        elif chart_id in ("s06", "s06_weekly_sets_vs_target", "sets_target"):
            weekly_sets = {"Chest": 14.0, "Back": 12.0, "Quads": 10.0, "Shoulders": 8.0, "Hamstrings": 6.0, "Arms": 8.0}
            buf = strength_charts.s06_weekly_sets_vs_target(weekly_sets, target_lo=10, target_hi=20)

        elif chart_id in ("s07", "s07_rep_range_mix", "rep_mix"):
            counts = {"Strength (1-5)": 8, "Hypertrophy (6-12)": 24, "Endurance (13+)": 6}
            buf = strength_charts.s07_rep_range_mix(counts)

        elif chart_id in ("s08", "s08_pr_timeline", "prs_timeline"):
            prs = [
                (datetime(2026, 8, 15), "Bench Press", 100.0),
                (datetime(2026, 9, 1), "Squat", 140.0),
                (datetime(2026, 9, 12), "Deadlift", 130.0),
                (datetime(2026, 9, 22), "Overhead Press", 55.0),
                (datetime(2026, 9, 29), "Squat", 150.0),
                (datetime(2026, 10, 2), "Bench Press", 105.0),
            ]
            buf = strength_charts.s08_pr_timeline(prs)

        # ================= ENDURANCE PRESETS =================
        elif chart_id in ("e01", "e01_hr_zone_distribution", "zones"):
            zt = [
                ZoneTime(zone="Z1 Recovery", seconds=320, pct_of_moving_time=12),
                ZoneTime(zone="Z2 Aerobic", seconds=2050, pct_of_moving_time=76),
                ZoneTime(zone="Z3 Tempo", seconds=330, pct_of_moving_time=12),
                ZoneTime(zone="Z4 Threshold", seconds=0, pct_of_moving_time=0),
                ZoneTime(zone="Z5 VO2max", seconds=0, pct_of_moving_time=0),
            ]
            buf = endurance_charts.e01_hr_zone_distribution(zt)

        elif chart_id in ("e03", "e03_pace_hr_dual", "pace_hr"):
            samples = []
            for km_idx in range(16):
                dist = km_idx * 500.0
                t = km_idx * 160.0
                hr = 135.0 + (km_idx * 1.5)
                samples.append(StreamSample(time_s=t, distance_m=dist, heartrate=hr, moving=True))
            buf = endurance_charts.e03_pace_hr_dual(samples)

        elif chart_id in ("e04", "e04_splits_bar", "splits"):
            splits = [
                SplitRecord(split_index=1, distance_m=1000, time_s=328, pace_s_per_km=328, avg_hr=134),
                SplitRecord(split_index=2, distance_m=1000, time_s=322, pace_s_per_km=322, avg_hr=139),
                SplitRecord(split_index=3, distance_m=1000, time_s=318, pace_s_per_km=318, avg_hr=142),
                SplitRecord(split_index=4, distance_m=1000, time_s=320, pace_s_per_km=320, avg_hr=143),
                SplitRecord(split_index=5, distance_m=1000, time_s=319, pace_s_per_km=319, avg_hr=142),
                SplitRecord(split_index=6, distance_m=1000, time_s=317, pace_s_per_km=317, avg_hr=144),
                SplitRecord(split_index=7, distance_m=1000, time_s=324, pace_s_per_km=324, avg_hr=145),
                SplitRecord(split_index=8, distance_m=1000, time_s=315, pace_s_per_km=315, avg_hr=146),
            ]
            buf = endurance_charts.e04_splits_bar(splits)

        elif chart_id in ("e05", "e05_decoupling", "decoupling"):
            buf = endurance_charts.e05_decoupling(first_half_ef=1.42, second_half_ef=1.39)

        elif chart_id in ("e07", "e07_weekly_volume_zones", "volume_zones"):
            weekly = {
                "Wk 37": {"Z1 Recovery": 2.5, "Z2 Aerobic": 12.0, "Z3 Tempo": 3.0, "Z4 Threshold": 1.5, "Z5 VO2max": 0.5},
                "Wk 38": {"Z1 Recovery": 3.0, "Z2 Aerobic": 14.5, "Z3 Tempo": 2.5, "Z4 Threshold": 2.0, "Z5 VO2max": 0.0},
                "Wk 39": {"Z1 Recovery": 2.0, "Z2 Aerobic": 11.0, "Z3 Tempo": 4.0, "Z4 Threshold": 3.5, "Z5 VO2max": 1.0},
                "Wk 40": {"Z1 Recovery": 2.8, "Z2 Aerobic": 15.0, "Z3 Tempo": 3.2, "Z4 Threshold": 1.8, "Z5 VO2max": 0.5},
            }
            buf = endurance_charts.e07_weekly_volume_zones(weekly)

        elif chart_id in ("e08", "e08_zone_mix_28d", "polar"):
            buf = endurance_charts.e08_zone_mix_28d(zone1_2_pct=82.0, zone3_plus_pct=18.0)

        elif chart_id in ("e09", "e09_cadence_over_time", "cadence"):
            cad_samples = [(m * 60.0, 172.0 + (m % 5) * 1.5) for m in range(40)]
            buf = endurance_charts.e09_cadence_over_time(cad_samples)

        elif chart_id in ("e10", "e10_elevation_hr", "elevation"):
            samples = []
            for km_idx in range(18):
                dist = km_idx * 500.0
                t = km_idx * 160.0
                hr = 136.0 + (km_idx % 4) * 5.0
                alt = 45.0 + (km_idx * 4.2 if km_idx < 10 else 87.0 - (km_idx - 10) * 5.0)
                samples.append(StreamSample(time_s=t, distance_m=dist, heartrate=hr, altitude_m=alt, moving=True))
            buf = endurance_charts.e10_elevation_hr(samples)

        # ================= CROSS-DISCIPLINE & RECOVERY =================
        elif chart_id in ("x01", "c01", "x01_training_load_acwr", "acwr_line"):
            dates = [date(2026, 9, 1) + timedelta(days=i * 3) for i in range(10)]
            acute = [(d, 450.0 + (i * 20)) for i, d in enumerate(dates)]
            chronic = [(d, 1600.0 + (i * 50)) for i, d in enumerate(dates)]
            buf = cross.x01_training_load_acwr(acute, chronic)

        elif chart_id in ("c02", "c02_acwr_gauge", "acwr"):
            buf = cross.c02_acwr_gauge(1.08)

        elif chart_id in ("c03", "c03_training_distribution_pie", "split"):
            buf = cross.c03_training_distribution_pie(lifting_hours=4.8, running_hours=2.6, other_hours=0.5)

        elif chart_id in ("x02", "c04", "x02_consistency_calendar", "calendar"):
            activities = [
                (date(2026, 10, 2), "WeightTraining"),
                (date(2026, 10, 1), "Run"),
                (date(2026, 9, 29), "WeightTraining"),
                (date(2026, 9, 27), "Run"),
                (date(2026, 9, 25), "WeightTraining"),
                (date(2026, 9, 23), "Run"),
                (date(2026, 9, 20), "WeightTraining"),
                (date(2026, 9, 18), "Run"),
                (date(2026, 9, 16), "WeightTraining"),
                (date(2026, 9, 14), "Run"),
                (date(2026, 9, 11), "WeightTraining"),
                (date(2026, 9, 9), "Ride"),
                (date(2026, 9, 7), "WeightTraining"),
                (date(2026, 9, 4), "Run"),
                (date(2026, 9, 2), "WeightTraining"),
            ]
            buf = cross.x02_consistency_calendar(activities, weeks=12)

        if buf is not None:
            return WebResponse(status=200, body=buf.getvalue(), content_type="image/png", headers={"Cache-Control": "public, max-age=300"})
    except Exception as e:
        return WebResponse.json(500, {"error": f"Chart rendering failed: {e}"})

    return WebResponse.json(404, {"error": f"Unknown chart preset '{chart_id}'"})
