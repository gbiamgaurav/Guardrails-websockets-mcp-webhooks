"""
Webhook Server - Event-driven HTTP callback system

This server implements a webhook pattern where:
1. Clients register webhook URLs
2. Server sends HTTP POST events to registered webhooks
3. Server maintains activity logs
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl
import httpx
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Webhook Server", version="1.0")

# Data Models
class WebhookRegistration(BaseModel):
    """Webhook registration payload"""
    url: HttpUrl
    event_types: list[str]  # e.g., ["message", "user_joined", "user_left"]
    name: str


class Event(BaseModel):
    """Event to be sent to webhooks"""
    type: str
    data: dict
    timestamp: str | None = None


class ActivityLogger:
    """Logs all webhook activities"""
    
    def __init__(self, log_file="webhook_activities.json"):
        self.log_file = log_file
        self.events = []
        self.webhooks_triggered = defaultdict(int)
        self.load_activities()
    
    def load_activities(self):
        """Load existing activities from file"""
        if Path(self.log_file).exists():
            try:
                with open(self.log_file, "r") as f:
                    data = json.load(f)
                    self.events = data.get("events", [])
                    self.webhooks_triggered = defaultdict(int, data.get("webhooks_triggered", {}))
            except Exception as e:
                logger.error(f"Error loading activities: {e}")
    
    def save_activities(self):
        """Save activities to file"""
        try:
            with open(self.log_file, "w") as f:
                json.dump({
                    "events": self.events,
                    "webhooks_triggered": dict(self.webhooks_triggered)
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving activities: {e}")
    
    def log_event(self, event_type: str, data: dict):
        """Log an event"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        self.save_activities()
        return event
    
    def log_webhook_triggered(self, webhook_url: str):
        """Log webhook trigger"""
        self.webhooks_triggered[str(webhook_url)] += 1
        self.save_activities()


# Global instances
logger_instance = ActivityLogger()
registered_webhooks = {}  # {id: {url, event_types, name, registered_at}}
webhook_counter = 0


async def send_webhook(webhook_url: str, event: dict):
    """Send webhook event via HTTP POST (background task)"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                str(webhook_url),
                json=event,
                headers={"Content-Type": "application/json"}
            )
            logger_instance.log_webhook_triggered(webhook_url)
            logger.info(f"✓ Webhook sent to {webhook_url} - Status: {response.status_code}")
    except httpx.TimeoutException:
        logger.error(f"✗ Webhook timeout for {webhook_url}")
    except httpx.RequestError as e:
        logger.error(f"✗ Webhook error for {webhook_url}: {str(e)}")


@app.get("/")
async def root():
    """API documentation"""
    return {
        "name": "Webhook Server",
        "version": "1.0",
        "endpoints": {
            "GET /": "This documentation",
            "POST /webhooks/register": "Register a webhook",
            "GET /webhooks": "List all registered webhooks",
            "DELETE /webhooks/{webhook_id}": "Unregister a webhook",
            "POST /events": "Trigger an event (sends to all matching webhooks)",
            "GET /activities": "Get activity logs",
            "POST /test-event": "Send a test event to all webhooks"
        }
    }


@app.post("/webhooks/register")
async def register_webhook(registration: WebhookRegistration):
    """Register a new webhook endpoint"""
    global webhook_counter
    
    webhook_counter += 1
    webhook_id = f"webhook_{webhook_counter}"
    
    webhook_data = {
        "id": webhook_id,
        "url": str(registration.url),
        "name": registration.name,
        "event_types": registration.event_types,
        "registered_at": datetime.now().isoformat(),
        "trigger_count": 0
    }
    
    registered_webhooks[webhook_id] = webhook_data
    
    logger_instance.log_event("webhook_registered", {
        "webhook_id": webhook_id,
        "url": str(registration.url),
        "name": registration.name,
        "event_types": registration.event_types
    })
    
    logger.info(f"Webhook registered: {webhook_id} -> {registration.url}")
    
    return {
        "status": "registered",
        "webhook_id": webhook_id,
        "details": webhook_data
    }


@app.get("/webhooks")
async def list_webhooks():
    """List all registered webhooks"""
    return {
        "total": len(registered_webhooks),
        "webhooks": list(registered_webhooks.values())
    }


@app.delete("/webhooks/{webhook_id}")
async def unregister_webhook(webhook_id: str):
    """Unregister a webhook"""
    if webhook_id not in registered_webhooks:
        raise HTTPException(status_code=404, detail=f"Webhook {webhook_id} not found")
    
    webhook_url = registered_webhooks[webhook_id]["url"]
    del registered_webhooks[webhook_id]
    
    logger_instance.log_event("webhook_unregistered", {
        "webhook_id": webhook_id,
        "url": webhook_url
    })
    
    logger.info(f"Webhook unregistered: {webhook_id}")
    
    return {"status": "unregistered", "webhook_id": webhook_id}


@app.post("/events")
async def trigger_event(event: Event, background_tasks: BackgroundTasks):
    """
    Trigger an event - sends to all matching webhooks
    
    Event types: "message", "user_action", "system_alert", etc.
    """
    if not event.timestamp:
        event.timestamp = datetime.now().isoformat()
    
    event_dict = event.model_dump()
    
    # Log the event
    logger_instance.log_event(event.type, event.data)
    
    # Send to matching webhooks
    matching_webhooks = [
        w for w in registered_webhooks.values()
        if event.type in w["event_types"]
    ]
    
    logger.info(f"Event triggered: {event.type} -> {len(matching_webhooks)} webhooks")
    
    # Queue webhook deliveries as background tasks
    for webhook in matching_webhooks:
        background_tasks.add_task(send_webhook, webhook["url"], event_dict)
    
    return {
        "event_type": event.type,
        "webhooks_notified": len(matching_webhooks),
        "timestamp": event.timestamp
    }


@app.post("/test-event")
async def send_test_event(background_tasks: BackgroundTasks):
    """Send a test event to all registered webhooks"""
    test_event = {
        "type": "test",
        "data": {
            "message": "This is a test webhook event",
            "server": "Webhook Demo Server"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    # Send to all webhooks
    for webhook in registered_webhooks.values():
        background_tasks.add_task(send_webhook, webhook["url"], test_event)
    
    logger_instance.log_event("test_event_triggered", {
        "webhooks_notified": len(registered_webhooks)
    })
    
    return {
        "status": "test event queued",
        "webhooks": len(registered_webhooks),
        "timestamp": test_event["timestamp"]
    }


@app.get("/activities")
async def get_activities(limit: int = 50):
    """Get activity logs"""
    logger_instance.load_activities()
    
    return {
        "total_events": len(logger_instance.events),
        "total_webhook_triggers": sum(logger_instance.webhooks_triggered.values()),
        "recent_events": logger_instance.events[-limit:],
        "webhook_trigger_counts": dict(logger_instance.webhooks_triggered)
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "registered_webhooks": len(registered_webhooks),
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
