// Configuration - Update based on your deployment environment
// For production, use environment-specific configuration
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? "http://127.0.0.1:5000"  // Development
    : "/api";  // Production (assumes API is served from same origin)

// State management
let currentScenario = null;
let startTime = null;
let timerInterval = null;
let currentUser = null;

// DOM Elements - Auth
const authSection = document.getElementById("authSection");
const appSection = document.getElementById("appSection");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const authMessage = document.getElementById("authMessage");
const logoutBtn = document.getElementById("logoutBtn");
const userInfo = document.getElementById("userInfo");
const userPoints = document.getElementById("userPoints");
const userLevel = document.getElementById("userLevel");

// DOM Elements - Navigation
const navButtons = document.querySelectorAll(".nav-btn");
const viewContents = document.querySelectorAll(".view-content");

// DOM Elements - Training
const startTrainingBtn = document.getElementById("startTrainingBtn");
const scenarioContainer = document.getElementById("scenarioContainer");
const resultContainer = document.getElementById("resultContainer");
const scenarioContent = document.getElementById("scenarioContent");
const scenarioType = document.getElementById("scenarioType");
const difficultyLevel = document.getElementById("difficultyLevel");
const timer = document.getElementById("timer");
const legitimateBtn = document.getElementById("legitimateBtn");
const phishingBtn = document.getElementById("phishingBtn");

// DOM Elements - Stats
const streakValue = document.getElementById("streakValue");
const accuracyValue = document.getElementById("accuracyValue");
const completedValue = document.getElementById("completedValue");

// DOM Elements - Tools
const analyzeUrlBtn = document.getElementById("analyzeUrlBtn");
const analyzeEmailBtn = document.getElementById("analyzeEmailBtn");
const urlInput = document.getElementById("urlInput");
const urlResult = document.getElementById("urlResult");
const emailSender = document.getElementById("emailSender");
const emailSubject = document.getElementById("emailSubject");
const emailBody = document.getElementById("emailBody");
const emailResult = document.getElementById("emailResult");

// ============== AUTH ==============

loginTab.addEventListener("click", () => {
    loginTab.classList.add("active");
    registerTab.classList.remove("active");
    loginForm.style.display = "flex";
    registerForm.style.display = "none";
    hideMessage();
});

registerTab.addEventListener("click", () => {
    registerTab.classList.add("active");
    loginTab.classList.remove("active");
    registerForm.style.display = "flex";
    loginForm.style.display = "none";
    hideMessage();
});

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("loginUsername").value;
    const password = document.getElementById("loginPassword").value;
    
    try {
        const response = await fetch(`${API_BASE}/api/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.user;
            showApp();
            showMessage("Login successful!", "success");
        } else {
            showMessage(data.error || "Login failed", "error");
        }
    } catch (error) {
        showMessage("Connection error. Please try again.", "error");
        console.error(error);
    }
});

registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("registerUsername").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;
    
    try {
        const response = await fetch(`${API_BASE}/api/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage("Registration successful! Please login.", "success");
            loginTab.click();
            registerForm.reset();
        } else {
            showMessage(data.error || "Registration failed", "error");
        }
    } catch (error) {
        showMessage("Connection error. Please try again.", "error");
        console.error(error);
    }
});

logoutBtn.addEventListener("click", async () => {
    try {
        await fetch(`${API_BASE}/api/logout`, {
            method: "POST",
            credentials: "include"
        });
        currentUser = null;
        showAuth();
    } catch (error) {
        console.error(error);
    }
});

function showAuth() {
    authSection.style.display = "flex";
    appSection.style.display = "none";
    userInfo.style.display = "none";
}

function showApp() {
    authSection.style.display = "none";
    appSection.style.display = "block";
    userInfo.style.display = "flex";
    updateUserInfo();
    loadProfile();
}

function updateUserInfo() {
    if (currentUser) {
        userPoints.textContent = `Points: ${currentUser.total_points}`;
        userLevel.textContent = `Level: ${currentUser.difficulty_level}`;
    }
}

function showMessage(message, type) {
    authMessage.textContent = message;
    authMessage.className = `message ${type} show`;
    setTimeout(hideMessage, 5000);
}

function hideMessage() {
    authMessage.className = "message";
}

// ============== NAVIGATION ==============

navButtons.forEach(button => {
    button.addEventListener("click", () => {
        const viewName = button.getAttribute("data-view");
        switchView(viewName);
        
        // Load data for the view
        if (viewName === "leaderboard") loadLeaderboard();
        else if (viewName === "achievements") loadAchievements();
        else if (viewName === "analytics") loadAnalytics();
    });
});

