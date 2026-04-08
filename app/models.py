from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Email(BaseModel):
    """Rich agent-visible email representation."""
    id: int
    subject: str
    sender: str
    body: str
    timestamp: str
    customer_tier: str = "free"  # free, pro, enterprise
    thread_id: Optional[str] = None
    sentiment: str = "neutral"   # frustration, anger, neutral, positive


class EmailRecord(BaseModel):
    """Internal ground truth for grading."""
    id: int
    subject: str
    sender: str
    body: str
    timestamp: str
    customer_tier: str
    expected_category: str
    expected_priority: str
    expected_response_keywords: List[str]
    difficulty: str
    sentiment: str = "neutral"
    thread_id: Optional[str] = None

    def to_email(self) -> Email:
        return Email(
            id=self.id,
            subject=self.subject,
            sender=self.sender,
            body=self.body,
            timestamp=self.timestamp,
            customer_tier=self.customer_tier,
            thread_id=self.thread_id,
            sentiment=self.sentiment
        )


class Observation(BaseModel):
    """Enhanced agent observation."""
    current_email: Optional[Email] = None
    task_id: str
    step: int
    total_steps: int
    history: List[Dict[str, Any]] = []


class Action(BaseModel):
    """Agent agent response."""
    category: str = "general"
    priority: str = "medium"
    response: str = ""


class Reward(BaseModel):
    """Rich feedback signal."""
    score: int
    cumulative_score: int = 0
    feedback: str = ""
    components: Dict[str, float] = {}


class State(BaseModel):
    """Full environment transparency for training."""
    task_id: str
    current_index: int
    total_emails: int
    history: List[Dict[str, Any]]
    cumulative_score: int
    done: bool
    metadata: Dict[str, Any] = {}