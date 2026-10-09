"""
api_showcase.py

Full API surface demo for GlowByte.
Not a test suite, just shows every command that exists (or will exist).
Run sections individually as you implement each feature.
"""

from glowbyte import Canvas, Layer, Gradient, Color


# ─────────────────────────────────────────────────────────────
# CANVAS
# ─────────────────────────────────────────────────────────────

canvas = Canvas(1920, 1080)                        # width, height
canvas = Canvas(1920, 1080, background="#1a1a1a")  # with solid background color
canvas = Canvas(1920, 1080, background="transparent")

canvas.width   # 1920
canvas.height  # 1080
canvas.size    # (1920, 1080)

canvas.clear()                   # remove all layers
canvas.flatten()                 # merge all layers into one
canvas.resize(1280, 720)         # resize the canvas (crops or pads)
canvas.crop(x=100, y=50, width=800, height=600)


# ─────────────────────────────────────────────────────────────
# CREATING LAYERS
# ─────────────────────────────────────────────────────────────

# from a file
layer = Layer.from_file("photo.png")
layer = Layer.from_file("photo.png", opacity=0.8)
layer = Layer.from_file("photo.png", blend_mode="multiply")
layer = Layer.from_file("photo.png", opacity=0.8, blend_mode="screen")

# from a PIL image already in memory
from PIL import Image
pil_img = Image.open("photo.png")
layer = Layer.from_image(pil_img)

# solid color fill
layer = Layer.solid(1920, 1080, color="#ff6600")
layer = Layer.solid(1920, 1080, color=(255, 100, 0))
layer = Layer.solid(1920, 1080, color=(255, 100, 0, 180))  # with alpha

# gradient fill
layer = Layer.gradient(
    1920, 1080,
    start_color="#000000",
    end_color="#ffffff",
    direction="horizontal",   # "horizontal" | "vertical" | "diagonal"
)
layer = Layer.gradient(
    1920, 1080,
    start_color="#ff0080",
    end_color="#0080ff",
    direction="radial",
    center=(960, 540),
)

# text
layer = Layer.text("Hello, world!")
layer = Layer.text(
    "Hello, world!",
    font="Arial",
    font_size=72,
    color="#ffffff",
    bold=True,
    italic=False,
    align="center",           # "left" | "center" | "right"
    max_width=800,            # wrap text at this width
)


# ─────────────────────────────────────────────────────────────
# LAYER PROPERTIES
# ─────────────────────────────────────────────────────────────

layer.opacity = 0.75          # 0.0 – 1.0
layer.blend_mode = "multiply" # see blend modes section
layer.visible = False
layer.name = "portrait"

layer.width
layer.height
layer.size    # (w, h)
layer.position  # (x, y)


# ─────────────────────────────────────────────────────────────
# TRANSFORMS
# ─────────────────────────────────────────────────────────────

layer.move(x=100, y=50)          # set position
layer.move_by(dx=10, dy=-20)     # relative move

layer.resize(800, 600)           # set size
layer.scale(1.5)                 # uniform scale
layer.scale(sx=1.5, sy=1.0)      # non-uniform scale

layer.rotate(45)                 # degrees, around layer center
layer.rotate(45, origin=(0, 0))  # around a specific point

layer.flip_horizontal()
layer.flip_vertical()

layer.crop(x=10, y=10, width=400, height=300)


# ─────────────────────────────────────────────────────────────
# FILTERS  (non-destructive, applied in order)
# ─────────────────────────────────────────────────────────────

layer.filter.brightness(1.2)       # > 1 brighter, < 1 darker
layer.filter.contrast(1.1)
layer.filter.saturation(1.3)       # > 1 more vivid, 0 = grayscale
layer.filter.hue_shift(30)         # degrees, -180 – 180

layer.filter.blur(radius=4)
layer.filter.sharpen(amount=1.5)
layer.filter.noise(amount=0.05)    # add grain

layer.filter.grayscale()
layer.filter.invert()
layer.filter.sepia()
layer.filter.posterize(levels=4)

layer.filter.temperature(200)      # warm (+) or cool (-), in kelvin offset
layer.filter.vignette(strength=0.6, radius=0.8)

layer.filter.clear()               # remove all filters on this layer
layer.filter.remove("blur")        # remove a specific filter


