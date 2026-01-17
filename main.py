from fastapi import FastAPI, UploadFile, File
import shutil
from pathlib import Path
from pipline import pipline_do
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# expose output folder
app.mount("/output", StaticFiles(directory="output"), name="output")


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/generate")
async def generate_subtitles(file: UploadFile = File(...)):
    # save uploaded video
    input_path = UPLOAD_DIR / file.filename

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # run pipeline
    output_video_path = await run_in_threadpool(
        pipline_do,
        str(input_path),
        str(OUTPUT_DIR)
    )

    # filename only (for frontend)
    output_filename = Path(output_video_path).name

    return {
        "status": "completed",
        "download_url": f"http://localhost:8000/output/{output_filename}"
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
