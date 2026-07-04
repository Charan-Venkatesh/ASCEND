from celery import Celery
from celery.schedules import crontab
from opentelemetry.instrumentation.celery import CeleryInstrumentor

from app.core.config import settings
from app.core.logging import configure_observability

configure_observability()
CeleryInstrumentor().instrument()

celery_app = Celery("ascend_os", broker=settings.redis_url, backend=settings.redis_url, include=["app.infrastructure.queue.tasks"])
celery_app.conf.timezone = "Asia/Kolkata"
celery_app.conf.beat_schedule = {
    "consume-domain-events-every-minute": {"task": "queue.consume_domain_events", "schedule": 60.0},
    "weekly-review-sunday-evening": {"task": "reviews.generate_weekly_reviews", "schedule": crontab(hour=19, minute=0, day_of_week="sun")},
    "monthly-review-first-day": {"task": "reviews.generate_monthly_reviews", "schedule": crontab(hour=19, minute=30, day_of_month="1")},
    "morning-reminders": {"task": "notifications.enqueue_morning_reminders", "schedule": crontab(hour=8, minute=30)},
}
