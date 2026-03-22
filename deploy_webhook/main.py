import hashlib
import hmac
import json
import logging
import os
import subprocess

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

WEBHOOK_SECRET = os.environ["WEBHOOK_SECRET"]
REPO_PATH = "/repo"


def verify_signature(payload: bytes, signature: str) -> bool:
    mac = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)


def run_deploy():
    logger.info("Starting deployment...")
    try:
        subprocess.run(["git", "pull"], cwd=REPO_PATH, check=True)
        subprocess.run(["chown", "-R", "1000:1000", REPO_PATH], check=True)
        subprocess.run(
            ["docker", "compose", "up", "-d", "--build", "--no-deps", "nginx", "backend"],
            cwd=REPO_PATH,
            check=True,
        )
        logger.info("Deployment complete.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Deployment failed: {e}")


@app.post("/deploy")
async def deploy(
    request: Request,
    background_tasks: BackgroundTasks,
    x_hub_signature_256: str = Header(...),
):
    payload = await request.body()

    if not verify_signature(payload, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = json.loads(payload)

    if data.get("ref") != "refs/heads/main":
        return {"status": "skipped", "reason": "not main branch"}

    background_tasks.add_task(run_deploy)
    return {"status": "deploying"}
