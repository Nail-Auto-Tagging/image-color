from colorsys import rgb_to_hsv
from math import sqrt


COLORS = dict((
    ((189, 16, 32), "RED"), #BD1020
    ((255, 165, 0), "ORANGE"), #FFA500
    ((255, 212, 0), "YELLOW"), #FFD400
    ((251, 206, 177), "NUDE"), #FBCEB1
    ((255, 192, 203), "PINK"), #FFC0CB
    ((255, 192, 203), "GREEN"), #81C147
    ((134, 206, 250), "SKYBLUE"), #86CEFA
    ((0, 0, 128), "NAVY"), #000080
    ((107, 63, 160), "PURPLE"), #6B3FA0
    ((0, 0, 0), "BLACK"), #000000
    ((255, 255, 255), "WHITE"), #FFFFFF
    ((192, 192, 192), "SILVER"), # C0C0C0
))

COLOR_MAP = {
    "RED": 1,
    "ORANGE": 2,
    "YELLOW": 3,
    "NUDE": 4,
    "PINK": 5,
    "GREEN": 6,
    "SKYBLUE": 7,
    "NAVY": 8,
    "PURPLE": 9,
    "BLACK": 10,
    "WHITE": 11,
    "SILVER": 12
}

def RGB_to_Hex(rgb):
    color = "#"
    
    for i in rgb:
        num = int(i)
        color += str(hex(num))[-2:].replace("x", "0").upper()
    return color


def to_hsv(color):
    return rgb_to_hsv(*[x / 255.0 for x in color])


def color_dist(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(to_hsv(c1), to_hsv(c2)))


def min_color_diff(color_to_match, colors):
    return min(
        (color_dist(color_to_match, test), colors[test])
        for test in colors)


def color_distance(rgb1):
    for color in COLORS:
        rgb2 = color
        rm = 0.5 * (rgb1[0] + rgb2[0])
        rd = ((2 + rm) * (rgb1[0] - rgb2[0])) ** 2
        gd = (4 * (rgb1[1] - rgb2[1])) ** 2
        bd = ((3 - rm) * (rgb1[2] - rgb2[2])) ** 2
        print((rd + gd + bd) ** 0.5)
    return (rd + gd + bd) ** 0.5


def closest_color(rgb):
    r, g, b = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr) ** 2 + abs(g - cg) ** 2 + abs(b - cb) ** 2)
        color_diffs.append((color_diff, COLORS[color]))
    return min(color_diffs)[1]


def convert_color_to_num(color_name):
    try:
        return COLOR_MAP[color_name]
    except:
        return None