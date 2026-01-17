from need.transcriber import extract_audio
from need.adtext import extarct_text
from need.fontss import generate_srt
from need.harden import encode,encodeass,encode_one_ass
from need.choice import get_style
from need.karoke import oneword_ass
from pathlib import Path



def pipline_do(input_path: str , output_dir:str):

    
    input_path = Path(input_path)
    output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)

    output_video_path = output_dir / f"{input_path.stem}_subtitled.mp4"
    
    audio = extract_audio(str(input_path))
    text = extarct_text(audio)

    generate_srt(text)
    one_ass = oneword_ass(text)

    encode_one_ass(

        video_path=str(input_path),
        ass_path=one_ass,
        output_path=str(output_video_path)
    )


    return str(output_video_path)

