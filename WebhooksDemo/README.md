# Webhook Demo - Event-Driven HTTP Callbacks

A practical implementation of the **Webhook pattern** demonstrating how to build event-driven systems using HTTP callbacks. Perfect for understanding asynchronous, decoupled communication between services.

---

## 📚 What is a Webhook?

A **webhook** is an automated HTTP callback mechanism that allows a server to send real-time data to registered client URLs when specific events occur.

**Simple Example:**
```
Event happens on Server → Server sends HTTP POST → Client receives notification
```

---

## 🚀 How It Works

### 1. **Registration Phase**
Client registers its webhook URL with the server:
```bash
POST /webhooks/register
{
  "url": "https://client.example.com/webhook",
  "event_types": ["message", "user_joined"],
  "name": "My Client"
}
```

### 2. **Event Trigger**
Something happens on the server:
```bash
POST /events
{
  "type": "message",
  "data": {"content": "Hello world"}
}
```

### 3. **Webhook Delivery**
Server sends HTTP POST to all registered webhooks:
```bash
POST https://client.example.com/webhook
{
  "type": "message",
  "data": {"content": "Hello world"},
  "timestamp": "2026-03-09T15:30:00"
}
```

### 4. **Acknowledgment**
Client receives and processes the event.

---

## 📊 WebSockets vs Webhooks

| Aspect | WebSockets | Webhooks |
|--------|-----------|----------|
| **Connection Type** | Persistent TCP connection | HTTP POST requests (stateless) |
| **Initiation** | Client initiates connection | Server initiates POST |
| **Direction** | Bidirectional (both ways) | Unidirectional (server → client) |
| **Real-time** | ✅ Instant delivery (<100ms) | ☑️ Near-instant, depends on HTTP |
| **Persistent Connection** | ✅ Yes (always connected) | ❌ No (new request each time) |
| **Overhead** | Low (after handshake) | Higher (HTTP overhead per request) |
| **Firewall Friendly** | ❌ Requires port opening | ✅ Standard HTTP ports (80, 443) |
| **Scalability** | Server needs many connections | More server-scalable |
| **Use Case** | Real-time chat, live updates | Event notifications, integrations |
| **Client Availability** | Client must be online | Can handle offline clients (with retries) |
| **Data Flow Example** | User types → broadcast instantly | Payment processed → notify merchant |

---

## 🔍 Detailed Comparison

### WebSockets
**Best for:** Real-time bidirectional communication
- Chat applications (user types, others see immediately)
- Live dashboards/notifications
- Multiplayer games
- Stock tickers
- Collaborative editing

```
Client ↔️↔️↔️ Server (persistent connection)
```

**Pros:**
- Very low latency
- Efficient bandwidth usage
- True bidirectional communication
- Great user experience for interactive apps

**Cons:**
- Not firewall friendly (requires special port config)
- More server resources (persistent connections)
- Requires client to be online

---

### Webhooks
**Best for:** Event-driven, decoupled systems
- GitHub → send push notifications to deployment service
- Payment processor → notify merchant of successful payment
- Form submission → trigger workflows
- Monitoring alert → notify administrators
- CMS → update external indices

```
Server → HTTP POST → Client (on-demand connection)
```

