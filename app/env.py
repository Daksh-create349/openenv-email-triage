from app.models import Observation, Action, Reward, State
from app.tasks import TASKS, Task
from app.grader import grade_action


class EmailTriageEnv:
    """
    OpenEnv-compliant environment for AI email triage (v2.0 - 100/100 Edition).
    
    Includes SLA-logic, Sentiment-awareness, and rich debugging info.
    """

    def __init__(self, task_id: str = "easy"):
        if task_id not in TASKS:
            raise ValueError(f"Unknown task_id '{task_id}'. Must be one of: {list(TASKS)}")
        self.task_id = task_id
        self.task: Task = TASKS[task_id]
        self._index = 0
        self._history: list[dict] = []
        self._cumulative_score = 0.0
        self._done = False

    def reset(self) -> Observation:
        """Reset environment to initial state."""
        self._index = 0
        self._history = []
        self._cumulative_score = 0.0
        self._done = False
        return self._make_obs()

    def step(self, action: Action) -> tuple[Observation | None, Reward, bool, dict]:
        """
        Apply action to current email. Rewards are normalized to ensure the SUM 
        for the task is strictly in (0, 1) (between 0.01 and 0.99).
        """
        if self._done:
            raise RuntimeError("Episode is done. Call reset() first.")

        email_record = self.task.emails[self._index]
        score, feedback, components = grade_action(email_record, action)

        # Normalize score based on task length so SUM stays < 1.0
        num_emails = len(self.task.emails)
        # Use 98% of the (0,1) range to stay safely inside bounds
        normalized_score = (score / num_emails) * 0.98
        
        # Add a tiny base reward per step to avoid hitting absolute 0.0
        step_reward = max(0.0001, normalized_score)

        self._cumulative_score += step_reward
        self._history.append({
            "step": self._index,
            "email_id": email_record.id,
            "customer": email_record.customer_tier,
            "sentiment": email_record.sentiment,
            "action": action.model_dump(),
            "score": round(step_reward, 5),
            "feedback": feedback,
            "components": components
        })

        self._index += 1
        self._done = self._index >= len(self.task.emails)

        # Final safety clamp on the last step to ensure total is strictly in (0.01, 0.99)
        if self._done:
            self._cumulative_score = max(0.01, min(0.99, self._cumulative_score))

        obs = None if self._done else self._make_obs()
        reward = Reward(
            score=round(step_reward, 5),
            cumulative_score=round(self._cumulative_score, 5),
            feedback=feedback,
            components=components
        )
        
        info = {
            "email_id": email_record.id,
            "customer_tier": email_record.customer_tier,
            "sentiment": email_record.sentiment,
            "score_feedback": feedback,
            "breakdown": components,
            "final_total": round(self._cumulative_score, 5) if self._done else None
        }

        return obs, reward, self._done, info

    def state(self) -> State:
        """Return full typed state with metadata."""
        return State(
            task_id=self.task_id,
            current_index=self._index,
            total_emails=len(self.task.emails),
            history=self._history,
            cumulative_score=round(self._cumulative_score, 4),
            done=self._done,
            metadata={
                "task_name": self.task.name,
                "difficulty": self.task.difficulty,
                "current_tier": self.task.emails[min(self._index, len(self.task.emails)-1)].customer_tier
            }
        )

    def _make_obs(self) -> Observation:
        return Observation(
            current_email=self.task.emails[self._index].to_email(),
            task_id=self.task_id,
            step=self._index,
            total_steps=len(self.task.emails),
            history=[
                {"email_id": h["email_id"], "score": h["score"], "customer": h["customer"]}
                for h in self._history
            ],
        )