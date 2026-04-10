"""
server/app.py — OpenEnv-compliant FastAPI server for Email Triage.
Entry point: server.app:main (for pyproject.toml [project.scripts])
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.env import EmailTriageEnv
from app.models import Action
from app.tasks import TASKS

app = FastAPI(
    title="Email Triage OpenEnv",
    description="An OpenEnv-compliant environment for AI email triage evaluation.",
    version="1.0.0",
)

# One env instance per session
_env: EmailTriageEnv | None = None


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    return """
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <title>Email Triage OpenEnv</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#e6edf3;min-height:100vh;display:flex;align-items:center;justify-content:center}
        .card{background:#161b22;border:1px solid #30363d;border-radius:16px;padding:48px;max-width:600px;width:90%;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,0.4)}
        .badge{display:inline-block;background:#238636;color:#fff;border-radius:20px;padding:4px 14px;font-size:12px;font-weight:600;letter-spacing:1px;margin-bottom:20px}
        h1{font-size:2.2rem;font-weight:700;margin-bottom:12px}
        h1 span{color:#58a6ff}
        p{color:#8b949e;line-height:1.6;margin-bottom:28px}
        .endpoints{text-align:left;background:#0d1117;border-radius:10px;padding:20px;margin-bottom:28px}
        .endpoint{display:flex;align-items:center;gap:12px;margin:10px 0}
        .method{font-size:11px;font-weight:700;padding:3px 8px;border-radius:4px;min-width:48px;text-align:center}
        .get{background:#1f6feb33;color:#58a6ff;border:1px solid #1f6feb}
        .post{background:#23863633;color:#3fb950;border:1px solid #238636}
        .path{font-family:monospace;color:#e6edf3;font-size:14px}
        .btn{display:inline-block;background:#238636;color:#fff;text-decoration:none;padding:12px 28px;border-radius:8px;font-weight:600}
    </style></head><body>
    <div class="card">
        <div class="badge">✅ RUNNING</div>
        <h1>📧 <span>Email Triage</span> OpenEnv</h1>
        <p>Enterprise-grade AI email triage with SLA awareness, sentiment analysis, and deterministic grading.</p>
        <div class="endpoints">
            <div class="endpoint"><span class="method post">POST</span><span class="path">/reset — Start a new episode</span></div>
            <div class="endpoint"><span class="method post">POST</span><span class="path">/step  — Submit an action</span></div>
            <div class="endpoint"><span class="method get">GET</span><span class="path">/health — Health check</span></div>
            <div class="endpoint"><span class="method get">GET</span><span class="path">/tasks  — List available tasks</span></div>
        </div>
        <a href="/docs" class="btn">📖 Open API Docs</a>
    </div></body></html>
    """


@app.get("/health")
def health():
    return {"status": "ok", "environment": "EmailTriageEnv", "version": "1.0.0"}


@app.get("/tasks")
def list_tasks():
    return {
        task_id: {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "difficulty": task.difficulty,
            "num_emails": len(task.emails),
        }
        for task_id, task in TASKS.items()
    }


class ResetRequest(BaseModel):
    task_id: str = "easy"


@app.post("/reset")
def reset(req: ResetRequest = ResetRequest()):
    global _env
    if req.task_id not in TASKS:
        raise HTTPException(status_code=400, detail=f"Unknown task_id '{req.task_id}'. Choose from: {list(TASKS)}")
    _env = EmailTriageEnv(task_id=req.task_id)
    obs = _env.reset()
    return obs.model_dump()


@app.post("/step")
def step(action: Action):
    if _env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    if _env._done:
        raise HTTPException(status_code=400, detail="Episode is finished. Call /reset to start a new one.")
    obs, reward, done, info = _env.step(action)
    return {
        "observation": obs.model_dump() if obs else None,
        "reward": reward.model_dump(),
        "done": done,
        "info": info,
    }


@app.get("/state")
def get_state():
    if _env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    return _env.state().model_dump()


def main() -> None:
    """Entry point for [project.scripts] server."""
    import uvicorn
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
