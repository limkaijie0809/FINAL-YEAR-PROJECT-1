from flask import Flask, jsonify, request, session
from flask_cors import CORS
import json
import random
from datetime import datetime, timedelta
import os

from database import get_db_connection, init_db, dict_from_row, dicts_from_rows
from security import hash_password, verify_password, encrypt_data, decrypt_data
from phishing_detector import analyze_url, analyze_email_content

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # was 'None'
app.config['SESSION_COOKIE_SECURE'] = False    # keep HTTP for local dev
CORS(app, supports_credentials=True)

# Initialize database on startup
init_db()

@app.route("/")
def home():
    return jsonify({"message": "Phishing Awareness Simulator API is running!"})

# ============== USER MANAGEMENT ==============

@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user with encrypted data storage."""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    
    # Check if user exists
    existing = conn.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                           (username, email)).fetchone()
    if existing:
        conn.close()
        return jsonify({"error": "Username or email already exists"}), 409
    
    # Hash password and create user
    password_hash = hash_password(password)
    
    try:
        cursor = conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        user_id = cursor.lastrowid
        
        # Initialize user statistics
        conn.execute('INSERT INTO user_statistics (user_id) VALUES (?)', (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id,
            "username": username
        }), 201
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 500

@app.route("/api/login", methods=["POST"])
def login():
    """Authenticate user and create session."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({"error": "Missing credentials"}), 400
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    
    if not user or not verify_password(password, user['password_hash']):
        conn.close()
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Update last login
    conn.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                (datetime.now(), user['id']))
    conn.commit()
    conn.close()
    
    # Create session
    session['user_id'] = user['id']
    session['username'] = user['username']
    
    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user['id'],
            "username": user['username'],
            "total_points": user['total_points'],
            "difficulty_level": user['difficulty_level']
        }
    })

@app.route("/api/logout", methods=["POST"])
def logout():
    """Logout user."""
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@app.route("/api/user/profile", methods=["GET"])
def get_profile():
    """Get user profile with statistics."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    stats = conn.execute('SELECT * FROM user_statistics WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "user": dict_from_row(user),
        "statistics": dict_from_row(stats) if stats else {}
    })

# ============== TRAINING/SCENARIOS ==============

@app.route("/api/scenario/next", methods=["GET"])
def get_next_scenario():
    """Get next training scenario based on adaptive difficulty."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    conn = get_db_connection()
    
    # Get user's difficulty level
    user = conn.execute('SELECT difficulty_level FROM users WHERE id = ?', (user_id,)).fetchone()
    difficulty = user['difficulty_level'] if user else 1
    
    # Get statistics to determine if difficulty should increase
    stats = conn.execute('SELECT * FROM user_statistics WHERE user_id = ?', (user_id,)).fetchone()
    
    # Adaptive difficulty: increase if accuracy > 80% and completed > 10 scenarios
    if stats and stats['scenarios_completed'] > 10 and stats['accuracy_percentage'] > 80:
        if difficulty < 3:
            difficulty += 1
            conn.execute('UPDATE users SET difficulty_level = ? WHERE id = ?', (difficulty, user_id))
            conn.commit()
    
    # Get scenarios at current difficulty level that user hasn't completed recently
    recent_ids = conn.execute(
        'SELECT scenario_id FROM user_attempts WHERE user_id = ? ORDER BY attempted_at DESC LIMIT 5',
        (user_id,)
    ).fetchall()
    recent_ids = [row['scenario_id'] for row in recent_ids]
    
    if recent_ids:
        placeholders = ','.join('?' * len(recent_ids))
        query = f'''
            SELECT * FROM phishing_scenarios 
            WHERE difficulty_level = ? AND id NOT IN ({placeholders})
            ORDER BY RANDOM() LIMIT 1
        '''
        scenario = conn.execute(query, [difficulty] + recent_ids).fetchone()
    else:
        scenario = conn.execute(
            'SELECT * FROM phishing_scenarios WHERE difficulty_level = ? ORDER BY RANDOM() LIMIT 1',
            (difficulty,)
        ).fetchone()
    
    conn.close()
    
    if not scenario:
        return jsonify({"error": "No scenarios available"}), 404
    
    scenario_dict = dict_from_row(scenario)
    
    # Remove the answer from response (client shouldn't see it yet)
    scenario_dict['answer_hidden'] = scenario_dict.pop('is_phishing')
    
    return jsonify({
        "scenario": scenario_dict,
        "difficulty": difficulty
    })