**Pros:**
- Works over standard HTTP (port 80/443)
- Firewall/NAT friendly
- Server-scalable (no persistent connections)
- Can implement retries and queuing
- Works with offline clients (if backed by queues)
- Decoupled systems (parties don't need live connection)

**Cons:**
- Slightly higher latency than WebSockets
- Client must expose HTTP endpoint
- Requires reliable delivery mechanism
- Testing is harder (needs callback URL)

---

## 💡 Real-World Examples

### Scenario 1: GitHub Push Notification
```
Developer pushes code to GitHub
      ↓
GitHub webhook triggers
      ↓
HTTP POST to deployment server
      ↓
Deployment service receives → starts build
```

**Why Webhook?**
- GitHub and deployment service are decoupled
- Deployment service can be offline initially
- Multiple services can receive events (GitHub only makes HTTP calls)
- Standard HTTP makes it firewall-friendly

### Scenario 2: Real-Time Chat
```
User A types a message
      ↓
WebSocket connection active
      ↓
Server receives and broadcasts instantly to all connected users
      ↓
Users B, C, D see message immediately
```

**Why WebSocket?**
- Users need instant feedback (<100ms)
- Many users connected simultaneously
- Bidirectional: users can send and receive
- Persistent connection is efficient

---

## 🛠️ Project Structure

```
WebhooksDemo/
├── main.py              # Webhook server
├── client.py            # Example webhook client
├── requirements.txt     # Dependencies
└── README.md            # This file
```

### main.py (Webhook Server)
- Manages webhook registrations
- Accepts event triggers
- Sends HTTP POST to registered webhooks
- Logs all activities

**Key Endpoints:**
- `POST /webhooks/register` - Register client webhook
- `POST /events` - Trigger an event
- `GET /webhooks` - List registered webhooks
- `DELETE /webhooks/{webhook_id}` - Unregister
- `GET /activities` - View logs
- `POST /test-event` - Send test event

### client.py (Webhook Client)
- Example HTTP server that receives webhooks
- Auto-registers with webhook server on startup
- Logs received events
- Ready to be copied and modified

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Webhook Server
```bash
python main.py
# or
uvicorn main:app --reload --port 8000
```

Server runs at: `http://localhost:8000`

### 3. Start a Webhook Client (new terminal)
```bash
python client.py
# or
uvicorn client:app --reload --port 8001
```

Client runs at: `http://localhost:8001`

### 4. Test the System

**Check server endpoints:**
```bash
curl http://localhost:8000/
curl http://localhost:8000/webhooks
```

**Send a test event:**
```bash
curl -X POST http://localhost:8000/test-event
```

**Send a custom event:**
```bash
curl -X POST http://localhost:8000/events \
  -H "Content-Type: application/json" \
  -d '{
    "type": "user_action",
    "data": {
      "user_id": "user123",
      "action": "purchased",
      "amount": 99.99
    }
  }'
```

**View activities:**
```bash
curl http://localhost:8000/activities | jq
```

**View received events on client:**
```bash
curl http://localhost:8001/events | jq
```

---

## 📝 Testing Workflow

### Test 1: Basic Registration
```bash
# Terminal 1: Start server
python main.py

# Terminal 2: Start client  
python client.py

# Terminal 3: Check registration
curl http://localhost:8000/webhooks | jq
```

Expected: Client should appear in list

### Test 2: Receive Webhook Event
```bash
# From Terminal 3, send test event
curl -X POST http://localhost:8000/test-event

# Check client received it
curl http://localhost:8001/events | jq
```

Expected: Event should appear in client's events

### Test 3: Multiple Clients
```bash
# Terminal 2: First client
python client.py

# Terminal 4: Second client (different port)  
PORT=8002 python client.py

# Terminal 3: Send event
curl -X POST http://localhost:8000/test-event

# Check both clients received
curl http://localhost:8001/events | jq
curl http://localhost:8002/events | jq
```

Expected: Both clients receive the same event

---

## 🔄 Event-Driven Architecture Pattern

This demo implements the classic **Event-Driven Architecture**:

```
┌─────────────────────────────────────────────────────┐
│          Webhook Server (Event Hub)                 │
│  ┌─────────────────────────────────────────────┐   │
│  │  - Listen for events                        │   │
│  │  - Route to interested subscribers          │   │
│  │  - Send HTTP callbacks                      │   │
│  └─────────────────────────────────────────────┘   │
└─────────┬────────────────────┬────────────────────┬─┘
          │                    │                    │
       HTTP POST            HTTP POST            HTTP POST
          │                    │                    │
    ┌─────▼──┐          ┌──────▼──┐         ┌──────▼──┐
    │Client 1 │          │ Client 2 │         │Client 3 │
    │(webhook)│          │(webhook) │         │(webhook)│
    └────────┘          └─────────┘         └────────┘
```

**Benefits:**
- **Decoupling**: Clients don't know about each other
- **Scalability**: Add new clients without changing server
- **Flexibility**: Different event types for different clients
- **Reliability**: Can add retry logic, queuing, deduplication

---

## 🔌 Webhook Reliability Patterns

### Pattern 1: Simple Delivery
Server sends once. Client handles failures.
```python
POST /webhook
# If fails, client responsible for retry
```

### Pattern 2: Retry with Exponential Backoff
Server retries failed deliveries:
```
Attempt 1 → fail → wait 1s
Attempt 2 → fail → wait 2s  
Attempt 3 → fail → wait 4s
Attempt 4 → fail → give up
```

### Pattern 3: Webhook Queue
Decouple event trigger from delivery:
```
Event → Queue → Background worker → Send webhooks
```

### Pattern 4: Signed Webhooks
Server signs request, client verifies authenticity:
```
X-Signature: sha256=abcd1234...
```

---

## 📚 Extending the Demo

### Try This:

1. **Add event filtering** - Client only receives specific event types
2. **Implement retries** - Let server retry failed webhook deliveries
3. **Add webhooks signing** - Sign requests for security
4. **Webhook events database** - Store all events with timestamps
5. **Webhook UI dashboard** - Web interface to view registrations
6. **Backpressure handling** - Queue events if clients are slow
7. **Webhook templates** - Different event schemas

---

## 🎓 Learning Path

1. **Understand the flow**: Follow the test workflows above
2. **Modify the server**: Add custom event types
3. **Extend the client**: Handle different event types differently
4. **Add persistence**: Store webhooks in a database
5. **Implement retries**: Add retry logic to deliveries
6. **Combine with other demos**: Send webhooks from WebsocketsDemo Chat!

---

## 🔗 Webhook vs WebSocket Use Cases

### Use Webhooks When:
- ✅ Clients are decoupled (don't need to know about each other)
- ✅ Firewall compatibility is important
- ✅ Clients might be offline initially
- ✅ You want to scale to thousands of clients
- ✅ Events are infrequent
- ✅ HTTP endpoints are readily available

**Examples:** GitHub notifications, payment confirmations, form submissions, monitoring alerts

### Use WebSockets When:
- ✅ Real-time interaction is needed (<100ms latency)
- ✅ Bidirectional communication required
- ✅ Clients need to stay connected
- ✅ Frequent updates (many per second)
- ✅ User experience matters most
- ✅ Game state synchronization

**Examples:** Chat apps, live dashboards, collaborative tools, multiplayer games

---

## 🚀 Resources

- [Standard Webhooks Spec](https://www.standardwebhooks.io/)
- [GitHub Webhooks](https://docs.github.com/webhooks)
- [Stripe Webhooks](https://stripe.com/docs/webhooks)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [HTTP Request Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

---

## 📝 Notes for Learners

- Webhooks are simpler than WebSockets for one-way notifications
- Real-world systems often use both patterns together
- Reliability and retry logic are critical in production
- Always secure webhooks with authentication
- Consider webhook ordering - events might arrive out of sequence

---

**Ready to explore event-driven architecture? Try adding features above!** 🎉
