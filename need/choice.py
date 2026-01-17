def yellow_sub():
    return "yellow_bg.ass"

def red_sub():
    return "red.ass"

def white_bold():
    return "white_bold.ass"

def tiktok_style():
    return "purple.ass"


def get_style(choice):
    styles = {
        "yellow": yellow_sub,
        "red": red_sub,
        "white": white_bold,
        "tiktok": tiktok_style
    }

    if choice not in styles:
        raise ValueError("Invalid subtitle style selected")

    return styles[choice]()
