"""
FastAPI server exposing the EmailTriageEnv via HTTP.
Endpoints: POST /reset, POST /step, GET /state, GET /tasks, GET /health
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from app.env import EmailTriageEnv
from app.models import Action, Observation, Reward, State
from app.tasks import TASKS

app = FastAPI(
    title="Email Triage OpenEnv",
    description="An OpenEnv-compliant environment for AI email triage evaluation.",
    version="1.0.0",
)

# One env instance per session (single-user; extend with session IDs if needed)
_env: EmailTriageEnv | None = None


@app.get("/", include_in_schema=False)
def root():
    """Redirect to Swagger UI for a better user experience."""
    return RedirectResponse(url="/docs")


class ResetRequest(BaseModel):
    task_id: str = "easy"


class StepResponse(BaseModel):
    observation: Observation | None
    reward: Reward
    done: bool
    info: dict


@app.get("/health")
def health():
    return {"status": "ok", "env": "email-triage-v1"}


@app.get("/tasks")
def list_tasks():
    return {
        tid: {
            "name": t.name,
            "description": t.description,
            "difficulty": t.difficulty,
            "num_emails": len(t.emails),
            "grading_note": t.grading_note,
        }
        for tid, t in TASKS.items()
    }


@app.post("/reset", response_model=Observation)
def reset(req: ResetRequest = ResetRequest()):
    global _env
    if req.task_id not in TASKS:
        raise HTTPException(status_code=400, detail=f"Unknown task_id '{req.task_id}'. Options: {list(TASKS)}")
    _env = EmailTriageEnv(task_id=req.task_id)
    return _env.reset()


@app.post("/step", response_model=StepResponse)
def step(action: Action):
    global _env
    if _env is None:
        raise HTTPException(status_code=400, detail="Call /reset first.")
    if _env._done:
        raise HTTPException(status_code=400, detail="Episode done. Call /reset to start a new episode.")
    obs, reward, done, info = _env.step(action)
    return StepResponse(observation=obs, reward=reward, done=done, info=info)


@app.get("/state", response_model=State)
def state():
    global _env
    if _env is None:
        raise HTTPException(status_code=400, detail="Call /reset first.")
    return _env.state()
