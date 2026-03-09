
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
from pathlib import Path
import os
from collections import defaultdict

# Activity Logger
class ActivityLogger:
    def __init__(self, log_file="activity.json"):
        self.log_file = log_file
        self.activities = []
        self.user_stats = defaultdict(lambda: {"join_count": 0, "message_count": 0, "typing_count": 0, "join_time": None, "last_activity": None})
        self.load_activities()
    
    def load_activities(self):
        """Load existing activities from file"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r") as f:
                    data = json.load(f)
                    self.activities = data.get("activities", [])
                    self.user_stats = defaultdict(lambda: {"join_count": 0, "message_count": 0, "typing_count": 0, "join_time": None, "last_activity": None}, data.get("user_stats", {}))
            except:
                pass
    
    def save_activities(self):
        """Save activities to file"""
        with open(self.log_file, "w") as f:
            json.dump({
                "activities": self.activities,
                "user_stats": dict(self.user_stats),
                "last_updated": datetime.now().isoformat()
            }, f, indent=2)
    
    def log_activity(self, username: str, event_type: str, details: str = ""):
        """Log user activity"""
        timestamp = datetime.now().isoformat()
        activity = {
            "timestamp": timestamp,
            "username": username,
            "event_type": event_type,
            "details": details
        }
        
        self.activities.append(activity)
        
        # Update user stats
        if event_type == "join":
            self.user_stats[username]["join_count"] += 1
            self.user_stats[username]["join_time"] = timestamp
        elif event_type == "message":
            self.user_stats[username]["message_count"] += 1
        elif event_type == "typing":
            self.user_stats[username]["typing_count"] += 1
        
        self.user_stats[username]["last_activity"] = timestamp
        self.save_activities()
        
        # Print to console
        print(f"📊 [{timestamp}] {event_type.upper()}: {username} - {details}")
    
    def get_stats(self):
        """Get activity statistics"""
        return {
            "total_activities": len(self.activities),
            "user_stats": dict(self.user_stats),
            "activity_log": self.activities[-100:]  # Last 100 activities
        }

activity_logger = ActivityLogger()

app = FastAPI(title="WebSocket Chat")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.users: dict[str, str] = {}  # socket_id -> username
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        socket_id = id(websocket)
        self.active_connections[str(socket_id)] = websocket
        return str(socket_id)
    
    def disconnect(self, socket_id: str):
        if socket_id in self.active_connections:
            del self.active_connections[socket_id]
        if socket_id in self.users:
            del self.users[socket_id]
    
    async def broadcast(self, message: dict, exclude_id: str = None):
        for socket_id, connection in self.active_connections.items():
            if exclude_id and socket_id == exclude_id:
                continue
            try:
                await connection.send_json(message)
            except:
                pass
    
    async def send_to(self, socket_id: str, message: dict):
        if socket_id in self.active_connections:
            try:
                await self.active_connections[socket_id].send_json(message)
            except:
                pass
    
    def set_username(self, socket_id: str, username: str):
        self.users[socket_id] = username
    
    def get_username(self, socket_id: str):
        return self.users.get(socket_id, "Anonymous")
    
    def get_online_users(self):
        return list(self.users.values())

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get():
    """Serve the chat UI"""
    html_path = Path(__file__).parent / "templates" / "index.html"
    if html_path.exists():
        return html_path.read_text()
    return "<h1>Chat UI not found</h1>"

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for chat"""
    socket_id = await manager.connect(websocket)
    print(f"✅ Client connected: {socket_id}")
    
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")
            
            # User joins
            if event_type == "join":
                username = data.get("username", "Anonymous")
                manager.set_username(socket_id, username)
                activity_logger.log_activity(username, "join", f"Joined chat (Socket: {socket_id})")
                
                await manager.broadcast({
                    "type": "userJoined",
                    "username": username,
                    "message": f"✅ {username} joined the chat",
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "users": manager.get_online_users()
                })
                print(f"{username} joined. Online: {len(manager.active_connections)}")
            
            # User sends message
            elif event_type == "message":
                username = manager.get_username(socket_id)
                message = data.get("message", "")
                activity_logger.log_activity(username, "message", f"Sent: {message[:50]}")
                
                await manager.broadcast({
                    "type": "message",
                    "username": username,
                    "message": message,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                print(f"{username}: {message}")
            
            # Typing indicator
            elif event_type == "typing":
                username = manager.get_username(socket_id)
                is_typing = data.get("isTyping", True)
                activity_logger.log_activity(username, "typing", f"Typing: {is_typing}")
                
                await manager.broadcast({
                    "type": "typing",
                    "username": username,
                    "isTyping": is_typing
                }, exclude_id=socket_id)
            
            # Private message
            elif event_type == "privateMessage":
                sender = manager.get_username(socket_id)
                recipient = data.get("recipient")
                message = data.get("message", "")
                
                # Find recipient socket_id by username
                for sid, uname in manager.users.items():
                    if uname == recipient:
                        await manager.send_to(sid, {
                            "type": "privateMessage",
                            "from": sender,
                            "message": message,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                        print(f"Private message from {sender} to {recipient}")
                        break
    
    except WebSocketDisconnect:
        username = manager.get_username(socket_id)
        manager.disconnect(socket_id)
        activity_logger.log_activity(username, "disconnect", f"Left chat (Socket: {socket_id})")
        
        await manager.broadcast({
            "type": "userLeft",
            "username": username,
            "message": f"👋 {username} left the chat",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "users": manager.get_online_users()
        })
        print(f"{username} disconnected. Online: {len(manager.active_connections)}")
    
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(socket_id)

@app.get("/health")
async def health():
    return {"status": "ok", "connections": len(manager.active_connections)}

@app.get("/stats")
async def get_stats():
    """Get user activity statistics"""
    stats = activity_logger.get_stats()
    stats["active_connections"] = len(manager.active_connections)
    stats["online_users"] = manager.get_online_users()
    return stats

@app.get("/admin", response_class=HTMLResponse)
async def admin_portal():
    """Serve the admin portal"""
    html_path = Path(__file__).parent / "templates" / "admin.html"
    if html_path.exists():
        return html_path.read_text()
    return "<h1>Admin Portal - HTML not found</h1>"

@app.get("/api/users/active")
async def get_active_users():
    """Get currently active/logged-in users"""
    return {
        "active_users": manager.get_online_users(),
        "active_count": len(manager.active_connections),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/users/all")
async def get_all_users():
    """Get all users with their stats"""
    all_users = []
    for username, stats in activity_logger.user_stats.items():
        is_online = username in manager.get_online_users()
        all_users.append({
            "username": username,
            "is_online": is_online,
            "join_count": stats["join_count"],
            "message_count": stats["message_count"],
            "typing_count": stats["typing_count"],
            "join_time": stats["join_time"],
            "last_activity": stats["last_activity"]
        })
    
    return {
        "total_users": len(all_users),
        "active_users": sum(1 for u in all_users if u["is_online"]),
        "inactive_users": sum(1 for u in all_users if not u["is_online"]),
        "users": all_users,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/users/history")
async def get_user_history(username: str = None):
    """Get login/logout history for users"""
    history = []
    for activity in activity_logger.activities:
        if username and activity["username"] != username:
            continue
        if activity["event_type"] in ["join", "disconnect"]:
            history.append(activity)
    
    return {
        "username": username,
        "history_count": len(history),
        "history": history,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

