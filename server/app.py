import os
from fastapi import FastAPI
from openenv_core.env_server import create_fastapi_app

# Adjust these imports to match your project
from app.env import EmailTriageEnv
from app.models import Action, Observation

# 1) Instantiate your environment
env = EmailTriageEnv()

# 2) Create FastAPI app using the official OpenEnv helper
# This ensures all URLs (/reset, /step, etc.) match the competition standard exactly
app: FastAPI = create_fastapi_app(
    env=env,
)

# 3) Define main() function for the [project.scripts] entrypoint
def main() -> None:
    import uvicorn
    port = int(os.getenv("PORT", "7860"))
    # Point uvicorn to this file and this app object
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)

# 4) Standard script guard
if __name__ == "__main__":
    main()
