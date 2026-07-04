import json
from datetime import UTC, date, datetime, timedelta
from uuid import UUID

from opentelemetry import trace
from redis import Redis
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert

from app.core.config import settings
from app.domain.dashboard.entities import DashboardSnapshot
from app.domain.identity.entities import User
from app.domain.mission.entities import Mission
from app.domain.roadmap.entities import Roadmap, RoadmapWeek
from app.domain.reviews.entities import Review
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.queue.celery_app import celery_app

tracer = trace.get_tracer(__name__)
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
STREAM = "ascend.domain.events"
GROUP = "dashboard-projector"
CONSUMER = "worker-1"


def _ensure_group() -> None:
    try:
        redis_client.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
    except Exception as exc:
        if "BUSYGROUP" not in str(exc):
            raise


@celery_app.task(name="queue.consume_domain_events")
def consume_domain_events() -> int:
    _ensure_group()
    processed = 0
    with tracer.start_as_current_span("redis_stream.consume_domain_events"):
        response = redis_client.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=25, block=1000)
        for _, messages in response:
            for message_id, fields in messages:
                event_type = fields.get("event_type")
                payload = json.loads(fields.get("payload", "{}"))
                if event_type == "mission.completed":
                    _project_mission_completed(payload)
                redis_client.xack(STREAM, GROUP, message_id)
                processed += 1
    return processed


def _project_mission_completed(payload: dict) -> None:
    user_id = UUID(payload["user_id"])
    with SessionLocal() as db:
        completed_count = db.scalar(select(func.count(Mission.id)).join(RoadmapWeek).join(Roadmap).where(Roadmap.user_id == user_id, Mission.status == "completed"))
        if completed_count is None:
            completed_count = 0
        snapshot_payload = {
            "streak": int(completed_count),
            "completed_missions": int(completed_count),
            "last_completed_day": payload.get("day_number"),
            "last_event_at": datetime.now(UTC).isoformat(),
            "skill_focus": ["Azure Architecture", "AI Orchestration", "Automation"],
            "review_due": "Sunday",
        }
        stmt = insert(DashboardSnapshot).values(user_id=user_id, payload=snapshot_payload).on_conflict_do_update(index_elements=["user_id"], set_={"payload": snapshot_payload, "updated_at": datetime.now(UTC)})
        db.execute(stmt)
        db.commit()


@celery_app.task(name="reviews.generate_weekly_reviews")
def generate_weekly_reviews() -> dict:
    with tracer.start_as_current_span("reviews.generate_weekly"):
        return _generate_reviews("weekly", date.today() - timedelta(days=6), date.today())


@celery_app.task(name="reviews.generate_monthly_reviews")
def generate_monthly_reviews() -> dict:
    with tracer.start_as_current_span("reviews.generate_monthly"):
        today = date.today()
        return _generate_reviews("monthly", today.replace(day=1), today)


def _generate_reviews(review_type: str, period_start: date, period_end: date) -> dict:
    created = 0
    with SessionLocal() as db:
        users = db.scalars(select(User)).all()
        for user in users:
            completed = db.scalar(select(func.count(Mission.id)).join(RoadmapWeek).join(Roadmap).where(Roadmap.user_id == user.id, Mission.status == "completed")) or 0
            metrics = {"completed_missions": int(completed), "period_start": period_start.isoformat(), "period_end": period_end.isoformat()}
            db.add(
                Review(
                    user_id=user.id,
                    review_type=review_type,
                    period_start=period_start,
                    period_end=period_end,
                    metrics_json=metrics,
                    ai_feedback=f"{review_type.title()} review generated from mission completion and execution consistency.",
                    improvement_plan="Keep evidence concrete, complete the next unlocked mission, and review weak interview topics before the next session.",
                )
            )
            created += 1
        db.commit()
    return {"status": "created", "review_type": review_type, "count": created}


@celery_app.task(name="notifications.enqueue_morning_reminders")
def enqueue_morning_reminders() -> dict:
    with tracer.start_as_current_span("notifications.enqueue_morning_reminders"):
        return {"status": "scheduled", "channel": "browser", "date": date.today().isoformat()}
