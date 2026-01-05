# Phishing Awareness Simulator with Gamification

A comprehensive security-focused training platform designed to educate users on detecting and avoiding phishing attacks through gamified learning experiences.

## 🎯 Project Overview

The Phishing Awareness Simulator integrates essential Security Technology (ST) components by simulating real-world phishing attempts including deceptive emails, spoofed websites, and fraudulent SMS messages. Users are exposed to controlled phishing scenarios in a safe environment where their responses are monitored and evaluated.

## ✨ Key Features

### 🔒 Security Technology Components
- **Secure Authentication**: User registration and login with bcrypt password hashing
- **Data Encryption**: Cryptographic encryption for protecting sensitive user data using Fernet encryption
- **Phishing Detection**: Advanced URL and email analysis using threat intelligence techniques
- **Sandboxed Environment**: Safe simulation of phishing attempts without real security risks

### 🎮 Gamification Features
- **Points System**: Earn points based on performance and answer speed
- **Achievements & Badges**: Unlock 7+ achievements for various milestones
- **Global Leaderboard**: Compete with other users
- **Streak Tracking**: Build and maintain answer streaks

### 🎓 Adaptive Learning
- **Dynamic Difficulty**: 4 difficulty levels that adapt based on user performance
- **Personalized Challenges**: Scenarios selected based on user skill level
- **Progress Tracking**: Detailed statistics on user improvement over time

### 📊 Analytics & Reporting
- **User Dashboard**: Comprehensive statistics on training progress
- **Performance Metrics**: Accuracy, streak, completion rate tracking
- **Risk Assessment**: Analysis of phishing detection vs. false positive rates
- **Difficulty Analysis**: Performance breakdown by difficulty level

### 🎯 Training Scenarios
- **Email Phishing**: Suspicious emails with various phishing indicators
- **SMS Phishing**: Text message-based phishing attempts
- **Website Spoofing**: Fake login pages and suspicious URLs
- **Multiple Difficulty Levels**: From beginner to expert scenarios

### 🔍 Detection Tools
- **URL Analyzer**: Real-time URL analysis for phishing indicators
- **Email Analyzer**: Comprehensive email content scanning
- **Threat Scoring**: Risk score calculation (0-100)
- **Educational Feedback**: Detailed explanations of phishing indicators

## 🏗️ Architecture

### Backend (Python/Flask)
```
backend/
├── app.py                  # Main Flask application with API endpoints
├── database.py             # Database connection and utilities
├── security.py             # Password hashing and encryption
├── phishing_detector.py    # ML/rule-based phishing detection
└── requirements.txt        # Python dependencies
```

### Frontend (HTML/CSS/JavaScript)
```
frontend/
├── index.html             # Main application interface
├── style.css              # Comprehensive styling
└── script.js              # Frontend logic and API integration
```

### Database (SQLite)
```
database/
├── schema.sql             # Database schema with sample data
└── phishing_simulator.db  # SQLite database (generated)
```

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip
- Modern web browser

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/limkaijie0809/FINAL-YEAR-PROJECT-1.git
cd FINAL-YEAR-PROJECT-1
```

2. **Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Initialize the database**
```bash
python3 -c "from database import init_db; init_db()"
```

4. **Start the backend server**
```bash
python3 app.py
```
The server will start on `http://localhost:5000`

5. **Open the frontend**
Open `frontend/index.html` in your web browser, or serve it with a simple HTTP server:
```bash
cd frontend
python3 -m http.server 8000
```
Then navigate to `http://localhost:8000`

## 🎮 Usage Guide

### Getting Started
1. **Register**: Create a new account with username, email, and password
2. **Login**: Access your personalized training dashboard
3. **Start Training**: Click "Start New Scenario" to begin

### Training Flow
1. Read the scenario carefully (email, SMS, or website)
2. Analyze for phishing indicators
3. Choose "Legitimate" or "Phishing"
4. Receive instant feedback with explanations
5. Earn points and unlock achievements
6. Progress through difficulty levels

### Navigation
- **🎯 Training**: Practice identifying phishing attempts
- **🏆 Leaderboard**: View top performers globally
- **🎖️ Achievements**: Track your unlocked badges
- **📊 Analytics**: Review your detailed statistics
- **🔍 Detection Tools**: Analyze URLs and emails

## 🔐 Security Features

### Password Security
- Passwords are hashed using bcrypt with salt
- Never stored in plain text
- Secure session management

