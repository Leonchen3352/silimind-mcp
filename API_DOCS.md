# SiliMind API Documentation

Base URL: `https://agent.silimind.net/api`

## Authentication

All API requests require a Bearer token obtained via login.

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "you@company.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "tokenType": "bearer",
  "role": "sales"
}
```

Use the token in all subsequent requests:
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## Core Resources

### Contacts (客户)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/contacts` | List contacts (paginated, searchable) |
| POST | `/contacts` | Create a contact |
| GET | `/contacts/{id}` | Get contact detail |
| PUT | `/contacts/{id}` | Update a contact |
| DELETE | `/contacts/{id}` | Delete a contact |

**Example — search contacts:**
```http
GET /api/contacts?q=acme&page=1&page_size=20
Authorization: Bearer <your-token>
```

**Example — create a contact:**
```http
POST /api/contacts
Content-Type: application/json
Authorization: Bearer <your-token>

{
  "name": "John Smith",
  "email": "john@acme.com",
  "company": "Acme Corp",
  "phone": "+86 138 0000 0000"
}
```

### Companies (公司)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/companies` | List companies |
| POST | `/companies` | Create a company |
| GET | `/companies/{id}` | Get company detail |
| PUT | `/companies/{id}` | Update |
| DELETE | `/companies/{id}` | Delete |

### Deals (商机)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/deals` | List deals |
| POST | `/deals` | Create a deal |
| GET | `/deals/{id}` | Get deal detail |
| PUT | `/deals/{id}` | Update deal (stage, amount, etc.) |
| DELETE | `/deals/{id}` | Delete |

**Example — list your pipeline:**
```http
GET /api/deals?stage=follow_up
Authorization: Bearer <your-token>
```

### Tasks (任务)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tasks` | List tasks |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update (complete, reschedule) |
| DELETE | `/tasks/{id}` | Delete |

### Interactions (沟通记录)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/interactions` | List interaction records |
| POST | `/interactions` | Log an interaction (call, email, meeting) |

### Visits (拜访)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/visits` | List visits |
| POST | `/visits` | Schedule a visit |

---

## AI Features

### AI Suggestions
```http
GET /api/ai/suggestions
Authorization: Bearer <your-token>
```

### AI Chat (agent)
```http
POST /api/agent-chat/{agent_id}/message
Content-Type: application/json
Authorization: Bearer <your-token>

{"content": "帮我总结这个客户最近的沟通"}
```
> Streaming SSE response.

---

## Knowledge Base (知识库)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/knowledge/docs` | List documents |
| POST | `/knowledge/docs/upload` | Upload document (PDF/DOCX/MD) |
| POST | `/knowledge/search` | Semantic search |

**Example — semantic search:**
```http
POST /api/knowledge/search
Content-Type: application/json
Authorization: Bearer <your-token>

{"query": "产品规格参数", "top_k": 5}
```

---

## Response Conventions

- Success: `200` / `201` (created)
- Auth failure: `401` — token expired or invalid
- Permission denied: `403`
- Not found: `404`
- Validation error: `422` with field details
- Rate limit: `429`

## Pagination

List endpoints use `page` and `page_size` query parameters (default: 20, max: 100).

## Rate Limits

- Per-token rate limiting applies
- Exceeding limits returns `429` with `Retry-After` header

---

## Support

- Docs: https://www.silimind.net
- MCP integration: https://github.com/Leonchen3352/silimind-mcp
- Contact: support@silimind.net
