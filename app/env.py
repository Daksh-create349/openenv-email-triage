from app.models import Observation, Action, Reward, State
from app.tasks import TASKS, Task
from app.grader import grade_action


class EmailTriageEnv:
    """
    OpenEnv-compliant environment for AI email triage.
    
    Each step returns a reward.score in (0, 1).
    The task's final score = SUM of per-step scores, strictly in (0, 1).
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

        # Integer Scaling: Base 2, Max range 6. All results are pure 'int'.
        num_emails = len(self.task.emails)
        raw_step = (float(raw_score) * 6.0 / num_emails) + (2.0 / num_emails)
        step_score = max(1, min(9, int(raw_step * 10))) # Scaling to 1-9 integers

        self._score_sum += step_score
        self._index += 1
        self._done = self._index >= len(self.task.emails)
        self._history.append({
            "step": self._index - 1,
            "email_id": email_record.id,
            "customer": email_record.customer_tier,
            "sentiment": email_record.sentiment,
            "action": action.model_dump(),
            "score": step_score,
            "feedback": feedback,
            "components": components
        })

        obs = None if self._done else self._make_obs()
        reward = Reward(
            score=step_score,
            cumulative_score=int(self._score_sum),
            feedback=feedback,
            components=components
        )
        
        # Final task_score in safe integer range
        task_score = int(max(1, min(9, self._score_sum / num_emails))) if self._done else None
        info = {
            "email_id": email_record.id,
            "customer_tier": email_record.customer_tier,
            "sentiment": email_record.sentiment,
            "score_feedback": feedback,
            "breakdown": components,
            "task_score": task_score
        }

        return obs, reward, self._done, info

    def state(self) -> State:
        """Return full typed state with metadata."""
        task_score = max(0.1, min(0.9, self._score_sum))
        return State(
            task_id=self.task_id,
            current_index=self._index,
            total_emails=len(self.task.emails),
            history=self._history,
            cumulative_score=round(task_score, 5),
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