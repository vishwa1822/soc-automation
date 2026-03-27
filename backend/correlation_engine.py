from sqlalchemy.orm import Session
import models


def get_user_sessions(db: Session, user_id: str):

    sessions = (
        db.query(models.LogEvent)
        .filter(models.LogEvent.user_id == user_id)
        .order_by(models.LogEvent.timestamp)
        .all()
    )

    timeline = []

    for event in sessions:
        timeline.append({
            "timestamp": event.timestamp,
            "event_type": event.event_type,
            "ip": event.ip_address,
            "status": event.login_status
        })

    return timeline