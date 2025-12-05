import re
import urllib.parse
from typing import Dict, List, Tuple

# Known phishing indicators
SUSPICIOUS_TLDS = ['.xyz', '.top', '.win', '.work', '.click', '.link', '.download']
SUSPICIOUS_KEYWORDS = ['verify', 'urgent', 'suspended', 'locked', 'confirm', 'update', 'secure', 'account']
TRUSTED_DOMAINS = ['google.com', 'microsoft.com', 'amazon.com', 'github.com', 'facebook.com']

def analyze_url(url: str) -> Dict:
    """
    Analyze a URL for phishing indicators using threat detection techniques.
    Returns a dictionary with analysis results.
    """
    if not url:
        return {"is_suspicious": False, "indicators": [], "risk_score": 0}
    
    indicators = []
    risk_score = 0
    
    try:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        
        # Check for HTTPS
        if parsed.scheme != 'https':
            indicators.append("No HTTPS encryption")
            risk_score += 20
        
        # Check for suspicious TLDs
        for tld in SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                indicators.append(f"Suspicious domain extension: {tld}")
                risk_score += 25
                break
        
        # Check for IP address instead of domain
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
            indicators.append("IP address used instead of domain name")
            risk_score += 40
        
        # Check for suspicious keywords in URL
        url_lower = url.lower()
        for keyword in SUSPICIOUS_KEYWORDS:
            if keyword in url_lower:
                indicators.append(f"Suspicious keyword: '{keyword}'")
                risk_score += 10
        
        # Check for typosquatting (common misspellings of trusted domains)
        for trusted in TRUSTED_DOMAINS:
            if is_typosquatting(domain, trusted):
                indicators.append(f"Possible typosquatting of {trusted}")
                risk_score += 50
        
        # Check for excessive subdomains
        subdomain_count = domain.count('.')
        if subdomain_count > 3:
            indicators.append(f"Excessive subdomains ({subdomain_count})")
            risk_score += 15
        
        # Check for suspicious characters
        if any(char in domain for char in ['@', '-']):
            if domain.count('-') > 2:
                indicators.append("Excessive hyphens in domain")
                risk_score += 15
        
        # Check URL length
        if len(url) > 100:
            indicators.append("Unusually long URL")
            risk_score += 10
            
    except Exception as e:
        indicators.append(f"Error parsing URL: {str(e)}")
        risk_score += 30
    
    # Cap risk score at 100
    risk_score = min(risk_score, 100)
    
    return {
        "is_suspicious": risk_score >= 40,
        "indicators": indicators,
        "risk_score": risk_score,
        "threat_level": get_threat_level(risk_score)
    }

def is_typosquatting(domain: str, trusted_domain: str) -> bool:
    """
    Check if a domain is likely typosquatting a trusted domain.
    Uses Levenshtein-like logic for simple detection.
    """
    # Remove common TLD to compare base domains
    domain_base = domain.split('.')[0] if '.' in domain else domain
    trusted_base = trusted_domain.split('.')[0]
    
    # Check for character substitution (e.g., '0' for 'o', '1' for 'l')
    substitutions = {'0': 'o', '1': 'l', '5': 's', '3': 'e'}
    normalized_domain = domain_base
    for key, val in substitutions.items():
        normalized_domain = normalized_domain.replace(key, val)
    
    # Check if very similar after normalization
    if normalized_domain == trusted_base or trusted_base in normalized_domain:
        return True
    
    # Check for simple character additions/deletions
    if len(domain_base) >= len(trusted_base) - 2 and len(domain_base) <= len(trusted_base) + 2:
        similarity = sum(c1 == c2 for c1, c2 in zip(domain_base, trusted_base))
        if similarity >= len(trusted_base) - 2:
            return True
    
    return False

def get_threat_level(risk_score: int) -> str:
    """Convert risk score to threat level."""
    if risk_score >= 70:
        return "HIGH"
    elif risk_score >= 40:
        return "MEDIUM"
    elif risk_score >= 20:
        return "LOW"
    else:
        return "SAFE"

def analyze_email_content(subject: str, body: str, sender: str) -> Dict:
    """
    Analyze email content for phishing indicators.
    """
    indicators = []
    risk_score = 0
    
    # Check for urgent language
    urgent_words = ['urgent', 'immediately', 'action required', 'suspend', 'verify now', 'expires']
    for word in urgent_words:
        if word in subject.lower() or word in body.lower():
            indicators.append(f"Urgent language: '{word}'")
            risk_score += 15
    
    # Check for generic greetings
    if re.search(r'\b(dear (user|customer|sir|madam))\b', body.lower()):
        indicators.append("Generic greeting (not personalized)")
        risk_score += 10
    
    # Check for threats
    threat_words = ['suspend', 'terminate', 'locked', 'disabled', 'blocked']
    for word in threat_words:
        if word in subject.lower() or word in body.lower():
            indicators.append(f"Threatening language: '{word}'")
            risk_score += 20
    
    # Check for too good to be true offers
    if re.search(r'\$\d+[,\d]*|\bwin\b|\bwon\b|\bprize\b|\bfree\b', body.lower()):
        indicators.append("Suspicious offer or prize mentioned")
        risk_score += 25
    
    # Check sender domain
    if sender and '@' in sender:
        domain = sender.split('@')[1].lower()
        # Check for suspicious TLDs in sender
        for tld in SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                indicators.append(f"Sender has suspicious domain extension")
                risk_score += 20
                break
    
    risk_score = min(risk_score, 100)
    
    return {
        "is_suspicious": risk_score >= 40,
        "indicators": indicators,
        "risk_score": risk_score,
        "threat_level": get_threat_level(risk_score)
    }