function switchView(viewName) {
    navButtons.forEach(btn => btn.classList.remove("active"));
    viewContents.forEach(view => view.classList.remove("active"));
    
    document.querySelector(`[data-view="${viewName}"]`).classList.add("active");
    document.getElementById(`${viewName}View`).classList.add("active");
}

// ============== TRAINING ==============

startTrainingBtn.addEventListener("click", loadNewScenario);

async function loadNewScenario() {
    try {
        const response = await fetch(`${API_BASE}/api/scenario/next`, {
            credentials: "include"
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentScenario = data.scenario;
            displayScenario(data.scenario);
            scenarioContainer.style.display = "block";
            resultContainer.style.display = "none";
            startTrainingBtn.disabled = true;
            startTimer();
        } else {
            alert(data.error || "Failed to load scenario");
        }
    } catch (error) {
        console.error(error);
        alert("Connection error. Please try again.");
    }
}

function displayScenario(scenario) {
    // Set type badge
    scenarioType.textContent = scenario.scenario_type.toUpperCase();
    scenarioType.className = `badge badge-${scenario.scenario_type}`;
    
    // Set difficulty badge
    const difficultyNames = ["", "Easy", "Medium", "Hard", "Expert"];
    difficultyLevel.textContent = difficultyNames[scenario.difficulty_level] || "Unknown";
    difficultyLevel.className = "badge badge-difficulty";
    
    // Display content based on type
    let content = "";
    
    if (scenario.scenario_type === "email") {
        content = `
            <div class="field">
                <span class="field-label">From:</span>
                <div class="field-value">${scenario.sender || "Unknown"}</div>
            </div>
            <div class="field">
                <span class="field-label">Subject:</span>
                <div class="field-value">${scenario.subject || "No Subject"}</div>
            </div>
            <div class="field">
                <span class="field-label">Message:</span>
                <div class="field-value">${scenario.body}</div>
            </div>
            ${scenario.url ? `
            <div class="field">
                <span class="field-label">Link:</span>
                <div class="field-value">${scenario.url}</div>
            </div>` : ""}
        `;
    } else if (scenario.scenario_type === "sms") {
        content = `
            <div class="field">
                <span class="field-label">From:</span>
                <div class="field-value">${scenario.sender || "Unknown"}</div>
            </div>
            <div class="field">
                <span class="field-label">Message:</span>
                <div class="field-value">${scenario.body}</div>
            </div>
            ${scenario.url ? `
            <div class="field">
                <span class="field-label">Link:</span>
                <div class="field-value">${scenario.url}</div>
            </div>` : ""}
        `;
    } else if (scenario.scenario_type === "website") {
        content = `
            <div class="field">
                <span class="field-label">URL:</span>
                <div class="field-value">${scenario.url || "N/A"}</div>
            </div>
            <div class="field">
                <span class="field-label">Description:</span>
                <div class="field-value">${scenario.body}</div>
            </div>
        `;
    }
    
    scenarioContent.innerHTML = content;
    
    // Enable answer buttons
    legitimateBtn.disabled = false;
    phishingBtn.disabled = false;
}

function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        timer.textContent = `⏱️ ${elapsed}s`;
    }, 1000);
}

function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    return Math.floor((Date.now() - startTime) / 1000);
}

legitimateBtn.addEventListener("click", () => submitAnswer(false));
phishingBtn.addEventListener("click", () => submitAnswer(true));

async function submitAnswer(isPhishing) {
    const timeTaken = stopTimer();
    
    // Disable buttons
    legitimateBtn.disabled = true;
    phishingBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE}/api/scenario/submit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
                scenario_id: currentScenario.id,
                user_answer: isPhishing,
                time_taken: timeTaken
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResult(data);
            updateStats(data.statistics);
            
            // Update user points
            if (currentUser) {
                currentUser.total_points += data.points_earned;
                updateUserInfo();
            }
        } else {
            alert(data.error || "Failed to submit answer");
        }
    } catch (error) {
        console.error(error);
        alert("Connection error. Please try again.");
    }
}

