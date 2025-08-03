import re
import sys


def hash_sequence(plain: str) -> int:
    hashed = 0

    for char in plain:
        hashed = ((hashed + ord(char)) * 17) % 256

    return hashed


init_sequence = sys.stdin.readline().strip().split(',')

print(sum(hash_sequence(step) for step in init_sequence))

boxes = [{} for i in range(256)]
for step in init_sequence:
    lens = re.match(r'^(?P<label>\w+)(?P<operation>[=-])(?P<focal_length>\d+)?$', step)
    box = hash_sequence(lens['label'])

    if lens['operation'] == '=':
        boxes[box][lens['label']] = int(lens['focal_length'])
    elif lens['label'] in boxes[box]:
        boxes[box].pop(lens['label'])

print(
    sum(
        bi * li * box[lens]
        for bi, box in enumerate(boxes, start=1)
        for li, lens in enumerate(box, start=1)
    )
)