# ─────────────────────────────────────────────────────────────
# BLEND MODES
# ─────────────────────────────────────────────────────────────

# set via Layer.from_file or layer.blend_mode =
blend_modes = [
    "normal",
    "multiply",
    "screen",
    "overlay",
    "soft_light",
    "hard_light",
    "darken",
    "lighten",
    "color_dodge",
    "color_burn",
    "difference",
    "exclusion",
    "hue",
    "saturation",
    "color",
    "luminosity",
]

layer.blend_mode = "soft_light"


# ─────────────────────────────────────────────────────────────
# EFFECTS  (layer-level, rendered after blend)
# ─────────────────────────────────────────────────────────────

layer.effects.drop_shadow(
    offset=(5, 5),
    blur=10,
    color="#000000",
    opacity=0.6,
)
layer.effects.inner_shadow(offset=(3, 3), blur=6, color="#000000", opacity=0.4)

layer.effects.stroke(width=3, color="#ffffff", position="outside")  # "inside" | "outside" | "center"

layer.effects.glow(radius=20, color="#ffaa00", opacity=0.8)          # outer glow
layer.effects.inner_glow(radius=10, color="#ffffff", opacity=0.5)

layer.effects.color_overlay(color="#ff0000", opacity=0.3)
layer.effects.gradient_overlay(
    start_color="#000000",
    end_color="#ffffff",
    direction="vertical",
    opacity=0.5,
)

layer.effects.clear()


# ─────────────────────────────────────────────────────────────
# CHROMA KEY / GREEN SCREEN
# ─────────────────────────────────────────────────────────────

layer.chroma_key(color="#00ff00", tolerance=0.3)    # remove green
layer.chroma_key(color=(0, 255, 0), tolerance=0.25, softness=0.1)


# ─────────────────────────────────────────────────────────────
# MASKS
# ─────────────────────────────────────────────────────────────

mask = Layer.from_file("mask.png")          # white = visible, black = hidden
layer.set_mask(mask)
layer.remove_mask()
layer.apply_mask()                          # bake mask into layer pixels


# ─────────────────────────────────────────────────────────────
# MANAGING LAYERS ON THE CANVAS
# ─────────────────────────────────────────────────────────────

canvas.add_layer(layer)
canvas.add_layer(layer, index=0)            # insert at position
canvas.add_layer(layer, name="portrait")

canvas.remove_layer(layer)
canvas.remove_layer("portrait")             # by name
canvas.remove_layer(index=2)               # by index

canvas.get_layer("portrait")               # by name
canvas.get_layer(index=0)                  # by index
canvas.layers                              # list of all layers

canvas.move_layer(layer, index=0)          # reorder
canvas.move_layer_up(layer)
canvas.move_layer_down(layer)
canvas.move_layer_to_top(layer)
canvas.move_layer_to_bottom(layer)

canvas.duplicate_layer(layer)


# ─────────────────────────────────────────────────────────────
# LAYER GROUPS
# ─────────────────────────────────────────────────────────────

group = canvas.create_group("background_elements")
group.add_layer(layer)
group.opacity = 0.9
group.blend_mode = "normal"
group.visible = False


# ─────────────────────────────────────────────────────────────
# SCENE: SAVE / LOAD COMPOSITION
# ─────────────────────────────────────────────────────────────

canvas.save_scene("my_scene.json")         # save all layers + settings to JSON
canvas.load_scene("my_scene.json")         # restore a saved composition


# ─────────────────────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────────────────────

canvas.export("result.png")
canvas.export("result.jpg", quality=90)
canvas.export("result.webp", quality=85)
canvas.export("result.tiff")

canvas.export("result.png", scale=2.0)    # export at 2× resolution
canvas.export("result.png", region=(0, 0, 960, 540))  # export a crop

img = canvas.to_image()                   # get as PIL Image without writing a file


# ─────────────────────────────────────────────────────────────
# BATCH PROCESSING  (CLI or scripted)
# ─────────────────────────────────────────────────────────────

import glowbyte

for path in ["a.png", "b.png", "c.png"]:
    canvas = Canvas(1920, 1080)
    canvas.add_layer(Layer.from_file(path))

    title = Layer.text("Watermark", font_size=48, color="#ffffff", opacity=0.5)
    title.move(50, 50)
    canvas.add_layer(title)

    out = path.replace(".png", "_out.png")
    canvas.export(out)