import os
import random
import subprocess
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1080, 1920
DURATION = 10  # seconds — change this to make clips longer/shorter
QUOTE_FILE = "current_quote.txt"
MUSIC_DIR = "music"
OUTPUT_DIR = "output"
IMAGE_PATH = os.path.join(OUTPUT_DIR, "quote_frame.png")
VIDEO_PATH = os.path.join(OUTPUT_DIR, "daily_video.mp4")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GRADIENTS = [
    ((255, 94, 98), (255, 195, 113)),
    ((44, 62, 80), (52, 152, 219)),
    ((131, 58, 180), (253, 29, 29)),
    ((0, 78, 146), (0, 191, 141)),
    ((41, 30, 74), (255, 105, 135)),
    ((17, 55, 94), (135, 206, 235)),
    ((94, 0, 122), (255, 128, 8)),
    ((0, 34, 63), (127, 219, 255)),
    ((70, 0, 43), (255, 178, 89)),
    ((10, 40, 30), (73, 190, 143)),
]


def make_gradient_background():
    top, bottom = random.choice(GRADIENTS)
    img = Image.new("RGB", (WIDTH, HEIGHT), top)
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top[0] + (bottom[0] - top[0]) * ratio)
        g = int(top[1] + (bottom[1] - top[1]) * ratio)
        b = int(top[2] + (bottom[2] - top[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    return img


def wrap_text(text, font, draw, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_quote(image, quote, book):
    draw = ImageDraw.Draw(image)
    max_width = int(WIDTH * 0.8)

    font_size = 90
    quote_font = ImageFont.truetype(FONT_BOLD, font_size)
    lines = wrap_text(f"\u201c{quote}\u201d", quote_font, draw, max_width)

    while len(lines) > 6 and font_size > 40:
        font_size -= 5
        quote_font = ImageFont.truetype(FONT_BOLD, font_size)
        lines = wrap_text(f"\u201c{quote}\u201d", quote_font, draw, max_width)

    line_height = int(font_size * 1.3)
    y = (HEIGHT - line_height * len(lines)) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        x = (WIDTH - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, font=quote_font, fill=(255, 255, 255))
        y += line_height

    book_font = ImageFont.truetype(FONT_REGULAR, 48)
    book_text = f"\u2014 {book}"
    bbox = draw.textbbox((0, 0), book_text, font=book_font)
    x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.text((x, y + 40), book_text, font=book_font, fill=(230, 230, 230))


def pick_music():
    if not os.path.isdir(MUSIC_DIR):
        return None
    tracks = [f for f in os.listdir(MUSIC_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a"))]
    return os.path.join(MUSIC_DIR, random.choice(tracks)) if tracks else None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(QUOTE_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    quote = lines[0]
    book = lines[1] if len(lines) > 1 else ""

    image = make_gradient_background()
    draw_quote(image, quote, book)
    image.save(IMAGE_PATH)

    music_path = pick_music()

    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", IMAGE_PATH]
    if music_path:
        cmd += ["-stream_loop", "-1", "-i", music_path]

    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-t", str(DURATION)]

    if music_path:
        fade_start = max(DURATION - 2, 0)
        cmd += ["-c:a", "aac", "-b:a", "192k", "-af", f"afade=t=out:st={fade_start}:d=2"]

    cmd += [VIDEO_PATH]
    subprocess.run(cmd, check=True)
    print(f"Video saved to {VIDEO_PATH}")


if __name__ == "__main__":
    main()
