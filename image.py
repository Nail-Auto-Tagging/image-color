import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from colorsys import rgb_to_hsv
from math import sqrt

colors = dict((
    ((189, 16, 32), "RED"),
    ((255, 165, 0), "ORANGE"),
    ((255, 212, 0), "YELLOW"),
    ((251, 206, 177), "nude"),
    ((255, 192, 203), "pink"),
    ((134, 206, 250), "skyblue"),
    ((0, 0, 128), "blue"),
    ((107, 63, 160), "purple"),
    ((0, 0, 0), "black"),
    ((255, 255, 255), "white"),
    ((192, 192, 192), "silver"),
))


def RGB_to_Hex(rgb):
    color = '#'
    for i in rgb:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
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
    for color in colors:
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
    for color in colors:
        cr, cg, cb = color
        color_diff = sqrt(abs(r - cr) ** 2 + abs(g - cg) ** 2 + abs(b - cb) ** 2)
        color_diffs.append((color_diff, colors[color]))
    return min(color_diffs)[1]


if __name__ == '__main__':
    img_path = 'c189763443b2eb28d730c2f4d59c4b4.png'
image = Image.open(img_path)
#  추출할 기본 색상의 수
num_colors = 2
small_image = image.resize((image.width, image.height))
result = small_image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
result = result.convert('RGB')
main_colors = result.getcolors()
main_colors.sort(reverse=True);
col_extract = []

#추출된 기본 색상을 표시합니다.
for count, col in main_colors:
    color = RGB_to_Hex(col)
print("이미지에서 가장 큰 비율의 색상 식별：" + color)
print("비슷한 색：" + closest_color(col))
col_extract.append([col[i] / 255 for i in range(3)])

# 추출된 기본 색상을 표시합니다.
plt.figure(dpi=150)
plt.bar(range(len(col_extract)), np.ones(len(col_extract)), color=(col_extract))
plt.xticks(range(len(col_extract)), (range(len(col_extract))))
plt.tight_layout()
plt.show()
