
from PIL import Image, ImageDraw
import math

WIDTH, HEIGHT = 72, 16
SPEED = 1
DURATION = 50

CYAN = (0, 0, 255)
RED = (0, 255, 0)
TAN = (210, 180, 140)
LIGHT_TAN = (225, 200, 165)
DARK_TAN = (190, 150, 105)

sprite = Image.open("sprite.png").convert("RGBA")

end_x = WIDTH - sprite.width - 4
frames = []

# Wavy sand surface: 1–3 pixels high
sand_heights = [
    2 + round(math.sin(px * 0.16))
    for px in range(WIDTH)
]

for x in range(0, end_x + 1, SPEED):
    frame = Image.new("RGB", (WIDTH, HEIGHT), CYAN)
    draw = ImageDraw.Draw(frame)

    # Draw sand, leaving the bottom border row red
    for px in range(1, WIDTH - 1):
        height = sand_heights[px]
        surface_y = HEIGHT - 1 - height

        for py in range(surface_y, HEIGHT - 1):
            color = TAN

            if py == surface_y:
                color = LIGHT_TAN
            elif py == HEIGHT - 2 and height >= 3:
                color = DARK_TAN

            draw.point((px, py), fill=color)

    # Draw moving PNG
    sprite_frame = Image.new(
        "RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0)
    )

    y = (HEIGHT - sprite.height) // 2 - 1
    sprite_frame.alpha_composite(sprite, (x, y))
    frame.paste(sprite_frame, (0, 0), sprite_frame)

    # Exactly one-pixel red border
    draw = ImageDraw.Draw(frame)
    draw.rectangle(
        (0, 0, WIDTH - 1, HEIGHT - 1),
        outline=RED,
        width=1
    )

    frames.append(frame)
    frames.append(frame)
    

# Add exact final position if needed
if end_x % SPEED != 0:
    frame = Image.new("RGB", (WIDTH, HEIGHT), CYAN)
    draw = ImageDraw.Draw(frame)

    for px in range(1, WIDTH - 1):
        height = sand_heights[px]
        surface_y = HEIGHT - 1 - height

        for py in range(surface_y, HEIGHT - 1):
            color = LIGHT_TAN if py == surface_y else TAN
            draw.point((px, py), fill=color)

    sprite_frame = Image.new(
        "RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0)
    )
    y = (HEIGHT - sprite.height) // 2 - 1
    sprite_frame.alpha_composite(sprite, (end_x, y))
    frame.paste(sprite_frame, (0, 0), sprite_frame)

    ImageDraw.Draw(frame).rectangle(
        (0, 0, WIDTH - 1, HEIGHT - 1),
        outline=RED,
        width=1
    )
    frames.append(frame)

frames[0].save(
    "sprite.gif",
    save_all=True,
    append_images=frames[1:],
    duration=DURATION,
    loop=0,
    optimize=False
)

print("created gif!")
