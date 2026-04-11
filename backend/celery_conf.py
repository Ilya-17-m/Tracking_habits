from celery import Celery


celery_app = Celery(
    'app',
    broker="redis://localhost:6379/0",
    backend="redis://localhost:3679/",
)

celery_app.conf.beat_schedule = {
    "chack-habits-every-minute": {
        "task": "celery_tasks.check_status_habit",
        "schedule": 60.0,
    }
}