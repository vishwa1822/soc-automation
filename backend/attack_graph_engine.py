from sqlalchemy.orm import Session
import models

def generate_attack_graph(db: Session):

    logs = db.query(models.LogEvent).all()

    nodes = []
    edges = []

    for log in logs:

        user_node = f"user:{log.user_id}"
        ip_node = f"ip:{log.ip_address}"
        event_node = f"event:{log.event_type}"
        resource_node = f"resource:{log.resource_accessed}"

        nodes.extend([
            {"id": user_node, "type": "user"},
            {"id": ip_node, "type": "ip"},
            {"id": event_node, "type": "event"},
            {"id": resource_node, "type": "resource"}
        ])

        edges.extend([
            {"source": ip_node, "target": user_node},
            {"source": user_node, "target": event_node},
            {"source": event_node, "target": resource_node}
        ])

    return {
        "nodes": nodes,
        "edges": edges
    }