@app.route("/api/scenario/submit", methods=["POST"])
def submit_answer():
    """Submit answer to a scenario and calculate results with gamification."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    scenario_id = data.get('scenario_id')
    user_answer = data.get('user_answer')  # True = phishing, False = legitimate
    time_taken = data.get('time_taken', 0)
    
    if scenario_id is None or user_answer is None:
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    
    # Get scenario
    scenario = conn.execute('SELECT * FROM phishing_scenarios WHERE id = ?', (scenario_id,)).fetchone()
    if not scenario:
        conn.close()
        return jsonify({"error": "Scenario not found"}), 404
    
    # Check if correct
    is_correct = (user_answer == bool(scenario['is_phishing']))
    
    # Calculate points
    points = 0
    if is_correct:
        base_points = scenario['difficulty_level'] * 10
        # Bonus points for speed (if answered quickly)
        time_bonus = max(0, 10 - time_taken // 10) if time_taken < 100 else 0
        points = base_points + time_bonus
    
    # Record attempt
    conn.execute(
        '''INSERT INTO user_attempts 
           (user_id, scenario_id, user_answer, is_correct, time_taken, points_earned)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (user_id, scenario_id, user_answer, is_correct, time_taken, points)
    )
    
    # Update user points
    conn.execute('UPDATE users SET total_points = total_points + ? WHERE id = ?', (points, user_id))
    
    # Update statistics
    stats = conn.execute('SELECT * FROM user_statistics WHERE user_id = ?', (user_id,)).fetchone()
    
    new_attempts = stats['total_attempts'] + 1
    new_correct = stats['correct_attempts'] + (1 if is_correct else 0)
    new_accuracy = (new_correct / new_attempts) * 100
    new_streak = stats['current_streak'] + 1 if is_correct else 0
    new_best_streak = max(stats['best_streak'], new_streak)
    new_scenarios = stats['scenarios_completed'] + 1
    
    # Track phishing detection stats
    new_phishing_detected = stats['phishing_detected']
    new_phishing_missed = stats['phishing_missed']
    new_false_positives = stats['false_positives']
    
    if scenario['is_phishing']:
        if user_answer:
            new_phishing_detected += 1
        else:
            new_phishing_missed += 1
    else:
        if user_answer:
            new_false_positives += 1
    
    conn.execute('''
        UPDATE user_statistics SET
            total_attempts = ?,
            correct_attempts = ?,
            accuracy_percentage = ?,
            current_streak = ?,
            best_streak = ?,
            scenarios_completed = ?,
            phishing_detected = ?,
            phishing_missed = ?,
            false_positives = ?,
            last_updated = ?
        WHERE user_id = ?
    ''', (new_attempts, new_correct, new_accuracy, new_streak, new_best_streak,
          new_scenarios, new_phishing_detected, new_phishing_missed, 
          new_false_positives, datetime.now(), user_id))
    
    # Check for new achievements
    user = conn.execute('SELECT total_points FROM users WHERE id = ?', (user_id,)).fetchone()
    new_achievements = check_achievements(conn, user_id, user['total_points'], 
                                         new_accuracy, new_streak, new_scenarios, 
                                         new_phishing_detected)
    
    conn.commit()
    conn.close()
    
    # Prepare feedback
    indicators = json.loads(scenario['phishing_indicators']) if scenario['phishing_indicators'] else []
    
    return jsonify({
        "is_correct": is_correct,
        "points_earned": points,
        "correct_answer": bool(scenario['is_phishing']),
        "explanation": {
            "subject": scenario['subject'],
            "sender": scenario['sender'],
            "url": scenario['url'],
            "indicators": indicators
        },
        "statistics": {
            "current_streak": new_streak,
            "accuracy": round(new_accuracy, 2),
            "scenarios_completed": new_scenarios
        },
        "new_achievements": new_achievements
    })

def check_achievements(conn, user_id, total_points, accuracy, streak, 
                       scenarios_completed, phishing_detected):
    """Check if user has earned any new achievements."""
    new_achievements = []
    
    # Get all achievements
    achievements = conn.execute('SELECT * FROM achievements').fetchall()
    
    # Get user's existing achievements
    existing = conn.execute(
        'SELECT achievement_id FROM user_achievements WHERE user_id = ?',
        (user_id,)
    ).fetchall()
    existing_ids = [row['achievement_id'] for row in existing]
    
    for achievement in achievements:
        if achievement['id'] in existing_ids:
            continue
        
        earned = False
        criteria_type = achievement['criteria_type']
        criteria_value = achievement['criteria_value']
        
        if criteria_type == 'points' and total_points >= criteria_value:
            earned = True
        elif criteria_type == 'accuracy' and accuracy >= criteria_value:
            earned = True
        elif criteria_type == 'streak' and streak >= criteria_value:
            earned = True
        elif criteria_type == 'scenarios_completed' and scenarios_completed >= criteria_value:
            earned = True
        elif criteria_type == 'phishing_detected' and phishing_detected >= criteria_value:
            earned = True
        
        if earned:
            conn.execute(
                'INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)',
                (user_id, achievement['id'])
            )
            new_achievements.append(dict_from_row(achievement))
    
    return new_achievements

# ============== GAMIFICATION ==============

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """Get top users leaderboard."""
    limit = request.args.get('limit', 10, type=int)
    
    conn = get_db_connection()
    leaders = conn.execute(
        'SELECT * FROM leaderboard LIMIT ?', (limit,)
    ).fetchall()
    conn.close()
    
    return jsonify({"leaderboard": dicts_from_rows(leaders)})

@app.route("/api/achievements", methods=["GET"])
def get_achievements():
    """Get all achievements and user's progress."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    conn = get_db_connection()
    
    # Get all achievements
    achievements = conn.execute('SELECT * FROM achievements').fetchall()
    
    # Get user's earned achievements
    earned = conn.execute('''
        SELECT a.*, ua.earned_at 
        FROM achievements a
        JOIN user_achievements ua ON a.id = ua.achievement_id
        WHERE ua.user_id = ?
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        "all_achievements": dicts_from_rows(achievements),
        "earned_achievements": dicts_from_rows(earned)
    })

# ============== ANALYTICS ==============

@app.route("/api/analytics/user", methods=["GET"])
def get_user_analytics():
    """Get detailed user analytics and progress."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    conn = get_db_connection()
    
    # Get user stats
    stats = conn.execute('SELECT * FROM user_statistics WHERE user_id = ?', (user_id,)).fetchone()
    
    # Get recent attempts
    recent = conn.execute('''
        SELECT ua.*, ps.scenario_type, ps.difficulty_level, ps.subject
        FROM user_attempts ua
        JOIN phishing_scenarios ps ON ua.scenario_id = ps.id
        WHERE ua.user_id = ?
        ORDER BY ua.attempted_at DESC
        LIMIT 20
    ''', (user_id,)).fetchall()
    
    # Get performance by difficulty
    performance = conn.execute('''
        SELECT 
            ps.difficulty_level,
            COUNT(*) as total,
            SUM(CASE WHEN ua.is_correct THEN 1 ELSE 0 END) as correct
        FROM user_attempts ua
        JOIN phishing_scenarios ps ON ua.scenario_id = ps.id
        WHERE ua.user_id = ?
        GROUP BY ps.difficulty_level
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    return jsonify({
        "statistics": dict_from_row(stats) if stats else {},
        "recent_attempts": dicts_from_rows(recent),
        "performance_by_difficulty": dicts_from_rows(performance)
    })

# ============== PHISHING DETECTION TOOLS ==============

@app.route("/api/analyze/url", methods=["POST"])
def analyze_url_endpoint():
    """Analyze a URL for phishing indicators (educational tool)."""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL required"}), 400
    
    analysis = analyze_url(url)
    return jsonify(analysis)

@app.route("/api/analyze/email", methods=["POST"])
def analyze_email_endpoint():
    """Analyze email content for phishing indicators (educational tool)."""
    data = request.json
    subject = data.get('subject', '')
    body = data.get('body', '')
    sender = data.get('sender', '')
    
    if not body:
        return jsonify({"error": "Email body required"}), 400
    
    analysis = analyze_email_content(subject, body, sender)
    return jsonify(analysis)

# ============== ADMIN/TESTING ==============

@app.route("/api/scenarios/all", methods=["GET"])
def get_all_scenarios():
    """Get all scenarios (for testing/admin)."""
    conn = get_db_connection()
    scenarios = conn.execute('SELECT * FROM phishing_scenarios').fetchall()
    conn.close()
    
    return jsonify({"scenarios": dicts_from_rows(scenarios)})

if __name__ == "__main__":
    # Debug mode should only be enabled in development, not production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