function displayResult(result) {
    scenarioContainer.style.display = "none";
    resultContainer.style.display = "block";
    startTrainingBtn.disabled = false;
    
    const isCorrect = result.is_correct;
    const correctAnswer = result.correct_answer ? "Phishing" : "Legitimate";
    
    let html = `
        <div class="result-header ${isCorrect ? 'result-correct' : 'result-incorrect'}">
            ${isCorrect ? '✅ Correct!' : '❌ Incorrect'}
        </div>
        <div class="result-points">
            Points earned: +${result.points_earned}
        </div>
        <div class="result-explanation">
            <h4>Explanation</h4>
            <p><strong>Correct Answer:</strong> This was a <strong>${correctAnswer}</strong> ${currentScenario.scenario_type}.</p>
    `;
    
    if (result.explanation.indicators && result.explanation.indicators.length > 0) {
        html += `
            <p><strong>Phishing Indicators:</strong></p>
            <ul>
                ${result.explanation.indicators.map(ind => `<li>${ind}</li>`).join('')}
            </ul>
        `;
    }
    
    if (result.explanation.sender) {
        html += `<p><strong>Sender:</strong> ${result.explanation.sender}</p>`;
    }
    if (result.explanation.url) {
        html += `<p><strong>URL:</strong> ${result.explanation.url}</p>`;
    }
    
    html += `</div>`;
    
    // Show new achievements
    if (result.new_achievements && result.new_achievements.length > 0) {
        html += `<div class="achievement-popup">`;
        result.new_achievements.forEach(ach => {
            html += `<div>🎉 New Achievement Unlocked: ${ach.icon} ${ach.name}!</div>`;
        });
        html += `</div>`;
    }
    
    html += `<button class="btn-primary" onclick="loadNewScenario()">Next Scenario</button>`;
    
    resultContainer.innerHTML = html;
}

function updateStats(stats) {
    streakValue.textContent = stats.current_streak;
    accuracyValue.textContent = `${stats.accuracy}%`;
    completedValue.textContent = stats.scenarios_completed;
}

// ============== PROFILE ==============

async function loadProfile() {
    try {
        const response = await fetch(`${API_BASE}/api/user/profile`, {
            credentials: "include"
        });
        
        const data = await response.json();
        
        if (response.ok && data.statistics) {
            updateStats({
                current_streak: data.statistics.current_streak,
                accuracy: data.statistics.accuracy_percentage.toFixed(2),
                scenarios_completed: data.statistics.scenarios_completed
            });
        }
    } catch (error) {
        console.error(error);
    }
}

// ============== LEADERBOARD ==============

