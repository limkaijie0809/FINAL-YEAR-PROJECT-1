-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    encrypted_data TEXT,
    total_points INTEGER DEFAULT 0,
    difficulty_level INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Phishing scenarios table
CREATE TABLE IF NOT EXISTS phishing_scenarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_type TEXT NOT NULL, -- 'email', 'website', 'sms'
    difficulty_level INTEGER NOT NULL, -- 1: Easy, 2: Medium, 3: Hard, 4: Expert
    subject TEXT,
    body TEXT NOT NULL,
    sender TEXT,
    url TEXT,
    is_phishing BOOLEAN NOT NULL,
    phishing_indicators TEXT, -- JSON array of indicators
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User attempts/responses table
CREATE TABLE IF NOT EXISTS user_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    user_answer BOOLEAN NOT NULL,
    is_correct BOOLEAN NOT NULL,
    time_taken INTEGER, -- seconds
    points_earned INTEGER DEFAULT 0,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (scenario_id) REFERENCES phishing_scenarios(id)
);

-- Achievements/Badges table
CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    icon TEXT,
    points_required INTEGER,
    criteria_type TEXT NOT NULL, -- 'points', 'streak', 'accuracy', 'scenarios_completed'
    criteria_value INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User achievements table
CREATE TABLE IF NOT EXISTS user_achievements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(id),
    UNIQUE(user_id, achievement_id)
);

-- User statistics table
CREATE TABLE IF NOT EXISTS user_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    total_attempts INTEGER DEFAULT 0,
    correct_attempts INTEGER DEFAULT 0,
    accuracy_percentage REAL DEFAULT 0.0,
    current_streak INTEGER DEFAULT 0,
    best_streak INTEGER DEFAULT 0,
    scenarios_completed INTEGER DEFAULT 0,
    phishing_detected INTEGER DEFAULT 0,
    phishing_missed INTEGER DEFAULT 0,
    false_positives INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Leaderboard view
CREATE VIEW IF NOT EXISTS leaderboard AS
SELECT 
    u.id,
    u.username,
    u.total_points,
    u.difficulty_level,
    us.accuracy_percentage,
    us.current_streak,
    us.scenarios_completed
FROM users u
LEFT JOIN user_statistics us ON u.id = us.user_id
ORDER BY u.total_points DESC, us.accuracy_percentage DESC;

-- Insert default achievements
INSERT OR IGNORE INTO achievements (name, description, icon, points_required, criteria_type, criteria_value) VALUES
('First Step', 'Complete your first training scenario', '🎯', 10, 'scenarios_completed', 1),
('Phishing Detective', 'Correctly identify 10 phishing attempts', '🔍', 100, 'phishing_detected', 10),
('Guardian', 'Reach 100 total points', '🛡️', 100, 'points', 100),
('Perfect Streak', 'Achieve a 5-answer correct streak', '🔥', 50, 'streak', 5),
('Expert Eye', 'Reach 90% accuracy', '👁️', 200, 'accuracy', 90),
('Century Club', 'Complete 100 scenarios', '💯', 500, 'scenarios_completed', 100),
('Master Defender', 'Reach Expert difficulty level', '🏆', 1000, 'points', 1000);

-- Insert sample phishing scenarios
INSERT OR IGNORE INTO phishing_scenarios (scenario_type, difficulty_level, subject, body, sender, url, is_phishing, phishing_indicators) VALUES
-- Easy phishing emails
('email', 1, 'Your account has been suspended!', 'Dear user, your account will be terminated. Click here to verify your identity immediately.', 'security@amaz0n.com', 'http://amaz0n-verify.com/login', 1, '["suspicious_sender", "urgent_language", "suspicious_url", "generic_greeting"]'),
('email', 1, 'Congratulations! You won $1,000,000', 'You have been selected as the lucky winner! Click here to claim your prize now!', 'lottery@winner-claim.net', 'http://claim-prize-now.xyz/form', 1, '["too_good_to_be_true", "suspicious_url", "urgency", "unexpected_prize"]'),

-- Easy legitimate emails
('email', 1, 'Your order confirmation', 'Thank you for your recent purchase. Your order #12345 has been confirmed and will ship within 2-3 business days.', 'orders@amazon.com', 'https://www.amazon.com/orders', 0, '[]'),
('email', 1, 'Weekly team meeting reminder', 'Hi Team, reminder that our weekly sync is scheduled for tomorrow at 2 PM in Conference Room A.', 'manager@company.com', NULL, 0, '[]'),

-- Medium phishing emails
('email', 2, 'Security Alert: Unusual Sign-in Activity', 'We detected a sign-in from an unusual location. If this wasn''t you, please verify your account by clicking the link below.', 'no-reply@security-microsoft.com', 'https://microsoft-verify-secure.com/signin', 1, '["similar_domain", "fear_tactics", "fake_security_alert"]'),
('email', 2, 'Your package could not be delivered', 'Dear customer, we attempted to deliver your package but no one was home. Please update your delivery preferences.', 'delivery@fedex-update.com', 'http://fedex-redelivery.net/update', 1, '["fake_delivery_notice", "suspicious_domain", "urgency"]'),

-- Medium legitimate emails
('email', 2, 'Your subscription renewal', 'Your Netflix subscription will renew on Jan 15, 2024. You can manage your subscription in your account settings.', 'info@netflix.com', 'https://www.netflix.com/account', 0, '[]'),

-- Hard phishing emails
('email', 3, 'IT Department: Required Security Update', 'All employees must install the latest security patch. Download and run the attached file before 5 PM today to maintain system access.', 'it-support@company-internal.net', 'https://company-updates.download/patch.exe', 1, '["impersonation", "malicious_attachment", "deadline_pressure", "authority_exploitation"]'),
('email', 3, 'Invoice Payment Due', 'Dear Sir/Madam, Your invoice #INV-2024-0891 is overdue. Please remit payment to avoid service interruption.', 'accounts@vendor-services.com', 'https://secure-payment-portal.net/pay', 1, '["fake_invoice", "payment_urgency", "professional_appearance"]'),

-- SMS scenarios
('sms', 1, NULL, 'URGENT: Your bank account has been locked. Click here to unlock: http://bank-unlock.xyz/secure', '555-0100', 'http://bank-unlock.xyz/secure', 1, '["urgency", "suspicious_url", "impersonation", "unexpected_message"]'),
('sms', 2, NULL, 'Your package is waiting. Confirm delivery address: https://delivery-confirm.net/track?id=8892', '555-PKGE', 'https://delivery-confirm.net/track?id=8892', 1, '["fake_delivery", "suspicious_short_url", "unexpected_message"]'),
('sms', 1, NULL, 'Hi! Your appointment is confirmed for tomorrow at 3 PM. Reply CANCEL to reschedule.', 'HealthClinic', NULL, 0, '[]'),

-- Website scenarios
('website', 2, NULL, 'This is a fake login page that looks like a bank website but has a suspicious URL and missing security indicators.', NULL, 'http://secure-bank-login.net', 1, '["no_https", "suspicious_domain", "missing_security_badges"]'),
('website', 3, NULL, 'This website appears legitimate with HTTPS but is actually a sophisticated phishing site mimicking a popular service.', NULL, 'https://paypa1.com/login', 1, '["typosquatting", "visual_similarity", "fake_ssl_certificate"]'),
('website', 1, NULL, 'Official GitHub login page with proper security indicators and valid certificate.', NULL, 'https://github.com/login', 0, '[]');
