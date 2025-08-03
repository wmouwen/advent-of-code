import math
import sys


class Tree:
    def __init__(self, height: int) -> None:
        self.height = height
        self.visible = False
        self.views = []


trees = [
    list(map(lambda height: Tree(height=int(height)), list(line.strip())))
    for line in sys.stdin
]

for y in range(len(trees)):
    for x in range(len(trees[y])):
        trees[y][x].visible = (
            y == 0
            or y == len(trees) - 1
            or x == 0
            or x == len(trees[y]) - 1
            or not sum(
                1 for yi in range(0, y) if trees[yi][x].height >= trees[y][x].height
            )
            or not sum(
                1
                for yi in range(y + 1, len(trees))
                if trees[yi][x].height >= trees[y][x].height
            )
            or not sum(
                1 for xi in range(0, x) if trees[y][xi].height >= trees[y][x].height
            )
            or not sum(
                1
                for xi in range(x + 1, len(trees[y]))
                if trees[y][xi].height >= trees[y][x].height
            )
        )

        visible = True
        view = 0
        for xi in range(x - 1, -1, -1):
            view += 1
            if trees[y][xi].height >= trees[y][x].height:
                visible = False
                break
        trees[y][x].visible = trees[y][x].visible or visible
        trees[y][x].views.append(view)

        visible = True
        view = 0
        for xi in range(x + 1, len(trees[y])):
            view += 1
            if trees[y][xi].height >= trees[y][x].height:
                visible = False
                break
        trees[y][x].visible = trees[y][x].visible or visible
        trees[y][x].views.append(view)

        visible = True
        view = 0
        for yi in range(y - 1, -1, -1):
            view += 1
            if trees[yi][x].height >= trees[y][x].height:
                visible = False
                break
        trees[y][x].visible = trees[y][x].visible or visible
        trees[y][x].views.append(view)

        visible = True
        view = 0
        for yi in range(y + 1, len(trees)):
            view += 1
            if trees[yi][x].height >= trees[y][x].height:
                visible = False
                break
        trees[y][x].visible = trees[y][x].visible or visible
        trees[y][x].views.append(view)

print(
    sum(
        1
        for y in range(len(trees))
        for x in range(len(trees[y]))
        if trees[y][x].visible
    )
)
print(
    max(
        math.prod(trees[y][x].views)
        for y in range(len(trees))
        for x in range(len(trees[y]))
    )
)