async function loadLeaderboard() {
    try {
        const response = await fetch(`${API_BASE}/api/leaderboard?limit=10`, {
            credentials: "include"
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayLeaderboard(data.leaderboard);
        }
    } catch (error) {
        console.error(error);
    }
}

function displayLeaderboard(leaders) {
    const table = document.getElementById("leaderboardTable");
    
    let html = `
        <div class="leaderboard-row leaderboard-header">
            <div>Rank</div>
            <div>Username</div>
            <div>Points</div>
            <div>Level</div>
            <div>Accuracy</div>
        </div>
    `;
    
    leaders.forEach((leader, index) => {
        const rank = index + 1;
        const rankClass = rank <= 3 ? `rank-${rank}` : 'rank-other';
        
        html += `
            <div class="leaderboard-row">
                <div class="rank-badge ${rankClass}">${rank}</div>
                <div>${leader.username}</div>
                <div>${leader.total_points}</div>
                <div>${leader.difficulty_level}</div>
                <div>${leader.accuracy_percentage ? leader.accuracy_percentage.toFixed(1) : 0}%</div>
            </div>
        `;
    });
    
    table.innerHTML = html;
}

// ============== ACHIEVEMENTS ==============

async function loadAchievements() {
    try {
        const response = await fetch(`${API_BASE}/api/achievements`, {
            credentials: "include"
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayAchievements(data.all_achievements, data.earned_achievements);
        }
    } catch (error) {
        console.error(error);
    }
}

function displayAchievements(allAchievements, earnedAchievements) {
    const grid = document.getElementById("achievementsGrid");
    const earnedIds = new Set(earnedAchievements.map(a => a.id));
    
    let html = "";
    
    allAchievements.forEach(achievement => {
        const isEarned = earnedIds.has(achievement.id);
        const cardClass = isEarned ? "achievement-card earned" : "achievement-card locked";
        
        html += `
            <div class="${cardClass}">
                <div class="achievement-icon">${achievement.icon}</div>
                <div class="achievement-name">${achievement.name}</div>
                <div class="achievement-description">${achievement.description}</div>
                <div class="achievement-progress">
                    ${isEarned ? '✓ Unlocked' : `Requires: ${achievement.criteria_value} ${achievement.criteria_type}`}
                </div>
            </div>
        `;
    });
    
    grid.innerHTML = html;
}

// ============== ANALYTICS ==============

async function loadAnalytics() {
    try {
        const response = await fetch(`${API_BASE}/api/analytics/user`, {
            credentials: "include"
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayAnalytics(data);
        }
    } catch (error) {
        console.error(error);
    }
}

function displayAnalytics(data) {
    const content = document.getElementById("analyticsContent");
    const stats = data.statistics || {};
    
    let html = `
        <div class="analytics-card">
            <h3>Overall Statistics</h3>
            <div class="analytics-grid">
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.total_attempts || 0}</div>
                    <div class="analytics-stat-label">Total Attempts</div>
                </div>
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.correct_attempts || 0}</div>
                    <div class="analytics-stat-label">Correct</div>
                </div>
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.accuracy_percentage ? stats.accuracy_percentage.toFixed(1) : 0}%</div>
                    <div class="analytics-stat-label">Accuracy</div>
                </div>
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.current_streak || 0}</div>
                    <div class="analytics-stat-label">Current Streak</div>
                </div>
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.best_streak || 0}</div>
                    <div class="analytics-stat-label">Best Streak</div>
                </div>
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.scenarios_completed || 0}</div>
                    <div class="analytics-stat-label">Completed</div>
                </div>
            </div>
        </div>

        <div class="analytics-card">
            <h3>Phishing Detection Performance</h3>
            <div class="analytics-grid">
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.phishing_detected || 0}</div>
                    <div class="analytics-stat-label">Phishing Detected</div>
                </div>
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.phishing_missed || 0}</div>
                    <div class="analytics-stat-label">Phishing Missed</div>
                </div>
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${stats.false_positives || 0}</div>
                    <div class="analytics-stat-label">False Positives</div>
                </div>
            </div>
        </div>
    `;
    
    if (data.performance_by_difficulty && data.performance_by_difficulty.length > 0) {
        html += `
            <div class="analytics-card">
                <h3>Performance by Difficulty</h3>
                <div class="analytics-grid">
        `;
        
        const diffNames = ["", "Easy", "Medium", "Hard", "Expert"];
        data.performance_by_difficulty.forEach(perf => {
            const accuracy = perf.total > 0 ? ((perf.correct / perf.total) * 100).toFixed(1) : 0;
            html += `
                <div class="analytics-stat">
                    <div class="analytics-stat-value">${accuracy}%</div>
                    <div class="analytics-stat-label">${diffNames[perf.difficulty_level]} (${perf.total} attempts)</div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
    }
    
    content.innerHTML = html;
}

// ============== DETECTION TOOLS ==============

analyzeUrlBtn.addEventListener("click", async () => {
    const url = urlInput.value.trim();
    
    if (!url) {
        alert("Please enter a URL");
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/analyze/url`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ url })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayUrlAnalysis(data);
        } else {
            alert(data.error || "Analysis failed");
        }
    } catch (error) {
        console.error(error);
        alert("Connection error. Please try again.");
    }
});

function displayUrlAnalysis(analysis) {
    const result = urlResult;
    const threatClass = `threat-${analysis.threat_level.toLowerCase()}`;
    
    let html = `
        <h4>URL Analysis Results</h4>
        <div class="threat-level ${threatClass}">${analysis.threat_level} RISK</div>
        <p><strong>Risk Score:</strong> ${analysis.risk_score}/100</p>
        <p><strong>Suspicious:</strong> ${analysis.is_suspicious ? 'Yes ⚠️' : 'No ✅'}</p>
    `;
    
    if (analysis.indicators && analysis.indicators.length > 0) {
        html += `
            <div class="indicator-list">
                <strong>Indicators Found:</strong>
                ${analysis.indicators.map(ind => `<div class="indicator-item">${ind}</div>`).join('')}
            </div>
        `;
    } else {
        html += `<p>✅ No suspicious indicators found.</p>`;
    }
    
    result.innerHTML = html;
    result.classList.add("show");
}

analyzeEmailBtn.addEventListener("click", async () => {
    const sender = emailSender.value.trim();
    const subject = emailSubject.value.trim();
    const body = emailBody.value.trim();
    
    if (!body) {
        alert("Please enter email body");
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/analyze/email`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ sender, subject, body })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayEmailAnalysis(data);
        } else {
            alert(data.error || "Analysis failed");
        }
    } catch (error) {
        console.error(error);
        alert("Connection error. Please try again.");
    }
});

function displayEmailAnalysis(analysis) {
    const result = emailResult;
    const threatClass = `threat-${analysis.threat_level.toLowerCase()}`;
    
    let html = `
        <h4>Email Analysis Results</h4>
        <div class="threat-level ${threatClass}">${analysis.threat_level} RISK</div>
        <p><strong>Risk Score:</strong> ${analysis.risk_score}/100</p>
        <p><strong>Suspicious:</strong> ${analysis.is_suspicious ? 'Yes ⚠️' : 'No ✅'}</p>
    `;
    
    if (analysis.indicators && analysis.indicators.length > 0) {
        html += `
            <div class="indicator-list">
                <strong>Indicators Found:</strong>
                ${analysis.indicators.map(ind => `<div class="indicator-item">${ind}</div>`).join('')}
            </div>
        `;
    } else {
        html += `<p>✅ No suspicious indicators found.</p>`;
    }
    
    result.innerHTML = html;
    result.classList.add("show");
}

// Initialize
showAuth();
