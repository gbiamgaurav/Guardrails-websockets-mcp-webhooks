"""
Webhook Client Examples

Shows how to:
1. Run a simple HTTP server to receive webhooks
2. Register with the webhook server
3. Receive and process webhook events
"""

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import httpx
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Client configuration
WEBHOOK_SERVER_URL = "http://localhost:8000"
CLIENT_PORT = 8001
CLIENT_HOST = "0.0.0.0"

# Store events received
received_events = []


async def register_webhook(client_app_url: str, event_types: list[str], name: str):
    """Register this client's webhook URL with the server"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{WEBHOOK_SERVER_URL}/webhooks/register",
                json={
                    "url": client_app_url,
                    "event_types": event_types,
                    "name": name
                }
            )
            result = response.json()
            logger.info(f"✓ Webhook registered: {result['webhook_id']}")
            return result["webhook_id"]
    except Exception as e:
        logger.error(f"✗ Failed to register webhook: {e}")
        return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    webhook_id = await register_webhook(
        f"http://localhost:{CLIENT_PORT}/webhook",
        event_types=["message", "test", "user_action"],
        name=f"Client on port {CLIENT_PORT}"
    )
    yield
    # Shutdown - could unregister here


app = FastAPI(title=f"Webhook Client - Port {CLIENT_PORT}", lifespan=lifespan)


@app.post("/webhook")
async def receive_webhook(request: Request):
    """Endpoint that receives webhook events"""
    try:
        payload = await request.json()
        
        # Log the received event
        event_log = {
            "received_at": datetime.now().isoformat(),
            "event_type": payload.get("type"),
            "data": payload.get("data"),
            "server_timestamp": payload.get("timestamp")
        }
        received_events.append(event_log)
        
        event_type = payload.get("type", "unknown")
        logger.info(f"📨 Received webhook event: {event_type}")
        logger.info(f"   Data: {json.dumps(payload.get('data', {}), indent=2)}")
        
        return {
            "status": "received",
            "event_type": event_type,
            "received_at": event_log["received_at"]
        }
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}, 400


@app.get("/")
async def root():
    """Client information"""
    return {
        "name": f"Webhook Client (Port {CLIENT_PORT})",
        "webhook_server": WEBHOOK_SERVER_URL,
        "webhook_endpoint": f"http://localhost:{CLIENT_PORT}/webhook",
        "endpoints": {
            "GET /": "This documentation",
            "POST /webhook": "Receives webhook events",
            "GET /events": "View received events",
            "GET /health": "Health check"
        }
    }


@app.get("/events")
async def get_events(limit: int = 20):
    """View received webhook events"""
    return {
        "total_received": len(received_events),
        "recent_events": received_events[-limit:]
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "ready_to_receive_webhooks": True,
        "events_received": len(received_events)
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting Webhook Client on port {CLIENT_PORT}")
    logger.info(f"Webhook endpoint: http://localhost:{CLIENT_PORT}/webhook")
    uvicorn.run(app, host=CLIENT_HOST, port=CLIENT_PORT)
