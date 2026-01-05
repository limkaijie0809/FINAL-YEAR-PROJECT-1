# API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication

All authenticated endpoints require a valid session cookie. The session is created after successful login.

---

## Endpoints

### 1. Health Check

**GET** `/`

Check if the API is running.

**Response:**
```json
{
  "message": "Phishing Awareness Simulator API is running!"
}
```

---

### 2. User Registration

**POST** `/api/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "string (required)",
  "email": "string (required)",
  "password": "string (required)"
}
```

**Success Response (201):**
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "username": "john_doe"
}
```

**Error Responses:**
- `400`: Missing required fields
- `409`: Username or email already exists
- `500`: Server error

---

### 3. User Login

**POST** `/api/login`

Authenticate user and create session.

**Request Body:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "total_points": 150,
    "difficulty_level": 2
  }
}
```

**Error Responses:**
- `400`: Missing credentials
- `401`: Invalid credentials

---

### 4. User Logout

**POST** `/api/logout`

Clear user session.

**Success Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

---

### 5. Get User Profile

**GET** `/api/user/profile`

Get authenticated user's profile and statistics.

**Authentication:** Required

**Success Response (200):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "total_points": 150,
    "difficulty_level": 2,
    "created_at": "2024-01-01 10:00:00"
  },
  "statistics": {
    "total_attempts": 25,
    "correct_attempts": 20,
    "accuracy_percentage": 80.0,
    "current_streak": 3,
    "best_streak": 7,
    "scenarios_completed": 25,
    "phishing_detected": 12,
    "phishing_missed": 3,
    "false_positives": 2
  }
}
```

**Error Responses:**
- `401`: Not authenticated
- `404`: User not found

---

### 6. Get Next Scenario

**GET** `/api/scenario/next`

Get the next training scenario based on adaptive difficulty.

**Authentication:** Required

**Success Response (200):**
```json
{
  "scenario": {
    "id": 5,
    "scenario_type": "email",
    "difficulty_level": 2,
    "subject": "Security Alert",
    "body": "Your account has unusual activity...",
    "sender": "security@fake-bank.com",
    "url": "http://fake-bank.com/verify",
    "answer_hidden": true
  },
  "difficulty": 2
}
```

**Error Responses:**
- `401`: Not authenticated
- `404`: No scenarios available

---

### 7. Submit Answer

**POST** `/api/scenario/submit`

Submit answer to a scenario and get feedback.

**Authentication:** Required

**Request Body:**
```json
{
  "scenario_id": 5,
  "user_answer": true,
  "time_taken": 45
}
```

**Parameters:**
- `scenario_id` (integer): ID of the scenario
- `user_answer` (boolean): true = phishing, false = legitimate
- `time_taken` (integer): Time taken in seconds

**Success Response (200):**
```json
{
  "is_correct": true,
  "points_earned": 25,
  "correct_answer": true,
  "explanation": {
    "subject": "Security Alert",
    "sender": "security@fake-bank.com",
    "url": "http://fake-bank.com/verify",
    "indicators": [
      "suspicious_sender",
      "urgent_language",
      "no_https"
    ]
  },
  "statistics": {
    "current_streak": 4,
    "accuracy": 81.5,
    "scenarios_completed": 26
  },
  "new_achievements": [
    {
      "id": 2,
      "name": "Phishing Detective",
      "description": "Correctly identify 10 phishing attempts",
      "icon": "🔍"
    }
  ]
}
```

**Error Responses:**
- `400`: Missing required fields
- `401`: Not authenticated
- `404`: Scenario not found

---

### 8. Get Leaderboard

**GET** `/api/leaderboard?limit=10`

Get top users on the leaderboard.

**Query Parameters:**
- `limit` (integer, optional): Number of users to return (default: 10)

**Success Response (200):**
```json
{
  "leaderboard": [
    {
      "id": 1,
      "username": "john_doe",
      "total_points": 500,
      "difficulty_level": 3,
      "accuracy_percentage": 85.5,
      "current_streak": 5,
      "scenarios_completed": 50
    }
  ]
}
```

---

### 9. Get Achievements

**GET** `/api/achievements`

Get all achievements and user's progress.

**Authentication:** Required

**Success Response (200):**
```json
{
  "all_achievements": [
    {
      "id": 1,
      "name": "First Step",
      "description": "Complete your first training scenario",
      "icon": "🎯",
      "points_required": 10,
      "criteria_type": "scenarios_completed",
      "criteria_value": 1
    }
  ],
  "earned_achievements": [
    {
      "id": 1,
      "name": "First Step",
      "description": "Complete your first training scenario",
      "icon": "🎯",
      "earned_at": "2024-01-01 10:30:00"
    }
  ]
}
```

**Error Response:**
- `401`: Not authenticated

---

### 10. Get User Analytics

**GET** `/api/analytics/user`

Get detailed analytics for the authenticated user.

**Authentication:** Required

**Success Response (200):**
```json
{
  "statistics": {
    "total_attempts": 25,
    "correct_attempts": 20,
    "accuracy_percentage": 80.0,
    "current_streak": 3,
    "best_streak": 7,
    "scenarios_completed": 25,
    "phishing_detected": 12,
    "phishing_missed": 3,
    "false_positives": 2
  },
  "recent_attempts": [
    {
      "id": 45,
      "scenario_id": 5,
      "scenario_type": "email",
      "difficulty_level": 2,
      "subject": "Security Alert",
      "user_answer": true,
      "is_correct": true,
      "points_earned": 25,
      "attempted_at": "2024-01-01 15:30:00"
    }
  ],
  "performance_by_difficulty": [
    {
      "difficulty_level": 1,
      "total": 10,
      "correct": 9
    },
    {
      "difficulty_level": 2,
      "total": 15,
      "correct": 11
    }
  ]
}
```

**Error Response:**
- `401`: Not authenticated

---

### 11. Analyze URL

**POST** `/api/analyze/url`

Analyze a URL for phishing indicators (educational tool).

**Authentication:** Required

**Request Body:**
```json
{
  "url": "http://fake-bank.com/verify"
}
```

**Success Response (200):**
```json
{
  "is_suspicious": true,
  "indicators": [
    "No HTTPS encryption",
    "Suspicious keyword: 'verify'",
    "Possible typosquatting of bank.com"
  ],
  "risk_score": 65,
  "threat_level": "MEDIUM"
}
```

**Error Response:**
- `400`: URL required
- `401`: Not authenticated

---

### 12. Analyze Email

**POST** `/api/analyze/email`

Analyze email content for phishing indicators (educational tool).

**Authentication:** Required

**Request Body:**
```json
{
  "sender": "security@fake-site.com",
  "subject": "URGENT: Account Suspended",
  "body": "Dear user, your account will be terminated. Click here immediately."
}
```

**Success Response (200):**
```json
{
  "is_suspicious": true,
  "indicators": [
    "Urgent language: 'urgent'",
    "Generic greeting (not personalized)",
    "Threatening language: 'suspended'",
    "Sender has suspicious domain extension"
  ],
  "risk_score": 70,
  "threat_level": "MEDIUM"
}
```

**Error Response:**
- `400`: Email body required
- `401`: Not authenticated

---

### 13. Get All Scenarios (Admin/Testing)

**GET** `/api/scenarios/all`

Get all scenarios (for testing or admin purposes).

**Success Response (200):**
```json
{
  "scenarios": [
    {
      "id": 1,
      "scenario_type": "email",
      "difficulty_level": 1,
      "subject": "Your account has been suspended!",
      "body": "Dear user, your account will be terminated...",
      "sender": "security@amaz0n.com",
      "url": "http://amaz0n-verify.com/login",
      "is_phishing": true,
      "phishing_indicators": "[\"suspicious_sender\", \"urgent_language\"]"
    }
  ]
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Description of what went wrong"
}
```

### 401 Unauthorized
```json
{
  "error": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 409 Conflict
```json
{
  "error": "Resource already exists"
}
```

### 500 Internal Server Error
```json
{
  "error": "Server error description"
}
```

---

## Data Models

### User
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "total_points": "integer",
  "difficulty_level": "integer (1-4)",
  "created_at": "timestamp",
  "last_login": "timestamp"
}
```

### Scenario
```json
{
  "id": "integer",
  "scenario_type": "string (email|sms|website)",
  "difficulty_level": "integer (1-4)",
  "subject": "string|null",
  "body": "string",
  "sender": "string|null",
  "url": "string|null",
  "is_phishing": "boolean",
  "phishing_indicators": "json array"
}
```

### Achievement
```json
{
  "id": "integer",
  "name": "string",
  "description": "string",
  "icon": "string (emoji)",
  "points_required": "integer",
  "criteria_type": "string (points|streak|accuracy|scenarios_completed|phishing_detected)",
  "criteria_value": "integer"
}
```

### User Statistics
```json
{
  "user_id": "integer",
  "total_attempts": "integer",
  "correct_attempts": "integer",
  "accuracy_percentage": "float",
  "current_streak": "integer",
  "best_streak": "integer",
  "scenarios_completed": "integer",
  "phishing_detected": "integer",
  "phishing_missed": "integer",
  "false_positives": "integer"
}
```

---

## Notes

1. **Sessions**: The API uses cookie-based sessions. Include credentials in fetch requests.
2. **CORS**: CORS is enabled for development. Configure appropriately for production.
3. **Rate Limiting**: Consider implementing rate limiting for production use.
4. **HTTPS**: Always use HTTPS in production for security.
5. **Database**: SQLite is used for simplicity. Consider PostgreSQL/MySQL for production.