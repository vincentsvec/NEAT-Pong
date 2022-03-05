"""
Global configuration variables. Change this to desired settings or leave default.
"""

colors = {
    "black": (0, 0, 0),
    "white": (230, 230, 230),
}

screen = {
    "width": 800,
    "height": 500,
    "fps": 1000
}

paddle_conf = {
    "width": round(screen["width"] / 80),
    "height": round(screen["width"] / 13),
    "color": colors["white"],
    "speed": 10
}

ball_conf = {
    "radius": 8,
    "color": colors["white"],
    "speed": 5,
}
