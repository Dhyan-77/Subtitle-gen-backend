from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from uuid import uuid4
import shutil
import traceback

from pipline import pipline_do  # your existing pipeline

# ----------------------------
# App
# ----------------------------
app = FastAPI()

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bigdihs.netlify.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Storage
# ----------------------------
UPLOAD_DIR = Path("/tmp/uploads")
OUTPUT_DIR = Path("/tmp/output")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

BASE_URL = "https://subtitle-gen-backend-7.onrender.com"

# ----------------------------
# In-memory job store
# ----------------------------
jobs = {}

# ----------------------------
# Health
# ----------------------------
@app.get("/")
def health():
    return {"status": "running"}

# ----------------------------
# Background worker
# ----------------------------
def process_job(job_id: str, input_path: Path):
    try:
        output_video = pipline_do(
            str(input_path),
            str(OUTPUT_DIR)
        )

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["output"] = Path(output_video).name

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["trace"] = traceback.format_exc()

# ----------------------------
# Create job
# ----------------------------
@app.post("/generate")
async def generate(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    job_id = uuid4().hex

    input_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    jobs[job_id] = {
        "status": "processing",
        "output": None,
        "error": None
    }

    background_tasks.add_task(
        process_job,
        job_id,
        input_path
    )

    return {"job_id": job_id}

# ----------------------------
# Job status
# ----------------------------
@app.get("/status/{job_id}")
def job_status(job_id: str):
    job = jobs.get(job_id)

    if not job:
        return {"status": "not_found"}

    if job["status"] == "completed":
        return {
            "status": "completed",
            "download_url": f"{BASE_URL}/output/{job['output']}"
        }

    if job["status"] == "failed":
        return {
            "status": "failed",
            "error": job["error"]
        }

    return {"status": "processing"}
