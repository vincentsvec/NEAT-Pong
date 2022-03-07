"""
Global configuration variables. Change this to desired settings or leave default.
"""

generations = 50

colors = {
    "black": (0, 0, 0),
    "white": (230, 230, 230),
    "grey": (120, 120, 120)
}

screen = {
    "width": 800,
    "height": 500,
    "train_fps": 1000,
    "test_fps": 30,
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
