# FastAPI WebSocket Chat Application

A modern, real-time chat application built with **FastAPI** and **WebSockets**, featuring a beautiful HTML-based UI.

## 📁 Project Structure

```
Websockets/
├── main.py                 # FastAPI server with WebSocket support
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Chat UI (HTML + CSS + JavaScript)
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### 3. Open in Browser
Visit `http://localhost:8000` and start chatting!

## ✨ Features

- 🔄 **Real-time bidirectional communication** via WebSockets
- 📝 **Live message broadcasting** - All users see messages instantly
- 👥 **Online users list** - See who's currently connected
- ✍️ **Typing indicators** - Know when others are typing
- 💬 **Private messaging** - Send direct messages to specific users
- 🎨 **Beautiful responsive UI** - Works on desktop and mobile
- 📱 **Mobile friendly** - Responsive design for all screen sizes

## 🔌 WebSocket Events

### Client → Server

**Join Chat**
```javascript
ws.send(JSON.stringify({
    type: 'join',
    username: 'John'
}))
```

**Send Message**
```javascript
ws.send(JSON.stringify({
    type: 'message',
    message: 'Hello everyone!'
}))
```

**Typing Indicator**
```javascript
ws.send(JSON.stringify({
    type: 'typing',
    isTyping: true
}))
```

**Private Message**
```javascript
ws.send(JSON.stringify({
    type: 'privateMessage',
    recipient: 'Jane',
    message: 'Hi Jane!'
}))
```

### Server → Client

**User Joined**
```python
{
    "type": "userJoined",
    "username": "John",
    "message": "✅ John joined the chat",
    "timestamp": "14:30:25",
    "users": ["John", "Jane", "Bob"]
}
```

**Message Broadcast**
```python
{
    "type": "message",
    "username": "John",
    "message": "Hello everyone!",
    "timestamp": "14:30:25"
}
```

**User Left**
```python
{
    "type": "userLeft",
    "username": "Jane",
    "message": "👋 Jane left the chat",
    "timestamp": "14:31:10",
    "users": ["John", "Bob"]
}
```

**Typing Indicator**
```python
{
    "type": "typing",
    "username": "Bob",
    "isTyping": true
}
```

## 🏗️ Architecture

### Backend (FastAPI)
- **ConnectionManager**: Manages all active WebSocket connections
- **Event Handler**: Routes incoming messages to appropriate handlers
- **Broadcasting**: Sends messages to all connected clients

### Frontend (HTML/JavaScript)
- Uses native **WebSocket API** (no external libraries needed!)
- Real-time DOM updates
- Auto-scrolling to latest messages
- Connection status indicator

## 📊 How It Works

1. **User connects**: Browser opens WebSocket connection to `/ws/chat`
2. **User joins**: Sends username via WebSocket
3. **Server broadcasts**: Notifies all users of new member
4. **User sends message**: Message sent through WebSocket
5. **Server broadcasts**: All clients receive message instantly
6. **User leaves**: Browser closes connection
7. **Server notifies**: All users see departure message

## 🔒 Connection Management

```python
# Connection Manager Features:
- Tracks active connections with unique socket IDs
- Stores username for each connection
- Broadcasts to all or specific clients
- Handles disconnections gracefully
- Prevents orphaned connections
```

## 📈 Scaling Tips

For production use with many concurrent users:

1. **Use session manager**: Store connections in database
2. **Add Redis**: For cross-server broadcasting
3. **Load balancing**: Use Nginx with sticky sessions
4. **Connection pooling**: Limit concurrent connections
5. **Message queue**: Use RabbitMQ or Kafka for reliability

## 🎯 WebSocket vs HTTP

| Feature | WebSocket | HTTP |
|---------|-----------|------|
| Connection | Persistent | Stateless |
| Latency | Ultra-low (<100ms) | Higher |
| Bandwidth | Lower (less overhead) | Higher headers |
| Direction | Bidirectional | Request-Response |
| Real-time | ✅ Yes | ❌ No (polling) |

## 🧪 Testing the Chat

### Multiple Tabs
1. Open `http://localhost:8000` in multiple browser tabs
2. Use different usernames in each tab
3. Send messages and watch them appear in real-time

### Network Tab
View WebSocket frames in DevTools:
1. Open Chrome DevTools
2. Go to Network tab
3. Filter by "WS"
4. Click the WebSocket connection
5. View frames being sent/received

## 🛠️ Development

### Hot Reload
The server runs with `--reload` flag, so changes to `main.py` restart automatically.

### Debug Mode
To see all WebSocket traffic:
```python
# In main.py, enable debug logging:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Example: Adding a Feature

### Add user count on messages

**Backend (main.py)**:
```python
elif event_type == "message":
    username = manager.get_username(socket_id)
    message = data.get("message", "")
    
    await manager.broadcast({
        "type": "message",
        "username": username,
        "message": message,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "userCount": len(manager.active_connections)  # Add this
    })
```

**Frontend (index.html)**:
```javascript
function addMessage(username, message, timestamp, userCount) {
    // ... existing code ...
    meta.textContent = `${username} • ${timestamp} (${userCount} online)`;
}
```

## 🐛 Troubleshooting

**"Connection refused"**
- Make sure server is running: `uvicorn main:app --reload`
- Check port 8000 is not in use: `lsof -i :8000`

**"WebSocket closed"**
- Server might have crashed, check console
- Connection timeout after 60 seconds of no activity

**"CORS error"**
- Should not happen, CORS middleware is enabled
- Check browser console for exact error

## 📚 Further Reading

- [FastAPI WebSocket Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [WebSocket Protocol (RFC 6455)](https://tools.ietf.org/html/rfc6455)

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using FastAPI and WebSockets**
