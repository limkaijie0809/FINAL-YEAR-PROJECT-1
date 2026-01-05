# Setup and Running Guide

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

The database will be automatically initialized when you first run the application. Alternatively, you can manually initialize it:

```bash
cd backend
python3 -c "from database import init_db; init_db()"
```

### 3. Start the Backend Server

```bash
cd backend
python3 app.py
```

The Flask server will start on `http://localhost:5000`

### 4. Access the Application

**Option A: Simple File Access (May have CORS issues)**
- Open `frontend/index.html` directly in your browser

**Option B: Using HTTP Server (Recommended)**
```bash
cd frontend
python3 -m http.server 8000
```
Then navigate to `http://localhost:8000`

**Option C: Serve Frontend from Backend (Best for Production)**

Add this to `backend/app.py`:
```python
from flask import send_from_directory
import os

frontend_dir = os.path.join(os.path.dirname(__file__), '../frontend')

@app.route('/')
def serve_frontend():
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(frontend_dir, path)
```

Then just access `http://localhost:5000` in your browser.

## Testing the Application

### 1. Register a New User
- Click "Register" tab
- Enter username, email, and password
- Click "Register" button
- Switch back to "Login" tab

### 2. Login
- Enter your username and password
- Click "Login" button
- You'll be redirected to the training dashboard

### 3. Start Training
- Click "Start New Scenario" button
- Read the email/SMS/website scenario carefully
- Analyze for phishing indicators
- Choose "Legitimate" or "Phishing"
- Review the feedback and explanation
- Earn points and unlock achievements!

### 4. Explore Features
- **🏆 Leaderboard**: See top performers
- **🎖️ Achievements**: Track your badges
- **📊 Analytics**: View detailed statistics
- **🔍 Detection Tools**: Analyze URLs and emails

## Testing the API Endpoints

You can test the API endpoints using curl:

### Register User
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  -c cookies.txt
```

### Get Next Scenario
```bash
curl http://localhost:5000/api/scenario/next \
  -b cookies.txt
```

### Submit Answer
```bash
curl -X POST http://localhost:5000/api/scenario/submit \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"scenario_id":1,"user_answer":true,"time_taken":30}'
```

### Get Leaderboard
```bash
curl http://localhost:5000/api/leaderboard
```

### Analyze URL
```bash
curl -X POST http://localhost:5000/api/analyze/url \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"url":"http://fake-bank.com/verify"}'
```

## Troubleshooting

### CORS Issues
If you encounter CORS errors:
1. Make sure the backend is running on port 5000
2. Access frontend through HTTP server, not file://
3. Check that CORS is enabled in Flask (it should be by default)

### Session Issues
If you get "Not authenticated" errors:
1. Make sure you're logged in
2. Check that cookies are enabled in your browser
3. Try using the same port for frontend and backend

### Database Issues
If scenarios don't load:
```bash
cd backend
rm ../database/phishing_simulator.db
python3 -c "from database import init_db; init_db()"
```

### Port Already in Use
If port 5000 or 8000 is already in use:
```bash
# For backend (change in app.py)
app.run(debug=True, host='0.0.0.0', port=5001)

# For frontend
python3 -m http.server 8001
```

## Production Deployment

### Security Considerations
1. Set `app.config['SECRET_KEY']` to a secure random value
2. Enable HTTPS
3. Set `SESSION_COOKIE_SECURE = True`
4. Use a production database (PostgreSQL/MySQL)
5. Implement rate limiting
6. Add logging and monitoring
7. Use environment variables for configuration

### Environment Variables
Create a `.env` file:
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Using Production WSGI Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Development Tips

### Running Tests
```bash
cd backend
python3 -c "from app import app; import tests; tests.run_all()"
```

### Adding New Scenarios
Insert into database:
```sql
INSERT INTO phishing_scenarios 
  (scenario_type, difficulty_level, subject, body, sender, url, is_phishing, phishing_indicators)
VALUES 
  ('email', 2, 'Your Subject', 'Email body...', 'sender@domain.com', 
   'http://url.com', 1, '["indicator1", "indicator2"]');
```

### Modifying Point System
Edit in `backend/app.py`, function `submit_answer()`:
```python
base_points = scenario['difficulty_level'] * 10  # Adjust multiplier
time_bonus = max(0, 10 - time_taken // 10)  # Adjust time bonus
```

## Features by Priority

### ✅ Implemented
- User authentication with encryption
- Phishing scenario database
- Adaptive difficulty system
- Points and achievements
- Leaderboard
- Analytics dashboard
- URL/Email detection tools
- Multiple scenario types (email, SMS, website)

### 🚧 Future Enhancements
- Machine learning model integration
- Real-time threat feed
- Organization management
- Custom scenario builder
- Export reports to PDF
- Email header analysis
- Browser extension

## Support

For issues or questions:
1. Check the API documentation in `API_DOCUMENTATION.md`
2. Review the README.md for feature details
3. Open an issue on GitHub

## License

MIT License - See LICENSE file for details
