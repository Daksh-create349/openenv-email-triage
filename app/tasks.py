from dataclasses import dataclass
from app.data import EMAILS
from app.models import EmailRecord


@dataclass
class Task:
    id: str
    name: str
    description: str
    difficulty: str
    emails: list[EmailRecord]
    grading_note: str


TASKS: dict[str, Task] = {
    "easy": Task(
        id="easy",
        name="Basic Email Triage",
        description=(
            "Classify 10 straightforward emails into the correct category (billing, technical, spam, general), "
            "assign an appropriate priority (low, medium, high, critical), and write a professional response. "
            "Emails are unambiguous with clear signals for category and priority."
        ),
        difficulty="easy",
        emails=[e for e in EMAILS if e.difficulty == "easy"],
        grading_note="Category and priority are clear-cut. Full marks achievable by careful reading.",
    ),
    "medium": Task(
        id="medium",
        name="Intermediate Email Triage",
        description=(
            "Classify 10 emails that require reading comprehension and business context. "
            "Priority judgment is key — some look routine but are actually urgent (e.g. entire team locked out). "
            "Responses must address the specific situation, not just be generic."
        ),
        difficulty="medium",
        emails=[e for e in EMAILS if e.difficulty == "medium"],
        grading_note="Priority especially tricky. Partial credit for being 1 priority level off.",
    ),
    "hard": Task(
        id="hard",
        name="Advanced Email Triage",
        description=(
            "Handle 10 complex, high-stakes, and ambiguous emails. Includes multi-issue complaints, "
            "legal threats, GDPR requests, security incidents, data loss, and fraud. "
            "Agent must identify the primary category from multiple overlapping signals, "
            "always escalate appropriately, and craft responses that address legal/security/emotional dimensions. "
            "Frontier models typically score below 0.7 on this task."
        ),
        difficulty="hard",
        emails=[e for e in EMAILS if e.difficulty == "hard"],
        grading_note="Most emails require critical priority. Response must contain specific keywords for safety/legal/security issues.",
    ),
}
