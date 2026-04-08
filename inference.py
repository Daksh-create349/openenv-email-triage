import os
import json
from openai import OpenAI
from app.env import EmailTriageEnv
from app.models import Action

# ── Load env vars ──────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional; fall back to shell env

# ── Proxy-Aware API Client Configuration ─────────────────────────────────────
# We prioritize "API_KEY" as it's the official variable used by the 
# OpenEnv competition proxy. We fall back to "OPENAI_API_KEY" for local dev.
api_key = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY") or "MISSING_KEY"
base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

TASKS_TO_RUN = ["easy", "medium", "hard"]

SYSTEM_PROMPT = """You are an expert customer support email triage agent.
For each email you receive, you must return ONLY valid JSON (no markdown, no backticks) with this exact structure:
{
  "category": "<billing|technical|spam|general>",
  "priority": "<low|medium|high|critical>",
  "response": "<professional reply to the customer>"
}

Business SLA Logic (CRITICAL):
- Enterprise Customers: Priority must ALWAYS be at least 'high' for any non-spam issue.
- Frustrated/Angry Customers: Priority must NEVER be 'low'.
- Production Outages: Always 'critical'.
- Security/Data Breach: Always 'critical'.

Category definitions:
- billing: payments, charges, invoices, refunds, subscriptions
- technical: bugs, crashes, errors, SSO, integrations, performance, access
- spam: unsolicited promotions, phishing, scam emails
- general: feature requests, questions, feedback, GDPR, other
"""


def clean_json(content: str) -> str:
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        inner = [l for l in lines if not l.startswith("```")]
        content = "\n".join(inner).strip()
    return content


def run_task(task_id: str) -> float:
    env = EmailTriageEnv(task_id=task_id)
    obs = env.reset()

    print("[START]")

    step_id = 0
    total_score = 0.0

    while True:
        email = obs.current_email
        prompt = (
            f"Email:\n"
            f"From: {email.sender}\n"
            f"Subject: {email.subject}\n"
            f"Body: {email.body}\n\n"
            f"Return ONLY valid JSON (no markdown, no backticks):\n"
            f'{{"category":"billing/technical/spam/general","priority":"low/medium/high/critical","response":"your reply"}}'
        )

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
            )
            content = response.choices[0].message.content
            content = clean_json(content)
            
            action_dict = json.loads(content)
            action = Action(**action_dict)
        except Exception as e:
            print(f"ERROR (Step {step_id}): {e}")
            if "api_key" in str(e).lower() or "401" in str(e):
                print("CRITICAL: Authentication failed. Check your OPENAI_API_KEY.")
            break

        obs, reward, done, info = env.step(action)

        print(f"[STEP] {step_id} | reward={reward.score}")

        total_score += reward.score
        step_id += 1

        if done:
            break

    # The environment already normalizes step_score so the sum is strictly in (0, 1)
    # Give it one more safety clamp just in case floating point math gets weird.
    total_score = max(0.01, min(0.99, total_score))
    print(f"[END] total_score={round(total_score, 4)}")
    return total_score



if __name__ == "__main__":
    all_scores = {}
    grand_total = 0.0

    for task_id in TASKS_TO_RUN:
        score = run_task(task_id)
        all_scores[task_id] = round(score, 4)
        grand_total += score

    print("\n" + "=" * 60)
    print(f"[SUMMARY] model={MODEL}")
    for tid, s in all_scores.items():
        print(f"  task={tid} total_score={s}")
    print(f"  grand_total={round(grand_total, 4)}")
    print("=" * 60)