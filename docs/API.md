# Devotional Journal API Documentation

**Base URL:** `/api/v1/`

**Authentication:** JWT Bearer Token (obtained via magic link flow)

---

## Authentication

### Request Magic Link
```
POST /auth/magic-link/request/
```

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:** `200 OK`
```json
{
  "message": "Magic link sent to your email"
}
```

### Verify Magic Link
```
POST /auth/magic-link/verify/
```

**Request Body:**
```json
{
  "token": "abc123..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "display_name": "John",
    "language_preference": "en"
  }
}
```

### Refresh Token
```
POST /auth/refresh/
```

**Request Body:**
```json
{
  "refresh_token": "eyJ..."
}
```

### Logout
```
POST /auth/logout/
```

---

## User Profile

### Get Current User
```
GET /me/
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "display_name": "John",
  "language_preference": "en",
  "timezone": "America/Chicago",
  "created_at": "2026-03-31T00:00:00Z"
}
```

### Update Profile
```
PATCH /me/
```

**Request Body:**
```json
{
  "display_name": "John Doe",
  "language_preference": "bilingual",
  "timezone": "America/New_York"
}
```

### Delete Account
```
DELETE /me/
```

### Get Streak Info
```
GET /me/streak/
```

**Response:**
```json
{
  "current_streak": 7,
  "longest_streak": 14,
  "last_entry_date": "2026-03-30",
  "total_entries": 42
}
```

---

## Bible Text

### List Translations
```
GET /bible/translations/
```

**Response:**
```json
[
  {
    "code": "KJV",
    "name": "King James Version",
    "language": "en",
    "is_public_domain": true
  }
]
```

### Read Passage
```
GET /bible/read/?translation=KJV&book=PSA&chapter=23&verse_start=1&verse_end=6
```

**Response:**
```json
{
  "reference": "Psalm 23:1-6",
  "translation": "KJV",
  "verses": [
    {
      "verse": 1,
      "text": "The Lord is my shepherd; I shall not want."
    },
    ...
  ]
}
```

### Search
```
GET /bible/search/?translation=KJV&q=shepherd
```

---

## Reading Plans

### List Plans
```
GET /plans/?category=faith&language=en
```

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": "uuid",
      "title": "30 Days in Psalms",
      "description": "A month-long journey...",
      "duration_days": 30,
      "category": "faith",
      "is_premium": false
    }
  ]
}
```

### Get Plan Detail
```
GET /plans/{id}/
```

### Enroll in Plan
```
POST /plans/{id}/enroll/
```

### Get Enrolled Plans
```
GET /plans/enrolled/
```

### Get Today's Reading
```
GET /plans/enrolled/{enrollment_id}/today/
```

**Response:**
```json
{
  "day_number": 7,
  "theme": "The Lord is My Shepherd",
  "passages": [
    {
      "reference": "Psalm 23:1-6",
      "verses": [...]
    }
  ],
  "reflection_prompts": [
    "What area of your life needs God's shepherding?",
    "When have you experienced God's provision?",
    "How can you rest in God's care today?"
  ]
}
```

### Advance to Next Day
```
POST /plans/enrolled/{enrollment_id}/advance/
```

---

## Journal

### List Entries
```
GET /journal/?date_from=2026-03-01&date_to=2026-03-31
```

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": "uuid",
      "date": "2026-03-30",
      "mood_tag": "grateful",
      "preview": "Today's reading reminded me...",
      "created_at": "2026-03-30T06:30:00Z"
    }
  ]
}
```

### Create Entry
```
POST /journal/
```

**Request Body:**
```json
{
  "date": "2026-03-31",
  "content": "My reflection on today's reading...",
  "mood_tag": "peaceful",
  "plan_enrollment_id": "uuid",
  "plan_day_id": "uuid"
}
```

### Get Entry
```
GET /journal/{id}/
```

**Response:**
```json
{
  "id": "uuid",
  "date": "2026-03-30",
  "content": "Full decrypted journal content...",
  "mood_tag": "grateful",
  "reflection_prompts_used": ["..."],
  "plan_enrollment": {...},
  "created_at": "2026-03-30T06:30:00Z",
  "updated_at": "2026-03-30T06:30:00Z"
}
```

### Update Entry
```
PATCH /journal/{id}/
```

### Delete Entry
```
DELETE /journal/{id}/
```

### Export Entries
```
GET /journal/export/?format=json
```

---

## Reflection Prompts

### Generate Prompts
```
POST /prompts/generate/
```

**Request Body:**
```json
{
  "passage": "The Lord is my shepherd; I shall not want...",
  "reference": "Psalm 23:1-6",
  "language": "en",
  "context": "fatherhood"
}
```

**Response:**
```json
{
  "prompts": [
    "What area of your life needs God's shepherding right now?",
    "How does this passage speak to your role as a father?",
    "What does it mean to 'not want' in your current season?"
  ]
}
```

---

## Groups (Phase 2)

### List My Groups
```
GET /groups/
```

### Create Group
```
POST /groups/
```

**Request Body:**
```json
{
  "name": "Men's Bible Study",
  "description": "Weekly study group",
  "max_members": 12
}
```

### Get Group Detail
```
GET /groups/{id}/
```

### Join Group
```
POST /groups/{id}/join/
```

**Request Body:**
```json
{
  "invite_code": "ABC123XY"
}
```

### Leave Group
```
DELETE /groups/{id}/leave/
```

### Get Engagement (Leaders Only)
```
GET /groups/{id}/engagement/
```

**Response:**
```json
[
  {
    "date": "2026-03-30",
    "total_members": 12,
    "members_active_today": 8,
    "avg_streak": 5.2,
    "plan_completion_pct": 67.5
  }
]
```

### Set Group Plan (Leaders Only)
```
POST /groups/{id}/set-plan/
```

**Request Body:**
```json
{
  "plan_id": "uuid"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

**Common Status Codes:**
- `400` - Bad Request (validation error)
- `401` - Unauthorized (missing/invalid token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error

---

## Rate Limits

- **Authentication:** 5 requests/minute per IP
- **LLM Prompts:** 10 requests/minute per user
- **General API:** 100 requests/minute per user
