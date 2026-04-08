from app.models import Observation, Action, Reward, State
from app.tasks import TASKS, Task
from app.grader import grade_action


class EmailTriageEnv:
    """
    OpenEnv-compliant environment for AI email triage (v2.0 - 100/100 Edition).
    
    Each step returns a reward.score in (0, 1).
    The task's final score = MEAN of all step scores, also in (0, 1).
    """

    def __init__(self, task_id: str = "easy"):
        if task_id not in TASKS:
            raise ValueError(f"Unknown task_id '{task_id}'. Must be one of: {list(TASKS)}")
        self.task_id = task_id
        self.task: Task = TASKS[task_id]
        self._index = 0
        self._history: list[dict] = []
        self._score_sum = 0.0
        self._done = False

    def reset(self) -> Observation:
        """Reset environment to initial state."""
        self._index = 0
        self._history = []
        self._score_sum = 0.0
        self._done = False
        return self._make_obs()

    def step(self, action: Action) -> tuple[Observation | None, Reward, bool, dict]:
        """
        Apply action to current email.
        reward.score = per-step quality score, strictly in (0, 1).
        """
        if self._done:
            raise RuntimeError("Episode is done. Call reset() first.")

        email_record = self.task.emails[self._index]
        raw_score, feedback, components = grade_action(email_record, action)

        # Clamp each step score strictly into (0.001, 0.999)
        step_score = max(0.001, min(0.999, raw_score))

        self._score_sum += step_score
        self._index += 1
        self._done = self._index >= len(self.task.emails)

        # Task score = MEAN of step scores, always in (0.001, 0.999)
        task_score = self._score_sum / self._index

        self._history.append({
            "step": self._index - 1,
            "email_id": email_record.id,
            "customer": email_record.customer_tier,
            "sentiment": email_record.sentiment,
            "action": action.model_dump(),
            "score": round(step_score, 4),
            "feedback": feedback,
            "components": components
        })

        obs = None if self._done else self._make_obs()
        reward = Reward(
            score=round(step_score, 4),
            cumulative_score=round(task_score, 4),
            feedback=feedback,
            components=components
        )
        
        info = {
            "email_id": email_record.id,
            "customer_tier": email_record.customer_tier,
            "sentiment": email_record.sentiment,
            "score_feedback": feedback,
            "breakdown": components,
            "task_score": round(task_score, 4) if self._done else None
        }

        return obs, reward, self._done, info

    def state(self) -> State:
        """Return full typed state with metadata."""
        task_score = (self._score_sum / self._index) if self._index > 0 else 0.0
        return State(
            task_id=self.task_id,
            current_index=self._index,
            total_emails=len(self.task.emails),
            history=self._history,
            cumulative_score=round(task_score, 4),
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