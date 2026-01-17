import re

WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z0-9]+)*")

def to_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def oneword_ass(segments, output="oneword.ass"):
    ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV
Style: Default,Arial,48,&H00FFFFFF,&H00000000,&H64000000,-1,0,1,2,0,2,40,40,30

[Events]
Format: Layer, Start, End, Style, Text
"""

    with open(output, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER)

        for seg in segments:
            text = seg["text"].replace("\n", " ")
            words = WORD_RE.findall(text)

            start = seg["start"]
            end = seg["end"]

            if not words:
                continue

            duration = max(0.12, (end - start) / len(words))
            current = start

            for word in words:
                f.write(
                    f"Dialogue: 0,{to_ass_time(current)},{to_ass_time(current + duration)},Default,{word}\n"
                )
                current += duration

    return output
