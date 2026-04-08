import os
from fastapi import FastAPI
from openenv_core.env_server import create_fastapi_app

from app.env import EmailTriageEnv
from app.models import Action, Observation

# 1) Instantiate your environment
env = EmailTriageEnv()

# 2) Create FastAPI app using the official OpenEnv helper
#    Positional args: env, action_cls, observation_cls
app: FastAPI = create_fastapi_app(env, Action, Observation)


# 3) Define main() for [project.scripts] entrypoint
def main() -> None:
    import uvicorn
    port = int(os.getenv("PORT", "7860"))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)


# 4) Standard script guard
if __name__ == "__main__":
    main()
