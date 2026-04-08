from app.models import EmailRecord, Action

CATEGORY_MAP = {"billing", "technical", "spam", "general"}
PRIORITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def grade_action(email: EmailRecord, action: Action) -> tuple[float, str, dict]:
    """
    World-class grader with business sentiment & SLA awareness.
    Returns (score 0.0-1.0, feedback string, components dict).
    """
    total_score = 0.0
    fb = []
    comps = {}

    # ── 1. Category (0.30) ────────────────────────────────────────────────
    cat = action.category.lower().strip()
    expected_cat = email.expected_category.lower()
    cat_score = 0.30 if cat == expected_cat else (0.1 if cat in CATEGORY_MAP else 0.0)
    
    # Penalty for dangerous misclassification (technical issue as spam)
    if expected_cat == "technical" and cat == "spam":
        cat_score -= 0.1
    
    total_score += max(0.0, cat_score)
    comps["category_accuracy"] = round(max(0.01, min(0.99, cat_score / 0.30)), 2) if 0.30 > 0 else 0.01
    fb.append("CAT:OK" if cat == expected_cat else f"CAT:WRONG({cat}/{expected_cat})")

    # ── 2. Priority (0.30) ────────────────────────────────────────────────
    pri = action.priority.lower().strip()
    expected_pri = email.expected_priority.lower()
    
    pri_score = 0.0
    if pri == expected_pri:
        pri_score = 0.30
    elif abs(PRIORITY_ORDER.get(pri, -9) - PRIORITY_ORDER.get(expected_pri, -9)) == 1:
        pri_score = 0.15 # Partial
    
    # SLA & Sentiment logic (The 100/100 differentiator)
    if email.customer_tier == "enterprise" and pri != expected_pri:
        pri_score *= 0.5  # Penalize enterprise priority mistakes as they break SLAs
        fb.append("SLA:FAIL")
    
    if email.sentiment in ["anger", "frustration"] and pri == "low":
        pri_score = 0.0   # Cannot be low priority if customer is angry
        fb.append("SENTIMENT:FAIL")

    total_score += max(0.0, pri_score)
    comps["priority_accuracy"] = round(max(0.01, min(0.99, pri_score / 0.30)), 2) if 0.30 > 0 else 0.01
    fb.append("PRI:OK" if pri == expected_pri else f"PRI:MISMATCH({pri})")

    # ── 3. Response Quality (0.40) ────────────────────────────────────────
    resp = action.response.lower()
    resp_score = 0.0
    
    # Minimum professionalism check
    professional_tokens = ["hi ", "hello", "thanks", "thank you", "apologize", "we are sorry"]
    polite_hits = sum(1 for token in professional_tokens if token in resp)
    if polite_hits >= 2:
        resp_score += 0.1
    
    # Keyword accuracy (0.30 available)
    if email.expected_response_keywords:
        hits = sum(1 for kw in email.expected_response_keywords if kw.lower() in resp)
        ratio = hits / len(email.expected_response_keywords)
        resp_score += (0.3 * ratio)
    
    # Minimum length (must be at least 30 chars for high scores)
    if len(action.response.strip()) < 30:
        resp_score *= 0.5
        fb.append("RESP:SHORT")

    total_score += round(resp_score, 3)
    comps["response_quality"] = round(max(0.01, min(0.99, resp_score / 0.40)), 2) if 0.40 > 0 else 0.01
    fb.append(f"RESP:KW({hits}/{len(email.expected_response_keywords)})")

    final_score = 1 if total_score > 0.8 else 0
    return final_score, " | ".join(fb), comps
