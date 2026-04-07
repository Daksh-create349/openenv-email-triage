---
title: My OpenEnv Email Triage
emoji: 📬
colorFrom: indigo
colorTo: red
sdk: docker
pinned: false
license: mit
tags:
- openenv
---



### 🧐 What is this? (In Simple Terms)
Imagine a **Flight Simulator for Customer Support Agents**. 

- **The Simulator (The Env):** This project is a virtual "Support Dashboard" that hands out 30 real-world customer emails. Some are easy (spam), but some are high-stakes (Data Breaches, Enterprise Outages).
- **The Pilot (The AI Agent):** Your AI model acts as the pilot. It must read the emails, figure out the category (Billing/Technical/Spam), set the priority, and write a polite reply.
- **The Score:** The simulator "grades" the AI's performance. It looks for accuracy, politeness, and how well it handles **VIP (Enterprise) customers**.

---

### 🚀 Quick Start (How to Run)

#### **1. Setup**
```bash
cd /Users/dakshsrivastava/Desktop/openenv-email-triage
source venv/bin/activate
pip install -r requirements.txt
```

#### **2. Start the Simulator (Terminal 1)**
```bash
uvicorn server:app --host 0.0.0.0 --port 7860
```

#### **3. Start the AI Agent (Terminal 2)**
```bash
cd /Users/dakshsrivastava/Desktop/openenv-email-triage
source venv/bin/activate
set -a && source .env && set +a
python inference.py
```

---

## 🏗️ Technical Specification

### 🎮 Action Space
The agent receives an email and must return a JSON object:
```json
{
  "category": "billing | technical | spam | general",
  "priority": "low | medium | high | critical",
  "response": "Professional reply (minimum 30 characters)"
}
```

### 👁️ Observation Space
At each step, the agent sees:
| Field | Type | Description |
|-------|------|-------------|
| `subject` | string | Email subject |
| `body` | string | Email body |
| `customer_tier` | string | **free**, **pro**, or **enterprise** (SLA target) |
| `sentiment` | string | **anger**, **frustration**, **neutral**, or **positive** |
| `thread_id` | string | Unique ID for the conversation thread |

---

## 🏆 Reward Function (100/100 Logic)

The reward is a continuous value between `0.0` and `1.0`.

| Component | Weight | Logic |
|-----------|--------|-------|
| **Category** | 0.30 | Exact match vs ground truth. |
| **Priority** | 0.30 | Matches ground truth urgency. Penalized 2x if **Enterprise SLA** is breached or if **Angry** customers are assigned "low" priority. |
| **Response** | 0.40 | Matches ground-truth keywords + Tone Bonus for politeness ("Apologize", "Thanks"). |

> [!IMPORTANT]
> **SLA Penalty:** If the customer is **Enterprise**, failing the priority check results in a 50% reduction in that step's score components. Business value is paramount.

---

## 📋 Task Tiers

| Task | Difficulty | Strategy |
|------|-----------|----------|
| `easy` | 🟢 Easy | Unambiguous signals (e.g., clear spam, clear failed payment). |
| `medium` | 🟡 Medium | Nuanced Priority: Identifying urgent issues hidden in neutral text. |
| `hard` | 🔴 Hard | High-stakes: GDPR data deletion, RCE security exploits, legal threats. |

---

## 🖼️ Project Structure
```bash
.
├── app/
│   ├── env.py        # Core Logic: reset(), step(), state()
│   ├── data.py       # 30 high-fidelity email records
│   ├── grader.py     # Deterministic scoring engine with SLA/Sentiment logic
│   ├── models.py     # Typed Pydantic models for Action/Observation/Reward
│   └── tasks.py      # Tiered difficulty definitions
├── server.py         # FastAPI instance for HF Space deployment
├── inference.py      # Official baseline AI agent
├── openenv.yaml      # Environment metadata for OpenEnv spec
└── Dockerfile        # Container config for 7860 port launch
```

---

## 🚀 Deployment (Hugging Face)
This project is fully containerized and compatible with Hugging Face Spaces. 
1. Build the image: `docker build -t email-env .`
2. Run locally: `docker run -p 7860:7860 email-env`
3. Environment variables required: `OPENAI_API_KEY`, `API_BASE_URL`, `MODEL_NAME`.

---

## 📊 Baseline Benchmark
Scores generated using `gpt-4o-mini` at `temperature=0.0`:
- **Easy:** 8.8 / 10.0
- **Medium:** 7.6 / 10.0
- **Hard:** 6.2 / 10.0
- **Grand Total:** 22.6 / 30.0

Run `python inference.py` to reproduce these scores on your current local machine.