### Data Encryption
- Sensitive data encrypted using Fernet (symmetric encryption)
- Encryption key stored securely
- Database contains only encrypted sensitive information

### Phishing Detection Algorithms
- **URL Analysis**: Checks for HTTPS, suspicious TLDs, IP addresses, typosquatting
- **Email Analysis**: Detects urgent language, generic greetings, threats, suspicious offers
- **Risk Scoring**: Comprehensive threat level assessment (HIGH/MEDIUM/LOW/SAFE)

## 📊 Database Schema

### Main Tables
- **users**: User accounts with encrypted data
- **phishing_scenarios**: Training scenarios (15+ pre-loaded)
- **user_attempts**: Individual training attempts
- **achievements**: Badge definitions (7 achievements)
- **user_achievements**: Earned badges
- **user_statistics**: Detailed performance metrics

### Pre-loaded Content
- 15+ phishing scenarios across 3 difficulty levels
- 7 achievement badges
- Sample legitimate and phishing examples

## 🎯 Achievement System

| Achievement | Description | Requirement |
|------------|-------------|-------------|
| 🎯 First Step | Complete first scenario | 1 scenario |
| 🔍 Phishing Detective | Detect 10 phishing attempts | 10 correct detections |
| 🛡️ Guardian | Reach 100 points | 100 points |
| 🔥 Perfect Streak | Correct streak of 5 | 5 in a row |
| 👁️ Expert Eye | Achieve 90% accuracy | 90% accuracy |
| 💯 Century Club | Complete 100 scenarios | 100 scenarios |
| 🏆 Master Defender | Reach expert level | 1000 points |

## 🔧 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/user/profile` - Get user profile

### Training
- `GET /api/scenario/next` - Get next adaptive scenario
- `POST /api/scenario/submit` - Submit answer

### Gamification
- `GET /api/leaderboard` - Get top users
- `GET /api/achievements` - Get user achievements

### Analytics
- `GET /api/analytics/user` - Get user analytics

### Tools
- `POST /api/analyze/url` - Analyze URL for phishing
- `POST /api/analyze/email` - Analyze email content

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0**: Web framework
- **flask-cors 4.0.0**: CORS support
- **bcrypt 4.1.2**: Password hashing
- **cryptography 41.0.7**: Data encryption
- **SQLAlchemy 2.0.23**: Database ORM
- **PyJWT 2.8.0**: JWT token support
- **scikit-learn 1.3.2**: ML capabilities
- **requests 2.31.0**: HTTP requests

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with gradients and animations
- **Vanilla JavaScript**: Dynamic functionality
- **Fetch API**: Backend communication

### Database
- **SQLite**: Lightweight database
- **SQL**: Query language

## 🎨 Design Highlights

- Modern gradient UI with purple theme
- Responsive design for mobile and desktop
- Smooth animations and transitions
- Intuitive navigation with tabbed interface
- Color-coded threat levels and difficulty badges

## 📈 Adaptive Learning Algorithm

The system automatically adjusts difficulty based on:
1. **Accuracy Rate**: Users with >80% accuracy advance
2. **Scenarios Completed**: Minimum 10 scenarios before advancement
3. **Performance Patterns**: Tracks strengths and weaknesses
4. **Dynamic Selection**: Avoids recently seen scenarios

## 🔬 Phishing Detection Features

### URL Analysis Indicators
- Missing HTTPS encryption
- Suspicious TLDs (.xyz, .top, .win, etc.)
- IP addresses instead of domains
- Typosquatting detection
- Excessive subdomains
- Suspicious characters and hyphens
- Unusually long URLs

### Email Analysis Indicators
- Urgent/threatening language
- Generic greetings
- Suspicious offers/prizes
- Suspicious sender domains
- Impersonation attempts
- Authority exploitation

## 🚀 Future Enhancements

- [ ] Machine learning model for advanced detection
- [ ] Real-time threat feed integration
- [ ] Multi-language support
- [ ] Organization/team features
- [ ] Custom scenario creation
- [ ] Email header analysis
- [ ] Browser extension for real-time protection
- [ ] Mobile application
- [ ] Detailed forensics mode
- [ ] Integration with security awareness programs

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Development Team
- Security Researchers
- UX Designers

## 🙏 Acknowledgments

- Inspired by real-world phishing attack patterns
- Security best practices from OWASP
- Gamification principles for effective learning
- Community feedback and testing

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

---

**Note**: This is an educational tool. Always practice good security hygiene and report real phishing attempts to appropriate authorities.
