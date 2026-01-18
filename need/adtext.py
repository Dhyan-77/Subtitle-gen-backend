import whisper

def extarct_text(audio_path):
    model = whisper.load_model("tiny",device="cpu")
    result = model.transcribe(audio_path)
    return  result ['segments']