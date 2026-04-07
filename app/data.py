from app.models import EmailRecord

EMAILS: list[EmailRecord] = [
    # ── EASY (unambiguous signals) ──────────────────────────────────────────
    EmailRecord(
        id=1, difficulty="easy", sentiment="positive", customer_tier="free",
        subject="Congratulations! You won a free iPhone 15!",
        sender="promo@win-prizes-now.xyz",
        body="Dear customer, you have been selected as today's lucky winner! Click the link below to claim your free iPhone 15 http://totally-not-scam.xyz/claim",
        timestamp="2024-01-15T08:00:00Z",
        expected_category="spam", expected_priority="low",
        expected_response_keywords=["spam", "ignore", "suspicious"]
    ),
    EmailRecord(
        id=2, difficulty="easy", sentiment="frustration", customer_tier="pro",
        subject="Double charge on my credit card",
        sender="alice.johnson@gmail.com",
        body="Hi, I noticed I was charged $49.99 twice this month for my subscription. My account is alice.johnson@gmail.com. Please refund.",
        timestamp="2024-01-15T09:00:00Z",
        expected_category="billing", expected_priority="high",
        expected_response_keywords=["refund", "apologize", "duplicate"]
    ),
    EmailRecord(
        id=3, difficulty="easy", sentiment="neutral", customer_tier="enterprise",
        subject="Invoice for ACM Corp #ACM-2024-001",
        sender="finance@acmecorp.com",
        body="Hello, we have not received our invoice for December. Please resend for our accounting team.",
        timestamp="2024-01-15T10:00:00Z",
        expected_category="billing", expected_priority="high", # Higher because Enterprise
        expected_response_keywords=["invoice", "resend", "account"]
    ),
    EmailRecord(
        id=4, difficulty="easy", sentiment="frustration", customer_tier="free",
        subject="Cannot login to my account",
        sender="david.lee@gmail.com",
        body="I cannot log into my account. I keep getting 'Invalid password'. Help reset access.",
        timestamp="2024-01-15T11:00:00Z",
        expected_category="technical", expected_priority="medium",
        expected_response_keywords=["password", "reset", "access"]
    ),
    EmailRecord(
        id=5, difficulty="easy", sentiment="neutral", customer_tier="free",
        subject="Work from home opportunity!!!",
        sender="jobs@quick-cash.biz",
        body="Make $5000 per week! Send $50 fee today!",
        timestamp="2024-01-15T11:15:00Z",
        expected_category="spam", expected_priority="low",
        expected_response_keywords=["spam", "ignore", "scam"]
    ),
    EmailRecord(
        id=6, difficulty="easy", sentiment="neutral", customer_tier="pro",
        subject="How do I add a new team member?",
        sender="sarah@agency.com",
        body="Hi, I just upgraded to Pro and want to add my colleague to the team. Where is the invite button?",
        timestamp="2024-01-15T12:00:00Z",
        expected_category="general", expected_priority="low",
        expected_response_keywords=["team", "invite", "member", "button"]
    ),
    EmailRecord(
        id=7, difficulty="easy", sentiment="neutral", customer_tier="enterprise",
        subject="White-labelling options",
        sender="mark@globalcorp.com",
        body="Does the enterprise plan include white-labelling for the client dashboard?",
        timestamp="2024-01-15T12:30:00Z",
        expected_category="general", expected_priority="medium",
        expected_response_keywords=["enterprise", "white-label", "dashboard", "branding"]
    ),
    EmailRecord(
        id=8, difficulty="easy", sentiment="neutral", customer_tier="free",
        subject="Feature request: mobile app",
        sender="tony@gmail.com",
        body="Your web app is great! Do you have plans for an iOS app?",
        timestamp="2024-01-15T13:00:00Z",
        expected_category="general", expected_priority="low",
        expected_response_keywords=["mobile", "iOS", "feedback", "roadmap"]
    ),
    EmailRecord(
        id=9, difficulty="easy", sentiment="frustration", customer_tier="pro",
        subject="API documentation is confusing",
        sender="dev@startup.io",
        body="I'm trying to use the /v1/export endpoint but the docs have an error in the JSON example. Please fix.",
        timestamp="2024-01-15T13:30:00Z",
        expected_category="technical", expected_priority="medium",
        expected_response_keywords=["API", "docs", "fix", "documentation"]
    ),
    EmailRecord(
        id=10, difficulty="easy", sentiment="neutral", customer_tier="enterprise",
        subject="Sales renewal for 2024",
        sender="procurement@megacorp.com",
        body="Hi, our contract expires next month. Please send the renewal proposal for 500 seats.",
        timestamp="2024-01-15T14:00:00Z",
        expected_category="billing", expected_priority="high",
        expected_response_keywords=["renewal", "proposal", "contract", "seats"]
    ),

    # ── MEDIUM (business logic, sentiment sensitivity) ──────────────────
    EmailRecord(
        id=11, difficulty="medium", sentiment="anger", customer_tier="enterprise",
        subject="URGENT: PRODUCTION DOWN - LOCKOUT",
        sender="cio@financial-serv.com",
        body="Our entire trading floor is locked out. Your SSO update broke our login. We are losing $50k per hour. Fix this NOW.",
        timestamp="2024-01-15T14:30:00Z",
        expected_category="technical", expected_priority="critical",
        expected_response_keywords=["SSO", "production", "urgent", "apologize", "immediate", "restored"]
    ),
    EmailRecord(
        id=12, difficulty="medium", sentiment="frustration", customer_tier="pro",
        subject="Refund for unused months",
        sender="lee@startup.io",
        body="We pivoted our business and don't need your tool. I want a refund for the remaining 8 months on our annual plan. Your policy is unclear.",
        timestamp="2024-01-15T15:00:00Z",
        expected_category="billing", expected_priority="medium",
        expected_response_keywords=["refund", "annual", "policy", "unused", "process"]
    ),
    EmailRecord(
        id=13, difficulty="medium", sentiment="neutral", customer_tier="enterprise",
        subject="Quarterly security audit",
        sender="sec-ops@megacorp.com",
        body="Attached is our mandatory security questionnaire. Please complete by EOD Friday to maintain compliance.",
        timestamp="2024-01-15T15:30:00Z",
        expected_category="general", expected_priority="high",
        expected_response_keywords=["security", "compliance", "audit", "questionnaire", "Friday"]
    ),
    EmailRecord(
        id=14, difficulty="medium", sentiment="anger", customer_tier="free",
        subject="Cancel my account IMMEDIATELY",
        sender="angry_user@yahoo.com",
        body="I've been trying to cancel for 3 days and the button doesn't work. If you charge me again I will call my bank for a chargeback.",
        timestamp="2024-01-15T16:00:00Z",
        expected_category="billing", expected_priority="high",
        expected_response_keywords=["cancel", "apologize", "confirm", "chargeback", "process"]
    ),
    EmailRecord(
        id=15, difficulty="medium", sentiment="neutral", customer_tier="pro",
        subject="Zapier integration intermittent errors",
        sender="marketing@growth.io",
        body="Our zaps are failing with 500 errors from your side. It happens roughly 1 out of 10 times. Please check logs.",
        timestamp="2024-01-15T16:30:00Z",
        expected_category="technical", expected_priority="medium",
        expected_response_keywords=["Zapier", "errors", "500", "logs", "intermittent", "investigate"]
    ),
    EmailRecord(
        id=16, difficulty="medium", sentiment="frustration", customer_tier="enterprise",
        subject="Missing features after upgrade",
        sender="admin@big-law.com",
        body="We upgraded to Enterprise for the audit logs but the feature still isn't showing in our settings. This is blocking our internal compliance check.",
        timestamp="2024-01-15T17:00:00Z",
        expected_category="technical", expected_priority="high",
        expected_response_keywords=["Enterprise", "audit logs", "settings", "compliance", "enable"]
    ),
    EmailRecord(
        id=17, difficulty="medium", sentiment="positive", customer_tier="pro",
        subject="Affiliate program query",
        sender="influencer@tech.com",
        body="Hi, I have a large audience and want to know if you offer an affiliate commission for referrals?",
        timestamp="2024-01-15T17:30:00Z",
        expected_category="general", expected_priority="low",
        expected_response_keywords=["affiliate", "referral", "commission", "program"]
    ),
    EmailRecord(
        id=18, difficulty="medium", sentiment="frustration", customer_tier="enterprise",
        subject="CSV Export is missing data columns",
        sender="analyst@retail-chain.com",
        body="The CSV export for 'Sales Report' is missing the 'Tax' column which we need for VAT filings in Europe. This was working last week.",
        timestamp="2024-01-15T18:00:00Z",
        expected_category="technical", expected_priority="high",
        expected_response_keywords=["CSV", "export", "column", "VAT", "sales", "report"]
    ),
    EmailRecord(
        id=19, difficulty="medium", sentiment="neutral", customer_tier="free",
        subject="Password reset link not arriving",
        sender="test@gmail.com",
        body="I've clicked reset 5 times. No email in spam or inbox. Can you manually reset?",
        timestamp="2024-01-15T18:30:00Z",
        expected_category="technical", expected_priority="medium",
        expected_response_keywords=["password", "reset", "manual", "link"]
    ),
    EmailRecord(
        id=20, difficulty="medium", sentiment="frustration", customer_tier="pro",
        subject="Wrong billing address on invoice",
        sender="founder@startup.io",
        body="Invoice #INV-928 has our old address. Our new office is at 123 Main St. We need a corrected PDF for tax purposes.",
        timestamp="2024-01-15T19:00:00Z",
        expected_category="billing", expected_priority="low",
        expected_response_keywords=["invoice", "address", "tax", "correct", "PDF"]
    ),

    # ── HARD (Legal, Security, Catastrophic issues) ─────────────────────
    EmailRecord(
        id=21, difficulty="hard", sentiment="anger", customer_tier="enterprise",
        subject="LEGAL NOTICE: Data breach on your platform",
        sender="legal@huge-bank.com",
        body="We have evidence that our customer data stored on your servers has been leaked. We are initiating a forensic audit and notifying the regulator. We need a full security report in 4 hours.",
        timestamp="2024-01-15T19:30:00Z",
        expected_category="technical", expected_priority="critical",
        expected_response_keywords=["security", "breach", "forensic", "breach", "urgent", "compliance", "escalate"]
    ),
    EmailRecord(
        id=22, difficulty="hard", sentiment="neutral", customer_tier="free",
        subject="GDPR Article 17 Erasure Request",
        sender="privacy@eu-user.de",
        body="I formally exercise my right to erasure. Please delete every scrap of my personal data. I will be tracking the 30-day legal window.",
        timestamp="2024-01-15T20:00:00Z",
        expected_category="general", expected_priority="critical",
        expected_response_keywords=["GDPR", "erasure", "deletion", "confirm", "confirm", "privacy"]
    ),
    EmailRecord(
        id=23, difficulty="hard", sentiment="frustration", customer_tier="enterprise",
        subject="Account Takeover - Ransom Paid?",
        sender="admin@crypto-exchange.io",
        body="One of our admins was phished. They changed the root email to malicious-hacker@gmail.com. We hold $10M in client funds. LOCK THE ACCOUNT NOW.",
        timestamp="2024-01-15T20:30:00Z",
        expected_category="technical", expected_priority="critical",
        expected_response_keywords=["phished", "takeover", "locked", "urgent", "security", "root"]
    ),
    EmailRecord(
        id=24, difficulty="hard", sentiment="anger", customer_tier="pro",
        subject="Disputing $5,000 Fraudulent Charge",
        sender="cfo@startup.co",
        body="Your system charged us for 100 enterprise seats we never ordered. This looks like fraud. I am calling my bank to reverse this. Explain yourself.",
        timestamp="2024-01-15T21:00:00Z",
        expected_category="billing", expected_priority="critical",
        expected_response_keywords=["fraud", "reverse", "seats", "dispute", "investigate", "apologize"]
    ),
    EmailRecord(
        id=25, difficulty="hard", sentiment="neutral", customer_tier="enterprise",
        subject="EU Tax Compliance (VAT / OSS)",
        sender="tax@global-corp.de",
        body="Your invoices do not meet the new 2024 EU VAT requirements for B2B cross-border services. We cannot legally pay these invoices in their current format. We need customized fiscal invoices.",
        timestamp="2024-01-15T21:30:00Z",
        expected_category="billing", expected_priority="high",
        expected_response_keywords=["VAT", "EU", "OSS", "B2B", "fiscal", "compliance", "invoice"]
    ),
    EmailRecord(
        id=26, difficulty="hard", sentiment="frustration", customer_tier="pro",
        subject="Deleted all my client campaigns",
        sender="ceo@ad-agency.com",
        body="I was trying to use the bulk editor and somehow it deleted all 50 active campaigns for our clients. We have lost $20k in scheduled spend. Is there a backup?!",
        timestamp="2024-01-15T22:00:00Z",
        expected_category="technical", expected_priority="critical",
        expected_response_keywords=["backup", "deleted", "restore", "campaigns", "urgent", "apologize"]
    ),
    EmailRecord(
        id=27, difficulty="hard", sentiment="neutral", customer_tier="enterprise",
        subject="Vulnerability Disclosure (RCE)",
        sender="security-researcher@hackerone.com",
        body="I've found a Remote Code Execution vulnerability in your workspace invitation flow. I can take over any account. See proof of concept attached.",
        timestamp="2024-01-15T22:30:00Z",
        expected_category="technical", expected_priority="critical",
        expected_response_keywords=["vulnerability", "RCE", "security", "disclosure", "bug bounty", "reproduce"]
    ),
    EmailRecord(
        id=28, difficulty="hard", sentiment="anger", customer_tier="enterprise",
        subject="Contract termination - Breach of SLA",
        sender="v-p@huge-enterprise.com",
        body="Your downtime yesterday lasted 6 hours. This breached our 99.9% uptime SLA. We are terminating our $100k/year contract effective immediately. Send final billing instructions.",
        timestamp="2024-01-15T23:00:00Z",
        expected_category="billing", expected_priority="critical",
        expected_response_keywords=["SLA", "termination", "contract", "uptime", "apologize", "escalate"]
    ),
    EmailRecord(
        id=29, difficulty="hard", sentiment="neutral", customer_tier="free",
        subject="Someone is using your platform for phishing",
        sender="abuse@google.com",
        body="Phishing emails are originating from your cloud servers. See attached headers. Suspend account ID #PH-123 immediately.",
        timestamp="2024-01-15T23:30:00Z",
        expected_category="spam", expected_priority="critical", # Critical because abuse
        expected_response_keywords=["phishing", "suspend", "abuse", "investigate", "urgent"]
    ),
    EmailRecord(
        id=30, difficulty="hard", sentiment="anger", customer_tier="enterprise",
        subject="CEO Escalation - No response in 3 weeks",
        sender="ceo@top-client.com",
        body="I've been emailing your support team for 3 weeks about our API keys. 4 agents, 0 fixes. I expect a call from your VP of Support in 1 hour or we move to a competitor.",
        timestamp="2024-01-15T23:45:00Z",
        expected_category="technical", expected_priority="critical",
        expected_response_keywords=["escalation", "VP", "apologize", "CEO", "urgent", "callback"]
    ),
]
