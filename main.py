from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
from pathlib import Path
import shutil
from pipline import pipline_do  # your existing FFmpeg/Whisper pipeline

# ----------------------------
# Configuration
# ----------------------------
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bigdihs.netlify.app",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories for temp storage
UPLOAD_DIR = Path("/tmp/uploads")
OUTPUT_DIR = Path("/tmp/output")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Expose output folder
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

# Base URL for download links (change to your Render URL)
BASE_URL = "https://subtitle-gen-backend-7.onrender.com"

# ----------------------------
# Routes
# ----------------------------
@app.get("/")
def health():
    return {"status": "running"}


@app.post("/generate")
async def generate_subtitles(file: UploadFile = File(...)):
    try:
        # Save uploaded video to temp folder
        input_path = UPLOAD_DIR / file.filename
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run FFmpeg/Whisper pipeline in a thread
        output_video_path = await run_in_threadpool(
            pipline_do,
            str(input_path),
            str(OUTPUT_DIR)
        )

        # Get only filename
        output_filename = Path(output_video_path).name

        # Return download URL
        return {
            "status": "completed",
            "download_url": f"{BASE_URL}/output/{output_filename}"
        }

    except Exception as e:
        # Return error info for debugging
        import traceback
        return {
            "status": "error",
            "message": str(e),
            "trace": traceback.format_exc()
        }
