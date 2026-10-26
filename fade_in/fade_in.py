from PIL import Image
import sys

# usage: python fade_gif.py input.png output.gif
src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else "fade.gif"

FADE_FRAMES = 20        
FADE_MS = 60            
HOLD_MS = 7755       
MAX_SIZE = 480         

img = Image.open(src).convert("RGB")
img.thumbnail((MAX_SIZE, MAX_SIZE))
black = Image.new("RGB", img.size, (0, 0, 0))

frames = [Image.blend(black, img, i / FADE_FRAMES) for i in range(FADE_FRAMES + 1)]
durations = [FADE_MS] * FADE_FRAMES + [HOLD_MS]

frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
)
print("saved", out)