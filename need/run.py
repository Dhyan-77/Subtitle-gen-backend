from transcriber import extract_audio
from adtext import extarct_text
from fontss import generate_srt
from harden import encode,encodeass,encode_one_ass
from choice import get_style
from karoke import oneword_ass

video_file = "kling.mp4"


audio = extract_audio(video_file)
text = extarct_text(audio)
generate_srt(text)



style_choice = "red"
ass_file = get_style(style_choice)


one_ass = oneword_ass(text)

final_one_word = encode_one_ass(video_file,one_ass)

#final_video = encodeass(video_file,ass_file)

print("✅ Subtitles hardcoded successfully:")


